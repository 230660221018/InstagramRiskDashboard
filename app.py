import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np

st.set_page_config(
    page_title="Instagram Risk Analytics Dashboard",
    layout="wide"
)

st.title("📊 Instagram Digital Addiction Risk Analytics Dashboard")

st.markdown("""
Dashboard analitik untuk monitoring risiko adiksi digital berdasarkan:

• Algoritma Rekomendasi Konten  
• Echo Chamber  
• Risiko Adiksi Digital
""")

#============================
# SIDEBAR
#============================

st.sidebar.header("Upload Dataset")

uploaded_file = st.sidebar.file_uploader(
    "Upload Excel",
    type=["xlsx"]
)

# DEFAULT DATA

if uploaded_file:

    df = pd.read_excel(uploaded_file)

else:

    st.sidebar.info(
        "Menggunakan dataset default penelitian."
    )

    df = pd.read_excel("dataset.xlsx")

#============================
# CLEANING
#============================

df.columns=df.columns.str.strip()

#============================
# SCORE CALCULATION
#============================

X1=['X1.1','X1.2','X1.3','X1.4','X1.5']

X2=['X2.1','X2.3','X2.4','X2.5']

Y=['Y1','Y2','Y3','Y4','Y5']

df['Algoritma Score']=df[X1].mean(axis=1)

df['Echo Score']=df[X2].mean(axis=1)

df['Risk Score']=df[Y].mean(axis=1)

#============================
# KPI
#============================

col1,col2,col3,col4=st.columns(4)

col1.metric(
    "Total Responden",
    len(df)
)

col2.metric(
    "Avg Algorithm",
    round(df['Algoritma Score'].mean(),2)
)

col3.metric(
    "Avg Echo Chamber",
    round(df['Echo Score'].mean(),2)
)

col4.metric(
    "Avg Risk",
    round(df['Risk Score'].mean(),2)
)

st.divider()

#============================
# CHARTS
#============================

left,right=st.columns(2)

with left:

    fig=px.histogram(
        df,
        x="Risk Score",
        nbins=10,
        title="Distribusi Risiko Adiksi Digital"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

with right:

    fig2=px.box(
        df,
        y="Risk Score",
        title="Risk Score Distribution"
    )

    st.plotly_chart(
        fig2,
        use_container_width=True
    )

#============================
# CORRELATION
#============================

st.subheader(
    "Relationship Analysis"
)

corr=df[
[
'Algoritma Score',
'Echo Score',
'Risk Score'
]
].corr()

fig3=px.imshow(
    corr,
    text_auto=True,
    color_continuous_scale='RdBu'
)

st.plotly_chart(
    fig3,
    use_container_width=True
)

#============================
# MITIGATION ENGINE
#============================

st.subheader(
    "Mitigation Recommendation"
)

avg_risk=df['Risk Score'].mean()

if avg_risk>=4:

    st.error(
        """
RISIKO TINGGI

Disarankan:

✔ pembatasan screen time

✔ diversifikasi konsumsi konten

✔ monitoring perilaku digital
"""
    )

elif avg_risk>=3:

    st.warning(
        """
RISIKO SEDANG

Disarankan:

✔ peningkatan literasi digital

✔ evaluasi pola konsumsi konten
"""
    )

else:

    st.success(
        """
RISIKO RENDAH

Penggunaan Instagram relatif terkendali.
"""
    )

#============================
# DATA VIEW
#============================

st.subheader(
    "Dataset Preview"
)

st.dataframe(df)
