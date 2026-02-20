import streamlit as st
import pandas as pd

st.set_page_config(page_title="Tes RIASEC Neutron", layout="centered")

st.title("🎯 Tes Minat & Bakat (RIASEC) Neutron Murangan")
st.write("Jawablah sesuai kepribadian Anda. Skala 1 (Tidak Sesuai) hingga 5 (Sangat Sesuai).")

# Data Pertanyaan
questions = {
    "Realistic (R)": ["Suka bekerja dengan alat/mesin", "Suka aktivitas luar ruangan", "Bisa memperbaiki barang rusak", "Menyukai aktivitas fisik", "Suka bekerja dengan tangan"],
    "Investigative (I)": ["Suka memecahkan masalah rumit", "Senang riset atau eksperimen", "Suka menganalisis data", "Tertarik sains/matematika", "Berpikir logis & sistematis"],
    "Artistic (A)": ["Suka menggambar/mendesain", "Suka menulis cerita/puisi", "Tertarik musik/seni", "Senang ekspresi kreatif", "Suka menciptakan ide baru"],
    "Social (S)": ["Senang membantu orang lain", "Suka mengajar/membimbing", "Nyaman bekerja dalam tim", "Peduli kesejahteraan sesama", "Senang berinteraksi sosial"],
    "Enterprising (E)": ["Suka memimpin kelompok", "Senang meyakinkan orang lain", "Tertarik bisnis/wirausaha", "Berani ambil keputusan", "Senang berkompetisi"],
    "Conventional (C)": ["Suka kerja terstruktur", "Teliti dalam tugas", "Nyaman dengan angka/data", "Suka perencanaan rinci", "Patuh pada aturan"]
}

# Inisialisasi skor di session state agar tidak hilang saat refresh
if 'scores' not in st.session_state:
    st.session_state.scores = {key: 0 for key in questions.keys()}

# Form Input
with st.form("quiz_form"):
    for category, qs in questions.items():
        st.markdown(f"### {category}")
        for i, q in enumerate(qs):
            st.select_slider(q, options=[1, 2, 3, 4, 5], value=3, key=f"q_{category}_{i}")
    
    submitted = st.form_submit_button("Lihat Hasil Analisis")

if submitted:
    # Hitung Skor
    current_scores = {key: 0 for key in questions.keys()}
    for category in questions.keys():
        for i in range(len(questions[category])):
            current_scores[category] += st.session_state[f"q_{category}_{i}"]
    
    st.divider()
    st.header("📊 Hasil Profil Minat Anda")

    # Visualisasi dengan Bar Chart bawaan Streamlit (Tanpa Plotly)
    chart_data = pd.DataFrame(current_scores.items(), columns=["Tipe", "Skor"]).set_index("Tipe")
    st.bar_chart(chart_data)

    # Menentukan Top 3
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
    
    # Menampilkan hasil dalam kolom
    cols = st.columns(3)
    for idx, (label, score) in enumerate(top_3):
        with cols[idx]:
            st.info(f"**{idx+1}. {label.split()[0]}**")
            st.write(f"Skor: **{score}**")
            st.caption(f"Bidang: {rekomendasi[label]}")

    # Menampilkan Kode Holland
    holland_code = "".join([x[0][0] for x in top_3])
    st.success(f"Kode Holland Anda adalah: **{holland_code}**")
    
    st.balloons()
