import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(
    page_title="Instagram Digital Addiction Risk Analytics Dashboard",
    page_icon="📊",
    layout="wide"
)

# =======================
# CSS
# =======================

st.markdown("""
<style>

.main .block-container{
padding-top:1rem;
padding-left:2rem;
padding-right:2rem;
max-width:100%;
}

.metric-card{
background:#111827;
padding:18px;
border-radius:18px;
color:white;
box-shadow:0 4px 20px rgba(0,0,0,0.12);
text-align:center;
}

.metric-title{
font-size:15px;
color:#cbd5e1;
}

.metric-value{
font-size:34px;
font-weight:bold;
}

</style>
""",unsafe_allow_html=True)

# =======================
# SIDEBAR
# =======================

st.sidebar.title("📂 Dataset")

uploaded_file = st.sidebar.file_uploader(
"Upload CSV / Excel",
type=["csv","xlsx"]
)

if uploaded_file:

    st.sidebar.success("Mode Preview Dataset Aktif")

    if uploaded_file.name.endswith(".csv"):
        df = pd.read_csv(uploaded_file)

    else:
        df = pd.read_excel(uploaded_file)

else:
    df = pd.read_csv("dataset.csv")

df.columns=df.columns.str.strip()

# =======================
# TEMPLATE
# =======================

st.sidebar.markdown("---")

st.sidebar.info("""
Template dataset:

Demografi:
- Jenis Kelamin
- Usia
- Domisili
- Lama Penggunaan Instagram
- Rata-rata Durasi Penggunaan Instagram per Hari
- Aktivitas Instagram yang Paling Sering Dilakukan

Variabel:
- X1.1 — X1.5
- X2.1 — X2.5
- Y1 — Y5
""")

with open("dataset.csv","rb") as f:
    st.sidebar.download_button(
        "⬇ Download Template",
        data=f,
        file_name="template_dataset.csv",
        mime="text/csv"
    )

# =======================
# SCORE
# =======================

X1=['X1.1','X1.2','X1.3','X1.4','X1.5']
X2=['X2.1','X2.2','X2.3','X2.4','X2.5']
Y=['Y1','Y2','Y3','Y4','Y5']

df['Algorithm Score']=df[X1].mean(axis=1)
df['Echo Score']=df[X2].mean(axis=1)
df['Risk Score']=df[Y].mean(axis=1)

# =======================
# FILTER
# =======================

st.sidebar.markdown("---")
st.sidebar.subheader("🎯 Filter")

gender=st.sidebar.multiselect(
"Jenis Kelamin",
df['Jenis Kelamin'].unique(),
default=df['Jenis Kelamin'].unique()
)

usia=st.sidebar.multiselect(
"Usia",
df['Usia'].unique(),
default=df['Usia'].unique()
)

durasi=st.sidebar.multiselect(
"Durasi Penggunaan",
df['Rata-rata Durasi Penggunaan Instagram per Hari'].unique(),
default=df['Rata-rata Durasi Penggunaan Instagram per Hari'].unique()
)

df=df[
(df['Jenis Kelamin'].isin(gender))
&
(df['Usia'].isin(usia))
&
(df['Rata-rata Durasi Penggunaan Instagram per Hari'].isin(durasi))
]

# =======================
# TITLE
# =======================

st.title("📊 Instagram Digital Addiction Risk Analytics Dashboard")

st.markdown("""
Dashboard analitik penelitian berbasis:

**Algoritma Rekomendasi Konten — Echo Chamber — Risiko Adiksi Digital**
""")

# =======================
# KPI
# =======================

c1,c2,c3,c4=st.columns(4)

with c1:
    st.markdown(f"""
<div class="metric-card">
<div class="metric-title">Total Responden</div>
<div class="metric-value">{len(df)}</div>
</div>
""",unsafe_allow_html=True)

with c2:
    st.markdown(f"""
<div class="metric-card">
<div class="metric-title">Algorithm Score</div>
<div class="metric-value">{round(df['Algorithm Score'].mean(),2)}</div>
</div>
""",unsafe_allow_html=True)

with c3:
    st.markdown(f"""
<div class="metric-card">
<div class="metric-title">Echo Score</div>
<div class="metric-value">{round(df['Echo Score'].mean(),2)}</div>
</div>
""",unsafe_allow_html=True)

with c4:
    st.markdown(f"""
<div class="metric-card">
<div class="metric-title">Risk Score</div>
<div class="metric-value">{round(df['Risk Score'].mean(),2)}</div>
</div>
""",unsafe_allow_html=True)

# =======================
# TABS
# =======================

tabs=st.tabs([
"Overview",
"Risk Analytics",
"Behavioral Insight",
"SmartPLS Result",
"Mitigation"
])

# =======================
# OVERVIEW
# =======================

with tabs[0]:

    col1,col2=st.columns(2)

    with col1:

        fig=px.histogram(
            df,
            x='Risk Score',
            nbins=12,
            color_discrete_sequence=['#ef4444']
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    with col2:

        fig2=px.pie(
            df,
            names='Jenis Kelamin',
            hole=0.5
        )

        st.plotly_chart(
            fig2,
            use_container_width=True
        )

    st.subheader("Distribusi Usia")

    usia_fig=px.bar(
        df['Usia'].value_counts().reset_index(),
        x='Usia',
        y='count'
    )

    st.plotly_chart(
        usia_fig,
        use_container_width=True
    )

# =======================
# RISK ANALYTICS
# =======================

with tabs[1]:

    corr=df[
    [
        'Algorithm Score',
        'Echo Score',
        'Risk Score'
    ]
    ].corr()

    heat=px.imshow(
        corr,
        text_auto=True,
        color_continuous_scale='RdBu'
    )

    st.plotly_chart(
        heat,
        use_container_width=True
    )

    scatter=px.scatter(
        df,
        x='Echo Score',
        y='Risk Score',
        color='Usia',
        size='Algorithm Score'
    )

    st.plotly_chart(
        scatter,
        use_container_width=True
    )

# =======================
# BEHAVIOR
# =======================

with tabs[2]:

    fig3=px.box(
        df,
        x='Usia',
        y='Risk Score',
        color='Usia'
    )

    st.plotly_chart(
        fig3,
        use_container_width=True
    )

    behavior=(
        df.groupby(
        'Aktivitas Instagram yang Paling Sering Dilakukan'
        )['Risk Score']
        .mean()
        .reset_index()
    )

    fig4=px.bar(
        behavior,
        x='Aktivitas Instagram yang Paling Sering Dilakukan',
        y='Risk Score',
        color='Risk Score'
    )

    st.plotly_chart(
        fig4,
        use_container_width=True
    )

# =======================
# SMARTPLS
# =======================

with tabs[3]:

    st.subheader("Validasi SmartPLS")

    outer=pd.DataFrame({

    'Indikator':[

    'X1.1','X1.2','X1.3','X1.4','X1.5',
    'X2.1','X2.3','X2.4','X2.5',
    'Y1','Y2','Y3','Y4','Y5'

    ],

    'Outer Loading':[

    0.860,0.757,0.750,0.868,0.798,
    0.816,0.757,0.712,0.802,
    0.820,0.891,0.783,0.718,0.874

    ]

    })

    st.dataframe(
        outer,
        use_container_width=True
    )

    construct=pd.DataFrame({

    'Construct':[

    'Algoritma Rekomendasi Konten',
    'Echo Chamber',
    'Risiko Adiksi Digital'

    ],

    'AVE':[

    0.653,
    0.597,
    0.672

    ],

    'CR':[

    0.904,
    0.855,
    0.911

    ]

    })

    st.dataframe(
        construct,
        use_container_width=True
    )

    st.success(
        "Model memenuhi validitas konvergen dan construct reliability."
    )

# =======================
# MITIGATION
# =======================

with tabs[4]:

    risk=df['Risk Score'].mean()

    st.subheader("Rekomendasi Mitigasi")

    if risk>=4:

        st.error("""
RISIKO TINGGI

• Batasi screen time Instagram

• Diversifikasi konsumsi konten

• Evaluasi pola penggunaan harian

• Tingkatkan literasi digital

• Gunakan fitur reminder penggunaan aplikasi
""")

    elif risk>=3:

        st.warning("""
RISIKO SEDANG

• Monitoring durasi penggunaan

• Evaluasi algoritma konsumsi konten

• Kurangi penggunaan impulsif
""")

    else:

        st.success("""
RISIKO RENDAH

Perilaku penggunaan Instagram relatif terkendali.
""")

# =======================
# RAW DATA
# =======================

st.markdown("---")

with st.expander("📄 Lihat Dataset"):

    st.dataframe(
        df,
        use_container_width=True
    )
