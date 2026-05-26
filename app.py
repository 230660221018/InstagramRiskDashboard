import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(
    page_title="Instagram Risk Analytics Dashboard",
    layout="wide"
)

#=================================================
# LOAD DATA
#=================================================

st.sidebar.title("⚙️ Dataset")

uploaded_file=st.sidebar.file_uploader(
    "Upload Excel / CSV",
    type=["xlsx","csv"]
)

if uploaded_file:

    if uploaded_file.name.endswith('.csv'):

        df=pd.read_csv(uploaded_file)

    else:

        df=pd.read_excel(uploaded_file)

else:

    df=pd.read_csv("dataset.csv")

df.columns=df.columns.str.strip()

#=================================================
# SCORE CALCULATION
#=================================================

X1=['X1.1','X1.2','X1.3','X1.4','X1.5']

X2=['X2.1','X2.2','X2.3','X2.4','X2.5']

Y=['Y1','Y2','Y3','Y4','Y5']

df['Algorithm Score']=df[X1].mean(axis=1)

df['Echo Score']=df[X2].mean(axis=1)

df['Risk Score']=df[Y].mean(axis=1)

#=================================================
# FILTER
#=================================================

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
    "Durasi Instagram",
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

#=================================================
# TITLE
#=================================================

st.title(
"📊 Instagram Digital Addiction Risk Analytics Dashboard"
)

st.markdown(
"""
Dashboard analitik berbasis **Algoritma Rekomendasi Konten, Echo Chamber, dan Risiko Adiksi Digital.**
"""
)

#=================================================
# KPI
#=================================================

c1,c2,c3,c4=st.columns(4)

c1.metric(
"Total Responden",
len(df)
)

c2.metric(
"Avg Algorithm",
round(df['Algorithm Score'].mean(),2)
)

c3.metric(
"Avg Echo Chamber",
round(df['Echo Score'].mean(),2)
)

c4.metric(
"Avg Risk",
round(df['Risk Score'].mean(),2)
)

tabs=st.tabs([

"Overview",

"Risk Analytics",

"Behavioral Insight",

"SmartPLS Result",

"Mitigation"

])

#=================================================
# OVERVIEW
#=================================================

with tabs[0]:

    col1,col2=st.columns(2)

    with col1:

        fig=px.histogram(
            df,
            x="Risk Score",
            nbins=10,
            color_discrete_sequence=['red']
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    with col2:

        fig2=px.pie(
            df,
            names='Jenis Kelamin'
        )

        st.plotly_chart(
            fig2,
            use_container_width=True
        )

#=================================================
# ANALYTICS
#=================================================

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

#=================================================
# BEHAVIORAL
#=================================================

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

    fig4=px.bar(
        df.groupby(
            'Aktivitas Instagram yang Paling Sering Dilakukan'
        )['Risk Score']
        .mean()
        .reset_index(),
        x='Aktivitas Instagram yang Paling Sering Dilakukan',
        y='Risk Score'
    )

    st.plotly_chart(
        fig4,
        use_container_width=True
    )

#=================================================
# SMARTPLS
#=================================================

with tabs[3]:

    st.subheader(
    "SmartPLS Validation Result"
    )

    outer=pd.DataFrame({

    'Indicator':

    ['X1.1','X1.2','X1.3','X1.4','X1.5',

    'X2.1','X2.3','X2.4','X2.5',

    'Y1','Y2','Y3','Y4','Y5'],

    'Loading':

    [0.860,0.757,0.750,0.868,0.798,

    0.816,0.757,0.712,0.802,

    0.820,0.891,0.783,0.718,0.874]

    })

    st.dataframe(outer)

    st.success(
    "AVE, Composite Reliability, dan Cronbach Alpha valid."
    )

#=================================================
# MITIGATION
#=================================================

with tabs[4]:

    risk=df['Risk Score'].mean()

    if risk>=4:

        st.error("""
RISIKO TINGGI

Mitigasi:

• screen time limitation

• diversifikasi konten

• evaluasi pola penggunaan Instagram

• peningkatan literasi digital
""")

    elif risk>=3:

        st.warning("""
RISIKO SEDANG

Mitigasi:

• monitoring durasi penggunaan

• evaluasi konsumsi konten
""")

    else:

        st.success("""
RISIKO RENDAH

Penggunaan Instagram relatif terkendali.
""")
