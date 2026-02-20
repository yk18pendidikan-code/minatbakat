import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="Tes Minat & Bakat (RIASEC)",
    layout="centered"
)

# ===============================
# RESPONSIVE CSS
# ===============================
st.markdown("""
<style>

/* Background */
.stApp {
    background: linear-gradient(135deg, #667eea, #764ba2);
    font-family: 'Segoe UI', sans-serif;
}

/* Main Card */
.main-card {
    background: white;
    padding: 40px;
    border-radius: 20px;
    box-shadow: 0 15px 35px rgba(0,0,0,0.15);
    max-width: 900px;
    margin: auto;
}

/* Title */
.title {
    text-align: center;
    font-size: 36px;
    font-weight: 700;
    color: #4b0082;
    margin-bottom: 10px;
}

.subtitle {
    text-align: center;
    font-size: 16px;
    color: #666;
    margin-bottom: 30px;
}

/* Section Header */
h3 {
    margin-top: 30px;
    color: #333;
}

/* Button */
.stButton > button {
    background: linear-gradient(90deg, #6C63FF, #5a52d4);
    color: white;
    border-radius: 12px;
    height: 50px;
    width: 100%;
    font-size: 18px;
    font-weight: 600;
    border: none;
    transition: 0.3s;
}

.stButton > button:hover {
    transform: scale(1.02);
    box-shadow: 0 5px 15px rgba(0,0,0,0.2);
}

/* Slider spacing */
.stSlider {
    margin-bottom: 20px;
}

/* Footer */
.footer {
    text-align: center;
    font-size: 13px;
    margin-top: 40px;
    color: #888;
}

/* Tablet */
@media (max-width: 992px) {
    .main-card {
        padding: 30px;
    }

    .title {
        font-size: 28px;
    }

    .subtitle {
        font-size: 14px;
    }
}

/* Mobile */
@media (max-width: 600px) {
    .main-card {
        padding: 20px;
        border-radius: 15px;
    }

    .title {
        font-size: 22px;
    }

    .subtitle {
        font-size: 13px;
    }

    .stButton > button {
        font-size: 16px;
        height: 45px;
    }

    h3 {
        font-size: 16px;
    }
}

/* Very Small Mobile */
@media (max-width: 400px) {
    .title {
        font-size: 18px;
    }

    .subtitle {
        font-size: 12px;
    }
}

</style>
""", unsafe_allow_html=True)

# ===============================
# HEADER
# ===============================
st.markdown('<div class="main-card">', unsafe_allow_html=True)

st.markdown('<div class="title">Tes Minat & Bakat - RIASEC</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Skala 1 = Sangat Tidak Sesuai | 5 = Sangat Sesuai</div>', unsafe_allow_html=True)

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

scores = {key: 0 for key in questions.keys()}

# ===============================
# FORM PERTANYAAN
# ===============================
for category, qs in questions.items():
    st.markdown(f"### Bagian {category}")
    for i, q in enumerate(qs):
        response = st.slider(
            label=q,
            min_value=1,
            max_value=5,
            value=3,
            key=f"{category}_{i}"
        )
        scores[category] += response

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

st.markdown('<div class="footer">© 2026 Tes Minat & Bakat RIASEC</div>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)
