import streamlit as st
import pandas as pd
from fpdf import FPDF

st.set_page_config(page_title="Tes RIASEC Neutron", layout="centered")

# =========================
# SISTEM AKSES & BATAS 1X
# =========================
AKSES_KODE = "neutronmurangan"

if "akses_granted" not in st.session_state:
    st.session_state.akses_granted = False

if "submitted_once" not in st.session_state:
    st.session_state.submitted_once = False

# Jika belum login
if not st.session_state.akses_granted:
    st.title("🔐 Akses Tes RIASEC Neutron Murangan")
    kode_input = st.text_input("Masukkan Kode Akses", type="password")

    if st.button("Masuk"):
        if kode_input == AKSES_KODE:
            st.session_state.akses_granted = True
            st.success("Akses diterima ✅")
            st.rerun()  # <-- ganti experimental_rerun() menjadi rerun()
        else:
            st.error("Kode akses salah ❌")
    st.stop()

# Jika sudah pernah submit
if st.session_state.submitted_once:
    st.warning("⚠️ Anda sudah mengerjakan tes ini. Tes hanya dapat dikerjakan 1 kali.")
    st.stop()

# =========================
# APLIKASI TES
# =========================
st.title("🎯 Tes Minat & Bakat (RIASEC) Neutron Murangan")
st.write("Jawablah sesuai kepribadian Anda. Skala 1 (Tidak Sesuai) hingga 5 (Sangat Sesuai).")

questions = {
    "Realistic (R)": ["Suka bekerja dengan alat/mesin", "Suka aktivitas luar ruangan", "Bisa memperbaiki barang rusak", "Menyukai aktivitas fisik", "Suka bekerja dengan tangan"],
    "Investigative (I)": ["Suka memecahkan masalah rumit", "Senang riset atau eksperimen", "Suka menganalisis data", "Tertarik sains/matematika", "Berpikir logis & sistematis"],
    "Artistic (A)": ["Suka menggambar/mendesain", "Suka menulis cerita/puisi", "Tertarik musik/seni", "Senang ekspresi kreatif", "Suka menciptakan ide baru"],
    "Social (S)": ["Senang membantu orang lain", "Suka mengajar/membimbing", "Nyaman bekerja dalam tim", "Peduli kesejahteraan sesama", "Senang berinteraksi sosial"],
    "Enterprising (E)": ["Suka memimpin kelompok", "Senang meyakinkan orang lain", "Tertarik bisnis/wirausaha", "Berani ambil keputusan", "Senang berkompetisi"],
    "Conventional (C)": ["Suka kerja terstruktur", "Teliti dalam tugas", "Nyaman dengan angka/data", "Suka perencanaan rinci", "Patuh pada aturan"]
}

with st.form("quiz_form"):
    for category, qs in questions.items():
        st.markdown(f"### {category}")
        for i, q in enumerate(qs):
            st.select_slider(q, options=[1, 2, 3, 4, 5], value=3, key=f"q_{category}_{i}")
    
    submitted = st.form_submit_button("Lihat Hasil Analisis")

# =========================
# MENAMPILKAN HASIL & DOWNLOAD PDF
# =========================
if submitted:
    st.session_state.submitted_once = True

    # Hitung skor
    current_scores = {key: 0 for key in questions.keys()}
    for category in questions.keys():
        for i in range(len(questions[category])):
            current_scores[category] += st.session_state[f"q_{category}_{i}"]
    
    st.divider()
    st.header("📊 Hasil Profil Minat Anda")
    chart_data = pd.DataFrame(current_scores.items(), columns=["Tipe", "Skor"]).set_index("Tipe")
    st.bar_chart(chart_data)

    sorted_scores = sorted(current_scores.items(), key=lambda x: x[1], reverse=True)
    top_3 = sorted_scores[:3]

    rekomendasi = {
        "Realistic (R)": "Teknik, Arsitektur, Otomotif, Perkebunan.",
        "Investigative (I)": "Peneliti, Dokter, Ahli IT, Ilmuwan.",
        "Artistic (A)": "Desainer, Seniman, Penulis, Arsitek.",
        "Social (S)": "Guru, Psikolog, Perawat, Konselor.",
        "Enterprising (E)": "Pengusaha, Marketing, Manajer, Hukum.",
        "Conventional (C)": "Akuntan, Administrasi, Perbankan, Auditor."
    }

    st.subheader("🏆 3 Tipe Dominan Anda")
    cols = st.columns(3)
    for idx, (label, score) in enumerate(top_3):
        with cols[idx]:
            st.info(f"**{idx+1}. {label.split()[0]}**")
            st.write(f"Skor: **{score}**")
            st.caption(f"Bidang: {rekomendasi[label]}")

    holland_code = "".join([x[0][0] for x in top_3])
    st.success(f"Kode Holland Anda adalah: **{holland_code}**")
    st.balloons()

    # =========================
    # FUNGSI PDF
    # =========================
    def create_pdf(scores, top3, holland_code):
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", "B", 16)
        pdf.cell(0, 10, "Hasil Tes RIASEC Neutron Murangan", ln=True, align="C")
        pdf.ln(10)
        pdf.set_font("Arial", "", 12)
        pdf.cell(0, 10, "📊 Skor Tiap Tipe:", ln=True)
        for tipe, skor in scores.items():
            pdf.cell(0, 8, f"- {tipe}: {skor}", ln=True)
        pdf.ln(5)
        pdf.cell(0, 10, "🏆 3 Tipe Dominan:", ln=True)
        for idx, (label, score) in enumerate(top3):
            pdf.cell(0, 8, f"{idx+1}. {label} - Skor: {score} - Bidang: {rekomendasi[label]}", ln=True)
        pdf.ln(5)
        pdf.cell(0, 10, f"Kode Holland: {holland_code}", ln=True)
        return pdf.output(dest="S").encode("latin1")

    pdf_data = create_pdf(current_scores, top_3, holland_code)
    st.download_button(
        label="📄 Unduh Hasil PDF",
        data=pdf_data,
        file_name="hasil_tes_riasec.pdf",
        mime="application/pdf"
    )
    
