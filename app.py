import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# ======================================================
# PAGE CONFIG
# ======================================================

st.set_page_config(
    page_title="Instagram Risk Dashboard",
    page_icon="📊",
    layout="wide"
)

# ======================================================
# SIMPLE UI STYLE (lebih clean & friendly)
# ======================================================

st.markdown("""
<style>

.main {
    background-color: #f8fafc;
}

.block-container {
    padding-top: 1.2rem;
    padding-left: 2rem;
    padding-right: 2rem;
}

.card {
    background: white;
    padding: 18px;
    border-radius: 14px;
    box-shadow: 0 2px 10px rgba(0,0,0,0.06);
}

.small {
    font-size: 13px;
    color: #6b7280;
}

.title {
    font-size: 26px;
    font-weight: 700;
}

</style>
""", unsafe_allow_html=True)

# ======================================================
# LOAD DATASET
# ======================================================

try:
    df = pd.read_csv("dataset.csv", encoding="utf-8")
except:
    df = pd.read_csv("dataset.csv", encoding="latin1")

df.columns = df.columns.str.strip()
df.columns = df.columns.str.replace("\n", " ", regex=True)

# ======================================================
# KONSTRUK VARIABEL
# ======================================================

X1 = ["X1.1","X1.2","X1.3","X1.4","X1.5"]
X2 = ["X2.1","X2.3","X2.4","X2.5"]
Y  = ["Y1","Y2","Y3","Y4","Y5"]

required_cols = X1 + X2 + Y

missing = [c for c in required_cols if c not in df.columns]

if missing:
    st.error(f"Dataset tidak lengkap: {missing}")
    st.stop()

# ======================================================
# HITUNG SKOR DASAR
# ======================================================

df["Skor Algoritma"] = df[X1].mean(axis=1)
df["Skor Echo Chamber"] = df[X2].mean(axis=1)
df["Skor Risiko"] = df[Y].mean(axis=1)

# ======================================================
# KATEGORI RISIKO (USER FRIENDLY)
# ======================================================

def kategori_risiko(x):
    if x < 2.61:
        return "Rendah"
    elif x < 3.41:
        return "Sedang"
    else:
        return "Tinggi"

df["Kategori Risiko"] = df["Skor Risiko"].apply(kategori_risiko)

# ======================================================
# USER-FRIENDLY RISK SUMMARY (INI PENGGANTI AMBIGUITAS)
# ======================================================

mean_risk = df["Skor Risiko"].mean()
dominant_risk = df["Kategori Risiko"].value_counts().idxmax()

# ======================================================
# HEADER
# ======================================================

st.markdown('<div class="title">📱 Instagram Risk Dashboard</div>', unsafe_allow_html=True)

st.caption(
    "Dashboard ini membantu memahami tingkat risiko penggunaan Instagram berdasarkan data responden."
)

# ======================================================
# RINGKASAN UTAMA (TIDAK AMBIGU)
# ======================================================

col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    <div class="card">
    <b>Rata-rata Risiko Pengguna</b><br>
    <h2>{:.2f}/5</h2>
    <div class="small">Menunjukkan tingkat risiko secara umum</div>
    </div>
    """.format(mean_risk), unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div class="card">
    <b>Kategori yang Paling Banyak</b><br>
    <h2>{dominant_risk}</h2>
    <div class="small">Berdasarkan jumlah responden terbanyak</div>
    </div>
    """, unsafe_allow_html=True)

# ======================================================
# INTERPRETASI OTOMATIS (UNTUK RESPONDEN)
# ======================================================

st.markdown("### 📌 Interpretasi Sederhana")

if mean_risk >= 3.41:
    st.error(
        "Sebagian besar pengguna menunjukkan tingkat risiko tinggi dalam penggunaan Instagram."
    )

elif mean_risk >= 2.61:
    st.warning(
        "Pengguna berada pada tingkat risiko sedang. Perlu pengelolaan penggunaan yang lebih seimbang."
    )

else:
    st.success(
        "Penggunaan Instagram masih dalam kategori aman dan terkendali."
    )

# ======================================================
# PENJELASAN METODE (VERSI SIMPLE)
# ======================================================

with st.expander("ℹ️ Cara Membaca Dashboard Ini"):
    st.markdown("""
    - Skor dihitung dari hasil kuesioner pengguna Instagram  
    - Skor 1–5 menunjukkan tingkat rendah hingga tinggi  
    - Semakin tinggi skor → semakin besar risiko penggunaan berlebihan  
    - Kategori dibuat untuk memudahkan pemahaman hasil analisis  
    """)

# ======================================================
# SIDEBAR
# ======================================================

st.sidebar.title("Filter Data")

st.sidebar.metric("Total Responden", len(df))

# ======================================================
# PART 2 - VISUALISASI USER FRIENDLY
# ======================================================

st.markdown("## 📊 Gambaran Penggunaan & Risiko")

# ======================================================
# DISTRIBUSI SKOR RISIKO
# ======================================================

col1, col2 = st.columns(2)

with col1:

    fig_risk = px.histogram(
        df,
        x="Skor Risiko",
        nbins=8,
        title="Sebaran Tingkat Risiko Pengguna",
        color_discrete_sequence=["#2563eb"]
    )

    fig_risk.update_layout(
        height=380,
        xaxis_title="Skor Risiko",
        yaxis_title="Jumlah Pengguna"
    )

    st.plotly_chart(fig_risk, use_container_width=True)

    st.caption("Semakin ke kanan, semakin tinggi tingkat risiko.")

# ======================================================
# KOMPOSISI KATEGORI RISIKO (DIPERBAIKI)
# ======================================================

with col2:

    kategori_df = df["Kategori Risiko"].value_counts().reset_index()
    kategori_df.columns = ["Kategori", "Jumlah"]

    fig_pie = px.pie(
        kategori_df,
        names="Kategori",
        values="Jumlah",
        hole=0.55,
        title="Sebaran Kategori Risiko"
    )

    fig_pie.update_layout(height=380)

    st.plotly_chart(fig_pie, use_container_width=True)

    st.caption("Menunjukkan kelompok pengguna berdasarkan tingkat risiko.")

# ======================================================
# RATA-RATA VARIABEL (SIMPLIFIED)
# ======================================================

st.markdown("---")

st.markdown("### 📌 Ringkasan Faktor Utama")

mean_df = pd.DataFrame({
    "Faktor": [
        "Algoritma Rekomendasi",
        "Echo Chamber",
        "Risiko Adiksi"
    ],
    "Skor": [
        df["Skor Algoritma"].mean(),
        df["Skor Echo Chamber"].mean(),
        df["Skor Risiko"].mean()
    ]
})

fig_bar = px.bar(
    mean_df,
    x="Faktor",
    y="Skor",
    text_auto=".2f",
    color="Skor",
    title="Rata-rata Setiap Faktor"
)

fig_bar.update_layout(
    height=420,
    xaxis_title="",
    yaxis_title="Skor Rata-rata"
)

st.plotly_chart(fig_bar, use_container_width=True)

st.caption("Nilai lebih tinggi menunjukkan pengaruh/tingkat yang lebih kuat.")

# ======================================================
# PART 3 - INSIGHT, SMARTPLS, MITIGASI (USER FRIENDLY)
# ======================================================

st.markdown("## 📌 Insight & Hasil Analisis")

# ======================================================
# INSIGHT SINGKAT (JANGAN PANJANG)
# ======================================================

col1, col2 = st.columns(2)

with col1:
    st.info(
        "Sebagian besar pengguna menunjukkan tingkat risiko penggunaan Instagram yang bervariasi dari sedang hingga tinggi."
    )

with col2:
    st.info(
        "Echo Chamber menjadi faktor yang paling berpengaruh terhadap peningkatan risiko adiksi digital."
    )

st.markdown("---")

# ======================================================
# SMARTPLS (VERSI SEDERHANA)
# ======================================================

st.markdown("### 📊 Hasil Analisis Model (SmartPLS)")

st.caption("Hasil ini menunjukkan hubungan antar faktor dalam penelitian.")

smartpls_simple = pd.DataFrame({
    "Hubungan": [
        "Algoritma → Risiko Adiksi",
        "Echo Chamber → Risiko Adiksi"
    ],
    "Hasil": [
        "Tidak signifikan",
        "Signifikan"
    ]
})

st.dataframe(
    smartpls_simple,
    use_container_width=True
)

st.caption(
    "Interpretasi: hanya Echo Chamber yang memiliki pengaruh nyata terhadap risiko adiksi."
)

st.markdown("---")

# ======================================================
# MITIGASI (VERSI USER FRIENDLY)
# ======================================================

st.markdown("### 🛡️ Saran Penggunaan yang Lebih Sehat")

mitigasi = pd.DataFrame({
    "Masalah": [
        "Penggunaan berlebihan",
        "Konten yang mirip terus-menerus",
        "Kurang variasi informasi",
        "Risiko ketergantungan"
    ],
    "Saran Sederhana": [
        "Batasi waktu penggunaan harian",
        "Cari akun dengan topik berbeda",
        "Ikuti sumber informasi beragam",
        "Gunakan fitur screen time"
    ]
})

st.dataframe(
    mitigasi,
    use_container_width=True
)

st.markdown("---")

# ======================================================
# PENUTUP INSIGHT
# ======================================================

st.success(
    """
    Kesimpulan sederhana:

    • Risiko penggunaan Instagram berada pada tingkat sedang hingga tinggi  
    • Echo Chamber memiliki pengaruh paling kuat  
    • Pengendalian pola konsumsi konten sangat diperlukan
    """
)
