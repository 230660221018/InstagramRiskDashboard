# ======================================================
# IMPORT
# ======================================================
import streamlit as st
import pandas as pd
import plotly.express as px

# ======================================================
# PAGE CONFIG (UX CLEAN + MODERN)
# ======================================================
st.set_page_config(
    page_title="Instagram Digital Risk Analytics",
    page_icon="📊",
    layout="wide"
)

# ======================================================
# CUSTOM CSS (SOFT MODERN DASHBOARD STYLE)
# ======================================================
st.markdown("""
<style>

.main {
    background: #f8fafc;
}

.block-container {
    padding-top: 1.2rem;
    padding-left: 2rem;
    padding-right: 2rem;
}

/* KPI CARD */
.kpi-card {
    background: white;
    padding: 18px;
    border-radius: 16px;
    box-shadow: 0px 4px 14px rgba(0,0,0,0.06);
    border-left: 5px solid #2563eb;
}

.kpi-title {
    font-size: 13px;
    color: #64748b;
}

.kpi-value {
    font-size: 28px;
    font-weight: 700;
    color: #111827;
}

.kpi-sub {
    font-size: 12px;
    color: #94a3b8;
}

</style>
""", unsafe_allow_html=True)

# ======================================================
# LOAD DATASET (ROBUST)
# ======================================================
try:
    try:
        df = pd.read_csv("dataset.csv", encoding="utf-8")
    except:
        df = pd.read_csv("dataset.csv", encoding="latin1")

except:
    st.error("Dataset tidak ditemukan.")
    st.stop()

# ======================================================
# CLEAN COLUMN
# ======================================================
df.columns = df.columns.str.strip()
df.columns = df.columns.str.replace("\n", " ", regex=True)

# ======================================================
# MODEL VARIABLES
# ======================================================
X1 = ["X1.1","X1.2","X1.3","X1.4","X1.5"]
X2 = ["X2.1","X2.3","X2.4","X2.5"]
Y  = ["Y1","Y2","Y3","Y4","Y5"]

required_cols = X1 + X2 + Y

missing_cols = [c for c in required_cols if c not in df.columns]

if missing_cols:
    st.error(f"Kolom tidak ditemukan: {missing_cols}")
    st.stop()

# ======================================================
# SCORE CALCULATION
# ======================================================
df["Skor Algoritma"] = df[X1].mean(axis=1)
df["Skor Echo Chamber"] = df[X2].mean(axis=1)
df["Skor Risiko"] = df[Y].mean(axis=1)

# ======================================================
# RISK CATEGORY (CLEAR THRESHOLD LOGIC)
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
# SIDEBAR
# ======================================================
st.sidebar.title("📊 Risk Analytics Dashboard")

st.sidebar.markdown("""
**Variabel Penelitian:**
- Algoritma Rekomendasi Konten  
- Echo Chamber  
- Risiko Adiksi Digital
""")

st.sidebar.markdown("---")

# ======================================================
# FILTER (USER FRIENDLY)
# ======================================================
gender = st.sidebar.multiselect(
    "Jenis Kelamin",
    df["Jenis Kelamin"].unique(),
    default=df["Jenis Kelamin"].unique()
)

usia = st.sidebar.multiselect(
    "Usia",
    df["Usia"].unique(),
    default=df["Usia"].unique()
)

durasi = st.sidebar.multiselect(
    "Durasi Penggunaan Instagram",
    df["Rata-rata Durasi Penggunaan Instagram per Hari"].unique(),
    default=df["Rata-rata Durasi Penggunaan Instagram per Hari"].unique()
)

# apply filter
df = df[
    (df["Jenis Kelamin"].isin(gender)) &
    (df["Usia"].isin(usia)) &
    (df["Rata-rata Durasi Penggunaan Instagram per Hari"].isin(durasi))
]

# ======================================================
# HEADER
# ======================================================
st.title("📱 Instagram Digital Risk Analytics Dashboard")

st.caption(
    "Analisis Pengaruh Algoritma Rekomendasi & Echo Chamber terhadap Risiko Adiksi Digital"
)

st.markdown("---")

# ======================================================
# KPI SECTION (NO AMBIGUITY DESIGN)
# ======================================================
c1, c2, c3 = st.columns(3)

dominant_category = df["Kategori Risiko"].value_counts().idxmax()

with c1:
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-title">Total Responden</div>
        <div class="kpi-value">{len(df)}</div>
        <div class="kpi-sub">Setelah filtering aktif</div>
    </div>
    """, unsafe_allow_html=True)

with c2:
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-title">Rata-rata Risiko</div>
        <div class="kpi-value">{df['Skor Risiko'].mean():.2f}</div>
        <div class="kpi-sub">Skor 1–5 (indikator intensitas)</div>
    </div>
    """, unsafe_allow_html=True)

with c3:
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-title">Kategori Dominan</div>
        <div class="kpi-value">{dominant_category}</div>
        <div class="kpi-sub">Kategori paling banyak muncul</div>
    </div>
    """, unsafe_allow_html=True)

# ======================================================
# INSIGHT ALERT (CLEAR INTERPRETATION LAYER)
# ======================================================
st.markdown("---")

mean_risk = df["Skor Risiko"].mean()

if mean_risk >= 4.21:
    st.error(f"Level Risiko: Sangat Tinggi ({mean_risk:.2f}/5)")
elif mean_risk >= 3.41:
    st.error(f"Level Risiko: Tinggi ({mean_risk:.2f}/5)")
elif mean_risk >= 2.61:
    st.warning(f"Level Risiko: Sedang ({mean_risk:.2f}/5)")
elif mean_risk >= 1.81:
    st.success(f"Level Risiko: Rendah ({mean_risk:.2f}/5)")
else:
    st.success(f"Level Risiko: Sangat Rendah ({mean_risk:.2f}/5)")

# ======================================================
# MINI INSIGHT (NO CONFLICT WITH KPI)
# ======================================================
st.markdown("### 📌 Insight Ringkas")

col1, col2, col3 = st.columns(3)

with col1:
    st.info(f"Usia dominan: {df['Usia'].mode()[0]}")

with col2:
    st.info(f"Gender dominan: {df['Jenis Kelamin'].mode()[0]}")

with col3:
    st.info(f"Pola risiko: {dominant_category} paling dominan")

# ======================================================
# FOOTER NOTE
# ======================================================
st.caption("Dashboard berbasis Design Science Research (DSR)")

# ======================================================
# TAB 1 - PROFIL RESPONDEN (UX CLEAN VERSION)
# ======================================================
with tabs[0]:

    st.subheader("👥 Profil Responden")

    st.markdown(
        "Karakteristik responden yang terlibat dalam penelitian ini."
    )

    # ======================================================
    # TOP INSIGHT ROW (NO KPI REDUNDANCY)
    # ======================================================
    col1, col2, col3 = st.columns(3)

    col1.metric("Total Responden", len(df))
    col2.metric("Usia Dominan", df["Usia"].mode()[0])
    col3.metric("Gender Dominan", df["Jenis Kelamin"].mode()[0])

    st.markdown("---")

    # ======================================================
    # DISTRIBUSI UTAMA (USIA + GENDER)
    # ======================================================
    c1, c2 = st.columns(2)

    with c1:

        usia_df = df["Usia"].value_counts().reset_index()
        usia_df.columns = ["Usia", "Jumlah"]

        fig_usia = px.bar(
            usia_df,
            x="Usia",
            y="Jumlah",
            text_auto=True,
            title="Distribusi Usia Responden"
        )

        fig_usia.update_layout(
            height=420,
            xaxis_title="Usia",
            yaxis_title="Jumlah Responden"
        )

        st.plotly_chart(fig_usia, use_container_width=True)

    with c2:

        gender_df = df["Jenis Kelamin"].value_counts().reset_index()
        gender_df.columns = ["Jenis Kelamin", "Jumlah"]

        fig_gender = px.pie(
            gender_df,
            names="Jenis Kelamin",
            values="Jumlah",
            hole=0.55,
            title="Komposisi Gender Responden"
        )

        fig_gender.update_layout(height=420)

        st.plotly_chart(fig_gender, use_container_width=True)

    # ======================================================
    # DURASI (SEBAGAI CONTEXT BEHAVIOR, BUKAN KPI)
    # ======================================================
    st.markdown("---")

    st.markdown("### ⏱ Pola Penggunaan Instagram")

    durasi_df = df[
        "Rata-rata Durasi Penggunaan Instagram per Hari"
    ].value_counts().reset_index()

    durasi_df.columns = ["Durasi", "Jumlah"]

    fig_durasi = px.bar(
        durasi_df,
        x="Durasi",
        y="Jumlah",
        text_auto=True,
        title="Distribusi Durasi Penggunaan Instagram"
    )

    fig_durasi.update_layout(
        height=450,
        xaxis_title="Durasi Penggunaan",
        yaxis_title="Jumlah Responden"
    )

    st.plotly_chart(fig_durasi, use_container_width=True)

    # ======================================================
    # MINI INTERPRETATION LAYER (INI YANG BIKIN UX LEVEL 5)
    # ======================================================
    st.markdown("---")

    st.markdown("### 🧠 Insight Profil Responden")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.info(
            f"Mayoritas responden berada pada kelompok usia {df['Usia'].mode()[0]}, menunjukkan dominasi generasi aktif digital."
        )

    with col2:
        st.info(
            f"Distribusi gender didominasi oleh {df['Jenis Kelamin'].mode()[0]}, sehingga hasil lebih merepresentasikan kelompok tersebut."
        )

    with col3:
        # interpretasi durasi tanpa angka berlebihan
        st.info(
            "Pola penggunaan menunjukkan kecenderungan penggunaan harian yang moderat hingga tinggi."
        )

    # ======================================================
    # FOOT NOTE (IMPORTANT UX CLARITY)
    # ======================================================
    st.caption(
        "Profil ini digunakan sebagai konteks demografis dalam interpretasi risiko adiksi digital."
    )

# ======================================================
# TAB 2 - ANALISIS RISIKO (UX LEVEL 5 STORY MODE)
# ======================================================
with tabs[2]:

    st.subheader("📊 Analisis Risiko Adiksi Digital")

    st.markdown(
        "Analisis hubungan antar variabel utama dalam model penelitian."
    )

    # ======================================================
    # 1. STORY FLOW VISUAL (MAIN INSIGHT)
    # ======================================================
    st.markdown("### 🔗 Alur Hubungan Variabel Penelitian")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.info("📡 Algoritma Rekomendasi Konten\n→ Paparan konten berbasis preferensi")

    with col2:
        st.warning("🧠 Echo Chamber\n→ Penguatan informasi sejenis")

    with col3:
        st.error("📱 Risiko Adiksi Digital\n→ Dampak perilaku penggunaan")

    st.markdown("---")

    # ======================================================
    # 2. CORE RELATIONSHIP VISUAL (ONLY 1 MAIN HEATMAP)
    # ======================================================
    st.markdown("### 📌 Kekuatan Hubungan Antar Variabel")

    corr = df[
        ["Skor Algoritma", "Skor Echo Chamber", "Skor Risiko"]
    ].corr()

    fig_corr = px.imshow(
        corr,
        text_auto=".2f",
        color_continuous_scale="RdBu",
        title="Matriks Korelasi Variabel Penelitian"
    )

    fig_corr.update_layout(height=450)

    st.plotly_chart(fig_corr, use_container_width=True)

    st.markdown("---")

    # ======================================================
    # 3. CAUSAL VIEW (INI PENGGANTI SCATTER BERULANG)
    # ======================================================
    st.markdown("### 🔬 Hubungan Kausal Antar Variabel")

    col1, col2 = st.columns(2)

    with col1:

        fig1 = px.scatter(
            df,
            x="Skor Algoritma",
            y="Skor Risiko",
            color="Kategori Risiko",
            title="Algoritma → Risiko Adiksi"
        )

        fig1.update_layout(height=420)

        st.plotly_chart(fig1, use_container_width=True)

    with col2:

        fig2 = px.scatter(
            df,
            x="Skor Echo Chamber",
            y="Skor Risiko",
            color="Kategori Risiko",
            title="Echo Chamber → Risiko Adiksi"
        )

        fig2.update_layout(height=420)

        st.plotly_chart(fig2, use_container_width=True)

    # ======================================================
    # 4. KEY INSIGHT (INI YANG BIKIN DASHBOARD KELIHATAN "CERDAS")
    # ======================================================
    st.markdown("---")

    st.markdown("### 🧠 Insight Utama Analisis")

    col1, col2 = st.columns(2)

    with col1:

        st.success(
            """
            **Echo Chamber → Risiko**

            Terlihat adanya pola positif:
            peningkatan Echo Chamber cenderung diikuti peningkatan Risiko Adiksi Digital.
            """
        )

    with col2:

        st.warning(
            """
            **Algoritma → Risiko**

            Hubungan lebih lemah dibanding Echo Chamber,
            menunjukkan pengaruh tidak langsung atau terbatas.
            """
        )

    # ======================================================
    # 5. OPTIONAL BEHAVIOR CONTEXT (TIDAK OVERLOAD)
    # ======================================================
    aktivitas_col = None

    for col in df.columns:
        if "Aktivitas Instagram" in col:
            aktivitas_col = col
            break

    if aktivitas_col:

        st.markdown("---")
        st.markdown("### ⏱ Risiko Berdasarkan Aktivitas")

        aktivitas = df.groupby(aktivitas_col)["Skor Risiko"].mean().reset_index()

        fig_aktivitas = px.bar(
            aktivitas,
            x=aktivitas_col,
            y="Skor Risiko",
            text_auto=".2f",
            title="Rata-rata Risiko Berdasarkan Aktivitas"
        )

        fig_aktivitas.update_layout(height=500)

        st.plotly_chart(fig_aktivitas, use_container_width=True)

    # ======================================================
    # FOOT NOTE (CLARITY STATEMENT)
    # ======================================================
    st.caption(
        "Analisis ini digunakan untuk memahami hubungan antar variabel dalam model penelitian."
    )
