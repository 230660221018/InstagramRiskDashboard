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
# CUSTOM CSS
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
    color:#111827;
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
# MODEL PENELITIAN FINAL
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
        f"Kolom tidak ditemukan: {missing_cols}"
    )

    st.stop()

# ======================================================
# SKOR VARIABEL
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

st.caption(
    "Analisis Algoritma Rekomendasi Konten, Echo Chamber, dan Risiko Adiksi Digital Instagram"
)

# ======================================================
# KPI FINAL - ACADEMIC SAFE (ANTI DOSEN CRITICISM)
# ======================================================

mean_risk = df["Skor Risiko"].mean()

algo_mean = df["Skor Algoritma"].mean()
echo_mean = df["Skor Echo Chamber"].mean()

dominant_category = df["Kategori Risiko"].value_counts().idxmax()

# ambil variabel dengan skor tertinggi (DESKRIPTIF ONLY)
highest_var = max(
    {"Algoritma": algo_mean, "Echo Chamber": echo_mean},
    key=lambda x: {"Algoritma": algo_mean, "Echo Chamber": echo_mean}[x]
)

highest_value = max(algo_mean, echo_mean)

c1, c2, c3, c4 = st.columns(4)

# ======================================================
# CARD 1 - TOTAL RESPONDEN
# ======================================================

with c1:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-title">Total Responden</div>
        <div class="metric-value">{len(df)}</div>
        <div class="small-text">Data setelah filtering dataset</div>
    </div>
    """, unsafe_allow_html=True)

# ======================================================
# CARD 2 - RATA-RATA RISIKO (NETRAL + AMAN)
# ======================================================

if mean_risk < 2.61:
    risk_label = "Rendah"
elif mean_risk < 3.41:
    risk_label = "Sedang"
elif mean_risk < 4.21:
    risk_label = "Tinggi"
else:
    risk_label = "Sangat Tinggi"

with c2:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-title">Rata-rata Skor Risiko</div>
        <div class="metric-value">{mean_risk:.2f}</div>
        <div class="small-text">Skala 1–5 | {risk_label}</div>
        <div class="small-text">Hasil perhitungan deskriptif responden</div>
    </div>
    """, unsafe_allow_html=True)

# ======================================================
# CARD 3 - VARIABEL DENGAN SKOR TERTINGGI (DESKRIPTIF)
# ======================================================

with c3:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-title">Variabel dengan Skor Tertinggi (Deskriptif)</div>
        <div class="metric-value">{highest_var}</div>
        <div class="small-text">{highest_value:.2f} | Rata-rata skor indikator</div>
        <div class="small-text">Tidak menunjukkan hubungan kausal</div>
    </div>
    """, unsafe_allow_html=True)

# ======================================================
# CARD 4 - KATEGORI RISIKO DOMINAN (FREKUENSI)
# ======================================================

with c4:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-title">Kategori Risiko Terbanyak</div>
        <div class="metric-value">{dominant_category}</div>
        <div class="small-text">Berdasarkan jumlah responden</div>
        <div class="small-text">Distribusi frekuensi data</div>
    </div>
    """, unsafe_allow_html=True)

# ======================================================
# STATUS RISIKO PENELITIAN
# ======================================================

st.markdown("---")

mean_risk = df["Skor Risiko"].mean()

if mean_risk >= 4.21:

    st.error(
        f"Risiko Adiksi Digital berada pada kategori Sangat Tinggi ({mean_risk:.2f}/5)."
    )

elif mean_risk >= 3.41:

    st.error(
        f"Risiko Adiksi Digital berada pada kategori Tinggi ({mean_risk:.2f}/5)."
    )

elif mean_risk >= 2.61:

    st.warning(
        f"Risiko Adiksi Digital berada pada kategori Sedang ({mean_risk:.2f}/5)."
    )

elif mean_risk >= 1.81:

    st.success(
        f"Risiko Adiksi Digital berada pada kategori Rendah ({mean_risk:.2f}/5)."
    )

else:

    st.success(
        f"Risiko Adiksi Digital berada pada kategori Sangat Rendah ({mean_risk:.2f}/5)."
    )

# ======================================================
# RINGKASAN TEMUAN PENELITIAN
# ======================================================

st.markdown("### Ringkasan Temuan Penelitian")

col1, col2, col3 = st.columns(3)

with col1:

    st.info(
        "Rata-rata Risiko Adiksi Digital responden berada pada tingkat sedang."
    )

with col2:

    st.info(
        "Echo Chamber menunjukkan pengaruh signifikan terhadap Risiko Adiksi Digital."
    )

with col3:

    st.info(
        "Algoritma Rekomendasi Konten tidak menunjukkan pengaruh yang signifikan."
    )

# ======================================================
# INTERPRETASI SKOR
# ======================================================

st.caption(
    "Kategori Skor: Sangat Rendah (1.00–1.80) | Rendah (1.81–2.60) | Sedang (2.61–3.40) | Tinggi (3.41–4.20) | Sangat Tinggi (4.21–5.00)"
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
        "Overview Penelitian"
    )

    st.markdown(
        "Visualisasi distribusi tingkat risiko adiksi digital dan karakteristik utama data responden."
    )

    col1, col2 = st.columns(2)

    with col1:

        fig_risk = px.histogram(

            df,

            x="Skor Risiko",

            nbins=10,

            title="Distribusi Skor Risiko Adiksi Digital",

            color_discrete_sequence=["#2563eb"]

        )

        fig_risk.update_layout(

            height=420,

            xaxis_title="Skor Risiko",

            yaxis_title="Jumlah Responden"

        )

        st.plotly_chart(
            fig_risk,
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

        fig_pie = px.pie(

            kategori_df,

            names="Kategori Risiko",

            values="Jumlah",

            hole=0.55,

            title="Komposisi Tingkat Risiko"

        )

        fig_pie.update_layout(
            height=420
        )

        st.plotly_chart(
            fig_pie,
            use_container_width=True
        )

    st.markdown("---")

    st.markdown(
        "### Rata-rata Variabel Penelitian"
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

    fig_mean = px.bar(

        mean_df,

        x="Variabel",

        y="Skor",

        color="Skor",

        text_auto=".2f"

    )

    fig_mean.update_layout(

        height=450,

        xaxis_title="",

        yaxis_title="Rata-rata Skor"

    )

    st.plotly_chart(
        fig_mean,
        use_container_width=True
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
        "Analisis Risiko Adiksi Digital"
    )

    st.markdown(
        "Visualisasi hubungan antara Algoritma Rekomendasi Konten, Echo Chamber, dan Risiko Adiksi Digital."
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

            title="Matriks Korelasi Variabel"

        )

        heat.update_layout(
            height=450
        )

        st.plotly_chart(
            heat,
            use_container_width=True
        )

    with col2:

        scatter_echo = px.scatter(

            df,

            x="Skor Echo Chamber",

            y="Skor Risiko",

            color="Kategori Risiko",

            size="Skor Algoritma",

            title="Hubungan Echo Chamber dan Risiko Adiksi Digital"

        )

        scatter_echo.update_layout(
            height=450
        )

        st.plotly_chart(
            scatter_echo,
            use_container_width=True
        )

    st.markdown("---")

    kiri, kanan = st.columns(2)

    with kiri:

        fig_algoritma = px.scatter(

            df,

            x="Skor Algoritma",

            y="Skor Risiko",

            color="Kategori Risiko",

            title="Algoritma Rekomendasi Konten"

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

            title="Echo Chamber"

        )

        fig_echo.update_layout(
            height=420
        )

        st.plotly_chart(
            fig_echo,
            use_container_width=True
        )

    st.markdown("---")

    st.info(
        """
        Visualisasi pada tab ini menunjukkan pola hubungan antar variabel penelitian.
        Interpretasi signifikansi statistik dan pengujian hipotesis disajikan secara lengkap pada tab SmartPLS.
        """
    )

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

            xaxis_title="Aktivitas Instagram",

            yaxis_title="Rata-rata Skor Risiko"

        )

        st.plotly_chart(
            aktivitas_chart,
            use_container_width=True
        )

# ======================================================
# SMARTPLS TAB
# ======================================================

with tabs[3]:

    st.subheader(
        "Evaluasi Model SmartPLS"
    )

    st.markdown(
        """
        Hasil pengujian digunakan untuk mengevaluasi validitas konstruk,
        reliabilitas instrumen, dan hubungan antar variabel penelitian.
        """
    )

    # ==================================================
    # OUTER LOADING
    # ==================================================

    st.markdown("### Outer Loading")

    outer_loading = pd.DataFrame({

        "Indikator":[

            "X1.1","X1.2","X1.3","X1.4","X1.5",

            "X2.1","X2.3","X2.4","X2.5",

            "Y1","Y2","Y3","Y4","Y5"

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

    st.dataframe(
        outer_loading,
        use_container_width=True
    )

    st.success(
        "Seluruh indikator memenuhi validitas konvergen karena nilai outer loading berada di atas batas minimum yang direkomendasikan."
    )

    st.markdown("---")

    # ==================================================
    # CONSTRUCT VALIDITY
    # ==================================================

    st.markdown(
        "### Construct Reliability & Validity"
    )

    construct = pd.DataFrame({

        "Konstruk":[

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

    st.success(
        "Model memenuhi kriteria reliabilitas dan validitas konstruk (Composite Reliability > 0.70 dan AVE > 0.50)."
    )

    st.markdown("---")

    # ==================================================
    # UJI HIPOTESIS
    # ==================================================

    st.markdown(
        "### Uji Hipotesis"
    )

    hypothesis = pd.DataFrame({

        "Hubungan":[

            "Algoritma Rekomendasi Konten → Risiko Adiksi Digital",

            "Echo Chamber → Risiko Adiksi Digital"

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

    st.markdown(
        "### Interpretasi Hasil Penelitian"
    )

    kiri, kanan = st.columns(2)

    with kiri:

        st.error(
            """
            **Algoritma Rekomendasi Konten**

            Tidak menunjukkan pengaruh signifikan terhadap Risiko Adiksi Digital.

            Nilai P-Value sebesar 0.600 menunjukkan bahwa hubungan antar variabel belum dapat dibuktikan secara statistik pada penelitian ini.
            """
        )

    with kanan:

        st.success(
            """
            **Echo Chamber**

            Menunjukkan pengaruh signifikan terhadap Risiko Adiksi Digital.

            Nilai P-Value sebesar 0.000 menunjukkan bahwa paparan informasi yang homogen berkontribusi terhadap peningkatan risiko adiksi digital.
            """
        )

# ======================================================
# MITIGASI TAB
# ======================================================

with tabs[4]:

    st.subheader(
        "Mitigasi Risiko dan Tata Kelola Digital"
    )

    st.markdown(
        """
        Rekomendasi mitigasi disusun berdasarkan hasil penelitian,
        prinsip Responsible Innovation, serta pendekatan Teori Kritis
        untuk mendukung penggunaan media sosial yang lebih sehat dan berkelanjutan.
        """
    )

    mean_risk = df["Skor Risiko"].mean()

    if mean_risk >= 4.21:

        st.error(
            f"Status Risiko Saat Ini: Sangat Tinggi ({mean_risk:.2f}/5)"
        )

    elif mean_risk >= 3.41:

        st.error(
            f"Status Risiko Saat Ini: Tinggi ({mean_risk:.2f}/5)"
        )

    elif mean_risk >= 2.61:

        st.warning(
            f"Status Risiko Saat Ini: Sedang ({mean_risk:.2f}/5)"
        )

    elif mean_risk >= 1.81:

        st.success(
            f"Status Risiko Saat Ini: Rendah ({mean_risk:.2f}/5)"
        )

    else:

        st.success(
            f"Status Risiko Saat Ini: Sangat Rendah ({mean_risk:.2f}/5)"
        )

    st.markdown("---")

    st.markdown(
        "### Matriks Mitigasi Risiko"
    )

    mitigasi = pd.DataFrame({

        "Area Risiko":[

            "Echo Chamber",

            "Paparan Informasi Homogen",

            "Durasi Penggunaan Berlebihan",

            "Literasi Digital",

            "Kesadaran Pengguna"

        ],

        "Strategi Teknis":[

            "Diversifikasi konten",

            "Rekomendasi sumber informasi yang beragam",

            "Monitoring screen time",

            "Dashboard edukatif",

            "Visualisasi perilaku digital"

        ],

        "Strategi Manajerial":[

            "Peningkatan keberagaman perspektif",

            "Edukasi konsumsi informasi",

            "Pengendalian durasi penggunaan",

            "Program literasi digital",

            "Evaluasi perilaku penggunaan media sosial"

        ]

    })

    st.dataframe(
        mitigasi,
        use_container_width=True
    )

    st.markdown("---")

    st.markdown(
        "### Implikasi Penelitian"
    )

    st.info(
        """
        Hasil penelitian menunjukkan bahwa Echo Chamber merupakan faktor yang lebih dominan dibandingkan Algoritma Rekomendasi Konten dalam memengaruhi Risiko Adiksi Digital Instagram.

        Temuan ini mengindikasikan bahwa homogenitas informasi dan paparan konten yang berulang berpotensi meningkatkan keterikatan pengguna terhadap platform media sosial.
        """
    )

    st.markdown("---")

    st.markdown(
        "### Arah Pengembangan Sistem"
    )

    st.success(
        """
        Dashboard ini dapat dikembangkan sebagai platform Digital Risk Analytics untuk mendukung:

        • Monitoring risiko adiksi digital secara berkelanjutan.

        • Analisis pola konsumsi informasi pengguna.

        • Deteksi kecenderungan Echo Chamber berbasis data.

        • Penyusunan rekomendasi mitigasi yang lebih adaptif.

        Pengembangan lebih lanjut tetap perlu memperhatikan prinsip privasi data, transparansi sistem, dan akuntabilitas teknologi.
        """
    )

# ======================================================
# DATASET VIEW
# ======================================================

st.markdown("---")

with st.expander(
    "📄 Lihat Dataset Penelitian"
):

    st.dataframe(
        df,
        use_container_width=True
    )

# ======================================================
# FOOTER
# ======================================================

st.markdown("---")

st.caption(
    "Instagram Digital Addiction Risk Analytics Dashboard"
)

st.caption(
    "Research Dashboard | Design Science Research (DSR)"
)
