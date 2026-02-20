import streamlit as st
import pandas as pd
import plotly.graph_objects as go

st.set_page_config(page_title="Tes RIASEC Pro", layout="centered")

st.title("🎯 Tes Minat & Bakat (RIASEC)")
st.write("Geser slider sesuai dengan seberapa cocok pernyataan tersebut dengan diri Anda.")

# Data Pertanyaan
questions = {
    "Realistic (R)": ["Bekerja dengan alat/mesin", "Aktivitas luar ruangan", "Memperbaiki barang", "Aktivitas fisik", "Bekerja dengan tangan"],
    "Investigative (I)": ["Memecahkan masalah kompleks", "Riset/Eksperimen", "Menganalisis data", "Sains/Matematika", "Berpikir logis"],
    "Artistic (A)": ["Menggambar/Mendesain", "Menulis cerita/puisi", "Musik/Seni", "Ekspresi kreatif", "Ide-ide baru"],
    "Social (S)": ["Membantu orang lain", "Mengajar/Membimbing", "Bekerja dalam tim", "Kesejahteraan sesama", "Interaksi sosial"],
    "Enterprising (E)": ["Memimpin kelompok", "Meyakinkan orang lain", "Bisnis/Wirausaha", "Mengambil keputusan", "Berkompetisi"],
    "Conventional (C)": ["Pekerjaan terstruktur", "Ketelitian tugas", "Bekerja dengan angka", "Perencanaan rinci", "Mengikuti aturan"]
}

# Inisialisasi skor
scores = {key: 0 for key in questions.keys()}

# Form Input
with st.form("riasec_form"):
    for category, qs in questions.items():
        st.subheader(f"--- Bagian {category} ---")
        for i, q in enumerate(qs):
            response = st.select_slider(
                q, options=[1, 2, 3, 4, 5], value=3, key=f"{category}_{i}"
            )
            scores[category] += response
    
    submit = st.form_submit_button("Analisis Hasil Saya")

if submit:
    st.divider()
    st.header("📊 Analisis Profil Anda")

    # Membuat Radar Chart
    categories = list(scores.keys())
    values = list(scores.values())
    values += [values[0]]  # Menutup garis radar
    categories += [categories[0]]

    fig = go.Figure()
    fig.add_trace(go.Scatterpolar(
        r=values,
        theta=categories,
        fill='toself',
        line_color='teal'
    ))
    fig.update_layout(polar=dict(radialaxis=dict(visible=True, range=[0, 25])), showlegend=False)
    
    st.plotly_chart(fig)

    # Menentukan Top 3
    sorted_scores = sorted(scores.items(), key=lambda x: x[1], reverse=True)
    top_3 = sorted_scores[:3]

    rekomendasi = {
        "Realistic (R)": "Teknik, Arsitektur, Otomotif, IT Hardware.",
        "Investigative (I)": "Data Scientist, Peneliti, Dokter, Arkeolog.",
        "Artistic (A)": "Desainer, Penulis, Musisi, Arsitek Kreatif.",
        "Social (S)": "Guru, Psikolog, Perawat, HRD.",
        "Enterprising (E)": "Manajer, Sales, Politisi, Entrepreneur.",
        "Conventional (C)": "Akuntan, Notaris, Auditor, Admin Database."
    }

    st.subheader("🏆 3 Tipe Dominan Anda:")
    cols = st.columns(3)
    for i, (label, score) in enumerate(top_3):
        with cols[i]:
            st.metric(label=f"Peringkat {i+1}", value=label.split()[0])
            st.write(f"**Skor:** {score}")
            st.caption(f"Fokus: {rekomendasi[label]}")

    st.success(f"Kode Holland Anda adalah: **{''.join([x[0][0] for x in top_3])}**")
