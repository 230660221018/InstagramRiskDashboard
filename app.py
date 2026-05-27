import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# ======================================================
# PAGE CONFIG
# ======================================================

st.set_page_config(
    page_title="Instagram Digital Risk Analytics",
    page_icon="📊",
    layout="wide"
)

# ======================================================
# MODERN UI STYLE
# ======================================================

st.markdown("""
<style>

.main{
    background: linear-gradient(to right, #f8fafc, #eef2ff);
}

.block-container{
    padding:1.5rem 2rem;
}

/* KPI CARD */
.card{
    background:white;
    padding:18px;
    border-radius:18px;
    box-shadow:0 10px 25px rgba(0,0,0,0.06);
    border-left:6px solid #4f46e5;
}

/* TITLE */
.title{
    font-size:26px;
    font-weight:800;
    color:#111827;
}

/* subtitle */
.subtitle{
    font-size:14px;
    color:#6b7280;
}

/* badge */
.badge{
    padding:6px 12px;
    border-radius:999px;
    font-size:12px;
    font-weight:600;
}

.low{background:#dcfce7;color:#166534;}
.mid{background:#fef9c3;color:#854d0e;}
.high{background:#fee2e2;color:#991b1b;}

.small{
    font-size:12px;
    color:#6b7280;
}

</style>
""", unsafe_allow_html=True)

# ======================================================
# LOAD DATA
# ======================================================

try:
    try:
        df = pd.read_csv("dataset.csv", encoding="utf-8")
    except:
        df = pd.read_csv("dataset.csv", encoding="latin1")
except:
    st.error("Dataset tidak ditemukan.")
    st.stop()

df.columns = df.columns.str.strip().str.replace("\n", " ", regex=True)

# ======================================================
# VARIABLE MODEL (RESEARCH FRAMEWORK)
# ======================================================

# X1 = Algoritma Rekomendasi Konten Instagram
X1 = ["X1.1","X1.2","X1.3","X1.4","X1.5"]

# X2 = Echo Chamber (paparan konten homogen)
X2 = ["X2.1","X2.3","X2.4","X2.5"]

# Y = Risiko Adiksi Digital Instagram
Y  = ["Y1","Y2","Y3","Y4","Y5"]

required = X1 + X2 + Y
missing = [c for c in required if c not in df.columns]

if missing:
    st.error(f"Kolom tidak ditemukan: {missing}")
    st.stop()

# ======================================================
# SCORE COMPUTATION
# ======================================================

df["Algoritma"] = df[X1].mean(axis=1)
df["EchoChamber"] = df[X2].mean(axis=1)
df["Risiko"] = df[Y].mean(axis=1)

# ======================================================
# RISK CATEGORY
# ======================================================

def risk_level(x):
    if x < 2.61:
        return "LOW"
    elif x < 3.41:
        return "MEDIUM"
    else:
        return "HIGH"

df["RiskLevel"] = df["Risiko"].apply(risk_level)

# ======================================================
# SIDEBAR FILTER (CLEAN)
# ======================================================

st.sidebar.title("🎛️ Filter Data")

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

df = df[
    (df["Jenis Kelamin"].isin(gender)) &
    (df["Usia"].isin(usia))
]

st.sidebar.metric("Total Responden", len(df))

# ======================================================
# HEADER (MODERN DASHBOARD STYLE)
# ======================================================

st.markdown("""
<div class="title">📊 Instagram Digital Risk Analytics Dashboard</div>
<div class="subtitle">
Model Penelitian: Algoritma Rekomendasi • Echo Chamber • Risiko Adiksi Digital Instagram
</div>
""", unsafe_allow_html=True)

st.markdown("---")

# ======================================================
# RESEARCH VARIABLE EXPLANATION (SHORT + CLEAR)
# ======================================================

st.markdown("### 🔎 Variabel Penelitian")

v1, v2, v3 = st.columns(3)

with v1:
    st.info("""
**Algoritma Rekomendasi Konten**  
Sistem personalisasi Instagram yang menentukan konten yang ditampilkan kepada pengguna.
""")

with v2:
    st.info("""
**Echo Chamber**  
Kondisi ketika pengguna lebih sering menerima informasi yang seragam atau sejenis.
""")

with v3:
    st.info("""
**Risiko Adiksi Digital**  
Tingkat kecenderungan penggunaan Instagram secara berlebihan yang bersifat kompulsif.
""")

# ======================================================
# KPI DASHBOARD
# ======================================================

st.markdown("---")

c1, c2, c3, c4 = st.columns(4)

c1.metric("Responden", len(df))
c2.metric("Algoritma", f"{df['Algoritma'].mean():.2f}")
c3.metric("Echo Chamber", f"{df['EchoChamber'].mean():.2f}")
c4.metric("Risiko", f"{df['Risiko'].mean():.2f}")

# ======================================================
# RISK STATUS (CLEAR + VISUAL + NON AMBIGUOUS)
# ======================================================

st.markdown("---")

mean_risk = df["Risiko"].mean()
progress = min(mean_risk / 5, 1)

if mean_risk < 2.61:
    label = "LOW RISK"
    color = "low"
elif mean_risk < 3.41:
    label = "MEDIUM RISK"
    color = "mid"
else:
    label = "HIGH RISK"
    color = "high"

col1, col2 = st.columns([2, 1])

with col1:

    st.markdown(f"""
    <div style="font-size:18px;font-weight:700;">
        Current Risk Status
    </div>

    <div style="margin-top:10px;">
        <span class="badge {color}">{label}</span>
        <span style="margin-left:10px;color:#6b7280;">
            Score: {mean_risk:.2f} / 5
        </span>
    </div>
    """, unsafe_allow_html=True)

    st.progress(progress)

    st.caption("Interpretasi berbasis skala Likert 1–5")

with col2:

fig = go.Figure()

fig.add_trace(go.Indicator(
    mode="gauge+number",
    value=float(mean_risk),
    title={"text": "Risk Level"},
    gauge={
        "axis": {"range": [0, 5]},
        "bar": {"color": "#4f46e5"},
        "steps": [
            {"range": [0, 2.6], "color": "#dcfce7"},
            {"range": [2.6, 3.4], "color": "#fef9c3"},
            {"range": [3.4, 5], "color": "#fee2e2"}
        ]
    }
))

fig.update_layout(height=220, margin=dict(l=10, r=10, t=30, b=10))
st.plotly_chart(fig, use_container_width=True)

# ======================================================
# QUICK INSIGHT (VISUAL-FIRST, MIN TEXT)
# ======================================================

st.markdown("---")
st.markdown("### ⚡ Key Insight")

i1, i2, i3 = st.columns(3)

i1.metric("Dominant Factor", "Echo Chamber")
i2.metric("Algorithm Effect", "Moderate")
i3.metric("User Exposure", "High Variation")

# ======================================================
# PART 2 — PROFIL RESPONDEN (UX LEVEL 5)
# ======================================================

st.subheader("👥 Profil Responden")

st.markdown("Distribusi karakteristik responden dalam penelitian.")

# ======================================================
# TOP ROW KPI MINI INSIGHT
# ======================================================

k1, k2, k3 = st.columns(3)

k1.metric("Total Responden", len(df))
k2.metric("Usia Dominan", df["Usia"].mode()[0])
k3.metric("Gender Dominan", df["Jenis Kelamin"].mode()[0])

st.markdown("---")

# ======================================================
# VISUAL 1: USIA
# ======================================================

c1, c2 = st.columns(2)

with c1:

    usia_df = df["Usia"].value_counts().reset_index()
    usia_df.columns = ["Usia", "Jumlah"]

    fig_usia = px.bar(
        usia_df,
        x="Usia",
        y="Jumlah",
        text_auto=True,
        color="Jumlah",
        title="Distribusi Usia Responden"
    )

    fig_usia.update_layout(height=420, showlegend=False)
    st.plotly_chart(fig_usia, use_container_width=True)

with c2:

    gender_df = df["Jenis Kelamin"].value_counts().reset_index()
    gender_df.columns = ["Jenis Kelamin", "Jumlah"]

    fig_gender = px.pie(
        gender_df,
        names="Jenis Kelamin",
        values="Jumlah",
        hole=0.55,
        title="Komposisi Gender Responden"
    )

    fig_gender.update_layout(height=420)
    st.plotly_chart(fig_gender, use_container_width=True)

# ======================================================
# VISUAL 2: DURASI PENGGUNAAN
# ======================================================

st.markdown("---")

durasi_df = df[
    "Rata-rata Durasi Penggunaan Instagram per Hari"
].value_counts().reset_index()

durasi_df.columns = ["Durasi", "Jumlah"]

fig_durasi = px.bar(
    durasi_df,
    x="Durasi",
    y="Jumlah",
    text_auto=True,
    color="Jumlah",
    title="Durasi Penggunaan Instagram per Hari"
)

fig_durasi.update_layout(height=450)

st.plotly_chart(fig_durasi, use_container_width=True)

# ======================================================
# MINI INSIGHT PANEL (NO PARAGRAPH)
# ======================================================

st.markdown("---")
st.markdown("### ⚡ Insight Singkat")

i1, i2, i3 = st.columns(3)

i1.metric(
    "Kelompok Terbanyak",
    df["Usia"].value_counts().idxmax()
)

i2.metric(
    "Dominasi Gender",
    df["Jenis Kelamin"].value_counts().idxmax()
)

i3.metric(
    "Pola Durasi",
    "Cenderung Moderate"
)

# ======================================================
# OPTIONAL DISTRIBUTION CHECK (LIGHT VISUAL)
# ======================================================

st.markdown("---")
st.markdown("### 📊 Distribusi Ringkas")

col1, col2 = st.columns(2)

with col1:

    fig_box = px.histogram(
        df,
        x="Skor Risiko",
        nbins=10,
        title="Sebaran Risiko Adiksi Digital"
    )

    fig_box.update_layout(height=400)
    st.plotly_chart(fig_box, use_container_width=True)

with col2:

    fig_stack = px.bar(
        df.groupby("RiskLevel").size().reset_index(name="Jumlah"),
        x="RiskLevel",
        y="Jumlah",
        text_auto=True,
        title="Kategori Risiko"
    )

    fig_stack.update_layout(height=400)
    st.plotly_chart(fig_stack, use_container_width=True)

# ======================================================
# FOOT NOTE MINI
# ======================================================

st.caption("Profil responden ditampilkan berdasarkan data survei yang telah difilter.")

# ======================================================
# PART 3 — SMARTPLS + MODEL EVALUATION (UX LEVEL 5)
# ======================================================

st.subheader("📊 SmartPLS Model Evaluation")
st.markdown("Evaluasi model struktural & pengujian hipotesis penelitian.")

st.markdown("---")

# ======================================================
# KPI MODEL QUALITY (FAST VIEW)
# ======================================================

q1, q2, q3 = st.columns(3)

q1.metric("Reliabilitas Model", "Good")
q2.metric("Validitas Konstruk", "Good")
q3.metric("Model Fit", "Acceptable")

st.markdown("---")

# ======================================================
# OUTER LOADING (SIMPLIFIED VISUAL TABLE)
# ======================================================

st.markdown("### 🔗 Outer Loading (Convergent Validity)")

outer_loading = pd.DataFrame({

    "Indikator":[
        "Algoritma (X1.1–X1.5)",
        "Echo Chamber (X2.1–X2.5)",
        "Risiko (Y1–Y5)"
    ],

    "Range Loading":[
        "0.75 – 0.86",
        "0.71 – 0.82",
        "0.71 – 0.89"
    ],

    "Status":[
        "Valid",
        "Valid",
        "Valid"
    ]
})

st.dataframe(outer_loading, use_container_width=True)

st.success("Semua indikator memenuhi validitas konvergen (outer loading > 0.70).")

st.markdown("---")

# ======================================================
# RELIABILITY & VALIDITY (CLEAN DASHBOARD TABLE)
# ======================================================

st.markdown("### 🧪 Construct Reliability & Validity")

construct = pd.DataFrame({

    "Konstruk":[
        "Algoritma Rekomendasi",
        "Echo Chamber",
        "Risiko Adiksi Digital"
    ],

    "Cronbach Alpha":[0.877, 0.777, 0.879],
    "Composite Reliability":[0.904, 0.855, 0.911],
    "AVE":[0.653, 0.597, 0.672],

    "Status":[
        "Reliable",
        "Reliable",
        "Reliable"
    ]
})

st.dataframe(construct, use_container_width=True)

st.success("Semua konstruk memenuhi reliabilitas dan validitas (CR > 0.70, AVE > 0.50).")

st.markdown("---")

# ======================================================
# HYPOTHESIS RESULT (CARD STYLE UX)
# ======================================================

st.markdown("### 🧠 Hasil Uji Hipotesis")

h1, h2 = st.columns(2)

with h1:

    st.error("""
    ❌ Algoritma Rekomendasi → Risiko Adiksi

    Tidak signifikan

    P-value: 0.600
    T-stat: 0.524
    """)

with h2:

    st.success("""
    ✅ Echo Chamber → Risiko Adiksi

    Signifikan

    P-value: 0.000
    T-stat: 4.114
    """)

st.markdown("---")

# ======================================================
# MINI PATH INSIGHT (VISUAL SUMMARY)
# ======================================================

st.markdown("### 📌 Model Insight Summary")

i1, i2, i3 = st.columns(3)

i1.metric("Faktor Terkuat", "Echo Chamber")
i2.metric("Faktor Lemah", "Algoritma")
i3.metric("Arah Pengaruh", "Positive Effect")

st.markdown("---")

# ======================================================
# MITIGATION STRATEGY (CLEAN TABLE UX)
# ======================================================

st.markdown("### 🛡️ Rekomendasi Mitigasi")

mitigasi = pd.DataFrame({

    "Area":[
        "Echo Chamber",
        "Paparan Informasi Seragam",
        "Durasi Penggunaan",
        "Literasi Digital",
        "Kesadaran Pengguna"
    ],

    "Strategi":[
        "Diversifikasi konten",
        "Rekomendasi sumber berbeda",
        "Screen time control",
        "Edukasi digital",
        "Dashboard monitoring"
    ],

    "Dampak":[
        "Mengurangi bias informasi",
        "Meningkatkan variasi konten",
        "Mengontrol penggunaan",
        "Meningkatkan literasi",
        "Meningkatkan awareness"
    ]
})

st.dataframe(mitigasi, use_container_width=True)

st.markdown("---")

# ======================================================
# FINAL INSIGHT (VERY IMPORTANT UX SECTION)
# ======================================================

st.markdown("### ⚡ Key Research Insight")

st.info("""
Hasil penelitian menunjukkan bahwa Echo Chamber merupakan faktor utama yang berpengaruh terhadap risiko adiksi digital Instagram, 
sedangkan algoritma rekomendasi tidak menunjukkan pengaruh signifikan.

Ini mengindikasikan bahwa pola konsumsi informasi (bukan hanya sistem algoritma) menjadi faktor dominan dalam perilaku adiktif pengguna.
""")

st.markdown("---")

# ======================================================
# SYSTEM IMPLICATION (FINAL BOX)
# ======================================================

st.success("""
🚀 Implikasi Sistem:

Dashboard ini dapat dikembangkan menjadi sistem monitoring risiko digital berbasis perilaku pengguna untuk:
- Deteksi pola konsumsi informasi
- Monitoring risiko adiksi digital
- Analisis Echo Chamber secara real-time
- Rekomendasi intervensi digital sehat
""")
