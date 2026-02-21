import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from fpdf import FPDF
from io import BytesIO

st.set_page_config(page_title="Tes RIASEC Neutron", layout="centered")

# =========================
# SISTEM AKSES & BATAS 1X
# =========================

AKSES_KODE = "neutronmurangan"

if "akses_granted" not in st.session_state:
    st.session_state.akses_granted = False
if "submitted_once" not in st.session_state:
    st.session_state.submitted_once = False

if not st.session_state.akses_granted:
    st.title("🔐 Akses Tes RIASEC Neutron Murangan")
    kode_input = st.text_input("Masukkan Kode Akses", type="password")
    if st.button("Masuk"):
        if kode_input == AKSES_KODE:
            st.session_state.akses_granted = True
            st.success("Akses diterima ✅")
            st.rerun()
        else:
            st.error("Kode akses salah ❌")
    st.stop()

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

if submitted:
    st.session_state.submitted_once = True

    # Hitung skor
    current_scores = {key: 0 for key in questions.keys()}
    for category in questions.keys():
        for i in range(len(questions[category])):
            current_scores[category] += st.session_state[f"q_{category}_{i}"]

    st.divider()
    st.header("📊 Hasil Profil Minat Anda")

    # Buat grafik bar
    fig, ax = plt.subplots(figsize=(8,5))
    colors = ['#4c72b0','#55a868','#c44e52','#8172b2','#ccb974','#64b5cd']
    ax.bar(current_scores.keys(), current_scores.values(), color=colors)
    ax.set_ylabel("Skor")
    ax.set_title("Hasil Tes RIASEC")
    st.pyplot(fig)

    # Top 3
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
    # PDF Laporan Profesional
    # =========================
    pdf = FPDF(orientation="P", unit="mm", format="A4")
    pdf.add_page()
    
    # Header
    pdf.set_font("Arial", "B", 18)
    pdf.cell(0, 10, "Laporan Hasil Tes RIASEC", ln=True, align="C")
    pdf.ln(5)
    pdf.set_font("Arial", "", 12)
    pdf.multi_cell(0, 6, "Tes ini bertujuan untuk mengetahui tipe minat dan bakat Anda berdasarkan model RIASEC.", align="C")
    pdf.ln(10)

    # Tabel skor lengkap
    pdf.set_font("Arial", "B", 12)
    pdf.cell(60, 8, "Tipe", border=1, align="C")
    pdf.cell(40, 8, "Skor", border=1, align="C")
    pdf.cell(90, 8, "Rekomendasi Bidang", border=1, align="C")
    pdf.ln()
    pdf.set_font("Arial", "", 12)
    for tipe, score in current_scores.items():
        pdf.cell(60, 8, tipe, border=1)
        pdf.cell(40, 8, str(score), border=1, align="C")
        pdf.cell(90, 8, rekomendasi[tipe], border=1)
        pdf.ln()
    pdf.ln(5)

    # Highlight top 3
    pdf.set_font("Arial", "B", 14)
    pdf.cell(0, 8, "🏆 3 Tipe Dominan Anda", ln=True)
    pdf.set_font("Arial", "", 12)
    for idx, (label, score) in enumerate(top_3):
        pdf.cell(0, 7, f"{idx+1}. {label} - Skor: {score} | Bidang: {rekomendasi[label]}", ln=True)
    pdf.ln(5)
    pdf.cell(0, 8, f"Holland Code: {holland_code}", ln=True)

    # Tambahkan grafik
    img_buffer = BytesIO()
    fig.savefig(img_buffer, format='png', dpi=150)
    img_buffer.seek(0)
    pdf.image(img_buffer, x=15, w=180)
    
    # Tombol download
    pdf_buffer = BytesIO()
    pdf.output(pdf_buffer)
    pdf_buffer.seek(0)
    st.download_button("⬇️ Unduh Laporan PDF Profesional", data=pdf_buffer, file_name="laporan_riasec.pdf", mime="application/pdf")
