import streamlit as st
import pandas as pd

st.set_page_config(page_title="Tes Minat & Bakat (RIASEC)", layout="centered")

st.title("✨ Tes Minat & Bakat - Model RIASEC ✨")
st.write("Jawablah setiap pernyataan sesuai dengan diri Anda.")
st.write("Skala: 1 = Sangat Tidak Sesuai | 5 = Sangat Sesuai")

questions = {
    "R": [
        "Saya senang bekerja dengan alat atau mesin.",
        "Saya suka kegiatan di luar ruangan.",
        "Saya tertarik memperbaiki barang rusak.",
        "Saya menikmati aktivitas fisik.",
        "Saya suka bekerja dengan tangan."
    ],
    "I": [
        "Saya suka memecahkan masalah kompleks.",
        "Saya menikmati penelitian atau eksperimen.",
        "Saya senang menganalisis data.",
        "Saya tertarik pada sains atau matematika.",
        "Saya suka berpikir logis dan sistematis."
    ],
    "A": [
        "Saya menikmati menggambar atau mendesain.",
        "Saya suka menulis cerita atau puisi.",
        "Saya tertarik pada musik atau seni pertunjukan.",
        "Saya senang mengekspresikan diri secara kreatif.",
        "Saya suka menciptakan ide-ide baru."
    ],
    "S": [
        "Saya senang membantu orang lain.",
        "Saya suka mengajar atau membimbing.",
        "Saya nyaman bekerja dalam tim.",
        "Saya peduli terhadap kesejahteraan orang lain.",
        "Saya senang berinteraksi dengan banyak orang."
    ],
    "E": [
        "Saya suka memimpin kelompok.",
        "Saya senang meyakinkan orang lain.",
        "Saya tertarik pada bisnis atau wirausaha.",
        "Saya suka mengambil keputusan penting.",
        "Saya senang berkompetisi."
    ],
    "C": [
        "Saya suka pekerjaan yang terstruktur.",
        "Saya teliti dalam mengerjakan tugas.",
        "Saya nyaman bekerja dengan angka atau data.",
        "Saya suka membuat perencanaan rinci.",
        "Saya mengikuti aturan dengan baik."
    ]
}

scores = {"R": 0, "I": 0, "A": 0, "S": 0, "E": 0, "C": 0}

st.subheader("Silakan jawab pertanyaan berikut:")

# Fungsi untuk membuat opsi estetis
def show_aesthetic_options(key_prefix):
    cols = st.columns(5)
    options = []
    for i, col in enumerate(cols, start=1):
        if col.button("⚪", key=f"{key_prefix}_{i}"):
            options.append(i)
    return options[0] if options else 3  # default 3

for category, qs in questions.items():
    st.markdown(f"### 🟢 Bagian {category}")
    for idx, q in enumerate(qs, start=1):
        st.markdown(f"**{idx}. {q}**")
        choice = st.radio(
            label="Pilih jawaban:",
            options=[1,2,3,4,5],
            index=2,
            horizontal=True,
            key=f"{category}_{idx}"
        )
        scores[category] += choice
        st.markdown("---")  # pemisah antar pertanyaan

# -----------------------------
# HASIL
# -----------------------------
if st.button("Lihat Hasil"):
    st.subheader("📊 Hasil Tes Anda")
    df = pd.DataFrame(scores.items(), columns=["Tipe", "Skor"])
    st.bar_chart(df.set_index("Tipe"))

    dominant = max(scores, key=scores.get)

    rekomendasi = {
        "R": "Teknik, Arsitektur, Otomotif, Teknologi Industri",
        "I": "Ilmu Data, Penelitian, Kedokteran, Sains",
        "A": "Desain Grafis, Musik, Seni, Penulisan",
        "S": "Psikologi, Pendidikan, Konseling, Keperawatan",
        "E": "Bisnis, Manajemen, Marketing, Wirausaha",
        "C": "Akuntansi, Administrasi, Keuangan, Analis Data"
    }

    st.success(f"Tipe dominan Anda adalah: {dominant}")
    st.info(f"Rekomendasi bidang yang cocok: {rekomendasi[dominant]}")
    st.write("Catatan: Tes ini bersifat eksploratif dan bukan alat diagnosis profesional.")
