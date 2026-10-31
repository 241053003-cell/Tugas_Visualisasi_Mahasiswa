# ============================================================
# DASHBOARD CUACA INDONESIA - STREAMLIT
# Bedah Kasus 3 - Visualisasi Data
# ============================================================
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

# ============================================================
# KONFIGURASI HALAMAN
# ============================================================
st.set_page_config(
    page_title="Dashboard Cuaca Indonesia",
    page_icon="🌤️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================
# CUSTOM CSS - TEMA CUACA
# ============================================================
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap');
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

    html, body, [class*="css"] {
        font-family: 'Poppins', 'Inter', sans-serif;
    }

    .stApp {
        background: linear-gradient(135deg, #e0f2fe 0%, #f0f9ff 50%, #fef3c7 100%);
    }

    /* ============ HERO ============ */
    .hero-section {
        background: linear-gradient(135deg, #0ea5e9 0%, #0284c7 50%, #0369a1 100%);
        padding: 45px 50px;
        border-radius: 24px;
        color: white;
        margin-bottom: 30px;
        box-shadow: 0 20px 45px rgba(14, 165, 233, 0.3);
        position: relative; overflow: hidden;
    }
    .hero-section::before {
        content: '☁️';
        position: absolute;
        top: 10px; right: 40px;
        font-size: 80px;
        opacity: 0.15;
    }
    .hero-section::after {
        content: '🌤️';
        position: absolute;
        bottom: -10px; right: 150px;
        font-size: 60px;
        opacity: 0.12;
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
        background: rgba(255, 255, 255, 0.22);
        padding: 5px 14px; border-radius: 20px;
        font-size: 12px; font-weight: 500;
        margin-bottom: 12px; backdrop-filter: blur(10px);
        position: relative; z-index: 1;
    }

    /* ============ KPI ============ */
    .kpi-card {
        background: white;
        padding: 24px 22px;
        border-radius: 18px;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.06);
        transition: all 0.3s ease;
        position: relative; overflow: hidden;
        height: 100%;
        border: 1px solid rgba(14, 165, 233, 0.1);
    }
    .kpi-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 12px 30px rgba(14, 165, 233, 0.2);
    }
    .kpi-card::before {
        content: '';
        position: absolute;
        top: 0; left: 0;
        width: 5px; height: 100%;
        border-radius: 5px 0 0 5px;
    }
    .kpi-card.card-1::before { background: linear-gradient(180deg, #f97316, #dc2626); }
    .kpi-card.card-2::before { background: linear-gradient(180deg, #0ea5e9, #0369a1); }
    .kpi-card.card-3::before { background: linear-gradient(180deg, #06b6d4, #0891b2); }
    .kpi-card.card-4::before { background: linear-gradient(180deg, #8b5cf6, #6d28d9); }

    .kpi-icon { font-size: 28px; margin-bottom: 10px; }
    .kpi-label {
        font-size: 13px; color: #64748b;
        font-weight: 500; text-transform: uppercase;
        letter-spacing: 1px; margin-bottom: 6px;
    }
    .kpi-value {
        font-size: 32px; font-weight: 700; color: #0f172a;
        letter-spacing: -0.5px; line-height: 1.1;
    }
    .kpi-unit {
        font-size: 14px; color: #64748b;
        font-weight: 400; margin-left: 4px;
    }

    /* ============ SECTION TITLE ============ */
    .section-title {
        font-size: 22px; font-weight: 600; color: #0f172a;
        margin: 30px 0 8px 0; padding-left: 14px;
        border-left: 4px solid #0ea5e9; line-height: 1.2;
    }
    .section-subtitle {
        font-size: 13px; color: #64748b;
        font-weight: 400; margin-top: 4px;
        padding-left: 18px; margin-bottom: 18px;
    }

    /* ============ SIDEBAR ============ */
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0c4a6e 0%, #075985 100%);
    }
    section[data-testid="stSidebar"] * {
        color: #e0f2fe !important;
    }
    section[data-testid="stSidebar"] .stMultiSelect label,
    section[data-testid="stSidebar"] .stSlider label {
        color: #bae6fd !important;
        font-weight: 500; font-size: 13px;
    }

    /* ============ CHART CONTAINER ============ */
    .chart-container {
        background: white;
        padding: 20px;
        border-radius: 18px;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.06);
        border: 1px solid rgba(14, 165, 233, 0.08);
        margin-bottom: 20px;
    }
    .chart-title {
        font-size: 16px; font-weight: 600;
        color: #0f172a; margin-bottom: 4px;
    }
    .chart-desc {
        font-size: 12px; color: #64748b;
        margin-bottom: 14px;
    }

    /* ============ EXPLAIN BOX ============ */
    .explain-box {
        background: linear-gradient(135deg, #eff6ff 0%, #dbeafe 100%);
        border-left: 4px solid #0ea5e9;
        padding: 16px 20px;
        border-radius: 12px;
        margin: 12px 0 20px 0;
        font-size: 13.5px;
        color: #1e3a8a;
        line-height: 1.7;
    }
    .explain-box b { color: #0369a1; }
    .explain-box code {
        background: white; padding: 2px 6px;
        border-radius: 4px; font-size: 12px; color: #dc2626;
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

    /* ============ DATA DICTIONARY ============ */
    .dict-table {
        width: 100%; border-collapse: collapse;
        font-size: 13px; background: white;
        border-radius: 12px; overflow: hidden;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.06);
    }
    .dict-table th {
        background: linear-gradient(135deg, #0ea5e9, #0369a1);
        color: white; padding: 12px 16px;
        text-align: left; font-weight: 600;
        font-size: 12px; text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    .dict-table td {
        padding: 12px 16px;
        border-bottom: 1px solid #f0f0f0;
        color: #334155;
    }
    .dict-table tr:last-child td { border-bottom: none; }
    .dict-table tr:hover td { background: #f0f9ff; }
    .badge {
        display: inline-block;
        padding: 3px 10px;
        border-radius: 20px;
        font-size: 11px;
        font-weight: 600;
    }
    .badge-nominal { background: #dbeafe; color: #1e40af; }
    .badge-interval { background: #fed7aa; color: #9a3412; }
    .badge-rasio { background: #d1fae5; color: #065f46; }

    /* ============ FOOTER ============ */
    .footer {
        text-align: center;
        padding: 30px 0 10px 0;
        color: #64748b;
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
    kota_list = ['Jakarta', 'Bandung', 'Surabaya', 'Medan', 'Yogyakarta']
    prob_kota = [0.30, 0.20, 0.20, 0.15, 0.15]
    kota = np.random.choice(kota_list, n_samples, p=prob_kota)

    # PERBAIKAN: freq='h' huruf kecil
    tanggal = pd.date_range(start='2026-01-01', periods=n_samples, freq='h')
    tanggal = np.random.choice(tanggal, n_samples, replace=False)
    tanggal = pd.to_datetime(tanggal)

    suhu_profile = {
        'Jakarta':    (31.0, 2.0),
        'Bandung':    (22.0, 3.0),
        'Surabaya':   (33.0, 2.5),
        'Medan':      (30.0, 2.5),
        'Yogyakarta': (28.0, 2.5),
    }
    suhu = np.array([np.random.normal(suhu_profile[k][0], suhu_profile[k][1]) for k in kota])
    suhu = np.round(suhu, 1)

    kelembaban_base = 90 - (suhu - 22) * 2
    kelembaban = kelembaban_base + np.random.normal(0, 5, n_samples)
    kelembaban = np.clip(kelembaban, 30, 100)
    kelembaban = np.round(kelembaban).astype(int)

    def tentukan_kondisi(kelembaban_val):
        if kelembaban_val > 85:
            return np.random.choice(['Hujan', 'Berawan'], p=[0.7, 0.3])
        elif kelembaban_val > 70:
            return np.random.choice(['Berawan', 'Cerah', 'Hujan'], p=[0.5, 0.3, 0.2])
        else:
            return np.random.choice(['Cerah', 'Berangin'], p=[0.7, 0.3])

    kondisi = np.array([tentukan_kondisi(k) for k in kelembaban])

    df = pd.DataFrame({
        'Tanggal': tanggal,
        'Kota': kota,
        'Suhu': suhu,
        'Kelembaban': kelembaban,
        'Kondisi': kondisi
    })
    df = df.sort_values('Tanggal').reset_index(drop=True)
    return df

df = generate_data()

# ============================================================
# PALET WARNA
# ============================================================
COLOR_PALETTE = ['#0ea5e9', '#f97316', '#06b6d4', '#8b5cf6', '#10b981']
KONDISI_COLORS = {
    'Cerah': '#fbbf24',
    'Berawan': '#94a3b8',
    'Hujan': '#3b82f6',
    'Berangin': '#06b6d4'
}

# ============================================================
# SIDEBAR
# ============================================================
with st.sidebar:
    st.markdown("""
        <div style='text-align: center; padding: 10px 0 20px 0;'>
            <div style='font-size: 42px;'>🌤️</div>
            <h2 style='font-size: 20px; margin: 8px 0 0 0; font-weight: 600;'>Filter Cuaca</h2>
            <p style='font-size: 12px; opacity: 0.7; margin-top: 4px;'>Sesuaikan data yang ingin Anda lihat</p>
        </div>
    """, unsafe_allow_html=True)
    st.markdown("---")

    selected_kota = st.multiselect(
        "🏙️ Pilih Kota:",
        options=df['Kota'].unique(),
        default=df['Kota'].unique()
    )

    selected_kondisi = st.multiselect(
        "☁️ Pilih Kondisi Cuaca:",
        options=df['Kondisi'].unique(),
        default=df['Kondisi'].unique()
    )

    suhu_range = st.slider(
        "🌡️ Rentang Suhu (°C):",
        min_value=float(df['Suhu'].min()),
        max_value=float(df['Suhu'].max()),
        value=(float(df['Suhu'].min()), float(df['Suhu'].max()))
    )

    st.markdown("---")
    st.markdown("""
        <div style='background: rgba(14, 165, 233, 0.15); padding: 14px; border-radius: 12px; margin-top: 10px;'>
            <p style='font-size: 12px; margin: 0; line-height: 1.6;'>
                💡 <b>Tips:</b> Kombinasikan filter untuk melihat pola cuaca yang lebih spesifik!
            </p>
        </div>
    """, unsafe_allow_html=True)

# Filter
df_filtered = df[
    (df['Kota'].isin(selected_kota)) &
    (df['Kondisi'].isin(selected_kondisi)) &
    (df['Suhu'].between(suhu_range[0], suhu_range[1]))
]

# ============================================================
# HERO
# ============================================================
st.markdown("""
    <div class='hero-section'>
        <div class='hero-badge'>🌤️ VISUALISASI DATA • PERTEMUAN 2</div>
        <h1 class='hero-title'>Dashboard Pengamatan Cuaca Indonesia</h1>
        <p class='hero-subtitle'>Analisis interaktif suhu, kelembaban, dan kondisi cuaca di 5 kota besar Indonesia</p>
    </div>
""", unsafe_allow_html=True)

# ============================================================
# KPI
# ============================================================
total_obs = len(df_filtered)
avg_suhu = df_filtered['Suhu'].mean() if total_obs > 0 else 0
avg_kelembaban = df_filtered['Kelembaban'].mean() if total_obs > 0 else 0
kota_terpanas = df_filtered.groupby('Kota')['Suhu'].mean().idxmax() if total_obs > 0 else "-"

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown(f"""
        <div class='kpi-card card-1'>
            <div class='kpi-icon'>🌡️</div>
            <div class='kpi-label'>Rata-rata Suhu</div>
            <div class='kpi-value'>{avg_suhu:.1f}<span class='kpi-unit'>°C</span></div>
        </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
        <div class='kpi-card card-2'>
            <div class='kpi-icon'>💧</div>
            <div class='kpi-label'>Rata-rata Kelembaban</div>
            <div class='kpi-value'>{avg_kelembaban:.0f}<span class='kpi-unit'>%</span></div>
        </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
        <div class='kpi-card card-3'>
            <div class='kpi-icon'>📍</div>
            <div class='kpi-label'>Total Observasi</div>
            <div class='kpi-value'>{total_obs:,}<span class='kpi-unit'>data</span></div>
        </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown(f"""
        <div class='kpi-card card-4'>
            <div class='kpi-icon'>🔥</div>
            <div class='kpi-label'>Kota Terpanas</div>
            <div class='kpi-value' style='font-size: 20px; margin-top: 8px;'>{kota_terpanas}</div>
        </div>
    """, unsafe_allow_html=True)

# ============================================================
# DATA DICTIONARY
# ============================================================
st.markdown("<div class='section-title'>📖 Kamus Data (Data Dictionary)</div>", unsafe_allow_html=True)
st.markdown("<div class='section-subtitle'>Penjelasan setiap kolom dan tipe data sesuai Skala Stevens (1946)</div>", unsafe_allow_html=True)

st.markdown("""
    <div class='explain-box'>
        <b>Tentang Dataset:</b> Dataset ini berisi 1.000 pengamatan cuaca dari 5 kota besar di Indonesia. 
        Setiap baris adalah satu observasi pada waktu tertentu. Perhatikan <b>perbedaan penting</b> antara Suhu (Interval) dan Kelembaban (Rasio)!
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
            <th>Contoh</th>
            <th>Visualisasi</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td><b>Tanggal</b></td>
            <td>Waktu</td>
            <td><span class='badge badge-interval'>Interval</span></td>
            <td>Waktu pengamatan cuaca dilakukan.</td>
            <td>2026-01-15 14:00</td>
            <td>Line Chart</td>
        </tr>
        <tr>
            <td><b>Kota</b></td>
            <td>Kategorik</td>
            <td><span class='badge badge-nominal'>Nominal</span></td>
            <td>Nama kota lokasi pengamatan. Label tanpa urutan.</td>
            <td>Jakarta, Bandung</td>
            <td>Bar Chart, Pie Chart</td>
        </tr>
        <tr>
            <td><b>Suhu</b></td>
            <td>Numerik</td>
            <td><span class='badge badge-interval'>Interval</span></td>
            <td>Suhu udara dalam °C. <b>0°C bukan berarti "tidak ada suhu"</b>. Operasi + dan - valid, tapi × dan ÷ tidak bermakna.</td>
            <td>32.5, 24.0</td>
            <td>Histogram, Box Plot, Line Chart</td>
        </tr>
        <tr>
            <td><b>Kelembaban</b></td>
            <td>Numerik</td>
            <td><span class='badge badge-rasio'>Rasio</span></td>
            <td>Persentase kelembaban udara. <b>0% berarti benar-benar tidak ada uap air</b>. Semua operasi matematika valid.</td>
            <td>75, 85, 60</td>
            <td>Histogram, Scatter Plot</td>
        </tr>
        <tr>
            <td><b>Kondisi</b></td>
            <td>Kategorik</td>
            <td><span class='badge badge-nominal'>Nominal</span></td>
            <td>Kondisi cuaca saat pengamatan.</td>
            <td>Cerah, Hujan</td>
            <td>Bar Chart, Pie Chart</td>
        </tr>
    </tbody>
</table>
""", unsafe_allow_html=True)

st.markdown("""
    <div class='warn-box'>
        ⚠️ <b>Perbedaan Kunci Interval vs Rasio:</b><br>
        • <b>Suhu (Interval):</b> 20°C <b>BUKAN</b> 2× lebih panas dari 10°C. Yang benar: 20°C adalah 10°C lebih panas dari 10°C.<br>
        • <b>Kelembaban (Rasio):</b> 80% <b>ADALAH</b> 2× lebih lembab dari 40%. Karena ada nol absolut (0% = tidak ada kelembaban sama sekali).
    </div>
""", unsafe_allow_html=True)

# ============================================================
# SECTION 1: KATEGORIK
# ============================================================
st.markdown("<div class='section-title'>🌍 Analisis Data Kategorik</div>", unsafe_allow_html=True)
st.markdown("<div class='section-subtitle'>Distribusi observasi berdasarkan Kota dan Kondisi Cuaca</div>", unsafe_allow_html=True)

col_a, col_b = st.columns(2)

with col_a:
    st.markdown("""
        <div class='chart-container'>
            <div class='chart-title'>1. Distribusi Observasi per Kota</div>
            <div class='chart-desc'>Kategorik Nominal • Bar Chart</div>
        </div>
    """, unsafe_allow_html=True)
    kota_counts = df_filtered['Kota'].value_counts().reset_index()
    kota_counts.columns = ['Kota', 'Jumlah']
    fig_kota = px.bar(
        kota_counts, x='Kota', y='Jumlah',
        color='Kota', text='Jumlah',
        color_discrete_sequence=COLOR_PALETTE
    )
    fig_kota.update_traces(
        textposition='outside', textfont_size=13,
        marker_line_width=0,
        hovertemplate='<b>%{x}</b><br>Jumlah: %{y} observasi<extra></extra>'
    )
    fig_kota.update_layout(
        showlegend=False,
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(family='Poppins', size=12, color='#0f172a'),
        margin=dict(t=20, b=20, l=20, r=20),
        height=340,
        xaxis=dict(showgrid=False, title=None),
        yaxis=dict(showgrid=True, gridcolor='#f0f0f0', title=None)
    )
    st.plotly_chart(fig_kota, use_container_width=True, config={'displayModeBar': False})

    if total_obs > 0:
        top_k = kota_counts.iloc[0]['Kota']
        top_n = kota_counts.iloc[0]['Jumlah']
        pct = top_n / total_obs * 100
        st.markdown(f"""
            <div class='explain-box'>
                <b>Insight:</b> Kota <b>{top_k}</b> memiliki observasi terbanyak 
                (<b>{top_n} data</b>, {pct:.1f}% dari total). Ini karena Jakarta diberi 
                probabilitas 30% saat pembuatan data, mencerminkan bahwa kota besar 
                biasanya memiliki lebih banyak stasiun pengamatan cuaca.
            </div>
        """, unsafe_allow_html=True)

with col_b:
    st.markdown("""
        <div class='chart-container'>
            <div class='chart-title'>2. Distribusi Kondisi Cuaca</div>
            <div class='chart-desc'>Kategorik Nominal • Donut Chart</div>
        </div>
    """, unsafe_allow_html=True)
    kondisi_counts = df_filtered['Kondisi'].value_counts().reset_index()
    kondisi_counts.columns = ['Kondisi', 'Jumlah']
    fig_kondisi = px.pie(
        kondisi_counts, names='Kondisi', values='Jumlah',
        hole=0.5,
        color='Kondisi',
        color_discrete_map=KONDISI_COLORS
    )
    fig_kondisi.update_traces(
        textposition='outside',
        textinfo='label+percent',
        textfont_size=13,
        marker=dict(line=dict(color='white', width=2)),
        hovertemplate='<b>%{label}</b><br>Jumlah: %{value}<br>(%{percent})<extra></extra>'
    )
    fig_kondisi.update_layout(
        showlegend=False,
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(family='Poppins', size=12, color='#0f172a'),
        margin=dict(t=20, b=20, l=20, r=20),
        height=340
    )
    st.plotly_chart(fig_kondisi, use_container_width=True, config={'displayModeBar': False})

    if total_obs > 0:
        top_kon = kondisi_counts.iloc[0]['Kondisi']
        top_kon_n = kondisi_counts.iloc[0]['Jumlah']
        st.markdown(f"""
            <div class='explain-box'>
                <b>Insight:</b> Kondisi <b>{top_kon}</b> paling sering terjadi 
                (<b>{top_kon_n} kali</b>). Pola ini dipengaruhi oleh kelembaban: 
                saat kelembaban > 85%, probabilitas Hujan mencapai 70%.
            </div>
        """, unsafe_allow_html=True)

# ============================================================
# SECTION 2: NUMERIK
# ============================================================
st.markdown("<div class='section-title'>🌡️ Analisis Data Numerik</div>", unsafe_allow_html=True)
st.markdown("<div class='section-subtitle'>Distribusi suhu (Interval) dan kelembaban (Rasio)</div>", unsafe_allow_html=True)

col_c, col_d = st.columns(2)

with col_c:
    st.markdown("""
        <div class='chart-container'>
            <div class='chart-title'>3. Distribusi Suhu</div>
            <div class='chart-desc'>Numerik Interval • Histogram</div>
        </div>
    """, unsafe_allow_html=True)
    fig_suhu = px.histogram(
        df_filtered, x='Suhu', nbins=30,
        marginal='box',
        color_discrete_sequence=['#f97316']
    )
    fig_suhu.update_traces(
        marker_line_width=0, opacity=0.85,
        hovertemplate='Suhu: %{x}°C<br>Frekuensi: %{y}<extra></extra>'
    )
    fig_suhu.update_layout(
        showlegend=False,
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(family='Poppins', size=12, color='#0f172a'),
        margin=dict(t=20, b=20, l=20, r=20),
        height=380,
        xaxis=dict(showgrid=False, title='Suhu (°C)'),
        yaxis=dict(showgrid=True, gridcolor='#f0f0f0', title=None)
    )
    st.plotly_chart(fig_suhu, use_container_width=True, config={'displayModeBar': False})

    if total_obs > 0:
        med = df_filtered['Suhu'].median()
        std = df_filtered['Suhu'].std()
        st.markdown(f"""
            <div class='explain-box'>
                <b>Cara Membaca:</b> Karena Suhu berskala <b>Interval</b>, kita 
                <i>tidak bisa</i> mengatakan "30°C dua kali lebih panas dari 15°C". 
                Tapi kita bisa hitung selisihnya: "15°C lebih panas".<br>
                <b>Statistik:</b> Median = <b>{med:.1f}°C</b> • Standar deviasi = <b>{std:.2f}</b><br>
                <b>Insight:</b> Distribusi suhu bersifat <i>bimodal</i> — ada dua puncak. 
                Puncak pertama di sekitar 22°C (Bandung yang sejuk) dan puncak kedua di 31–33°C 
                (Jakarta, Surabaya, Medan yang panas).
            </div>
        """, unsafe_allow_html=True)

with col_d:
    st.markdown("""
        <div class='chart-container'>
            <div class='chart-title'>4. Distribusi Kelembaban</div>
            <div class='chart-desc'>Numerik Rasio • Histogram</div>
        </div>
    """, unsafe_allow_html=True)
    fig_kelembaban = px.histogram(
        df_filtered, x='Kelembaban', nbins=30,
        marginal='box',
        color_discrete_sequence=['#06b6d4']
    )
    fig_kelembaban.update_traces(
        marker_line_width=0, opacity=0.85,
        hovertemplate='Kelembaban: %{x}%<br>Frekuensi: %{y}<extra></extra>'
    )
    fig_kelembaban.update_layout(
        showlegend=False,
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(family='Poppins', size=12, color='#0f172a'),
        margin=dict(t=20, b=20, l=20, r=20),
        height=380,
        xaxis=dict(showgrid=False, title='Kelembaban (%)'),
        yaxis=dict(showgrid=True, gridcolor='#f0f0f0', title=None)
    )
    st.plotly_chart(fig_kelembaban, use_container_width=True, config={'displayModeBar': False})

    if total_obs > 0:
        med_k = df_filtered['Kelembaban'].median()
        std_k = df_filtered['Kelembaban'].std()
        st.markdown(f"""
            <div class='explain-box'>
                <b>Cara Membaca:</b> Kelembaban berskala <b>Rasio</b>, jadi kita 
                <i>bisa</i> mengatakan "80% adalah 2× lebih lembab dari 40%". 
                Ini karena ada nol absolut (0% = tidak ada uap air).<br>
                <b>Statistik:</b> Median = <b>{med_k:.0f}%</b> • Standar deviasi = <b>{std_k:.2f}</b><br>
                <b>Insight:</b> Kelembaban cenderung tinggi (>70%) karena Indonesia beriklim tropis.
            </div>
        """, unsafe_allow_html=True)

# ============================================================
# SECTION 3: TIME SERIES
# ============================================================
st.markdown("<div class='section-title'>📈 Analisis Time Series</div>", unsafe_allow_html=True)
st.markdown("<div class='section-subtitle'>Tren suhu berdasarkan waktu pengamatan</div>", unsafe_allow_html=True)

st.markdown("""
    <div class='chart-container'>
        <div class='chart-title'>5. Tren Suhu per Kota Sepanjang Waktu</div>
        <div class='chart-desc'>Waktu Interval • Line Chart</div>
    </div>
""", unsafe_allow_html=True)

df_sorted = df_filtered.sort_values('Tanggal')
fig_line = px.line(
    df_sorted, x='Tanggal', y='Suhu',
    color='Kota',
    color_discrete_sequence=COLOR_PALETTE,
    markers=False
)
fig_line.update_traces(line=dict(width=1.5), opacity=0.8)
fig_line.update_layout(
    plot_bgcolor='rgba(0,0,0,0)',
    paper_bgcolor='rgba(0,0,0,0)',
    font=dict(family='Poppins', size=12, color='#0f172a'),
    margin=dict(t=20, b=20, l=20, r=20),
    height=420,
    legend=dict(
        orientation='h', yanchor='bottom', y=1.02,
        xanchor='center', x=0.5,
        bgcolor='rgba(255,255,255,0.8)',
        bordercolor='#e2e8f0', borderwidth=1
    ),
    xaxis=dict(showgrid=True, gridcolor='#f0f0f0', title=None),
    yaxis=dict(showgrid=True, gridcolor='#f0f0f0', title='Suhu (°C)')
)
st.plotly_chart(fig_line, use_container_width=True, config={'displayModeBar': False})

if total_obs > 0:
    st.markdown(f"""
        <div class='explain-box'>
            <b>Cara Membaca:</b> Setiap garis mewakili satu kota. Sumbu Y menunjukkan suhu, 
            sumbu X menunjukkan waktu. Gunakan <i>hover</i> untuk melihat detail waktu tertentu.<br>
            <b>Insight:</b> Bandung (garis paling bawah) konsisten lebih sejuk dari kota lain — 
            ini karena Bandung terletak di dataran tinggi. Surabaya dan Jakarta paling panas sepanjang waktu.
        </div>
    """, unsafe_allow_html=True)

# ============================================================
# SECTION 4: SCATTER
# ============================================================
st.markdown("<div class='section-title'>🔍 Hubungan Suhu vs Kelembaban</div>", unsafe_allow_html=True)
st.markdown("<div class='section-subtitle'>Apakah suhu yang lebih tinggi berarti kelembaban yang lebih rendah?</div>", unsafe_allow_html=True)

st.markdown("""
    <div class='chart-container'>
        <div class='chart-title'>6. Scatter Plot: Suhu vs Kelembaban</div>
        <div class='chart-desc'>2 Variabel Numerik + 1 Kategorik • Scatter Plot</div>
    </div>
""", unsafe_allow_html=True)

fig_scatter = px.scatter(
    df_filtered, x='Suhu', y='Kelembaban',
    color='Kondisi',
    color_discrete_map=KONDISI_COLORS,
    hover_data=['Kota'],
    opacity=0.7
)
fig_scatter.update_traces(marker=dict(size=7, line=dict(width=0.5, color='white')))
fig_scatter.update_layout(
    plot_bgcolor='rgba(0,0,0,0)',
    paper_bgcolor='rgba(0,0,0,0)',
    font=dict(family='Poppins', size=12, color='#0f172a'),
    margin=dict(t=20, b=20, l=20, r=20),
    height=480,
    legend=dict(
        orientation='h', yanchor='bottom', y=1.02,
        xanchor='center', x=0.5,
        bgcolor='rgba(255,255,255,0.8)',
        bordercolor='#e2e8f0', borderwidth=1
    ),
    xaxis=dict(showgrid=True, gridcolor='#f0f0f0', title='Suhu (°C)'),
    yaxis=dict(showgrid=True, gridcolor='#f0f0f0', title='Kelembaban (%)')
)
st.plotly_chart(fig_scatter, use_container_width=True, config={'displayModeBar': False})

if total_obs > 0:
    corr = df_filtered[['Suhu', 'Kelembaban']].corr().iloc[0, 1]
    def interpretasi_corr(val):
        abs_val = abs(val)
        if abs_val < 0.2: return "sangat lemah / tidak ada"
        elif abs_val < 0.4: return "lemah"
        elif abs_val < 0.6: return "sedang"
        elif abs_val < 0.8: return "kuat"
        else: return "sangat kuat"

    st.markdown(f"""
        <div class='explain-box'>
            <b>Cara Membaca:</b> Setiap titik adalah satu observasi. Posisi horizontal = suhu, 
            vertikal = kelembaban. Warna = kondisi cuaca.<br>
            <b>Korelasi Pearson:</b> <b>{corr:.3f}</b> ({interpretasi_corr(corr)})<br>
            <b>Insight:</b> Terdapat korelasi <b>negatif</b>, artinya semakin tinggi suhu, 
            semakin rendah kelembaban. Pola ini muncul karena pada pembuatan data kami 
            menggunakan rumus <code>kelembaban = 90 - (suhu - 22) × 2</code>. Secara fisika, 
            ini juga masuk akal — udara panas lebih mudah menahan uap air sebelum jenuh.
        </div>
    """, unsafe_allow_html=True)

# ============================================================
# SECTION 5: BOX PLOT
# ============================================================
st.markdown("<div class='section-title'>📦 Perbandingan Suhu Antar Kota</div>", unsafe_allow_html=True)
st.markdown("<div class='section-subtitle'>Melihat variabilitas suhu dan kelembaban di setiap kota</div>", unsafe_allow_html=True)

col_e, col_f = st.columns(2)

with col_e:
    st.markdown("""
        <div class='chart-container'>
            <div class='chart-title'>7. Box Plot Suhu per Kota</div>
            <div class='chart-desc'>Numerik vs Kategorik • Box Plot</div>
        </div>
    """, unsafe_allow_html=True)
    fig_box_suhu = px.box(
        df_filtered, x='Kota', y='Suhu',
        color='Kota',
        color_discrete_sequence=COLOR_PALETTE,
        points='outliers'
    )
    fig_box_suhu.update_traces(line_width=1.5)
    fig_box_suhu.update_layout(
        showlegend=False,
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(family='Poppins', size=12, color='#0f172a'),
        margin=dict(t=20, b=20, l=20, r=20),
        height=380,
        xaxis=dict(showgrid=False, title=None),
        yaxis=dict(showgrid=True, gridcolor='#f0f0f0', title='Suhu (°C)')
    )
    st.plotly_chart(fig_box_suhu, use_container_width=True, config={'displayModeBar': False})

with col_f:
    st.markdown("""
        <div class='chart-container'>
            <div class='chart-title'>8. Box Plot Kelembaban per Kota</div>
            <div class='chart-desc'>Numerik vs Kategorik • Box Plot</div>
        </div>
    """, unsafe_allow_html=True)
    fig_box_kelembaban = px.box(
        df_filtered, x='Kota', y='Kelembaban',
        color='Kota',
        color_discrete_sequence=COLOR_PALETTE,
        points='outliers'
    )
    fig_box_kelembaban.update_traces(line_width=1.5)
    fig_box_kelembaban.update_layout(
        showlegend=False,
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(family='Poppins', size=12, color='#0f172a'),
        margin=dict(t=20, b=20, l=20, r=20),
        height=380,
        xaxis=dict(showgrid=False, title=None),
        yaxis=dict(showgrid=True, gridcolor='#f0f0f0', title='Kelembaban (%)')
    )
    st.plotly_chart(fig_box_kelembaban, use_container_width=True, config={'displayModeBar': False})

if total_obs > 0:
    hottest = df_filtered.groupby('Kota')['Suhu'].mean().idxmax()
    hottest_val = df_filtered.groupby('Kota')['Suhu'].mean().max()
    coolest = df_filtered.groupby('Kota')['Suhu'].mean().idxmin()
    coolest_val = df_filtered.groupby('Kota')['Suhu'].mean().min()
    st.markdown(f"""
        <div class='explain-box'>
            <b>Insight Suhu:</b> <b>{hottest}</b> adalah kota terpanas dengan rata-rata 
            <b>{hottest_val:.1f}°C</b>, sedangkan <b>{coolest}</b> adalah yang paling sejuk 
            (<b>{coolest_val:.1f}°C</b>). Selisih <b>{hottest_val - coolest_val:.1f}°C</b> 
            ini mencerminkan perbedaan geografis (dataran rendah vs dataran tinggi).
        </div>
    """, unsafe_allow_html=True)

# ============================================================
# KESIMPULAN OTOMATIS
# ============================================================
st.markdown("<div class='section-title'>💡 Kesimpulan Otomatis</div>", unsafe_allow_html=True)
st.markdown("<div class='section-subtitle'>Rangkuman temuan berdasarkan filter yang aktif</div>", unsafe_allow_html=True)

if total_obs > 0:
    kor = df_filtered['Kota'].mode()[0]
    kon = df_filtered['Kondisi'].mode()[0]
    kor_h = df_filtered.groupby('Kota')['Kelembaban'].mean().idxmax()

    st.markdown(f"""
        <div class='insight-box'>
            ✅ Berdasarkan <b>{total_obs:,} pengamatan</b> yang lolos filter:<br><br>
            🌡️ Rata-rata suhu = <b>{avg_suhu:.1f}°C</b> • Kota terpanas: <b>{kota_terpanas}</b><br>
            💧 Rata-rata kelembaban = <b>{avg_kelembaban:.0f}%</b> • Kota paling lembab: <b>{kor_h}</b><br>
            ☁️ Kondisi paling sering: <b>{kon}</b><br>
            📍 Kota paling banyak diamati: <b>{kor}</b><br><br>
            <b>Pelajaran Tipe Data:</b> Perhatikan bahwa <b>Suhu</b> dan <b>Kelembaban</b> 
            meskipun sama-sama numerik, memiliki <i>skala</i> yang berbeda. Suhu adalah <b>Interval</b> 
            (tidak ada nol absolut), sedangkan Kelembaban adalah <b>Rasio</b> (ada nol absolut). 
            Perbedaan ini memengaruhi operasi matematika yang valid!
        </div>
    """, unsafe_allow_html=True)

# ============================================================
# FOOTER
# ============================================================
st.markdown("""
    <div class='footer'>
        <p style='margin: 0;'>🌤️ <b>Dashboard Pengamatan Cuaca Indonesia</b> • Dibuat dengan Streamlit & Plotly</p>
        <p style='margin: 6px 0 0 0; font-size: 12px;'>Bedah Kasus 3 • Visualisasi Data • Program Studi Sistem Informasi</p>
    </div>
""", unsafe_allow_html=True)