import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="Tes Minat & Bakat (RIASEC)",
    layout="centered"
)

# ===============================
# CUSTOM CSS
# ===============================
st.markdown("""
<style>

/* BODY BACKGROUND */
.stApp {
    background-color: #f4f6f9;
    font-family: 'Segoe UI', sans-serif;
}

/* MAIN CARD */
.card {
    background: #ffffff;
    padding: 40px;
    border-radius: 14px;
    box-shadow: 0 8px 25px rgba(0,0,0,0.1);
    max-width: 900px;
    margin: 30px auto;
    border: 1px solid #eee;
}

/* TITLE MERAH */
.title {
    text-align: center;
    font-size: 34px;
    font-weight: 700;
    color: #c40000 !important;
    margin-bottom: 10px;
}

/* SUBTITLE */
.subtitle {
    text-align: center;
    font-size: 15px;
    color: #222 !important;
    margin-bottom: 30px;
}

/* SECTION HEADER */
h3 {
    margin-top: 30px;
    color: #c40000 !important;
}

/* RADIO SPACING */
div[role="radiogroup"] {
    margin-bottom: 20px;
}

/* BUTTON MERAH */
.stButton > button {
    background-color: #c40000;
    color: white !important;
    border-radius: 8px;
    height: 45px;
    width: 100%;
    font-size: 16px;
    font-weight: 600;
    border: none;
}

.stButton > button:hover {
    background-color: #990000;
    color: white !important;
}

/* FOOTER */
.footer {
    text-align: center;
    font-size: 13px;
    margin-top: 40px;
    color: #777 !important;
}

/* CHART PUTIH */
[data-testid="stVerticalBlock"] .stBarChart svg {
    background-color: #ffffff !important;
}

/* RESPONSIVE */
@media (max-width: 600px) {
    .card {
        padding: 20px;
    }

    .title {
        font-size: 24px;
    }

    .subtitle {
        font-size: 13px;
    }

    h3 {
        font-size: 16px;
    }
}

</style>
""", unsafe_allow_html=True)

# ===============================
# CARD CONTAINER START
# ===============================
st.markdown('<div class="card">', unsafe_allow_html=True)

st.markdown('<div class="title">Tes Minat & Bakat - RIASEC</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Pilih jawaban yang paling sesuai dengan diri Anda</div>', unsafe_allow_html=True)

# ===============================
# DATA PERTANYAAN
# ===============================
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

options = {
    1: "1 - Sangat Tidak Sesuai",
    2: "2 - Tidak Sesuai",
    3: "3 - Netral",
    4: "4 - Sesuai",
    5: "5 - Sangat Sesuai"
}

scores = {key: 0 for key in questions.keys()}

# ===============================
# FORM PERTANYAAN
# ===============================
for category, qs in questions.items():
    st.markdown(f"### Bagian {category}")
    for i, q in enumerate(qs):
        choice = st.radio(
            q,
            options=list(options.keys()),
            format_func=lambda x: options[x],
            key=f"{category}_{i}"
        )
        scores[category] += choice

# ===============================
# HASIL
# ===============================
if st.button("Lihat Hasil"):
    st.subheader("Hasil Tes Anda")

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
    st.info(f"Rekomendasi bidang: {rekomendasi[dominant]}")

# ===============================
# FOOTER
# ===============================
st.markdown('<div class="footer">© 2026 Tes Minat & Bakat RIASEC</div>', unsafe_allow_html=True)

# ===============================
# CARD CONTAINER END
# ===============================
st.markdown('</div>', unsafe_allow_html=True)
