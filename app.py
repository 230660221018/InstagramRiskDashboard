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
# CUSTOM CSS (CLEAN UX)
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
    padding:18px;
    border-radius:16px;
    box-shadow:0px 4px 10px rgba(0,0,0,0.06);
    border-left:5px solid #2563eb;
}

.metric-title{
    font-size:13px;
    color:#64748b;
}

.metric-value{
    font-size:28px;
    font-weight:700;
    color:#111827;
}

.small-text{
    font-size:12px;
    color:#94a3b8;
}

</style>
""", unsafe_allow_html=True)

# ======================================================
# LOAD DATASET (SAFE LOADER)
# ======================================================

try:
    try:
        df = pd.read_csv("dataset.csv", encoding="utf-8")
    except:
        df = pd.read_csv("dataset.csv", encoding="latin1")

except:
    st.error("Dataset tidak ditemukan. Pastikan dataset.csv tersedia.")
    st.stop()

# ======================================================
# CLEAN COLUMN
# ======================================================

df.columns = df.columns.str.strip()
df.columns = df.columns.str.replace("\n", " ", regex=True)

# ======================================================
# MODEL VARIABEL PENELITIAN
# ======================================================

X1 = ["X1.1","X1.2","X1.3","X1.4","X1.5"]
X2 = ["X2.1","X2.3","X2.4","X2.5"]
Y  = ["Y1","Y2","Y3","Y4","Y5"]

required_cols = X1 + X2 + Y

missing_cols = [c for c in required_cols if c not in df.columns]

if missing_cols:
    st.error(f"Kolom tidak ditemukan: {missing_cols}")
    st.stop()

# ======================================================
# SKOR VARIABEL
# ======================================================

df["Skor Algoritma"] = df[X1].mean(axis=1)
df["Skor Echo Chamber"] = df[X2].mean(axis=1)
df["Skor Risiko"] = df[Y].mean(axis=1)

# ======================================================
# KATEGORI RISIKO (LOGIC STABLE)
# ======================================================

def kategori_risiko(x):
    if x < 2.61:
        return "Rendah"
    elif x < 3.41:
        return "Sedang"
    else:
        return "Tinggi"

df["Kategori Risiko"] = df["Skor Risiko"].apply(kategori_risiko)

# ======================================================
# HEADER (CLEAR POSITIONING)
# ======================================================

st.title("📱 Instagram Digital Addiction Risk Analytics Dashboard")

st.caption(
    "Analisis hubungan Algoritma Rekomendasi, Echo Chamber, dan Risiko Adiksi Digital"
)

st.markdown("---")

# ======================================================
# RISK INTELLIGENCE ENGINE (ANTI AMBIGUITY CORE)
# ======================================================

mean_risk = df["Skor Risiko"].mean()

risk_dist = df["Kategori Risiko"].value_counts(normalize=True)

dominant_category = df["Kategori Risiko"].value_counts().idxmax()
dominant_percent = risk_dist.max() * 100

low_pct = risk_dist.get("Rendah", 0) * 100
med_pct = risk_dist.get("Sedang", 0) * 100
high_pct = risk_dist.get("Tinggi", 0) * 100

# ======================================================
# KPI CARDS (EXECUTIVE SNAPSHOT)
# ======================================================

c1, c2, c3 = st.columns(3)

with c1:
    st.metric("Total Responden", len(df))

with c2:
    st.metric("Rata-rata Risiko", f"{mean_risk:.2f} / 5")

with c3:
    st.metric("Kategori Dominan", f"{dominant_category} ({dominant_percent:.1f}%)")

st.markdown("---")

# ======================================================
# MAIN INTERPRETATION ENGINE (FIX AMBIGUITY)
# ======================================================

if mean_risk >= 3.41:

    st.error(f"""
### ⚠️ Risiko Tinggi Terdeteksi

- Rata-rata risiko: **{mean_risk:.2f}/5**
- Kategori dominan: **{dominant_category} ({dominant_percent:.1f}%)**
- Distribusi menunjukkan kecenderungan risiko tinggi

**Kesimpulan:** Kondisi menunjukkan risiko adiksi digital yang perlu perhatian serius.
""")

elif mean_risk >= 2.61:

    st.warning(f"""
### ⚠️ Risiko Moderat

- Rata-rata risiko: **{mean_risk:.2f}/5**
- Kategori dominan: **{dominant_category} ({dominant_percent:.1f}%)**
- Terdapat perbedaan antara mean dan distribusi kategori

**Kesimpulan:** Kondisi cukup stabil namun mulai menunjukkan pola risiko digital.
""")

else:

    st.success(f"""
### ✔ Risiko Rendah

- Rata-rata risiko: **{mean_risk:.2f}/5**
- Kategori dominan: **{dominant_category} ({dominant_percent:.1f}%)**

**Kesimpulan:** Risiko adiksi digital masih dalam batas aman.
""")

st.markdown("---")

# ======================================================
# VISUAL SNAPSHOT (LIGHTWEIGHT DASHBOARD VIEW)
# ======================================================

col1, col2 = st.columns(2)

with col1:

    fig1 = px.histogram(
        df,
        x="Skor Risiko",
        nbins=10,
        title="Distribusi Skor Risiko"
    )

    fig1.update_layout(height=380)

    st.plotly_chart(fig1, use_container_width=True)

with col2:

    pie_df = df["Kategori Risiko"].value_counts().reset_index()
    pie_df.columns = ["Kategori Risiko", "Jumlah"]

    fig2 = px.pie(
        pie_df,
        names="Kategori Risiko",
        values="Jumlah",
        hole=0.55,
        title="Distribusi Kategori Risiko"
    )

    fig2.update_layout(height=380)

    st.plotly_chart(fig2, use_container_width=True)

st.markdown("---")

# ======================================================
# INSIGHT PANEL (NO TEXT HEAVY)
# ======================================================

i1, i2, i3 = st.columns(3)

i1.metric("Dominasi Risiko", dominant_category)
i2.metric("Proporsi Dominan", f"{dominant_percent:.1f}%")
i3.metric(
    "Sebaran Data",
    "Seimbang" if max(risk_dist) < 0.6 else "Condong"
)

st.markdown("---")

# ======================================================
# FOOTNOTE (ANTI MISINTERPRETATION)
# ======================================================

st.caption(
    "Dashboard ini menggabungkan mean (rata-rata) dan distribusi kategori untuk menghindari bias interpretasi tunggal."
)

# ======================================================
# PART 2 — PROFIL RESPONDEN (UX LEVEL 5 CLEAN)
# ======================================================

st.subheader("👥 Profil Responden")

st.markdown("Karakteristik responden dalam penelitian ini")

st.markdown("---")

# ======================================================
# INSIGHT ENGINE (AUTO SUMMARY)
# ======================================================

total = len(df)

usia_dominan = df["Usia"].value_counts().idxmax()
usia_pct = df["Usia"].value_counts(normalize=True).max() * 100

gender_dominan = df["Jenis Kelamin"].value_counts().idxmax()
gender_pct = df["Jenis Kelamin"].value_counts(normalize=True).max() * 100

durasi_dominan = df["Rata-rata Durasi Penggunaan Instagram per Hari"].value_counts().idxmax()
durasi_pct = df["Rata-rata Durasi Penggunaan Instagram per Hari"].value_counts(normalize=True).max() * 100

# ======================================================
# KPI MINI INSIGHT (CLEAR + NO NOISE)
# ======================================================

k1, k2, k3 = st.columns(3)

k1.metric("Total Responden", total)

k2.metric(
    "Usia Dominan",
    f"{usia_dominan} ({usia_pct:.1f}%)"
)

k3.metric(
    "Gender Dominan",
    f"{gender_dominan} ({gender_pct:.1f}%)"
)

st.markdown("---")

# ======================================================
# VISUAL 1 — USIA & GENDER
# ======================================================

col1, col2 = st.columns(2)

with col1:

    usia_df = df["Usia"].value_counts().reset_index()
    usia_df.columns = ["Usia", "Jumlah"]

    fig_usia = px.bar(
        usia_df,
        x="Usia",
        y="Jumlah",
        text_auto=True,
        title="Distribusi Usia Responden"
    )

    fig_usia.update_layout(height=400)

    st.plotly_chart(fig_usia, use_container_width=True)

with col2:

    gender_df = df["Jenis Kelamin"].value_counts().reset_index()
    gender_df.columns = ["Jenis Kelamin", "Jumlah"]

    fig_gender = px.pie(
        gender_df,
        names="Jenis Kelamin",
        values="Jumlah",
        hole=0.55,
        title="Komposisi Gender"
    )

    fig_gender.update_layout(height=400)

    st.plotly_chart(fig_gender, use_container_width=True)

st.markdown("---")

# ======================================================
# VISUAL 2 — DURASI PENGGUNAAN
# ======================================================

durasi_df = df[
    "Rata-rata Durasi Penggunaan Instagram per Hari"
].value_counts().reset_index()

durasi_df.columns = ["Durasi", "Jumlah"]

fig_durasi = px.bar(
    durasi_df,
    x="Durasi",
    y="Jumlah",
    text_auto=True,
    title="Durasi Penggunaan Instagram per Hari"
)

fig_durasi.update_layout(height=420)

st.plotly_chart(fig_durasi, use_container_width=True)

st.markdown("---")

# ======================================================
# INSIGHT LAYER (ANTI BIAS INTERPRETATION)
# ======================================================

st.markdown("### ⚡ Insight Profil Responden")

i1, i2, i3 = st.columns(3)

i1.metric(
    "Kelompok Terbesar",
    usia_dominan
)

i2.metric(
    "Dominasi Gender",
    gender_dominan
)

i3.metric(
    "Pola Durasi",
    "Mayoritas Moderat" if durasi_pct < 60 else "Dominasi Tinggi"
)

st.markdown("---")

# ======================================================
# DISTRIBUSI RINGKAS (VALIDATION CHECK)
# ======================================================

col1, col2 = st.columns(2)

with col1:

    fig_risk = px.histogram(
        df,
        x="Skor Risiko",
        nbins=10,
        title="Sebaran Risiko Adiksi Digital"
    )

    fig_risk.update_layout(height=380)

    st.plotly_chart(fig_risk, use_container_width=True)

with col2:

    risk_dist = df["Kategori Risiko"].value_counts().reset_index()
    risk_dist.columns = ["Kategori Risiko", "Jumlah"]

    fig_risk_pie = px.pie(
        risk_dist,
        names="Kategori Risiko",
        values="Jumlah",
        hole=0.55,
        title="Kategori Risiko"
    )

    fig_risk_pie.update_layout(height=380)

    st.plotly_chart(fig_risk_pie, use_container_width=True)

st.markdown("---")

# ======================================================
# FINAL SUMMARY (SINGLE LINE INSIGHT)
# ======================================================

st.info(
    f"""
    Profil responden menunjukkan dominasi kelompok {usia_dominan} dengan gender {gender_dominan}.
    Distribusi ini menunjukkan bahwa sampel cukup terpusat pada kelompok tertentu,
    sehingga interpretasi hasil perlu mempertimbangkan karakteristik demografis ini.
    """
)

# ======================================================
# PART 3 — SMARTPLS (UX LEVEL 6 ACADEMIC ENGINE)
# ======================================================

with tabs[3]:

    st.subheader("📊 Evaluasi Model SmartPLS")

    st.markdown(
        "Evaluasi model pengukuran dan struktural dalam penelitian."
    )

    st.markdown("---")

    # ======================================================
    # INTERPRETATION ENGINE (AUTO LOGIC)
    # ======================================================

    alg_to_risk_p = 0.600
    echo_to_risk_p = 0.000

    alg_significant = alg_to_risk_p < 0.05
    echo_significant = echo_to_risk_p < 0.05

    # ======================================================
    # MODEL SUMMARY CARD (CLEAR MESSAGE)
    # ======================================================

    if echo_significant and not alg_significant:

        st.success(
            """
### ✔ Hasil Model Struktural

- Echo Chamber → Risiko Adiksi: **Signifikan**
- Algoritma Rekomendasi → Risiko Adiksi: **Tidak Signifikan**

**Kesimpulan utama:**
Echo Chamber merupakan faktor dominan dalam meningkatkan risiko adiksi digital.
"""
        )

    elif echo_significant and alg_significant:

        st.warning(
            """
### ⚠ Hasil Model Struktural

- Kedua variabel memiliki pengaruh signifikan

**Kesimpulan:**
Baik algoritma maupun echo chamber berkontribusi terhadap risiko adiksi digital.
"""
        )

    else:

        st.error(
            """
### ✖ Hasil Model Struktural

- Tidak ditemukan pengaruh signifikan yang kuat

**Kesimpulan:**
Model belum menunjukkan hubungan struktural yang kuat.
"""
        )

    st.markdown("---")

    # ======================================================
    # OUTER LOADING
    # ======================================================

    st.markdown("### 🔎 Outer Loading (Validitas Konvergen)")

    outer_loading = pd.DataFrame({

        "Indikator":[
            "X1.1","X1.2","X1.3","X1.4","X1.5",
            "X2.1","X2.3","X2.4","X2.5",
            "Y1","Y2","Y3","Y4","Y5"
        ],

        "Loading":[
            0.860,0.757,0.750,0.868,0.798,
            0.816,0.757,0.712,0.802,
            0.820,0.891,0.783,0.718,0.874
        ]
    })

    st.dataframe(outer_loading, use_container_width=True)

    st.info(
        "Seluruh indikator berada di atas batas 0.70 sehingga validitas konvergen terpenuhi."
    )

    st.markdown("---")

    # ======================================================
    # RELIABILITY TABLE
    # ======================================================

    st.markdown("### 📦 Construct Reliability & Validity")

    construct = pd.DataFrame({

        "Konstruk":[
            "Algoritma Rekomendasi",
            "Echo Chamber",
            "Risiko Adiksi Digital"
        ],

        "Cronbach Alpha":[0.877,0.777,0.879],

        "Composite Reliability":[0.904,0.855,0.911],

        "AVE":[0.653,0.597,0.672]
    })

    st.dataframe(construct, use_container_width=True)

    st.success(
        "Model memenuhi standar reliabilitas (CR > 0.70) dan validitas (AVE > 0.50)."
    )

    st.markdown("---")

    # ======================================================
    # VISUAL HIGHLIGHT (NO OVERLOAD)
    # ======================================================

    col1, col2 = st.columns(2)

    with col1:

        fig_outer = px.bar(
            outer_loading,
            x="Indikator",
            y="Loading",
            title="Outer Loading"
        )

        fig_outer.update_layout(height=400)

        st.plotly_chart(fig_outer, use_container_width=True)

    with col2:

        fig_construct = px.bar(
            construct,
            x="Konstruk",
            y="Composite Reliability",
            text_auto=".3f",
            title="Composite Reliability"
        )

        fig_construct.update_layout(height=400)

        st.plotly_chart(fig_construct, use_container_width=True)

    st.markdown("---")

    # ======================================================
    # HYPOTHESIS ENGINE (INTELLIGENT INTERPRETATION)
    # ======================================================

    st.markdown("### 🧪 Uji Hipotesis")

    hypothesis = pd.DataFrame({

        "Hubungan":[
            "Algoritma → Risiko Adiksi",
            "Echo Chamber → Risiko Adiksi"
        ],

        "P Value":[0.600,0.000],

        "Status":[
            "Tidak Signifikan",
            "Signifikan"
        ]
    })

    st.dataframe(hypothesis, use_container_width=True)

    st.markdown("---")

    # ======================================================
    # AUTO NARRATIVE (INI YANG MEMBEDAKAN UX LEVEL 6)
    # ======================================================

    st.markdown("### 📌 Interpretasi Akademik Otomatis")

    st.info(
        f"""
- Pengaruh algoritma terhadap risiko adiksi **tidak signifikan (p = {alg_to_risk_p})**
- Pengaruh echo chamber terhadap risiko adiksi **signifikan (p = {echo_to_risk_p})**

👉 Artinya, perilaku adiksi digital lebih dipengaruhi oleh *lingkungan informasi yang homogen* dibandingkan mekanisme algoritma itu sendiri.

👉 Temuan ini menunjukkan bahwa faktor sosial-kognitif lebih dominan dibanding faktor teknis platform.
"""
    )

    st.markdown("---")

    # ======================================================
    # FINAL CONCLUSION BLOCK (READY FOR SCRAPING BAB 4)
    # ======================================================

    st.success(
        """
### 🧠 Kesimpulan Model

Model penelitian menunjukkan bahwa:

- Echo Chamber merupakan variabel utama yang memengaruhi risiko adiksi digital
- Algoritma rekomendasi tidak memberikan pengaruh signifikan
- Model memiliki validitas dan reliabilitas yang baik

Kesimpulan ini dapat digunakan langsung sebagai dasar pembahasan Bab IV.
"""
    )
