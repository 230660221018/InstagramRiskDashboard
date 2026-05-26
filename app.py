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
border-radius:20px;
box-shadow:0px 6px 18px rgba(0,0,0,0.08);
border-left:8px solid #2563eb;
}

.metric-title{
font-size:14px;
color:#6b7280;
}

.metric-value{
font-size:32px;
font-weight:700;
color:#111827;
}

.small-text{
font-size:13px;
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
        f"Kolom berikut tidak ditemukan pada dataset: {missing_cols}"
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
Dashboard analitik penelitian:

**Pengaruh Algoritma Rekomendasi Konten dan Echo Chamber terhadap Risiko Adiksi Digital Instagram**
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
# HEADER
# ======================================================

st.title(
    "📱 Instagram Digital Addiction Risk Analytics Dashboard"
)

st.markdown("""
Visualisasi analitik hasil penelitian berbasis data responden Instagram di Kabupaten Sumedang menggunakan pendekatan **SmartPLS**.
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
    Data aktif setelah filtering
    </div>

    </div>
    """, unsafe_allow_html=True)

with c2:

    st.markdown(f"""
    <div class="metric-card">

    <div class="metric-title">
    Pengaruh Algoritma
    </div>

    <div class="metric-value">
    {round(df['Skor Algoritma'].mean(),2)}/5
    </div>

    <div class="small-text">
    Rata-rata persepsi responden
    </div>

    </div>
    """, unsafe_allow_html=True)

with c3:

    st.markdown(f"""
    <div class="metric-card">

    <div class="metric-title">
    Tingkat Echo Chamber
    </div>

    <div class="metric-value">
    {round(df['Skor Echo Chamber'].mean(),2)}/5
    </div>

    <div class="small-text">
    Intensitas homogenitas informasi
    </div>

    </div>
    """, unsafe_allow_html=True)

with c4:

    st.markdown(f"""
    <div class="metric-card">

    <div class="metric-title">
    Risiko Adiksi Digital
    </div>

    <div class="metric-value">
    {round(df['Skor Risiko'].mean(),2)}/5
    </div>

    <div class="small-text">
    Tingkat kecenderungan adiksi
    </div>

    </div>
    """, unsafe_allow_html=True)

# ======================================================
# INTERPRETASI SKOR
# ======================================================

st.info("""
Interpretasi skor Likert:

• 1.00 – 1.80 = Sangat Rendah

• 1.81 – 2.60 = Rendah

• 2.61 – 3.40 = Sedang

• 3.41 – 4.20 = Tinggi

• 4.21 – 5.00 = Sangat Tinggi
""")

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
        "Ringkasan Risiko Digital Instagram"
    )

    col1, col2 = st.columns(2)

    with col1:

        fig1 = px.histogram(

            df,

            x="Skor Risiko",

            nbins=10,

            color_discrete_sequence=["#ef4444"]

        )

        fig1.update_layout(
            height=420,
            title="Distribusi Skor Risiko Adiksi Digital"
        )

        st.plotly_chart(
            fig1,
            use_container_width=True
        )

    with col2:

        fig2 = px.pie(

            df,

            names="Jenis Kelamin",

            hole=0.5

        )

        fig2.update_layout(
            height=420,
            title="Komposisi Jenis Kelamin Responden"
        )

        st.plotly_chart(
            fig2,
            use_container_width=True
        )

    st.markdown("---")

    st.markdown(
        "### Distribusi Kategori Risiko"
    )

    risk_dist = (

        df["Kategori Risiko"]

        .value_counts()

        .reset_index()

    )

    risk_dist.columns = [
        "Kategori Risiko",
        "Jumlah"
    ]

    risk_chart = px.bar(

        risk_dist,

        x="Kategori Risiko",

        y="Jumlah",

        color="Kategori Risiko",

        text_auto=True

    )

    risk_chart.update_layout(
        height=420
    )

    st.plotly_chart(
        risk_chart,
        use_container_width=True
    )

    total_high = len(
        df[
            df["Kategori Risiko"] == "Tinggi"
        ]
    )

    persentase_high = round(
        (total_high / len(df)) * 100,
        1
    )

    st.success(
        f"{persentase_high}% responden berada pada kategori Risiko Tinggi."
    )

# ======================================================
# PROFIL RESPONDEN
# ======================================================

with tabs[1]:

    st.subheader(
        "Profil Responden Penelitian"
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

            color="Jumlah"

        )

        usia_chart.update_layout(
            height=420
        )

        st.plotly_chart(
            usia_chart,
            use_container_width=True
        )

    with kanan:

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

            color="Jumlah"

        )

        durasi_chart.update_layout(
            height=420
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

    st.info("""
Bagian ini menampilkan pola hubungan antar variabel penelitian.
Visualisasi digunakan untuk membantu interpretasi hubungan Algoritma Rekomendasi Konten, Echo Chamber, dan Risiko Adiksi Digital sebelum dikonfirmasi melalui pengujian SmartPLS.
""")

    left, right = st.columns(2)

    with left:

        corr = df[

            [

                "Skor Algoritma",

                "Skor Echo Chamber",

                "Skor Risiko"

            ]

        ].corr()

        heat = px.imshow(

            corr,

            text_auto=True,

            color_continuous_scale="RdBu",

            title="Matriks Korelasi Antar Variabel"

        )

        heat.update_layout(
            height=420
        )

        st.plotly_chart(
            heat,
            use_container_width=True
        )

    with right:

        scatter = px.scatter(

            df,

            x="Skor Echo Chamber",

            y="Skor Risiko",

            color="Usia",

            size="Skor Algoritma",

            trendline="ols",

            title="Hubungan Echo Chamber dan Risiko Adiksi Digital"

        )

        scatter.update_layout(
            height=420
        )

        st.plotly_chart(
            scatter,
            use_container_width=True
        )

    st.markdown("---")

    st.markdown(
        "### Perbandingan Pengaruh Variabel terhadap Risiko Adiksi Digital"
    )

    compare_col1, compare_col2 = st.columns(2)

    with compare_col1:

        alg_chart = px.scatter(

            df,

            x="Skor Algoritma",

            y="Skor Risiko",

            trendline="ols",

            title="Algoritma Rekomendasi → Risiko Adiksi Digital"

        )

        alg_chart.update_layout(
            height=420
        )

        st.plotly_chart(
            alg_chart,
            use_container_width=True
        )

    with compare_col2:

        echo_chart = px.scatter(

            df,

            x="Skor Echo Chamber",

            y="Skor Risiko",

            trendline="ols",

            title="Echo Chamber → Risiko Adiksi Digital"

        )

        echo_chart.update_layout(
            height=420
        )

        st.plotly_chart(
            echo_chart,
            use_container_width=True
        )

    st.warning("""
Visualisasi menunjukkan bahwa hubungan antara Echo Chamber dan Risiko Adiksi Digital cenderung lebih kuat dibandingkan hubungan antara Algoritma Rekomendasi Konten dan Risiko Adiksi Digital.

Namun demikian, kesimpulan akhir mengenai signifikansi pengaruh ditentukan berdasarkan hasil pengujian SmartPLS pada tab berikutnya.
""")

    st.markdown("---")

    aktivitas_col = None

    for col in df.columns:

        if "Aktivitas Instagram" in col:

            aktivitas_col = col

            break

    if aktivitas_col:

        st.markdown(
            "### Risiko Adiksi Berdasarkan Aktivitas Instagram Dominan"
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

            text_auto=True

        )

        aktivitas_chart.update_layout(
            height=500
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
        "Hasil Pengujian SmartPLS"
    )

    st.info("""
Temuan utama penelitian:

• Algoritma Rekomendasi Konten tidak berpengaruh signifikan terhadap Risiko Adiksi Digital (p > 0.05).

• Echo Chamber berpengaruh signifikan terhadap Risiko Adiksi Digital (p < 0.05).

• Echo Chamber merupakan faktor dominan yang memengaruhi Risiko Adiksi Digital pada responden.
""")

    st.markdown("---")

    st.markdown(
        "### Outer Loading"
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

    st.dataframe(
        outer_loading,
        use_container_width=True
    )

    st.success(
        "Seluruh indikator memenuhi syarat validitas konvergen (loading > 0.70)."
    )

    st.markdown("---")

    st.markdown(
        "### Construct Reliability & Validity"
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

    st.success(
        "Model memenuhi validitas konvergen, reliabilitas konstruk, dan nilai AVE yang baik."
    )

    st.markdown("---")

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
        "### Visualisasi Besaran Pengaruh Antar Variabel"
    )

    path_df = pd.DataFrame({

        "Variabel":[

            "Algoritma Rekomendasi",

            "Echo Chamber"

        ],

        "Koefisien Jalur":[

            0.052,

            0.491

        ]

    })

    path_chart = px.bar(

        path_df,

        x="Variabel",

        y="Koefisien Jalur",

        color="Koefisien Jalur",

        text_auto=True

    )

    path_chart.update_layout(
        height=450
    )

    st.plotly_chart(
        path_chart,
        use_container_width=True
    )

    st.info("""
Interpretasi:

Koefisien jalur menunjukkan bahwa Echo Chamber memiliki pengaruh yang jauh lebih besar terhadap Risiko Adiksi Digital dibandingkan Algoritma Rekomendasi Konten.

Temuan ini menunjukkan bahwa homogenitas informasi yang diterima pengguna menjadi faktor yang lebih dominan dibandingkan mekanisme rekomendasi konten itu sendiri.
""")

    st.markdown("---")

    st.markdown(
        "### Analisis Sosioteknis (Lensa Teori Kritis)"
    )

    st.warning("""
Dari perspektif Teori Kritis, teknologi tidak dipandang sebagai alat yang netral.

Hasil penelitian menunjukkan bahwa paparan Echo Chamber dapat memperkuat keterikatan pengguna terhadap lingkungan informasi yang homogen.

Kondisi ini berpotensi:

• Mengurangi keberagaman perspektif informasi.

• Memperkuat bias konfirmasi pengguna.

• Meningkatkan ketergantungan terhadap platform digital.

• Mendorong perilaku penggunaan berulang secara tidak sadar.

Oleh karena itu, mitigasi tidak hanya perlu dilakukan pada aspek teknis, tetapi juga pada aspek sosial dan literasi digital pengguna.
""")

# ======================================================
# MITIGASI TAB
# ======================================================

with tabs[4]:

    st.subheader(
        "Rekomendasi Mitigasi Risiko"
    )

    st.info("""
Strategi mitigasi dirumuskan berdasarkan hasil pengujian SmartPLS yang menunjukkan bahwa Echo Chamber merupakan faktor dominan yang memengaruhi Risiko Adiksi Digital.
""")

    mitigation_df = pd.DataFrame({

        "Area Risiko":[

            "Echo Chamber",

            "Adiksi Digital",

            "Bias Informasi",

            "Ketergantungan Platform"

        ],

        "Strategi Teknis":[

            "Diversifikasi rekomendasi konten",

            "Screen time reminder",

            "Penyajian sumber informasi alternatif",

            "Monitoring aktivitas digital"

        ],

        "Strategi Manajerial":[

            "Literasi digital",

            "Edukasi penggunaan sehat",

            "Peningkatan kesadaran kritis",

            "Kebijakan penggunaan media sosial"

        ]

    })

    st.dataframe(
        mitigation_df,
        use_container_width=True
    )

    st.markdown("---")

    risk = df["Skor Risiko"].mean()

    if risk >= 4:

        st.error("""

### RISIKO TINGGI

• Batasi screen time Instagram.

• Aktifkan pengingat waktu penggunaan aplikasi.

• Diversifikasi sumber informasi.

• Kurangi paparan konten homogen.

• Tingkatkan literasi digital.

• Evaluasi pola penggunaan media sosial secara berkala.

""")

    elif risk >= 3:

        st.warning("""

### RISIKO SEDANG

• Monitoring durasi penggunaan Instagram.

• Kurangi konsumsi konten repetitif.

• Tingkatkan kesadaran penggunaan digital.

• Diversifikasi akun dan sumber informasi.

• Batasi aktivitas scrolling tanpa tujuan.

""")

    else:

        st.success("""

### RISIKO RENDAH

Penggunaan Instagram relatif terkendali.

Tetap pertahankan pola penggunaan yang sehat dan seimbang.

""")

    st.markdown("---")

    st.markdown(
        "### Refleksi Keberlanjutan dan Evolusi AI"
    )

    st.info("""
Dashboard dirancang sebagai artefak Digital Risk Analytics yang dapat dikembangkan lebih lanjut dengan teknologi Artificial Intelligence dan Machine Learning.

Ke depan, sistem dapat digunakan untuk:

• Prediksi risiko adiksi digital secara otomatis.

• Deteksi pola Echo Chamber berbasis AI.

• Personalisasi rekomendasi mitigasi.

• Monitoring perilaku digital secara berkelanjutan.

Dengan pendekatan Responsible Innovation, pengembangan sistem harus tetap memperhatikan aspek privasi, transparansi, dan dampak sosial teknologi.
""")

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

st.caption(
    "Instagram Digital Addiction Risk Analytics Dashboard | Design Science Research (DSR)"
)
