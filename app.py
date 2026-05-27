# ======================================================
# 1. IMPORT
# ======================================================
import streamlit as st
import pandas as pd
import plotly.express as px

# ======================================================
# 2. PAGE CONFIG
# ======================================================
st.set_page_config(
    page_title="Instagram Digital Risk Analytics",
    page_icon="📊",
    layout="wide"
)

# ======================================================
# 3. CSS (CLEAN UX STYLE)
# ======================================================
st.markdown("""
<style>
.main { background: #f8fafc; }

.block-container {
    padding: 1.5rem 2rem;
}

.kpi {
    background: white;
    padding: 18px;
    border-radius: 14px;
    box-shadow: 0px 4px 12px rgba(0,0,0,0.06);
    border-left: 5px solid #2563eb;
}

.kpi-title { font-size: 13px; color: #64748b; }
.kpi-value { font-size: 26px; font-weight: 700; }
.kpi-sub { font-size: 12px; color: #94a3b8; }
</style>
""", unsafe_allow_html=True)

# ======================================================
# 4. LOAD DATA
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
# 5. CLEAN DATA
# ======================================================
df.columns = df.columns.str.strip()
df.columns = df.columns.str.replace("\n", " ", regex=True)

# ======================================================
# 6. MODEL VARIABLES
# ======================================================
X1 = ["X1.1","X1.2","X1.3","X1.4","X1.5"]
X2 = ["X2.1","X2.3","X2.4","X2.5"]
Y  = ["Y1","Y2","Y3","Y4","Y5"]

required = X1 + X2 + Y

missing = [c for c in required if c not in df.columns]
if missing:
    st.error(f"Missing columns: {missing}")
    st.stop()

# ======================================================
# 7. FEATURE ENGINEERING
# ======================================================
df["Skor Algoritma"] = df[X1].mean(axis=1)
df["Skor Echo Chamber"] = df[X2].mean(axis=1)
df["Skor Risiko"] = df[Y].mean(axis=1)

def kategori(x):
    if x < 2.61:
        return "Rendah"
    elif x < 3.41:
        return "Sedang"
    else:
        return "Tinggi"

df["Kategori Risiko"] = df["Skor Risiko"].apply(kategori)

# ======================================================
# 8. SIDEBAR FILTER
# ======================================================
st.sidebar.title("📊 Dashboard Control")

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
    "Durasi Instagram",
    df["Rata-rata Durasi Penggunaan Instagram per Hari"].unique(),
    default=df["Rata-rata Durasi Penggunaan Instagram per Hari"].unique()
)

df = df[
    (df["Jenis Kelamin"].isin(gender)) &
    (df["Usia"].isin(usia)) &
    (df["Rata-rata Durasi Penggunaan Instagram per Hari"].isin(durasi))
]

# ======================================================
# 9. HEADER
# ======================================================
st.title("📱 Instagram Digital Risk Analytics Dashboard")
st.caption("Analisis Pengaruh Algoritma & Echo Chamber terhadap Risiko Adiksi Digital")

st.markdown("---")

# ======================================================
# 10. KPI (NO AMBIGUITY)
# ======================================================
dominant = df["Kategori Risiko"].value_counts().idxmax()

c1, c2, c3 = st.columns(3)

with c1:
    st.markdown(f"""
    <div class="kpi">
        <div class="kpi-title">Total Responden</div>
        <div class="kpi-value">{len(df)}</div>
        <div class="kpi-sub">Setelah filtering</div>
    </div>
    """, unsafe_allow_html=True)

with c2:
    st.markdown(f"""
    <div class="kpi">
        <div class="kpi-title">Rata-rata Risiko</div>
        <div class="kpi-value">{df['Skor Risiko'].mean():.2f}</div>
        <div class="kpi-sub">Skala 1–5</div>
    </div>
    """, unsafe_allow_html=True)

with c3:
    st.markdown(f"""
    <div class="kpi">
        <div class="kpi-title">Kategori Dominan</div>
        <div class="kpi-value">{dominant}</div>
        <div class="kpi-sub">Distribusi terbesar</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# ======================================================
# 11. RISK INTERPRETATION
# ======================================================
mean = df["Skor Risiko"].mean()

if mean >= 4.21:
    st.error(f"Risiko: Sangat Tinggi ({mean:.2f})")
elif mean >= 3.41:
    st.error(f"Risiko: Tinggi ({mean:.2f})")
elif mean >= 2.61:
    st.warning(f"Risiko: Sedang ({mean:.2f})")
elif mean >= 1.81:
    st.success(f"Risiko: Rendah ({mean:.2f})")
else:
    st.success(f"Risiko: Sangat Rendah ({mean:.2f})")

# ======================================================
# 12. TABS (IMPORTANT: NO ERROR STRUCTURE)
# ======================================================
tabs = st.tabs([
    "Overview",
    "Profil",
    "Analisis Risiko",
    "SmartPLS",
    "Mitigasi"
])

# ======================================================
# TAB 1 - OVERVIEW
# ======================================================
with tabs[0]:

    st.subheader("Overview")

    col1, col2 = st.columns(2)

    with col1:
        fig = px.histogram(df, x="Skor Risiko", nbins=10)
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        fig = px.pie(df, names="Kategori Risiko")
        st.plotly_chart(fig, use_container_width=True)

# ======================================================
# TAB 2 - PROFIL
# ======================================================
with tabs[1]:

    st.subheader("Profil Responden")

    st.bar_chart(df["Usia"].value_counts())

    st.bar_chart(df["Jenis Kelamin"].value_counts())

# ======================================================
# TAB 3 - ANALISIS RISIKO
# ======================================================
with tabs[2]:

    st.subheader("Analisis Hubungan Variabel")

    corr = df[["Skor Algoritma","Skor Echo Chamber","Skor Risiko"]].corr()

    fig = px.imshow(corr, text_auto=True)
    st.plotly_chart(fig, use_container_width=True)

    st.scatter_chart(df[["Skor Echo Chamber","Skor Risiko"]])

# ======================================================
# TAB 4 - SMARTPLS
# ======================================================
with tabs[3]:

    st.subheader("Evaluasi Model")

    st.write("Outer loading & reliability (static table)")

# ======================================================
# TAB 5 - MITIGASI
# ======================================================
with tabs[4]:

    st.subheader("Mitigasi Risiko")

    st.info("Echo Chamber adalah faktor paling dominan dalam risiko adiksi digital.")

# ======================================================
# FOOTER
# ======================================================
st.markdown("---")
st.caption("DSR Research Dashboard | Production Ready Version")
