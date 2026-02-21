import streamlit as st
import pandas as pd
from fpdf import FPDF
import tempfile

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
    st.title("Akses Tes RIASEC Neutron Murangan")
    kode_input = st.text_input("Masukkan Kode Akses", type="password")
    if st.button("Masuk"):
        if kode_input == AKSES_KODE:
            st.session_state.akses_granted = True
            st.success("Akses diterima")
            st.rerun()
        else:
            st.error("Kode akses salah")
    st.stop()

if st.session_state.submitted_once:
    st.warning("Anda sudah mengerjakan tes ini. Tes hanya dapat dikerjakan 1 kali.")
    st.stop()

# =========================
# APLIKASI TES
# =========================
st.title("Tes Minat & Bakat (RIASEC) Neutron Murangan")
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
            st.select_slider(q, options=[1,2,3,4,5], value=3, key=f"q_{category}_{i}")
    submitted = st.form_submit_button("Lihat Hasil Analisis")

if submitted:
    st.session_state.submitted_once = True

    # Hitung skor
    current_scores = {key: 0 for key in questions.keys()}
    for category in questions.keys():
        for i in range(len(questions[category])):
            current_scores[category] += st.session_state[f"q_{category}_{i}"]

    st.divider()
    st.header("Hasil Profil Minat Anda")
    df_scores = pd.DataFrame(current_scores.items(), columns=["Tipe", "Skor"]).set_index("Tipe")
    st.bar_chart(df_scores)

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

    st.subheader("3 Tipe Dominan Anda")
    cols = st.columns(3)
    for idx, (label, score) in enumerate(top_3):
        with cols[idx]:
            st.info(f"{idx+1}. {label.split()[0]}")
            st.write(f"Skor: {score}")
            st.caption(f"Bidang: {rekomendasi[label]}")

    holland_code = "".join([x[0][0] for x in top_3])
    st.success(f"Kode Holland Anda: {holland_code}")

    # =========================
    # PDF Profesional Tanpa Emoji
    # =========================
    pdf = FPDF(orientation="P", unit="mm", format="A4")
    pdf.add_page()

    pdf.set_font("Arial", "B", 16)
    pdf.cell(0,10,"Laporan Hasil Tes RIASEC", ln=True, align="C")
    pdf.ln(5)
    pdf.set_font("Arial", "", 12)
    pdf.multi_cell(0,6,"Tes ini bertujuan untuk mengetahui tipe minat dan bakat Anda berdasarkan model RIASEC.", align="C")
    pdf.ln(10)

    # Tabel skor lengkap
    pdf.set_font("Arial", "B", 12)
    pdf.cell(60,8,"Tipe", border=1, align="C")
    pdf.cell(40,8,"Skor", border=1, align="C")
    pdf.cell(90,8,"Rekomendasi Bidang", border=1, align="C")
    pdf.ln()
    pdf.set_font("Arial", "", 12)
    for tipe, score in current_scores.items():
        pdf.cell(60,8,tipe, border=1)
        pdf.cell(40,8,str(score), border=1, align="C")
        pdf.cell(90,8,rekomendasi[tipe], border=1)
        pdf.ln()
    pdf.ln(5)

    # Top 3 dominan
    pdf.set_font("Arial", "B", 14)
    pdf.cell(0,8,"3 Tipe Dominan Anda", ln=True)
    pdf.set_font("Arial","",12)
    for idx,(label, score) in enumerate(top_3):
        pdf.cell(0,7,f"{idx+1}. {label} - Skor: {score} | Bidang: {rekomendasi[label]}", ln=True)
    pdf.ln(5)
    pdf.cell(0,8,f"Holland Code: {holland_code}", ln=True)
    pdf.ln(5)

    # Grafik sederhana kotak warna
    max_score = 25
    bar_width = 100
    bar_height = 7
    colors = ["#4c72b0","#55a868","#c44e52","#8172b2","#ccb974","#64b5cd"]

    for i,(tipe,score) in enumerate(current_scores.items()):
        pdf.set_fill_color(*[int(colors[i][j:j+2],16) for j in (1,3,5)])
        bar_len = int(score/max_score*bar_width)
        pdf.cell(40,bar_height,tipe,border=0)
        pdf.cell(bar_len,bar_height,"",border=1,ln=1,fill=True)

    # Tombol download PDF
    pdf_buffer = tempfile.NamedTemporaryFile(suffix=".pdf", delete=False)
    pdf.output(pdf_buffer.name)
    pdf_buffer.seek(0)
    st.download_button("Unduh Laporan PDF Profesional", data=pdf_buffer, file_name="laporan_riasec.pdf", mime="application/pdf")
