import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

# =====================================================
# CONFIG
# =====================================================

st.set_page_config(
    page_title="Instagram Digital Addiction Risk Analytics Dashboard",
    layout="wide",
    page_icon="📈"
)

# =====================================================
# CSS MODERN PROFESSIONAL UI
# =====================================================

st.markdown("""
<style>

.main{
background-color:#0F172A;
color:white;
}

h1,h2,h3{
color:white;
}

.block-container{
padding-top:1rem;
}

.metric-card{
background:linear-gradient(135deg,#1E293B,#0F172A);
padding:20px;
border-radius:20px;
box-shadow:0px 4px 20px rgba(0,0,0,.3);
}

[data-testid="metric-container"]{
background:linear-gradient(135deg,#1E293B,#111827);
padding:18px;
border-radius:16px;
border:1px solid #334155;
}

.stTabs [data-baseweb="tab-list"]{
gap:10px;
}

.stTabs [data-baseweb="tab"]{
background:#1E293B;
border-radius:12px;
padding:10px 18px;
}

</style>
""",unsafe_allow_html=True)

# =====================================================
# SIDEBAR
# =====================================================

st.sidebar.title("⚙️ Pengaturan Dashboard")

uploaded=st.sidebar.file_uploader(
"Upload Dataset CSV / Excel",
type=["csv","xlsx"]
)

# =====================================================
# LOAD DATA
# =====================================================

if uploaded:

    if uploaded.name.endswith(".csv"):

        df=pd.read_csv(uploaded)

    else:

        df=pd.read_excel(uploaded)

else:

    try:
        df=pd.read_csv("dataset.csv")

    except:

        st.warning("Upload dataset terlebih dahulu.")
        st.stop()

df.columns=df.columns.str.strip()

# =====================================================
# VALIDASI
# =====================================================

required_cols=[

'Jenis Kelamin',
'Usia',
'Rata-rata Durasi Penggunaan Instagram per Hari',

'X1.1','X1.2','X1.3','X1.4','X1.5',

'X2.1','X2.3','X2.4','X2.5',

'Y1','Y2','Y3','Y4','Y5'

]

missing=[x for x in required_cols if x not in df.columns]

if missing:

    st.error(f"Kolom tidak ditemukan: {missing}")

    st.stop()

# =====================================================
# SCORE CALCULATION
# =====================================================

X1=['X1.1','X1.2','X1.3','X1.4','X1.5']

X2=['X2.1','X2.3','X2.4','X2.5']

Y=['Y1','Y2','Y3','Y4','Y5']

df['Skor Algoritma']=df[X1].mean(axis=1)

df['Skor Echo']=df[X2].mean(axis=1)

df['Skor Risiko']=df[Y].mean(axis=1)

# =====================================================
# FILTER
# =====================================================

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

df=df[

(df['Jenis Kelamin'].isin(gender))

&

(df['Usia'].isin(usia))

]

# =====================================================
# HEADER
# =====================================================

st.title("Instagram Digital Addiction Risk Analytics Dashboard")

st.markdown("""
Dashboard analitik interaktif berbasis penelitian mengenai:

**Algoritma Rekomendasi Konten — Echo Chamber — Risiko Adiksi Digital Instagram**
""")

# =====================================================
# KPI
# =====================================================

avg_alg=round(df['Skor Algoritma'].mean(),2)

avg_echo=round(df['Skor Echo'].mean(),2)

avg_risk=round(df['Skor Risiko'].mean(),2)

risk_level="RENDAH"

if avg_risk>=4:

    risk_level="TINGGI"

elif avg_risk>=3:

    risk_level="SEDANG"

c1,c2,c3,c4,c5=st.columns(5)

c1.metric("Total Responden",len(df))

c2.metric("Skor Algoritma",avg_alg)

c3.metric("Skor Echo Chamber",avg_echo)

c4.metric("Skor Risiko",avg_risk)

c5.metric("Level Risiko",risk_level)

# =====================================================
# TABS
# =====================================================

tab1,tab2,tab3,tab4,tab5=st.tabs([

"Overview",

"Risk Analytics",

"Behavioral Insight",

"SmartPLS",

"Mitigasi"

])

# =====================================================
# OVERVIEW
# =====================================================

with tab1:

    col1,col2=st.columns(2)

    with col1:

        fig=px.histogram(

            df,

            x='Skor Risiko',

            nbins=10,

            color_discrete_sequence=['#3B82F6']

        )

        st.plotly_chart(fig,use_container_width=True)

    with col2:

        fig2=px.pie(

            df,

            names='Jenis Kelamin',

            hole=.5

        )

        st.plotly_chart(fig2,use_container_width=True)

# =====================================================
# RISK ANALYTICS
# =====================================================

with tab2:

    col1,col2=st.columns(2)

    with col1:

        gauge=go.Figure(go.Indicator(

            mode="gauge+number",

            value=avg_risk,

            title={'text':'Indeks Risiko Digital'},

            gauge={

                'axis':{'range':[0,5]},

                'bar':{'color':'red'}

            }

        ))

        st.plotly_chart(gauge,use_container_width=True)

    with col2:

        corr=df[

        ['Skor Algoritma','Skor Echo','Skor Risiko']

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

# =====================================================
# BEHAVIORAL
# =====================================================

with tab3:

    radar=go.Figure()

    radar.add_trace(go.Scatterpolar(

        r=[avg_alg,avg_echo,avg_risk],

        theta=[

        'Algoritma',

        'Echo',

        'Risiko'

        ],

        fill='toself'

    ))

    st.plotly_chart(

        radar,

        use_container_width=True

    )

    fig3=px.box(

        df,

        x='Usia',

        y='Skor Risiko',

        color='Usia'

    )

    st.plotly_chart(

        fig3,

        use_container_width=True

    )

# =====================================================
# SMARTPLS RESULT
# =====================================================

with tab4:

    st.subheader("Outer Loading")

    outer=pd.DataFrame({

    'Indikator':[

    'X1.1','X1.2','X1.3','X1.4','X1.5',

    'X2.1','X2.3','X2.4','X2.5',

    'Y1','Y2','Y3','Y4','Y5'

    ],

    'Loading':[

    0.860,0.757,0.750,0.868,0.798,

    0.816,0.757,0.712,0.802,

    0.820,0.891,0.783,0.718,0.874

    ]

    })

    st.dataframe(outer,use_container_width=True)

    st.subheader("Reliability & Validity")

    reli=pd.DataFrame({

    'Konstruk':[

    'Algoritma',

    'Echo Chamber',

    'Risiko Digital'

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

    st.dataframe(reli,use_container_width=True)

    st.subheader("Uji Hipotesis")

    hypo=pd.DataFrame({

    'Path':[

    'Algoritma → Risiko',

    'Echo → Risiko'

    ],

    'P Value':[

    0.600,

    0.000

    ]

    })

    st.dataframe(hypo,use_container_width=True)

# =====================================================
# MITIGASI
# =====================================================

with tab5:

    if avg_risk>=4:

        st.error("""

### Risiko Tinggi

Mitigasi yang direkomendasikan:

• Pembatasan screen time

• Diversifikasi konten

• Edukasi literasi digital

• Monitoring perilaku penggunaan

""")

    elif avg_risk>=3:

        st.warning("""

### Risiko Sedang

Mitigasi:

• Evaluasi pola konsumsi konten

• Monitoring durasi penggunaan

• Pengurangan exposure algoritmik

""")

    else:

        st.success("""

### Risiko Rendah

Penggunaan Instagram relatif terkendali.

""")

# =====================================================
# DOWNLOAD
# =====================================================

st.download_button(

"Download Dataset Hasil Analisis",

df.to_csv(index=False),

"processed_dataset.csv",

"text/csv"

)

st.markdown("---")

st.caption(
"Instagram Digital Addiction Risk Analytics Dashboard | Streamlit • Plotly • SmartPLS Research Artifact"
)
