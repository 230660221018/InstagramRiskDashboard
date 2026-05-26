import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# ==========================================================
# PAGE CONFIG
# ==========================================================

st.set_page_config(
    page_title="Instagram Digital Addiction Risk Analytics Dashboard",
    page_icon="📱",
    layout="wide"
)

# ==========================================================
# MODERN CSS
# ==========================================================

st.markdown("""

<style>

@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap');

html, body, [class*="css"] {
font-family: 'Poppins', sans-serif;
}

.main{
background:#F8FAFC;
}

.block-container{
padding-top:1rem;
padding-left:2rem;
padding-right:2rem;
}

.hero{

background:linear-gradient(
135deg,
#2563eb,
#7c3aed
);

padding:30px;

border-radius:24px;

color:white;

margin-bottom:20px;

box-shadow:0 8px 30px rgba(0,0,0,0.15);

}

.card{

background:white;

padding:22px;

border-radius:22px;

box-shadow:0px 8px 24px rgba(0,0,0,0.07);

margin-bottom:18px;

}

.metric-card{

background:white;

padding:22px;

border-radius:22px;

box-shadow:0px 8px 20px rgba(0,0,0,0.08);

border-left:7px solid #2563EB;

}

.metric-title{

font-size:14px;

color:#64748B;

}

.metric-value{

font-size:32px;

font-weight:700;

color:#111827;

}

.info-box{

background:#EEF2FF;

padding:18px;

border-radius:18px;

border-left:7px solid #4F46E5;

margin-bottom:15px;

}

.valid-box{

background:#ECFDF5;

padding:18px;

border-radius:18px;

border-left:7px solid #10B981;

margin-bottom:15px;

}

.warning-box{

background:#FEF3C7;

padding:18px;

border-radius:18px;

border-left:7px solid #F59E0B;

margin-bottom:15px;

}

</style>

""",unsafe_allow_html=True)

# ==========================================================
# LOAD DATASET
# ==========================================================

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
        "dataset.csv tidak ditemukan di repository GitHub."
    )

    st.stop()

# ==========================================================
# CLEAN COLUMN
# ==========================================================

df.columns=df.columns.str.strip()

df.columns=df.columns.str.replace(
'\n',
' ',
regex=True
)

# ==========================================================
# MODEL FINAL PENELITIAN
# X2.2 DIELIMINASI
# ==========================================================

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

# ==========================================================
# SCORE CALCULATION
# ==========================================================

df['Skor Algoritma']=df[X1].mean(axis=1)

df['Skor Echo Chamber']=df[X2].mean(axis=1)

df['Skor Risiko']=df[Y].mean(axis=1)

# ==========================================================
# SIDEBAR
# ==========================================================

st.sidebar.title(
"⚙️ Dashboard Penelitian"
)

st.sidebar.markdown("""

### Instagram Digital Addiction Risk Analytics Dashboard

Dashboard analitik penelitian berbasis:

✅ Algoritma Rekomendasi Konten

✅ Echo Chamber

✅ Risiko Adiksi Digital

Populasi penelitian:

**Pengguna Instagram berdomisili Kabupaten Sumedang**

""")

st.sidebar.markdown("---")

# ==========================================================
# FILTER
# ==========================================================

gender=st.sidebar.multiselect(

"Jenis Kelamin",

options=df['Jenis Kelamin'].unique(),

default=df['Jenis Kelamin'].unique()

)

usia=st.sidebar.multiselect(

"Kelompok Usia",

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

# ==========================================================
# APPLY FILTER
# ==========================================================

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

# ==========================================================
# HERO SECTION
# ==========================================================

st.markdown(f"""

<div class='hero'>

<h1>

📱 Instagram Digital Addiction Risk Analytics Dashboard

</h1>

<p style='font-size:17px;'>

Dashboard penelitian kuantitatif berbasis SmartPLS untuk menganalisis pengaruh:

<b>Algoritma Rekomendasi Konten</b> dan
<b>Echo Chamber</b> terhadap
<b>Risiko Adiksi Digital Instagram</b>

pada pengguna Instagram berdomisili
<b>Kabupaten Sumedang.</b>

</p>

</div>

""",unsafe_allow_html=True)

# ==========================================================
# KPI SECTION
# ==========================================================

c1,c2,c3,c4=st.columns(4)

with c1:

    st.markdown(f"""

<div class='metric-card'>

<div class='metric-title'>
Jumlah Responden Aktif
</div>

<div class='metric-value'>
{len(df)}
</div>

</div>

""",unsafe_allow_html=True)

with c2:

    st.markdown(f"""

<div class='metric-card'>

<div class='metric-title'>
Rata-rata Algoritma Konten
</div>

<div class='metric-value'>
{round(df['Skor Algoritma'].mean(),2)}/5
</div>

</div>

""",unsafe_allow_html=True)

with c3:

    st.markdown(f"""

<div class='metric-card'>

<div class='metric-title'>
Rata-rata Echo Chamber
</div>

<div class='metric-value'>
{round(df['Skor Echo Chamber'].mean(),2)}/5
</div>

</div>

""",unsafe_allow_html=True)

with c4:

    st.markdown(f"""

<div class='metric-card'>

<div class='metric-title'>
Rata-rata Risiko Adiksi
</div>

<div class='metric-value'>
{round(df['Skor Risiko'].mean(),2)}/5
</div>

</div>

""",unsafe_allow_html=True)

# ==========================================================
# RESEARCH INFORMATION
# ==========================================================

st.markdown("""

<div class='card'>

<h3>
📌 Informasi Penelitian
</h3>

Penelitian menggunakan pendekatan
<b>Partial Least Squares Structural Equation Modeling (PLS-SEM)</b>
melalui SmartPLS.

Objek penelitian:

<b>Pengguna Instagram berdomisili Kabupaten Sumedang.</b>

Model penelitian:

Algoritma Rekomendasi Konten → Risiko Adiksi Digital

Echo Chamber → Risiko Adiksi Digital

</div>

""",unsafe_allow_html=True)

# ==========================================================
# VALIDITY EXPLANATION
# ==========================================================

st.markdown("""

<div class='valid-box'>

<h4>
✔ Interpretasi Outer Loading
</h4>

Pada pengujian SmartPLS, indikator dinyatakan memiliki
<b>validitas konvergen yang baik</b>
apabila nilai
<b>Outer Loading > 0.70.</b>

Interpretasi umum:

• <b>>0.70</b> = indikator valid dan dipertahankan.

• <b>0.40–0.70</b> = dievaluasi berdasarkan AVE,
Composite Reliability,
serta kontribusi indikator.

• <b><0.40</b> = direkomendasikan untuk dieliminasi.

Pada model final penelitian ini,
indikator
<b>X2.2 dieliminasi</b>
karena tidak memenuhi kriteria validitas.

</div>

""",unsafe_allow_html=True)

# ==========================================================
# USER SIMULATION
# ==========================================================

st.markdown("""

<div class='warning-box'>

<h4>
🧠 Simulasi Risiko Pengguna
</h4>

Fitur ini memungkinkan pengguna melakukan simulasi sederhana
untuk melihat estimasi tingkat risiko adiksi digital.

</div>

""",unsafe_allow_html=True)

sim1,sim2=st.columns(2)

with sim1:

    simulasi_algoritma=st.slider(

        "Algoritma Rekomendasi Konten",

        1.0,

        5.0,

        3.5,

        0.1

    )

with sim2:

    simulasi_echo=st.slider(

        "Echo Chamber",

        1.0,

        5.0,

        3.5,

        0.1

    )

prediksi=(

(simulasi_algoritma*0.35)

+

(simulasi_echo*0.65)

)

if prediksi>=4:

    st.error(
        f"Prediksi Risiko Tinggi ({round(prediksi,2)}/5)"
    )

elif prediksi>=3:

    st.warning(
        f"Prediksi Risiko Sedang ({round(prediksi,2)}/5)"
    )

else:

    st.success(
        f"Prediksi Risiko Rendah ({round(prediksi,2)}/5)"
    )

# ==========================================================
# TABS
# ==========================================================

tabs=st.tabs([

"Overview",

"Profil Responden",

"Analisis Risiko",

"SmartPLS",

"Mitigasi"

])

# ==========================================================
# TAB 1 — OVERVIEW
# ==========================================================

with tabs[0]:

    st.subheader(
    "📊 Gambaran Umum Risiko Adiksi Digital"
    )

    kiri,kanan=st.columns(2)

    with kiri:

        fig1=px.histogram(

            df,

            x='Skor Risiko',

            nbins=10,

            color_discrete_sequence=['#7C3AED']

        )

        fig1.update_layout(

            title='Distribusi Risiko Adiksi Digital',

            plot_bgcolor='white',

            paper_bgcolor='white',

            height=450

        )

        st.plotly_chart(
            fig1,
            use_container_width=True
        )

    with kanan:

        fig2=px.pie(

            df,

            names='Jenis Kelamin',

            hole=0.55,

            color_discrete_sequence=[
            '#2563EB',
            '#7C3AED'
            ]

        )

        fig2.update_layout(

            title='Komposisi Jenis Kelamin Responden',

            height=450

        )

        st.plotly_chart(
            fig2,
            use_container_width=True
        )

    st.markdown("---")

    colA,colB=st.columns(2)

    with colA:

        risk_usia=px.box(

            df,

            x='Usia',

            y='Skor Risiko',

            color='Usia'

        )

        risk_usia.update_layout(

            title='Risiko Adiksi berdasarkan Kelompok Usia',

            height=450

        )

        st.plotly_chart(
            risk_usia,
            use_container_width=True
        )

    with colB:

        durasi_chart=px.bar(

            df.groupby(
            'Rata-rata Durasi Penggunaan Instagram per Hari'
            )['Skor Risiko']

            .mean()

            .reset_index(),

            x='Rata-rata Durasi Penggunaan Instagram per Hari',

            y='Skor Risiko',

            color='Skor Risiko',

            color_continuous_scale='Purples'

        )

        durasi_chart.update_layout(

            title='Rata-rata Risiko berdasarkan Durasi Penggunaan',

            height=450

        )

        st.plotly_chart(
            durasi_chart,
            use_container_width=True
        )

# ==========================================================
# TAB 2 — PROFIL RESPONDEN
# ==========================================================

with tabs[1]:

    st.subheader(
    "👥 Profil Responden Penelitian"
    )

    st.info("""

Seluruh responden dalam penelitian ini merupakan
**pengguna Instagram berdomisili Kabupaten Sumedang.**

Visualisasi berikut membantu memahami karakteristik responden.

""")

    kiri,kanan=st.columns(2)

    with kiri:

        usia_df=(
            df['Usia']
            .value_counts()
            .reset_index()
        )

        usia_df.columns=[
        'Kelompok Usia',
        'Jumlah'
        ]

        usia_bar=px.bar(

            usia_df,

            x='Kelompok Usia',

            y='Jumlah',

            color='Jumlah',

            color_continuous_scale='Blues'

        )

        usia_bar.update_layout(

            title='Distribusi Kelompok Usia',

            height=450

        )

        st.plotly_chart(
            usia_bar,
            use_container_width=True
        )

    with kanan:

        aktivitas_col=None

        for col in df.columns:

            if "Aktivitas Instagram" in col:

                aktivitas_col=col

                break

        if aktivitas_col:

            aktivitas=(
                df[aktivitas_col]
                .value_counts()
                .reset_index()
            )

            aktivitas.columns=[
            'Aktivitas',
            'Jumlah'
            ]

            aktivitas_chart=px.bar(

                aktivitas,

                x='Aktivitas',

                y='Jumlah',

                color='Jumlah',

                color_continuous_scale='Purples'

            )

            aktivitas_chart.update_layout(

                title='Aktivitas Instagram yang Paling Sering Dilakukan',

                height=450

            )

            st.plotly_chart(
                aktivitas_chart,
                use_container_width=True
            )

# ==========================================================
# TAB 3 — ANALISIS RISIKO
# ==========================================================

with tabs[2]:

    st.subheader(
    "🧠 Analisis Risiko Adiksi Digital"
    )

    st.markdown("""

Analisis berikut menunjukkan hubungan antar konstruk penelitian:

- Algoritma Rekomendasi Konten
- Echo Chamber
- Risiko Adiksi Digital

""")

    kiri,kanan=st.columns(2)

    with kiri:

        corr=df[[

        'Skor Algoritma',

        'Skor Echo Chamber',

        'Skor Risiko'

        ]].corr()

        heat=px.imshow(

            corr,

            text_auto=True,

            color_continuous_scale='RdBu'

        )

        heat.update_layout(

            title='Correlation Matrix',

            height=450

        )

        st.plotly_chart(
            heat,
            use_container_width=True
        )

    with kanan:

        scatter=px.scatter(

            df,

            x='Skor Echo Chamber',

            y='Skor Risiko',

            color='Usia',

            size='Skor Algoritma',

            hover_data=[
            'Jenis Kelamin'
            ]

        )

        scatter.update_layout(

            title='Echo Chamber vs Risiko Adiksi',

            height=450

        )

        st.plotly_chart(
            scatter,
            use_container_width=True
        )

    st.markdown("---")

    if aktivitas_col:

        aktivitas_risk=(

            df.groupby(
                aktivitas_col
            )['Skor Risiko']

            .mean()

            .reset_index()

        )

        risk_chart=px.bar(

            aktivitas_risk,

            x=aktivitas_col,

            y='Skor Risiko',

            color='Skor Risiko',

            color_continuous_scale='Reds'

        )

        risk_chart.update_layout(

            title='Rata-rata Risiko berdasarkan Aktivitas Instagram',

            height=500

        )

        st.plotly_chart(
            risk_chart,
            use_container_width=True
        )

# ==========================================================
# TAB 4 — SMARTPLS RESULT
# ==========================================================

with tabs[3]:

    st.subheader(
    "🧪 Hasil Pengujian SmartPLS"
    )

    st.markdown("""

Dashboard ini menggunakan hasil pengolahan data penelitian
dengan metode **PLS-SEM (SmartPLS)**.

Kriteria evaluasi model:

✔ Outer Loading > 0.70

✔ Cronbach Alpha > 0.70

✔ Composite Reliability > 0.70

✔ AVE > 0.50

✔ Hipotesis signifikan apabila P Value < 0.05

""")

    st.markdown("---")

    st.markdown(
    "### Outer Loading Model Final"
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

    'Outer Loading':[

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
    "Seluruh indikator pada model final memenuhi kriteria validitas konvergen (>0.70)."
    )

    st.info(
    "Catatan: indikator X2.2 dieliminasi karena tidak memenuhi kriteria outer loading."
    )

    st.markdown("---")

    st.markdown(
    "### Construct Reliability & Validity"
    )

    construct=pd.DataFrame({

    'Konstruk':[

    'Algoritma Rekomendasi Konten',

    'Echo Chamber',

    'Risiko Adiksi Digital'

    ],

    'Cronbach Alpha':[

    0.877,

    0.777,

    0.879

    ],

    'Composite Reliability':[

    0.904,

    0.855,

    0.911

    ],

    'AVE':[

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
    "Model memenuhi syarat reliability dan convergent validity."
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

    'Keputusan':[

    'Tidak Signifikan',

    'Signifikan'

    ]

    })

    st.dataframe(
        hypothesis,
        use_container_width=True
    )

    st.warning("""

Interpretasi hasil penelitian:

• Algoritma Rekomendasi Konten → Risiko Adiksi Digital
tidak berpengaruh signifikan.

• Echo Chamber → Risiko Adiksi Digital
berpengaruh positif dan signifikan.

""")

# ==========================================================
# TAB 5 — MITIGASI
# ==========================================================

with tabs[4]:

    st.subheader(
    "🛡️ Rekomendasi Mitigasi Risiko Digital"
    )

    avg_risk=round(
        df['Skor Risiko'].mean(),
        2
    )

    st.metric(
        "Rata-rata Risiko Digital Saat Ini",
        f"{avg_risk}/5"
    )

    if avg_risk>=4:

        st.error("""

RISIKO TINGGI

Rekomendasi:

• Batasi screen time Instagram.

• Kurangi konsumsi konten repetitif.

• Diversifikasi sumber informasi digital.

• Gunakan fitur pengingat waktu aplikasi.

• Tingkatkan literasi digital.

""")

    elif avg_risk>=3:

        st.warning("""

RISIKO SEDANG

Rekomendasi:

• Monitoring durasi penggunaan harian.

• Evaluasi pola penggunaan media sosial.

• Kurangi paparan echo chamber.

• Tingkatkan kesadaran digital.

""")

    else:

        st.success("""

RISIKO RENDAH

Penggunaan Instagram relatif terkendali.

Pertahankan pola penggunaan sehat.

""")

    st.markdown("---")

    st.markdown(
    "### Insight Penelitian"
    )

    st.info("""

Berdasarkan model penelitian,
faktor **Echo Chamber**
memiliki pengaruh signifikan terhadap
Risiko Adiksi Digital.

Hal ini menunjukkan bahwa pola konsumsi
konten homogen dan berulang
dapat meningkatkan potensi adiksi media sosial.

""")

# ==========================================================
# DATASET VIEW
# ==========================================================

st.markdown("---")

with st.expander(
"📄 Lihat Dataset Penelitian"
):

    st.dataframe(
        df,
        use_container_width=True
    )

st.caption(
"Instagram Digital Addiction Risk Analytics Dashboard | Penelitian Pengguna Instagram Kabupaten Sumedang"
)
