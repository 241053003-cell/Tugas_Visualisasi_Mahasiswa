import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

# ============================================================
# KONFIGURASI HALAMAN
# ============================================================
st.set_page_config(
    page_title="Dashboard Profil Mahasiswa",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================
# CUSTOM CSS - DESAIN MODERN
# ============================================================
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap');
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

    html, body, [class*="css"] {
        font-family: 'Poppins', 'Inter', sans-serif;
    }

    .stApp {
        background: linear-gradient(135deg, #f5f7fa 0%, #e8ecf3 100%);
    }

    /* ============ HERO SECTION ============ */
    .hero-section {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 50%, #6b8dd6 100%);
        padding: 40px 50px;
        border-radius: 24px;
        color: white;
        margin-bottom: 30px;
        box-shadow: 0 20px 40px rgba(102, 126, 234, 0.25);
        position: relative;
        overflow: hidden;
    }
    .hero-section::before {
        content: '';
        position: absolute;
        top: -50%; right: -10%;
        width: 300px; height: 300px;
        background: rgba(255, 255, 255, 0.1);
        border-radius: 50%;
    }
    .hero-section::after {
        content: '';
        position: absolute;
        bottom: -60%; right: 10%;
        width: 200px; height: 200px;
        background: rgba(255, 255, 255, 0.08);
        border-radius: 50%;
    }
    .hero-title {
        font-size: 40px; font-weight: 700; margin: 0;
        letter-spacing: -0.5px; position: relative; z-index: 1;
    }
    .hero-subtitle {
        font-size: 16px; font-weight: 300; opacity: 0.95;
        margin-top: 8px; position: relative; z-index: 1;
    }
    .hero-badge {
        display: inline-block;
        background: rgba(255, 255, 255, 0.2);
        padding: 5px 14px; border-radius: 20px;
        font-size: 12px; font-weight: 500;
        margin-bottom: 12px; backdrop-filter: blur(10px);
        position: relative; z-index: 1;
    }

    /* ============ KPI CARDS ============ */
    .kpi-card {
        background: white;
        padding: 24px 22px;
        border-radius: 18px;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.06);
        border: 1px solid rgba(102, 126, 234, 0.1);
        transition: all 0.3s ease;
        position: relative; overflow: hidden;
        height: 100%;
    }
    .kpi-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 12px 30px rgba(102, 126, 234, 0.2);
    }
    .kpi-card::before {
        content: '';
        position: absolute;
        top: 0; left: 0;
        width: 5px; height: 100%;
        border-radius: 5px 0 0 5px;
    }
    .kpi-card.card-1::before { background: linear-gradient(180deg, #667eea, #764ba2); }
    .kpi-card.card-2::before { background: linear-gradient(180deg, #f093fb, #f5576c); }
    .kpi-card.card-3::before { background: linear-gradient(180deg, #4facfe, #00f2fe); }
    .kpi-card.card-4::before { background: linear-gradient(180deg, #43e97b, #38f9d7); }

    .kpi-icon { font-size: 28px; margin-bottom: 10px; }
    .kpi-label {
        font-size: 13px; color: #8892b0;
        font-weight: 500; text-transform: uppercase;
        letter-spacing: 1px; margin-bottom: 6px;
    }
    .kpi-value {
        font-size: 32px; font-weight: 700; color: #1a202c;
        letter-spacing: -0.5px; line-height: 1.1;
    }
    .kpi-unit {
        font-size: 14px; color: #8892b0;
        font-weight: 400; margin-left: 4px;
    }

    /* ============ SECTION TITLE ============ */
    .section-title {
        font-size: 22px; font-weight: 600; color: #1a202c;
        margin: 30px 0 8px 0; padding-left: 14px;
        border-left: 4px solid #667eea; line-height: 1.2;
    }
    .section-subtitle {
        font-size: 13px; color: #8892b0;
        font-weight: 400; margin-top: 4px;
        padding-left: 18px; margin-bottom: 18px;
    }

    /* ============ SIDEBAR ============ */
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #1e293b 0%, #334155 100%);
    }
    section[data-testid="stSidebar"] * {
        color: #e2e8f0 !important;
    }
    section[data-testid="stSidebar"] .stMultiSelect label,
    section[data-testid="stSidebar"] .stSlider label {
        color: #cbd5e1 !important;
        font-weight: 500; font-size: 13px;
    }

    /* ============ CHART CONTAINER ============ */
    .chart-container {
        background: white;
        padding: 20px;
        border-radius: 18px;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.06);
        border: 1px solid rgba(102, 126, 234, 0.08);
        margin-bottom: 20px;
    }
    .chart-title {
        font-size: 16px; font-weight: 600;
        color: #1a202c; margin-bottom: 4px;
    }
    .chart-desc {
        font-size: 12px; color: #8892b0;
        margin-bottom: 14px;
    }

    /* ============ EXPLANATION BOX ============ */
    .explain-box {
        background: linear-gradient(135deg, #eef2ff 0%, #e0e7ff 100%);
        border-left: 4px solid #667eea;
        padding: 16px 20px;
        border-radius: 12px;
        margin: 12px 0 20px 0;
        font-size: 13.5px;
        color: #334155;
        line-height: 1.7;
    }
    .explain-box b { color: #4338ca; }
    .explain-box code {
        background: white;
        padding: 2px 6px;
        border-radius: 4px;
        font-size: 12px;
        color: #dc2626;
    }

    .insight-box {
        background: linear-gradient(135deg, #ecfdf5 0%, #d1fae5 100%);
        border-left: 4px solid #10b981;
        padding: 16px 20px;
        border-radius: 12px;
        margin: 12px 0;
        font-size: 13.5px;
        color: #064e3b;
        line-height: 1.7;
    }

    .warn-box {
        background: linear-gradient(135deg, #fef3c7 0%, #fde68a 100%);
        border-left: 4px solid #f59e0b;
        padding: 16px 20px;
        border-radius: 12px;
        margin: 12px 0;
        font-size: 13.5px;
        color: #78350f;
        line-height: 1.7;
    }

    /* ============ DATA DICTIONARY TABLE ============ */
    .dict-table {
        width: 100%;
        border-collapse: collapse;
        font-size: 13px;
        background: white;
        border-radius: 12px;
        overflow: hidden;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.06);
    }
    .dict-table th {
        background: linear-gradient(135deg, #667eea, #764ba2);
        color: white;
        padding: 12px 16px;
        text-align: left;
        font-weight: 600;
        font-size: 12px;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    .dict-table td {
        padding: 12px 16px;
        border-bottom: 1px solid #f0f0f0;
        color: #334155;
    }
    .dict-table tr:last-child td { border-bottom: none; }
    .dict-table tr:hover td { background: #f8fafc; }
    .badge {
        display: inline-block;
        padding: 3px 10px;
        border-radius: 20px;
        font-size: 11px;
        font-weight: 600;
    }
    .badge-nominal { background: #dbeafe; color: #1e40af; }
    .badge-ordinal { background: #ede9fe; color: #6d28d9; }
    .badge-kontinu { background: #fee2e2; color: #b91c1c; }
    .badge-diskrit { background: #fef3c7; color: #92400e; }

    /* ============ FOOTER ============ */
    .footer {
        text-align: center;
        padding: 30px 0 10px 0;
        color: #8892b0;
        font-size: 13px;
        border-top: 1px solid #e2e8f0;
        margin-top: 40px;
    }

    .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
    }
</style>
""", unsafe_allow_html=True)

# ============================================================
# GENERATE DATA
# ============================================================
@st.cache_data
def generate_data(n_samples=1000):
    np.random.seed(42)
    jurusan_list = ['Sistem Informasi', 'Manajemen', 'Akuntansi', 'Ilmu Komunikasi']
    prob_jurusan = [0.35, 0.30, 0.20, 0.15]
    jurusan = np.random.choice(jurusan_list, n_samples, p=prob_jurusan)
    semester = np.random.randint(1, 9, n_samples)
    base_ipk = np.random.normal(3.2, 0.4, n_samples)
    jurusan_effect = {'Sistem Informasi': 0.1, 'Manajemen': -0.05, 'Akuntansi': 0.05, 'Ilmu Komunikasi': 0.0}
    ipk = base_ipk + [jurusan_effect[j] for j in jurusan]
    ipk = np.clip(ipk, 2.0, 4.0)
    ipk = np.round(ipk, 2)
    usia = np.random.normal(20, 1.5, n_samples).astype(int)
    usia = np.clip(usia, 17, 25)
    df = pd.DataFrame({
        'Jurusan': jurusan,
        'Semester': semester,
        'IPK': ipk,
        'Usia': usia
    })
    return df

df = generate_data()

# ============================================================
# PALET WARNA
# ============================================================
COLOR_PALETTE = ['#667eea', '#f5576c', '#4facfe', '#43e97b']
GRADIENT_BLUE = ['#e0e7ff', '#c7d2fe', '#a5b4fc', '#818cf8', '#6366f1', '#4f46e5']

# ============================================================
# SIDEBAR
# ============================================================
with st.sidebar:
    st.markdown("""
        <div style='text-align: center; padding: 10px 0 20px 0;'>
            <div style='font-size: 42px;'>🎓</div>
            <h2 style='font-size: 20px; margin: 8px 0 0 0; font-weight: 600;'>Filter Data</h2>
            <p style='font-size: 12px; opacity: 0.7; margin-top: 4px;'>Sesuaikan data yang ingin Anda lihat</p>
        </div>
    """, unsafe_allow_html=True)
    st.markdown("---")

    selected_jurusan = st.multiselect(
        "🏫 Pilih Jurusan:",
        options=df['Jurusan'].unique(),
        default=df['Jurusan'].unique()
    )

    selected_semester = st.slider(
        "📚 Rentang Semester:",
        min_value=int(df['Semester'].min()),
        max_value=int(df['Semester'].max()),
        value=(int(df['Semester'].min()), int(df['Semester'].max()))
    )

    st.markdown("---")
    st.markdown("""
        <div style='background: rgba(102, 126, 234, 0.15); padding: 14px; border-radius: 12px; margin-top: 10px;'>
            <p style='font-size: 12px; margin: 0; line-height: 1.6;'>
                💡 <b>Tips:</b> Gunakan filter di atas untuk mengeksplorasi data. Semua grafik akan menyesuaikan secara otomatis.
            </p>
        </div>
    """, unsafe_allow_html=True)

# Filter data
df_filtered = df[
    (df['Jurusan'].isin(selected_jurusan)) & 
    (df['Semester'].between(selected_semester[0], selected_semester[1]))
]

# ============================================================
# HERO SECTION
# ============================================================
st.markdown("""
    <div class='hero-section'>
        <div class='hero-badge'>📊 VISUALISASI DATA • PERTEMUAN 2</div>
        <h1 class='hero-title'>Dashboard Profil Mahasiswa</h1>
        <p class='hero-subtitle'>Analisis interaktif tipe data dan visualisasi untuk 1.000 sampel mahasiswa</p>
    </div>
""", unsafe_allow_html=True)

# ============================================================
# KPI CARDS
# ============================================================
total_mhs = len(df_filtered)
avg_ipk = df_filtered['IPK'].mean() if total_mhs > 0 else 0
avg_usia = df_filtered['Usia'].mean() if total_mhs > 0 else 0
top_jurusan = df_filtered['Jurusan'].mode()[0] if total_mhs > 0 else "-"

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown(f"""
        <div class='kpi-card card-1'>
            <div class='kpi-icon'>👥</div>
            <div class='kpi-label'>Total Mahasiswa</div>
            <div class='kpi-value'>{total_mhs:,}<span class='kpi-unit'>orang</span></div>
        </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
        <div class='kpi-card card-2'>
            <div class='kpi-icon'>🎯</div>
            <div class='kpi-label'>Rata-rata IPK</div>
            <div class='kpi-value'>{avg_ipk:.2f}<span class='kpi-unit'>/ 4.00</span></div>
        </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
        <div class='kpi-card card-3'>
            <div class='kpi-icon'>🎂</div>
            <div class='kpi-label'>Rata-rata Usia</div>
            <div class='kpi-value'>{avg_usia:.1f}<span class='kpi-unit'>tahun</span></div>
        </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown(f"""
        <div class='kpi-card card-4'>
            <div class='kpi-icon'>🏆</div>
            <div class='kpi-label'>Jurusan Terbanyak</div>
            <div class='kpi-value' style='font-size: 18px; margin-top: 8px;'>{top_jurusan}</div>
        </div>
    """, unsafe_allow_html=True)

# ============================================================
# DATA DICTIONARY
# ============================================================
st.markdown("<div class='section-title'>📖 Kamus Data (Data Dictionary)</div>", unsafe_allow_html=True)
st.markdown("<div class='section-subtitle'>Penjelasan setiap kolom, tipe data, dan visualisasi yang direkomendasikan</div>", unsafe_allow_html=True)

st.markdown("""
    <div class='explain-box'>
        <b>Tentang Dataset:</b> Dataset ini berisi 1.000 profil mahasiswa dari 4 jurusan yang berbeda. 
        Setiap baris merepresentasikan satu mahasiswa dengan 4 atribut: <code>Jurusan</code>, <code>Semester</code>, <code>IPK</code>, dan <code>Usia</code>. 
        Pemilihan tipe data dan visualisasi mengikuti teori <b>Skala Stevens (1946)</b> yang dibahas pada Pertemuan 2.
    </div>
""", unsafe_allow_html=True)

st.markdown("""
<table class='dict-table'>
    <thead>
        <tr>
            <th>Kolom</th>
            <th>Tipe Data</th>
            <th>Sub-Tipe (Skala)</th>
            <th>Deskripsi</th>
            <th>Contoh Nilai</th>
            <th>Visualisasi</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td><b>Jurusan</b></td>
            <td>Kategorik</td>
            <td><span class='badge badge-nominal'>Nominal</span></td>
            <td>Nama program studi mahasiswa. Hanya label, tidak ada urutan.</td>
            <td>Sistem Informasi, Manajemen</td>
            <td>Bar Chart, Pie Chart</td>
        </tr>
        <tr>
            <td><b>Semester</b></td>
            <td>Kategorik</td>
            <td><span class='badge badge-ordinal'>Ordinal</span></td>
            <td>Tingkat semester (1–8). Memiliki urutan tapi jarak antar semester tidak selalu sama.</td>
            <td>1, 2, 3, ..., 8</td>
            <td>Bar Chart Berurutan</td>
        </tr>
        <tr>
            <td><b>IPK</b></td>
            <td>Numerik</td>
            <td><span class='badge badge-kontinu'>Kontinu (Rasio)</span></td>
            <td>Indeks Prestasi Kumulatif. Nilai desimal 2.00–4.00 dengan nol absolut.</td>
            <td>3.45, 3.72, 2.89</td>
            <td>Histogram, Box Plot</td>
        </tr>
        <tr>
            <td><b>Usia</b></td>
            <td>Numerik</td>
            <td><span class='badge badge-kontinu'>Kontinu (Rasio)</span></td>
            <td>Usia mahasiswa dalam tahun. Rentang 17–25 tahun.</td>
            <td>18, 19, 20, 21</td>
            <td>Histogram, Scatter Plot</td>
        </tr>
    </tbody>
</table>
""", unsafe_allow_html=True)

st.markdown("""
    <div class='warn-box'>
        ⚠️ <b>Catatan Penting:</b> Data ini adalah <b>data sintesis</b> (dibuat dengan Python menggunakan distribusi normal) untuk keperluan pembelajaran. 
        Distribusinya dirancang menyerupai data nyata, dengan rata-rata IPK ≈ 3.2 dan usia ≈ 20 tahun.
    </div>
""", unsafe_allow_html=True)

# ============================================================
# SECTION 1: KATEGORIK
# ============================================================
st.markdown("<div class='section-title'>📊 Analisis Data Kategorik</div>", unsafe_allow_html=True)
st.markdown("<div class='section-subtitle'>Data kategorik adalah data yang merepresentasikan kelompok atau label. Tidak bisa dihitung secara matematis.</div>", unsafe_allow_html=True)

col_a, col_b = st.columns(2)

with col_a:
    st.markdown("""
        <div class='chart-container'>
            <div class='chart-title'>1. Distribusi per Jurusan</div>
            <div class='chart-desc'>Tipe: Kategorik Nominal • Visualisasi: Bar Chart</div>
        </div>
    """, unsafe_allow_html=True)
    jurusan_counts = df_filtered['Jurusan'].value_counts().reset_index()
    jurusan_counts.columns = ['Jurusan', 'Jumlah']
    fig_jurusan = px.bar(
        jurusan_counts, x='Jurusan', y='Jumlah',
        color='Jurusan', text='Jumlah',
        color_discrete_sequence=COLOR_PALETTE
    )
    fig_jurusan.update_traces(
        textposition='outside', textfont_size=13,
        marker_line_width=0,
        hovertemplate='<b>%{x}</b><br>Jumlah: %{y} mahasiswa<extra></extra>'
    )
    fig_jurusan.update_layout(
        showlegend=False,
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(family='Poppins', size=12, color='#1a202c'),
        margin=dict(t=20, b=20, l=20, r=20),
        height=340,
        xaxis=dict(showgrid=False, title=None),
        yaxis=dict(showgrid=True, gridcolor='#f0f0f0', title=None)
    )
    st.plotly_chart(fig_jurusan, use_container_width=True, config={'displayModeBar': False})

    # Penjelasan chart
    top_j = jurusan_counts.iloc[0]['Jurusan'] if len(jurusan_counts) > 0 else "-"
    top_n = jurusan_counts.iloc[0]['Jumlah'] if len(jurusan_counts) > 0 else 0
    pct = (top_n / total_mhs * 100) if total_mhs > 0 else 0
    st.markdown(f"""
        <div class='explain-box'>
            <b>Cara Membaca:</b> Setiap batang mewakili satu jurusan. Semakin tinggi batangnya, semakin banyak mahasiswa di jurusan tersebut.<br>
            <b>Insight:</b> Jurusan <b>{top_j}</b> adalah yang terbanyak dengan <b>{top_n} mahasiswa</b> ({pct:.1f}% dari total). 
            Hal ini masuk akal karena pada pembuatan data, jurusan Sistem Informasi diberi probabilitas tertinggi (35%).
        </div>
    """, unsafe_allow_html=True)

with col_b:
    st.markdown("""
        <div class='chart-container'>
            <div class='chart-title'>2. Distribusi per Semester</div>
            <div class='chart-desc'>Tipe: Kategorik Ordinal • Visualisasi: Bar Chart Berurutan</div>
        </div>
    """, unsafe_allow_html=True)
    semester_counts = df_filtered['Semester'].value_counts().sort_index().reset_index()
    semester_counts.columns = ['Semester', 'Jumlah']
    fig_semester = px.bar(
        semester_counts, x='Semester', y='Jumlah',
        text='Jumlah', color='Jumlah',
        color_continuous_scale=GRADIENT_BLUE
    )
    fig_semester.update_traces(
        textposition='outside', textfont_size=13,
        marker_line_width=0,
        hovertemplate='<b>Semester %{x}</b><br>Jumlah: %{y} mahasiswa<extra></extra>'
    )
    fig_semester.update_layout(
        showlegend=False, coloraxis_showscale=False,
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(family='Poppins', size=12, color='#1a202c'),
        margin=dict(t=20, b=20, l=20, r=20),
        height=340,
        xaxis=dict(showgrid=False, title=None, dtick=1),
        yaxis=dict(showgrid=True, gridcolor='#f0f0f0', title=None)
    )
    st.plotly_chart(fig_semester, use_container_width=True, config={'displayModeBar': False})

    # Penjelasan chart
    if len(semester_counts) > 0:
        top_sem = semester_counts.loc[semester_counts['Jumlah'].idxmax()]
        st.markdown(f"""
            <div class='explain-box'>
                <b>Cara Membaca:</b> Karena semester bersifat <i>ordinal</i>, batang disusun berurutan dari 1 hingga 8. 
                Warna batang merepresentasikan jumlah (semakin gelap = semakin banyak).<br>
                <b>Insight:</b> Semester <b>{int(top_sem['Semester'])}</b> memiliki mahasiswa terbanyak yaitu <b>{int(top_sem['Jumlah'])} orang</b>. 
                Distribusi semester pada dataset ini relatif merata karena dibuat dengan metode acak seragam (<i>uniform random</i>).
            </div>
        """, unsafe_allow_html=True)

# ============================================================
# SECTION 2: NUMERIK
# ============================================================
st.markdown("<div class='section-title'>📈 Analisis Data Numerik</div>", unsafe_allow_html=True)
st.markdown("<div class='section-subtitle'>Data numerik adalah data berupa angka yang bisa dihitung atau diukur secara matematis.</div>", unsafe_allow_html=True)

col_c, col_d = st.columns(2)

with col_c:
    st.markdown("""
        <div class='chart-container'>
            <div class='chart-title'>3. Distribusi IPK</div>
            <div class='chart-desc'>Tipe: Numerik Kontinu • Visualisasi: Histogram + Box Plot</div>
        </div>
    """, unsafe_allow_html=True)
    fig_ipk = px.histogram(
        df_filtered, x='IPK', nbins=30,
        marginal='box',
        color_discrete_sequence=['#667eea']
    )
    fig_ipk.update_traces(
        marker_line_width=0, opacity=0.85,
        hovertemplate='IPK: %{x}<br>Frekuensi: %{y}<extra></extra>'
    )
    fig_ipk.update_layout(
        showlegend=False,
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(family='Poppins', size=12, color='#1a202c'),
        margin=dict(t=20, b=20, l=20, r=20),
        height=380,
        xaxis=dict(showgrid=False, title=None),
        yaxis=dict(showgrid=True, gridcolor='#f0f0f0', title=None)
    )
    st.plotly_chart(fig_ipk, use_container_width=True, config={'displayModeBar': False})

    # Penjelasan chart
    if total_mhs > 0:
        median_ipk = df_filtered['IPK'].median()
        std_ipk = df_filtered['IPK'].std()
        min_ipk = df_filtered['IPK'].min()
        max_ipk = df_filtered['IPK'].max()
        st.markdown(f"""
            <div class='explain-box'>
                <b>Cara Membaca:</b> Sumbu X menunjukkan rentang IPK, sumbu Y menunjukkan berapa banyak mahasiswa di rentang itu. 
                Kotak di atas histogram (box plot) menunjukkan <i>median</i> dan <i>quartile</i>.<br>
                <b>Statistik:</b> Median IPK = <b>{median_ipk:.2f}</b> • Standar deviasi = <b>{std_ipk:.2f}</b> • 
                Nilai minimum = <b>{min_ipk:.2f}</b> • Maksimum = <b>{max_ipk:.2f}</b><br>
                <b>Insight:</b> IPK berdistribusi normal (berbentuk lonceng) dengan puncak di sekitar 3.2–3.3. 
                Artinya mayoritas mahasiswa memiliki IPK di kisaran tersebut.
            </div>
        """, unsafe_allow_html=True)

with col_d:
    st.markdown("""
        <div class='chart-container'>
            <div class='chart-title'>4. Sebaran IPK per Jurusan</div>
            <div class='chart-desc'>Tipe: Numerik Kontinu vs Kategorik • Visualisasi: Box Plot</div>
        </div>
    """, unsafe_allow_html=True)
    fig_box = px.box(
        df_filtered, x='Jurusan', y='IPK',
        color='Jurusan', points='outliers',
        color_discrete_sequence=COLOR_PALETTE
    )
    fig_box.update_traces(marker_line_width=0, line_width=1.5)
    fig_box.update_layout(
        showlegend=False,
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(family='Poppins', size=12, color='#1a202c'),
        margin=dict(t=20, b=20, l=20, r=20),
        height=380,
        xaxis=dict(showgrid=False, title=None),
        yaxis=dict(showgrid=True, gridcolor='#f0f0f0', title=None)
    )
    st.plotly_chart(fig_box, use_container_width=True, config={'displayModeBar': False})

    # Penjelasan chart
    if total_mhs > 0:
        best_j = df_filtered.groupby('Jurusan')['IPK'].mean().idxmax()
        best_i = df_filtered.groupby('Jurusan')['IPK'].mean().max()
        worst_j = df_filtered.groupby('Jurusan')['IPK'].mean().idxmin()
        worst_i = df_filtered.groupby('Jurusan')['IPK'].mean().min()
        st.markdown(f"""
            <div class='explain-box'>
                <b>Cara Membaca:</b> Setiap kotak mewakili sebaran IPK di satu jurusan. 
                Garis tengah di dalam kotak = median. Bagian atas & bawah kotak = kuartil 3 & 1. 
                Titik di luar <i>whisker</i> = <i>outlier</i> (nilai ekstrem).<br>
                <b>Insight:</b> Jurusan <b>{best_j}</b> punya rata-rata IPK tertinggi (<b>{best_i:.2f}</b>), 
                sedangkan <b>{worst_j}</b> terendah (<b>{worst_i:.2f}</b>). 
                Perbedaan ini muncul karena saat pembuatan data, kami menambahkan <i>efek jurusan</i> untuk mensimulasikan variasi nyata.
            </div>
        """, unsafe_allow_html=True)

# ============================================================
# SECTION 3: SCATTER PLOT
# ============================================================
st.markdown("<div class='section-title'>🔍 Eksplorasi Hubungan Antar Variabel</div>", unsafe_allow_html=True)
st.markdown("<div class='section-subtitle'>Melihat apakah ada korelasi antara usia, IPK, dan semester</div>", unsafe_allow_html=True)

st.markdown("""
    <div class='chart-container'>
        <div class='chart-title'>5. Hubungan Usia, IPK, dan Semester</div>
        <div class='chart-desc'>Tipe: 2 Variabel Numerik + 1 Kategorik • Visualisasi: Scatter Plot</div>
    </div>
""", unsafe_allow_html=True)

fig_scatter = px.scatter(
    df_filtered, x='Usia', y='IPK',
    color='Jurusan', size='Semester',
    hover_data=['Semester'],
    color_discrete_sequence=COLOR_PALETTE,
    size_max=20
)
fig_scatter.update_traces(marker=dict(line=dict(width=1, color='white'), opacity=0.75))
fig_scatter.update_layout(
    plot_bgcolor='rgba(0,0,0,0)',
    paper_bgcolor='rgba(0,0,0,0)',
    font=dict(family='Poppins', size=12, color='#1a202c'),
    margin=dict(t=20, b=20, l=20, r=20),
    height=480,
    legend=dict(
        orientation='h', yanchor='bottom', y=1.02,
        xanchor='center', x=0.5,
        bgcolor='rgba(255,255,255,0.8)',
        bordercolor='#e2e8f0', borderwidth=1
    ),
    xaxis=dict(showgrid=True, gridcolor='#f0f0f0', title='Usia (tahun)'),
    yaxis=dict(showgrid=True, gridcolor='#f0f0f0', title='IPK')
)
st.plotly_chart(fig_scatter, use_container_width=True, config={'displayModeBar': False})

if total_mhs > 0:
    corr_usia_ipk = df_filtered[['Usia', 'IPK']].corr().iloc[0, 1]
    corr_sem_ipk = df_filtered[['Semester', 'IPK']].corr().iloc[0, 1]
    corr_sem_usia = df_filtered[['Semester', 'Usia']].corr().iloc[0, 1]

    def interpretasi_corr(val):
        abs_val = abs(val)
        if abs_val < 0.2: return "sangat lemah / tidak ada"
        elif abs_val < 0.4: return "lemah"
        elif abs_val < 0.6: return "sedang"
        elif abs_val < 0.8: return "kuat"
        else: return "sangat kuat"

    st.markdown(f"""
        <div class='explain-box'>
            <b>Cara Membaca:</b> Setiap titik = 1 mahasiswa. Posisi horizontal (X) menunjukkan usia, 
            posisi vertikal (Y) menunjukkan IPK. Ukuran titik merepresentasikan semester. 
            Warna menunjukkan jurusan.<br><br>
            <b>Analisis Korelasi (Pearson):</b><br>
            • Usia ↔ IPK: <b>{corr_usia_ipk:.3f}</b> ({interpretasi_corr(corr_usia_ipk)})<br>
            • Semester ↔ IPK: <b>{corr_sem_ipk:.3f}</b> ({interpretasi_corr(corr_sem_ipk)})<br>
            • Semester ↔ Usia: <b>{corr_sem_usia:.3f}</b> ({interpretasi_corr(corr_sem_usia)})<br><br>
            <b>Insight:</b> Hubungan Usia–IPK sangat lemah, artinya usia tidak terlalu memengaruhi IPK. 
            Sebaliknya, Semester–Usia memiliki korelasi positif yang wajar (semakin tinggi semester, semakin tua usia). 
            Ini membuktikan bahwa IPK lebih ditentukan oleh faktor lain (seperti jurusan), bukan oleh usia.
        </div>
    """, unsafe_allow_html=True)

# ============================================================
# INSIGHT AKHIR
# ============================================================
st.markdown("<div class='section-title'>💡 Kesimpulan Otomatis</div>", unsafe_allow_html=True)
st.markdown("<div class='section-subtitle'>Rangkuman temuan utama berdasarkan data yang sedang difilter</div>", unsafe_allow_html=True)

if total_mhs > 0:
    best_jurusan = df_filtered.groupby('Jurusan')['IPK'].mean().idxmax()
    best_ipk = df_filtered.groupby('Jurusan')['IPK'].mean().max()
    oldest = df_filtered['Usia'].max()
    youngest = df_filtered['Usia'].min()

    st.markdown(f"""
        <div class='insight-box'>
            ✅ Berdasarkan <b>{total_mhs:,} mahasiswa</b> yang lolos filter:<br><br>
            🏆 Jurusan <b>{best_jurusan}</b> memiliki rata-rata IPK tertinggi, yaitu <b>{best_ipk:.2f}</b>.<br>
            🎂 Rentang usia mahasiswa adalah <b>{youngest}–{oldest} tahun</b>, dengan rata-rata <b>{avg_usia:.1f} tahun</b>.<br>
            🎯 Rata-rata IPK keseluruhan adalah <b>{avg_ipk:.2f}</b> dari skala maksimum 4.00.<br>
            📚 Semester yang ditampilkan saat ini: <b>{selected_semester[0]} hingga {selected_semester[1]}</b>.<br><br>
            <b>Rekomendasi:</b> Gunakan filter di sidebar kiri untuk mengeksplorasi kombinasi jurusan dan semester yang berbeda, 
            dan perhatikan bagaimana rata-rata IPK berubah. Ini membantu Anda memahami bahwa <i>kesimpulan data bergantung pada sampel yang dipilih</i>.
        </div>
    """, unsafe_allow_html=True)

# ============================================================
# FOOTER
# ============================================================
st.markdown("""
    <div class='footer'>
        <p style='margin: 0;'>🎓 <b>Dashboard Profil Mahasiswa</b> • Dibuat dengan Streamlit & Plotly</p>
        <p style='margin: 6px 0 0 0; font-size: 12px;'>Bedah Kasus 2 • Visualisasi Data • Program Studi Sistem Informasi</p>
    </div>
""", unsafe_allow_html=True)