import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# ======================================================
# PAGE CONFIG
# ======================================================

st.set_page_config(
    page_title="Instagram Digital Addiction Risk Analytics Dashboard",
    page_icon="📊",
    layout="wide"
)

# ======================================================
# CUSTOM STYLE
# ======================================================

st.markdown("""
<style>

.main{
    background:#f8fafc;
}

.block-container{
    padding-top:1rem;
    padding-left:2rem;
    padding-right:2rem;
}

.metric-card{
    background:white;
    padding:20px;
    border-radius:18px;
    box-shadow:0px 4px 12px rgba(0,0,0,0.08);
    border-left:6px solid #2563eb;
}

.metric-title{
    font-size:14px;
    color:#64748b;
}

.metric-value{
    font-size:30px;
    font-weight:700;
    color:#0f172a;
}

.small-text{
    font-size:12px;
    color:#64748b;
}

</style>
""", unsafe_allow_html=True)

# ======================================================
# LOAD DATASET
# ======================================================

try:

    try:

        df = pd.read_csv(
            "dataset.csv",
            encoding="utf-8"
        )

    except:

        df = pd.read_csv(
            "dataset.csv",
            encoding="latin1"
        )

except:

    st.error(
        "dataset.csv tidak ditemukan pada repository."
    )

    st.stop()

# ======================================================
# CLEANING COLUMN
# ======================================================

df.columns = df.columns.str.strip()

df.columns = df.columns.str.replace(
    "\n",
    " ",
    regex=True
)

# ======================================================
# MODEL FINAL PENELITIAN
# X2.2 DIHAPUS
# ======================================================

X1 = [
    "X1.1",
    "X1.2",
    "X1.3",
    "X1.4",
    "X1.5"
]

X2 = [
    "X2.1",
    "X2.3",
    "X2.4",
    "X2.5"
]

Y = [
    "Y1",
    "Y2",
    "Y3",
    "Y4",
    "Y5"
]

# ======================================================
# VALIDASI DATASET
# ======================================================

required_cols = X1 + X2 + Y

missing_cols = [

    col

    for col in required_cols

    if col not in df.columns

]

if missing_cols:

    st.error(
        f"Kolom berikut tidak ditemukan: {missing_cols}"
    )

    st.stop()

# ======================================================
# SCORE
# ======================================================

df["Skor Algoritma"] = df[X1].mean(axis=1)

df["Skor Echo Chamber"] = df[X2].mean(axis=1)

df["Skor Risiko"] = df[Y].mean(axis=1)

# ======================================================
# KATEGORI RISIKO
# ======================================================

def kategori_risiko(x):

    if x < 2.61:
        return "Rendah"

    elif x < 3.41:
        return "Sedang"

    else:
        return "Tinggi"

df["Kategori Risiko"] = df[
    "Skor Risiko"
].apply(kategori_risiko)

# ======================================================
# SIDEBAR
# ======================================================

st.sidebar.title(
    "📊 Dashboard Penelitian"
)

st.sidebar.markdown("""
Analisis hubungan:

• Algoritma Rekomendasi Konten

• Echo Chamber

• Risiko Adiksi Digital Instagram
""")

st.sidebar.markdown("---")

# ======================================================
# FILTER
# ======================================================

gender = st.sidebar.multiselect(

    "Jenis Kelamin",

    options=df["Jenis Kelamin"].unique(),

    default=df["Jenis Kelamin"].unique()

)

usia = st.sidebar.multiselect(

    "Usia",

    options=df["Usia"].unique(),

    default=df["Usia"].unique()

)

durasi = st.sidebar.multiselect(

    "Durasi Penggunaan Instagram",

    options=df[
        "Rata-rata Durasi Penggunaan Instagram per Hari"
    ].unique(),

    default=df[
        "Rata-rata Durasi Penggunaan Instagram per Hari"
    ].unique()

)

# ======================================================
# FILTER DATAFRAME
# ======================================================

df = df[

    (df["Jenis Kelamin"].isin(gender))

    &

    (df["Usia"].isin(usia))

    &

    (
        df[
            "Rata-rata Durasi Penggunaan Instagram per Hari"
        ].isin(durasi)
    )

]

# ======================================================
# SIDEBAR SUMMARY
# ======================================================

st.sidebar.markdown("---")

st.sidebar.metric(
    "Responden Aktif",
    len(df)
)

# ======================================================
# HEADER
# ======================================================

st.title(
    "📱 Instagram Digital Addiction Risk Analytics Dashboard"
)

st.markdown("""
Analisis hubungan **Algoritma Rekomendasi Konten**, **Echo Chamber**, dan **Risiko Adiksi Digital Instagram** berdasarkan data responden Kabupaten Sumedang.
""")

# ======================================================
# KPI CARDS
# ======================================================

c1, c2, c3, c4 = st.columns(4)

with c1:

    st.markdown(f"""
    <div class="metric-card">

    <div class="metric-title">
    Total Responden
    </div>

    <div class="metric-value">
    {len(df)}
    </div>

    <div class="small-text">
    Data setelah filtering
    </div>

    </div>
    """, unsafe_allow_html=True)

with c2:

    st.markdown(f"""
    <div class="metric-card">

    <div class="metric-title">
    Skor Algoritma
    </div>

    <div class="metric-value">
    {df['Skor Algoritma'].mean():.2f}/5
    </div>

    <div class="small-text">
    Persepsi responden
    </div>

    </div>
    """, unsafe_allow_html=True)

with c3:

    st.markdown(f"""
    <div class="metric-card">

    <div class="metric-title">
    Skor Echo Chamber
    </div>

    <div class="metric-value">
    {df['Skor Echo Chamber'].mean():.2f}/5
    </div>

    <div class="small-text">
    Homogenitas informasi
    </div>

    </div>
    """, unsafe_allow_html=True)

with c4:

    st.markdown(f"""
    <div class="metric-card">

    <div class="metric-title">
    Skor Risiko
    </div>

    <div class="metric-value">
    {df['Skor Risiko'].mean():.2f}/5
    </div>

    <div class="small-text">
    Risiko adiksi digital
    </div>

    </div>
    """, unsafe_allow_html=True)

# ======================================================
# STATUS RISIKO
# ======================================================

mean_risk = df["Skor Risiko"].mean()

if mean_risk >= 3.41:

    st.error(
        f"Status Risiko Saat Ini: TINGGI ({mean_risk:.2f}/5)"
    )

elif mean_risk >= 2.61:

    st.warning(
        f"Status Risiko Saat Ini: SEDANG ({mean_risk:.2f}/5)"
    )

else:

    st.success(
        f"Status Risiko Saat Ini: RENDAH ({mean_risk:.2f}/5)"
    )

# ======================================================
# RINGKASAN TEMUAN
# ======================================================

st.markdown("### Ringkasan Temuan")

colA, colB, colC = st.columns(3)

with colA:

    st.success(
        "Echo Chamber menunjukkan hubungan yang lebih kuat terhadap Risiko Adiksi Digital."
    )

with colB:

    st.info(
        "Algoritma Rekomendasi Konten berperan sebagai mekanisme personalisasi informasi."
    )

with colC:

    st.warning(
        "Sebagian besar responden berada pada kategori risiko sedang hingga tinggi."
    )

# ======================================================
# INTERPRETASI SKOR
# ======================================================

st.caption(
"""
Interpretasi Skor:
1.00–1.80 (Sangat Rendah) |
1.81–2.60 (Rendah) |
2.61–3.40 (Sedang) |
3.41–4.20 (Tinggi) |
4.21–5.00 (Sangat Tinggi)
"""
)

# ======================================================
# TABS
# ======================================================

tabs = st.tabs([

    "Overview",

    "Profil Responden",

    "Analisis Risiko",

    "SmartPLS",

    "Mitigasi"

])

# ======================================================
# OVERVIEW TAB
# ======================================================

with tabs[0]:

    st.subheader(
        "Ringkasan Hasil Analisis"
    )

    col1, col2 = st.columns(2)

    with col1:

        fig1 = px.histogram(

            df,

            x="Skor Risiko",

            nbins=10,

            color="Kategori Risiko",

            title="Distribusi Risiko Adiksi Digital"

        )

        fig1.update_layout(
            height=420,
            xaxis_title="Skor Risiko",
            yaxis_title="Jumlah Responden"
        )

        st.plotly_chart(
            fig1,
            use_container_width=True
        )

    with col2:

        kategori_df = (

            df["Kategori Risiko"]

            .value_counts()

            .reset_index()

        )

        kategori_df.columns = [

            "Kategori Risiko",

            "Jumlah"

        ]

        fig2 = px.pie(

            kategori_df,

            names="Kategori Risiko",

            values="Jumlah",

            hole=0.55,

            title="Komposisi Tingkat Risiko"

        )

        fig2.update_layout(
            height=420
        )

        st.plotly_chart(
            fig2,
            use_container_width=True
        )

    st.markdown("---")

    st.markdown(
        "### Rata-rata Skor Variabel Penelitian"
    )

    mean_df = pd.DataFrame({

        "Variabel":[

            "Algoritma Rekomendasi",

            "Echo Chamber",

            "Risiko Adiksi Digital"

        ],

        "Skor":[

            df["Skor Algoritma"].mean(),

            df["Skor Echo Chamber"].mean(),

            df["Skor Risiko"].mean()

        ]

    })

    mean_chart = px.bar(

        mean_df,

        x="Variabel",

        y="Skor",

        color="Skor",

        text_auto=".2f"

    )

    mean_chart.update_layout(
        height=450,
        xaxis_title="",
        yaxis_title="Rata-rata Skor"
    )

    st.plotly_chart(
        mean_chart,
        use_container_width=True
    )

    st.caption(
        "Grafik menunjukkan rata-rata skor dari setiap variabel yang digunakan dalam penelitian."
    )

# ======================================================
# PROFIL RESPONDEN
# ======================================================

with tabs[1]:

    st.subheader(
        "Profil Responden"
    )

    kiri, kanan = st.columns(2)

    with kiri:

        usia_df = (

            df["Usia"]

            .value_counts()

            .reset_index()

        )

        usia_df.columns = [

            "Usia",

            "Jumlah"

        ]

        usia_chart = px.bar(

            usia_df,

            x="Usia",

            y="Jumlah",

            color="Jumlah",

            text_auto=True,

            title="Distribusi Usia Responden"

        )

        usia_chart.update_layout(
            height=420
        )

        st.plotly_chart(
            usia_chart,
            use_container_width=True
        )

    with kanan:

        gender_df = (

            df["Jenis Kelamin"]

            .value_counts()

            .reset_index()

        )

        gender_df.columns = [

            "Jenis Kelamin",

            "Jumlah"

        ]

        gender_chart = px.pie(

            gender_df,

            names="Jenis Kelamin",

            values="Jumlah",

            hole=0.55,

            title="Komposisi Jenis Kelamin"

        )

        gender_chart.update_layout(
            height=420
        )

        st.plotly_chart(
            gender_chart,
            use_container_width=True
        )

    st.markdown("---")

    durasi_df = (

        df[
            "Rata-rata Durasi Penggunaan Instagram per Hari"
        ]

        .value_counts()

        .reset_index()

    )

    durasi_df.columns = [

        "Durasi",

        "Jumlah"

    ]

    durasi_chart = px.bar(

        durasi_df,

        x="Durasi",

        y="Jumlah",

        color="Jumlah",

        text_auto=True,

        title="Durasi Penggunaan Instagram per Hari"

    )

    durasi_chart.update_layout(
        height=450
    )

    st.plotly_chart(
        durasi_chart,
        use_container_width=True
    )

# ======================================================
# ANALISIS RISIKO
# ======================================================

with tabs[2]:

    st.subheader(
        "Analisis Hubungan Variabel"
    )

    st.caption(
        "Visualisasi berikut membantu melihat hubungan antara Algoritma Rekomendasi, Echo Chamber, dan Risiko Adiksi Digital."
    )

    col1, col2 = st.columns(2)

    with col1:

        corr = df[

            [

                "Skor Algoritma",

                "Skor Echo Chamber",

                "Skor Risiko"

            ]

        ].corr()

        heat = px.imshow(

            corr,

            text_auto=".2f",

            color_continuous_scale="RdBu",

            title="Korelasi Antar Variabel"

        )

        heat.update_layout(
            height=450
        )

        st.plotly_chart(
            heat,
            use_container_width=True
        )

    with col2:

        scatter = px.scatter(

            df,

            x="Skor Echo Chamber",

            y="Skor Risiko",

            color="Kategori Risiko",

            size="Skor Algoritma",

            title="Hubungan Echo Chamber dan Risiko Adiksi Digital"

        )

        scatter.update_layout(
            height=450
        )

        st.plotly_chart(
            scatter,
            use_container_width=True
        )

    st.markdown("---")

    st.markdown(
        "### Perbandingan Hubungan Variabel"
    )

    kiri, kanan = st.columns(2)

    with kiri:

        fig_algoritma = px.scatter(

            df,

            x="Skor Algoritma",

            y="Skor Risiko",

            color="Kategori Risiko",

            title="Algoritma Rekomendasi dan Risiko Adiksi Digital"

        )

        fig_algoritma.update_layout(
            height=420
        )

        st.plotly_chart(
            fig_algoritma,
            use_container_width=True
        )

    with kanan:

        fig_echo = px.scatter(

            df,

            x="Skor Echo Chamber",

            y="Skor Risiko",

            color="Kategori Risiko",

            title="Echo Chamber dan Risiko Adiksi Digital"

        )

        fig_echo.update_layout(
            height=420
        )

        st.plotly_chart(
            fig_echo,
            use_container_width=True
        )

    st.markdown("---")

    st.success("""
Temuan Utama:

• Responden dengan skor Echo Chamber yang lebih tinggi cenderung memiliki skor Risiko Adiksi Digital yang lebih tinggi.

• Hubungan Echo Chamber dengan Risiko Adiksi Digital terlihat lebih kuat dibandingkan hubungan Algoritma Rekomendasi.

• Hasil pengujian statistik lengkap dapat dilihat pada tab SmartPLS.
""")

    aktivitas_col = None

    for col in df.columns:

        if "Aktivitas Instagram" in col:

            aktivitas_col = col

            break

    if aktivitas_col:

        st.markdown("---")

        st.markdown(
            "### Risiko Berdasarkan Aktivitas Instagram"
        )

        aktivitas = (

            df.groupby(
                aktivitas_col
            )["Skor Risiko"]

            .mean()

            .reset_index()

        )

        aktivitas_chart = px.bar(

            aktivitas,

            x=aktivitas_col,

            y="Skor Risiko",

            color="Skor Risiko",

            text_auto=".2f"

        )

        aktivitas_chart.update_layout(
            height=500,
            xaxis_title="Aktivitas",
            yaxis_title="Rata-rata Skor Risiko"
        )

        st.plotly_chart(
            aktivitas_chart,
            use_container_width=True
        )

        st.caption(
            "Grafik menunjukkan aktivitas Instagram yang memiliki rata-rata skor risiko lebih tinggi dibanding aktivitas lainnya."
        )

# ======================================================
# SMARTPLS TAB
# ======================================================

with tabs[3]:

    st.subheader(
        "Hasil Pengujian Model Penelitian"
    )

    st.markdown("""
Dashboard ini menggunakan hasil pengujian SmartPLS untuk mengevaluasi hubungan antara:

• Algoritma Rekomendasi Konten

• Echo Chamber

• Risiko Adiksi Digital Instagram
""")

    st.markdown("---")

# ======================================================
# OUTER LOADING
# ======================================================

    st.markdown(
        "### Validitas Indikator (Outer Loading)"
    )

    outer_loading = pd.DataFrame({

        "Indikator":[

            "X1.1",
            "X1.2",
            "X1.3",
            "X1.4",
            "X1.5",

            "X2.1",
            "X2.3",
            "X2.4",
            "X2.5",

            "Y1",
            "Y2",
            "Y3",
            "Y4",
            "Y5"

        ],

        "Loading":[

            0.860,
            0.757,
            0.750,
            0.868,
            0.798,

            0.816,
            0.757,
            0.712,
            0.802,

            0.820,
            0.891,
            0.783,
            0.718,
            0.874

        ]

    })

    fig_outer = px.bar(

        outer_loading,

        x="Indikator",

        y="Loading",

        color="Loading",

        text_auto=".3f",

        title="Nilai Outer Loading"

    )

    fig_outer.update_layout(
        height=500
    )

    st.plotly_chart(
        fig_outer,
        use_container_width=True
    )

    st.success(
        "Seluruh indikator memenuhi kriteria validitas konvergen (Outer Loading > 0.70)."
    )

# ======================================================
# RELIABILITY
# ======================================================

    st.markdown("---")

    st.markdown(
        "### Reliability dan Validity"
    )

    construct = pd.DataFrame({

        "Construct":[

            "Algoritma Rekomendasi Konten",

            "Echo Chamber",

            "Risiko Adiksi Digital"

        ],

        "Cronbach Alpha":[

            0.877,
            0.777,
            0.879

        ],

        "Composite Reliability":[

            0.904,
            0.855,
            0.911

        ],

        "AVE":[

            0.653,
            0.597,
            0.672

        ]

    })

    st.dataframe(
        construct,
        use_container_width=True
    )

    st.info("""
Interpretasi:

• Seluruh konstruk reliabel.

• Composite Reliability > 0.70.

• AVE > 0.50.

• Model layak digunakan untuk pengujian hipotesis.
""")

# ======================================================
# HYPOTHESIS
# ======================================================

    st.markdown("---")

    st.markdown(
        "### Hasil Pengujian Hipotesis"
    )

    hypothesis = pd.DataFrame({

        "Hubungan":[

            "Algoritma Rekomendasi → Risiko Adiksi",

            "Echo Chamber → Risiko Adiksi"

        ],

        "T Statistics":[

            0.524,
            4.114

        ],

        "P Value":[

            0.600,
            0.000

        ],

        "Status":[

            "Tidak Signifikan",

            "Signifikan"

        ]

    })

    st.dataframe(
        hypothesis,
        use_container_width=True
    )

    st.markdown("---")

    col1,col2=st.columns(2)

    with col1:

        st.error("""
Hubungan Tidak Signifikan

Algoritma Rekomendasi Konten → Risiko Adiksi Digital

P Value = 0.600
""")

    with col2:

        st.success("""
Hubungan Signifikan

Echo Chamber → Risiko Adiksi Digital

P Value = 0.000
""")

# ======================================================
# KEY INSIGHT
# ======================================================

    st.markdown("---")

    st.markdown(
        "### Insight Penelitian"
    )

    st.success("""
Temuan utama penelitian menunjukkan bahwa Echo Chamber memiliki pengaruh signifikan terhadap Risiko Adiksi Digital Instagram.

Sebaliknya, Algoritma Rekomendasi Konten tidak menunjukkan pengaruh langsung yang signifikan.

Hasil ini mengindikasikan bahwa risiko adiksi lebih dipengaruhi oleh homogenitas informasi dan keterpaparan pada sudut pandang yang berulang dibandingkan mekanisme rekomendasi konten itu sendiri.
""")
