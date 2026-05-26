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
""",unsafe_allow_html=True)

# ======================================================
# LOAD DATASET
# ======================================================

try:

    try:
        df=pd.read_csv(
            "dataset.csv",
            encoding='utf-8'
        )

    except:
        df=pd.read_csv(
            "dataset.csv",
            encoding='latin1'
        )

except:

    st.error(
        "dataset.csv tidak ditemukan pada repository."
    )

    st.stop()

# ======================================================
# CLEANING COLUMN
# ======================================================

df.columns=df.columns.str.strip()

df.columns=df.columns.str.replace(
'\n',
' ',
regex=True
)

# ======================================================
# MODEL FINAL PENELITIAN
# X2.2 DIHAPUS
# ======================================================

X1=[
'X1.1',
'X1.2',
'X1.3',
'X1.4',
'X1.5'
]

X2=[
'X2.1',
'X2.3',
'X2.4',
'X2.5'
]

Y=[
'Y1',
'Y2',
'Y3',
'Y4',
'Y5'
]

# ======================================================
# SCORE
# ======================================================

df['Skor Algoritma']=df[X1].mean(axis=1)

df['Skor Echo Chamber']=df[X2].mean(axis=1)

df['Skor Risiko']=df[Y].mean(axis=1)

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

gender=st.sidebar.multiselect(

"Jenis Kelamin",

options=df['Jenis Kelamin'].unique(),

default=df['Jenis Kelamin'].unique()

)

usia=st.sidebar.multiselect(

"Usia",

options=df['Usia'].unique(),

default=df['Usia'].unique()

)

durasi=st.sidebar.multiselect(

"Durasi Penggunaan Instagram",

options=df[
'Rata-rata Durasi Penggunaan Instagram per Hari'
].unique(),

default=df[
'Rata-rata Durasi Penggunaan Instagram per Hari'
].unique()

)

# ======================================================
# FILTER DATAFRAME
# ======================================================

df=df[

(df['Jenis Kelamin'].isin(gender))

&

(df['Usia'].isin(usia))

&

(
df[
'Rata-rata Durasi Penggunaan Instagram per Hari'
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
Visualisasi analitik hasil penelitian berbasis data responden Instagram menggunakan pendekatan **SmartPLS**.
""")

# ======================================================
# KPI CARDS
# ======================================================

c1,c2,c3,c4=st.columns(4)

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
    """,unsafe_allow_html=True)

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
    """,unsafe_allow_html=True)

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
    """,unsafe_allow_html=True)

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
    """,unsafe_allow_html=True)

st.info("""
Interpretasi skor:

**1–2 = Rendah**

**2–3 = Sedang**

**3–5 = Tinggi**
""")

# ======================================================
# TABS
# ======================================================

tabs=st.tabs([

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

    col1,col2=st.columns(2)

    with col1:

        fig1=px.histogram(

            df,

            x='Skor Risiko',

            nbins=10,

            color_discrete_sequence=['#ef4444']

        )

        fig1.update_layout(
            height=420
        )

        st.plotly_chart(
            fig1,
            use_container_width=True
        )

    with col2:

        fig2=px.pie(

            df,

            names='Jenis Kelamin',

            hole=0.5

        )

        fig2.update_layout(
            height=420
        )

        st.plotly_chart(
            fig2,
            use_container_width=True
        )

# ======================================================
# PROFIL RESPONDEN
# ======================================================

with tabs[1]:

    st.subheader(
    "Profil Responden Penelitian"
    )

    kiri,kanan=st.columns(2)

    with kiri:

        usia_df=(
            df['Usia']
            .value_counts()
            .reset_index()
        )

        usia_df.columns=[
            'Usia',
            'Jumlah'
        ]

        usia_chart=px.bar(

            usia_df,

            x='Usia',

            y='Jumlah',

            color='Jumlah'

        )

        usia_chart.update_layout(
            height=420
        )

        st.plotly_chart(
            usia_chart,
            use_container_width=True
        )

    with kanan:

        durasi_df=(

            df[
            'Rata-rata Durasi Penggunaan Instagram per Hari'
            ]

            .value_counts()

            .reset_index()

        )

        durasi_df.columns=[
            'Durasi',
            'Jumlah'
        ]

        durasi_chart=px.bar(

            durasi_df,

            x='Durasi',

            y='Jumlah',

            color='Jumlah'

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

    left,right=st.columns(2)

    with left:

        corr=df[

        [

        'Skor Algoritma',

        'Skor Echo Chamber',

        'Skor Risiko'

        ]

        ].corr()

        heat=px.imshow(

            corr,

            text_auto=True,

            color_continuous_scale='RdBu'

        )

        heat.update_layout(
            height=420
        )

        st.plotly_chart(
            heat,
            use_container_width=True
        )

    with right:

        scatter=px.scatter(

            df,

            x='Skor Echo Chamber',

            y='Skor Risiko',

            color='Usia',

            size='Skor Algoritma'

        )

        scatter.update_layout(
            height=420
        )

        st.plotly_chart(
            scatter,
            use_container_width=True
        )

    st.markdown("---")

    aktivitas_col=None

    for col in df.columns:

        if "Aktivitas Instagram" in col:

            aktivitas_col=col

            break

    if aktivitas_col:

        aktivitas=(
            df.groupby(
                aktivitas_col
            )['Skor Risiko']
            .mean()
            .reset_index()
        )

        aktivitas_chart=px.bar(

            aktivitas,

            x=aktivitas_col,

            y='Skor Risiko',

            color='Skor Risiko'

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

    st.markdown(
    "### Outer Loading"
    )

    outer_loading=pd.DataFrame({

    'Indikator':[

    'X1.1',
    'X1.2',
    'X1.3',
    'X1.4',
    'X1.5',

    'X2.1',
    'X2.3',
    'X2.4',
    'X2.5',

    'Y1',
    'Y2',
    'Y3',
    'Y4',
    'Y5'

    ],

    'Loading':[

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

    st.markdown("---")

    st.markdown(
    "### Construct Reliability & Validity"
    )

    construct=pd.DataFrame({

    'Construct':[

    'Algoritma Rekomendasi Konten',

    'Echo Chamber',

    'Risiko Adiksi Digital'

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
    "Model memenuhi validitas konvergen dan construct reliability."
    )

    st.markdown("---")

    st.markdown(
    "### Uji Hipotesis"
    )

    hypothesis=pd.DataFrame({

    'Hubungan':[

    'Algoritma Rekomendasi Konten → Risiko Adiksi Digital',

    'Echo Chamber → Risiko Adiksi Digital'

    ],

    'T Statistics':[

    0.524,

    4.114

    ],

    'P Value':[

    0.600,

    0.000

    ],

    'Status':[

    'Tidak Signifikan',

    'Signifikan'

    ]

    })

    st.dataframe(
        hypothesis,
        use_container_width=True
    )

# ======================================================
# MITIGASI TAB
# ======================================================

with tabs[4]:

    st.subheader(
    "Rekomendasi Mitigasi"
    )

    risk=df['Skor Risiko'].mean()

    if risk>=4:

        st.error("""

RISIKO TINGGI

• Batasi screen time Instagram.

• Diversifikasi konsumsi konten.

• Gunakan fitur pengingat waktu aplikasi.

• Tingkatkan literasi digital.

• Evaluasi pola penggunaan media sosial.

""")

    elif risk>=3:

        st.warning("""

RISIKO SEDANG

• Monitoring durasi penggunaan.

• Kurangi konsumsi konten repetitif.

• Tingkatkan kesadaran penggunaan digital.

""")

    else:

        st.success("""

RISIKO RENDAH

Penggunaan Instagram relatif terkendali.

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
"Instagram Digital Addiction Risk Analytics Dashboard | DSR Research Dashboard"
)
