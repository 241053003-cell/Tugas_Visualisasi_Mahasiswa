# ============================================================
# DASHBOARD PENJUALAN - STREAMLIT
# Bedah Kasus 1 - Visualisasi Data
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
    page_title="Dashboard Penjualan",
    page_icon="🛒",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================
# CUSTOM CSS - TEMA EMERALD & GOLD
# ============================================================
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap');

    html, body, [class*="css"] {
        font-family: 'Poppins', 'Inter', sans-serif;
    }

    .stApp {
        background: linear-gradient(135deg, #ecfdf5 0%, #f0fdf4 50%, #fefce8 100%);
    }

    /* ============ HERO ============ */
    .hero-section {
        background: linear-gradient(135deg, #059669 0%, #10b981 50%, #14b8a6 100%);
        padding: 45px 50px;
        border-radius: 24px;
        color: white;
        margin-bottom: 30px;
        box-shadow: 0 20px 45px rgba(5, 150, 105, 0.3);
        position: relative; overflow: hidden;
    }
    .hero-section::before {
        content: '💰';
        position: absolute;
        top: 10px; right: 40px;
        font-size: 80px;
        opacity: 0.15;
    }
    .hero-section::after {
        content: '🛒';
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
        border: 1px solid rgba(16, 185, 129, 0.1);
    }
    .kpi-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 12px 30px rgba(16, 185, 129, 0.2);
    }
    .kpi-card::before {
        content: '';
        position: absolute;
        top: 0; left: 0;
        width: 5px; height: 100%;
        border-radius: 5px 0 0 5px;
    }
    .kpi-card.card-1::before { background: linear-gradient(180deg, #10b981, #047857); }
    .kpi-card.card-2::before { background: linear-gradient(180deg, #f59e0b, #d97706); }
    .kpi-card.card-3::before { background: linear-gradient(180deg, #06b6d4, #0891b2); }
    .kpi-card.card-4::before { background: linear-gradient(180deg, #8b5cf6, #6d28d9); }

    .kpi-icon { font-size: 28px; margin-bottom: 10px; }
    .kpi-label {
        font-size: 13px; color: #64748b;
        font-weight: 500; text-transform: uppercase;
        letter-spacing: 1px; margin-bottom: 6px;
    }
    .kpi-value {
        font-size: 26px; font-weight: 700; color: #0f172a;
        letter-spacing: -0.5px; line-height: 1.1;
    }
    .kpi-unit {
        font-size: 13px; color: #64748b;
        font-weight: 400; margin-left: 4px;
    }

    /* ============ SECTION TITLE ============ */
    .section-title {
        font-size: 22px; font-weight: 600; color: #0f172a;
        margin: 30px 0 8px 0; padding-left: 14px;
        border-left: 4px solid #10b981; line-height: 1.2;
    }
    .section-subtitle {
        font-size: 13px; color: #64748b;
        font-weight: 400; margin-top: 4px;
        padding-left: 18px; margin-bottom: 18px;
    }

    /* ============ SIDEBAR ============ */
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #064e3b 0%, #065f46 100%);
    }
    section[data-testid="stSidebar"] * {
        color: #d1fae5 !important;
    }
    section[data-testid="stSidebar"] .stMultiSelect label,
    section[data-testid="stSidebar"] .stSlider label,
    section[data-testid="stSidebar"] .stDateInput label {
        color: #a7f3d0 !important;
        font-weight: 500; font-size: 13px;
    }

    /* ============ CHART CONTAINER ============ */
    .chart-container {
        background: white;
        padding: 20px;
        border-radius: 18px;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.06);
        border: 1px solid rgba(16, 185, 129, 0.08);
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

    /* ============ BOXES ============ */
    .explain-box {
        background: linear-gradient(135deg, #ecfdf5 0%, #d1fae5 100%);
        border-left: 4px solid #10b981;
        padding: 16px 20px;
        border-radius: 12px;
        margin: 12px 0 20px 0;
        font-size: 13.5px;
        color: #064e3b;
        line-height: 1.7;
    }
    .explain-box b { color: #047857; }
    .explain-box code {
        background: white; padding: 2px 6px;
        border-radius: 4px; font-size: 12px; color: #dc2626;
    }

    .insight-box {
        background: linear-gradient(135deg, #fef3c7 0%, #fde68a 100%);
        border-left: 4px solid #f59e0b;
        padding: 16px 20px;
        border-radius: 12px;
        margin: 12px 0;
        font-size: 13.5px;
        color: #78350f;
        line-height: 1.7;
    }

    .warn-box {
        background: linear-gradient(135deg, #fee2e2 0%, #fecaca 100%);
        border-left: 4px solid #ef4444;
        padding: 16px 20px;
        border-radius: 12px;
        margin: 12px 0;
        font-size: 13.5px;
        color: #7f1d1d;
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
        background: linear-gradient(135deg, #10b981, #047857);
        color: white; padding: 12px 16px;
        text-align: left; font-weight: 600;
        font-size: 12px; text-transform: uppercase;
    }
    .dict-table td {
        padding: 12px 16px;
        border-bottom: 1px solid #f0f0f0;
        color: #334155;
    }
    .dict-table tr:last-child td { border-bottom: none; }
    .dict-table tr:hover td { background: #f0fdf4; }
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
    .badge-diskrit { background: #fef3c7; color: #92400e; }
    .badge-kontinu { background: #fee2e2; color: #b91c1c; }

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

    kategori_list = ['Elektronik', 'Pendidikan', 'Fashion', 'Makanan', 'Kesehatan']
    prob_kategori = [0.25, 0.20, 0.25, 0.20, 0.10]
    kategori = np.random.choice(kategori_list, n_samples, p=prob_kategori)

    produk_per_kategori = {
        'Elektronik': ['Laptop', 'Smartphone', 'Tablet', 'Headphone', 'Kamera'],
        'Pendidikan': ['Buku', 'Alat Tulis', 'Tas Sekolah', 'Kalkulator'],
        'Fashion':    ['Kemeja', 'Sepatu', 'Jaket', 'Tas', 'Topi'],
        'Makanan':    ['Snack', 'Minuman', 'Kopi', 'Cokelat'],
        'Kesehatan':  ['Vitamin', 'Masker', 'Hand Sanitizer', 'Termometer'],
    }
    produk = np.array([np.random.choice(produk_per_kategori[k]) for k in kategori])

    harga_profile = {
        'Laptop': (8500000, 3000000), 'Smartphone': (4500000, 1500000),
        'Tablet': (3800000, 1000000), 'Headphone': (750000, 250000),
        'Kamera': (6000000, 2000000), 'Buku': (85000, 25000),
        'Alat Tulis': (35000, 10000), 'Tas Sekolah': (250000, 75000),
        'Kalkulator': (175000, 50000), 'Kemeja': (180000, 60000),
        'Sepatu': (450000, 150000), 'Jaket': (380000, 120000),
        'Tas': (280000, 90000), 'Topi': (95000, 30000),
        'Snack': (15000, 5000), 'Minuman': (8000, 3000),
        'Kopi': (45000, 15000), 'Cokelat': (25000, 8000),
        'Vitamin': (85000, 25000), 'Masker': (45000, 15000),
        'Hand Sanitizer': (35000, 10000), 'Termometer': (125000, 40000),
    }
    harga = np.array([
        max(1000, np.random.normal(harga_profile[p][0], harga_profile[p][1]))
        for p in produk
    ])
    harga = np.round(harga, -3).astype(int)

    base_qty = 100 - (harga / 200000)
    base_qty = np.clip(base_qty, 2, 150)
    jumlah_terjual = np.random.poisson(base_qty).astype(int)
    jumlah_terjual = np.clip(jumlah_terjual, 1, 200)

    tanggal = pd.date_range(start='2025-01-01', periods=n_samples, freq='D')
    tanggal = np.random.choice(tanggal, n_samples, replace=False)
    tanggal = pd.to_datetime(tanggal)

    df = pd.DataFrame({
        'Tanggal':        tanggal,
        'Produk':         produk,
        'Kategori':       kategori,
        'Harga (Rp)':     harga,
        'Jumlah Terjual': jumlah_terjual,
    })
    df['Total Pendapatan'] = df['Harga (Rp)'] * df['Jumlah Terjual']
    df = df.sort_values('Tanggal').reset_index(drop=True)
    return df

df = generate_data()

# ============================================================
# PALET WARNA
# ============================================================
COLOR_PALETTE = ['#10b981', '#f59e0b', '#06b6d4', '#8b5cf6', '#ef4444']
KATEGORI_COLORS = {
    'Elektronik': '#3b82f6',
    'Pendidikan': '#10b981',
    'Fashion':    '#f59e0b',
    'Makanan':    '#ef4444',
    'Kesehatan':  '#8b5cf6',
}

# Helper format rupiah
def format_rp(val):
    if val >= 1e9: return f"Rp {val/1e9:.2f} M"
    elif val >= 1e6: return f"Rp {val/1e6:.1f} Jt"
    elif val >= 1e3: return f"Rp {val/1e3:.0f} Rb"
    return f"Rp {val:.0f}"

# ============================================================
# SIDEBAR
# ============================================================
with st.sidebar:
    st.markdown("""
        <div style='text-align: center; padding: 10px 0 20px 0;'>
            <div style='font-size: 42px;'>🛒</div>
            <h2 style='font-size: 20px; margin: 8px 0 0 0; font-weight: 600;'>Filter Penjualan</h2>
            <p style='font-size: 12px; opacity: 0.7; margin-top: 4px;'>Sesuaikan data yang ingin dilihat</p>
        </div>
    """, unsafe_allow_html=True)
    st.markdown("---")

    selected_kategori = st.multiselect(
        "🏷️ Pilih Kategori:",
        options=df['Kategori'].unique(),
        default=df['Kategori'].unique()
    )

    # Filter produk berdasarkan kategori terpilih
    produk_available = df[df['Kategori'].isin(selected_kategori)]['Produk'].unique()
    selected_produk = st.multiselect(
        "📦 Pilih Produk:",
        options=produk_available,
        default=produk_available
    )

    min_date = df['Tanggal'].min().date()
    max_date = df['Tanggal'].max().date()
    date_range = st.date_input(
        "📅 Rentang Tanggal:",
        value=(min_date, max_date),
        min_value=min_date,
        max_value=max_date
    )

    st.markdown("---")
    st.markdown("""
        <div style='background: rgba(16, 185, 129, 0.15); padding: 14px; border-radius: 12px;'>
            <p style='font-size: 12px; margin: 0; line-height: 1.6;'>
                💡 <b>Tips:</b> Klik kategori di atas untuk filter produk secara otomatis!
            </p>
        </div>
    """, unsafe_allow_html=True)

# Filter data
df_filtered = df[
    (df['Kategori'].isin(selected_kategori)) &
    (df['Produk'].isin(selected_produk))
]

if len(date_range) == 2:
    df_filtered = df_filtered[
        (df_filtered['Tanggal'].dt.date >= date_range[0]) &
        (df_filtered['Tanggal'].dt.date <= date_range[1])
    ]

# ============================================================
# HERO
# ============================================================
st.markdown("""
    <div class='hero-section'>
        <div class='hero-badge'>🛒 VISUALISASI DATA • PERTEMUAN 2</div>
        <h1 class='hero-title'>Dashboard Operasional Penjualan</h1>
        <p class='hero-subtitle'>Analisis interaktif 1.000 transaksi penjualan multi-kategori</p>
    </div>
""", unsafe_allow_html=True)

# ============================================================
# KPI
# ============================================================
total_trx = len(df_filtered)
total_rev = df_filtered['Total Pendapatan'].sum() if total_trx > 0 else 0
total_unit = df_filtered['Jumlah Terjual'].sum() if total_trx > 0 else 0
avg_trx = df_filtered['Total Pendapatan'].mean() if total_trx > 0 else 0

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown(f"""
        <div class='kpi-card card-1'>
            <div class='kpi-icon'>💰</div>
            <div class='kpi-label'>Total Pendapatan</div>
            <div class='kpi-value'>{format_rp(total_rev)}</div>
        </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
        <div class='kpi-card card-2'>
            <div class='kpi-icon'>📦</div>
            <div class='kpi-label'>Total Unit Terjual</div>
            <div class='kpi-value'>{total_unit:,}<span class='kpi-unit'>unit</span></div>
        </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
        <div class='kpi-card card-3'>
            <div class='kpi-icon'>🧾</div>
            <div class='kpi-label'>Total Transaksi</div>
            <div class='kpi-value'>{total_trx:,}<span class='kpi-unit'>trx</span></div>
        </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown(f"""
        <div class='kpi-card card-4'>
            <div class='kpi-icon'>📊</div>
            <div class='kpi-label'>Rata-rata per Transaksi</div>
            <div class='kpi-value'>{format_rp(avg_trx)}</div>
        </div>
    """, unsafe_allow_html=True)

# ============================================================
# DATA DICTIONARY
# ============================================================
st.markdown("<div class='section-title'>📖 Kamus Data (Data Dictionary)</div>", unsafe_allow_html=True)
st.markdown("<div class='section-subtitle'>Penjelasan tipe data setiap kolom sesuai Skala Stevens (1946)</div>", unsafe_allow_html=True)

st.markdown("""
    <div class='explain-box'>
        <b>Tentang Dataset:</b> Dataset ini berisi 1.000 transaksi penjualan dari 22 produk dalam 5 kategori. 
        Fokus utama: perhatikan bahwa <b>Harga</b> berskala <b>Kontinu</b> (hasil mengukur), sedangkan 
        <b>Jumlah Terjual</b> berskala <b>Diskrit</b> (hasil menghitung). Ini dua sub-tipe Numerik yang berbeda!
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
            <td>Tanggal transaksi penjualan terjadi.</td>
            <td>2025-03-15</td>
            <td>Line Chart (tren)</td>
        </tr>
        <tr>
            <td><b>Produk</b></td>
            <td>Kategorik</td>
            <td><span class='badge badge-nominal'>Nominal</span></td>
            <td>Nama produk yang terjual. Label tanpa urutan.</td>
            <td>Laptop, Buku</td>
            <td>Bar Chart, Pie Chart</td>
        </tr>
        <tr>
            <td><b>Kategori</b></td>
            <td>Kategorik</td>
            <td><span class='badge badge-nominal'>Nominal</span></td>
            <td>Kategori produk. Label tanpa urutan.</td>
            <td>Elektronik, Fashion</td>
            <td>Bar Chart, Pie Chart</td>
        </tr>
        <tr>
            <td><b>Harga (Rp)</b></td>
            <td>Numerik</td>
            <td><span class='badge badge-kontinu'>Kontinu (Rasio)</span></td>
            <td>Harga produk dalam Rupiah. Hasil <b>mengukur</b>. Nilai desimal/rentang, ada nol absolut.</td>
            <td>8.500.000, 75.000</td>
            <td>Histogram, Box Plot</td>
        </tr>
        <tr>
            <td><b>Jumlah Terjual</b></td>
            <td>Numerik</td>
            <td><span class='badge badge-diskrit'>Diskrit (Rasio)</span></td>
            <td>Jumlah unit terjual. Hasil <b>menghitung</b>. Nilai bulat (integer).</td>
            <td>45, 120, 3</td>
            <td>Histogram, Bar Chart</td>
        </tr>
    </tbody>
</table>
""", unsafe_allow_html=True)

st.markdown("""
    <div class='warn-box'>
        ⚠️ <b>Perbedaan Kunci Diskrit vs Kontinu:</b><br>
        • <b>Jumlah Terjual (Diskrit):</b> Tidak bisa bernilai 3.5 unit. Harus bilangan bulat. Hasil <i>counting</i>.<br>
        • <b>Harga (Kontinu):</b> Bisa bernilai Rp 8.500.000 atau Rp 8.500.123,45. Hasil <i>measuring</i>. Bisa dipecah lebih kecil tanpa batas.
    </div>
""", unsafe_allow_html=True)

# ============================================================
# SECTION 1: KATEGORIK
# ============================================================
st.markdown("<div class='section-title'>🏷️ Analisis Data Kategorik</div>", unsafe_allow_html=True)
st.markdown("<div class='section-subtitle'>Distribusi pendapatan dan transaksi berdasarkan kategori & produk</div>", unsafe_allow_html=True)

col_a, col_b = st.columns(2)

with col_a:
    st.markdown("""
        <div class='chart-container'>
            <div class='chart-title'>1. Pendapatan per Kategori</div>
            <div class='chart-desc'>Kategorik Nominal • Bar Chart</div>
        </div>
    """, unsafe_allow_html=True)
    kat_rev = df_filtered.groupby('Kategori')['Total Pendapatan'].sum().sort_values(ascending=False).reset_index()
    fig_kategori = px.bar(
        kat_rev, x='Kategori', y='Total Pendapatan',
        color='Kategori', text='Total Pendapatan',
        color_discrete_map=KATEGORI_COLORS
    )
    fig_kategori.update_traces(
        texttemplate='Rp %{text:.3s}',
        textposition='outside', textfont_size=12,
        marker_line_width=0,
        hovertemplate='<b>%{x}</b><br>Pendapatan: Rp %{y:,.0f}<extra></extra>'
    )
    fig_kategori.update_layout(
        showlegend=False,
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(family='Poppins', size=12, color='#0f172a'),
        margin=dict(t=20, b=20, l=20, r=20),
        height=340,
        xaxis=dict(showgrid=False, title=None),
        yaxis=dict(showgrid=True, gridcolor='#f0f0f0', title=None)
    )
    st.plotly_chart(fig_kategori, use_container_width=True, config={'displayModeBar': False})

    if total_trx > 0 and len(kat_rev) > 0:
        top_kat = kat_rev.iloc[0]['Kategori']
        top_rev = kat_rev.iloc[0]['Total Pendapatan']
        st.markdown(f"""
            <div class='explain-box'>
                <b>Insight:</b> Kategori <b>{top_kat}</b> menghasilkan pendapatan tertinggi 
                (<b>{format_rp(top_rev)}</b>). Produk elektronik biasanya punya harga tinggi 
                sehingga mendominasi pendapatan meski jumlah unitnya mungkin lebih sedikit.
            </div>
        """, unsafe_allow_html=True)

with col_b:
    st.markdown("""
        <div class='chart-container'>
            <div class='chart-title'>2. Top 8 Produk Terlaris</div>
            <div class='chart-desc'>Kategorik Nominal • Bar Chart Horizontal</div>
        </div>
    """, unsafe_allow_html=True)
    top_produk = df_filtered.groupby('Produk')['Jumlah Terjual'].sum().sort_values(ascending=False).head(8).reset_index()
    fig_produk = px.bar(
        top_produk.sort_values('Jumlah Terjual'),
        x='Jumlah Terjual', y='Produk',
        color='Jumlah Terjual',
        text='Jumlah Terjual',
        color_continuous_scale=['#d1fae5', '#6ee7b7', '#10b981', '#047857']
    )
    fig_produk.update_traces(
        textposition='outside', textfont_size=12,
        marker_line_width=0,
        hovertemplate='<b>%{y}</b><br>Terjual: %{x} unit<extra></extra>'
    )
    fig_produk.update_layout(
        showlegend=False, coloraxis_showscale=False,
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(family='Poppins', size=12, color='#0f172a'),
        margin=dict(t=20, b=20, l=20, r=20),
        height=340,
        xaxis=dict(showgrid=True, gridcolor='#f0f0f0', title=None),
        yaxis=dict(showgrid=False, title=None)
    )
    st.plotly_chart(fig_produk, use_container_width=True, config={'displayModeBar': False})

    if len(top_produk) > 0:
        best = top_produk.iloc[0]['Produk']
        best_n = int(top_produk.iloc[0]['Jumlah Terjual'])
        st.markdown(f"""
            <div class='explain-box'>
                <b>Insight:</b> <b>{best}</b> adalah produk terlaris dengan 
                <b>{best_n} unit</b> terjual. Produk murah seperti makanan/minuman biasanya 
                dominan karena volume pembelian berulang lebih tinggi.
            </div>
        """, unsafe_allow_html=True)

# ============================================================
# SECTION 2: NUMERIK
# ============================================================
st.markdown("<div class='section-title'>💵 Analisis Data Numerik</div>", unsafe_allow_html=True)
st.markdown("<div class='section-subtitle'>Distribusi Harga (Kontinu) dan Jumlah Terjual (Diskrit)</div>", unsafe_allow_html=True)

col_c, col_d = st.columns(2)

with col_c:
    st.markdown("""
        <div class='chart-container'>
            <div class='chart-title'>3. Distribusi Harga Produk</div>
            <div class='chart-desc'>Numerik Kontinu (Rasio) • Histogram</div>
        </div>
    """, unsafe_allow_html=True)
    fig_harga = px.histogram(
        df_filtered, x='Harga (Rp)', nbins=40,
        marginal='box',
        color_discrete_sequence=['#f59e0b']
    )
    fig_harga.update_traces(
        marker_line_width=0, opacity=0.85,
        hovertemplate='Harga: Rp %{x:,.0f}<br>Frekuensi: %{y}<extra></extra>'
    )
    fig_harga.update_layout(
        showlegend=False,
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(family='Poppins', size=12, color='#0f172a'),
        margin=dict(t=20, b=20, l=20, r=20),
        height=380,
        xaxis=dict(showgrid=False, title='Harga (Rp)'),
        yaxis=dict(showgrid=True, gridcolor='#f0f0f0', title=None)
    )
    st.plotly_chart(fig_harga, use_container_width=True, config={'displayModeBar': False})

    if total_trx > 0:
        med_h = df_filtered['Harga (Rp)'].median()
        std_h = df_filtered['Harga (Rp)'].std()
        st.markdown(f"""
            <div class='explain-box'>
                <b>Cara Membaca:</b> Distribusi harga sangat <i>right-skewed</i> (miring ke kanan) — 
                mayoritas produk berharga murah, tapi ada beberapa produk sangat mahal (Laptop, Kamera).<br>
                <b>Statistik:</b> Median = <b>{format_rp(med_h)}</b> • Standar deviasi = <b>{format_rp(std_h)}</b><br>
                <b>Insight:</b> Karena Harga berskala <b>Kontinu (Rasio)</b>, kita bisa membandingkan: 
                "Laptop 10× lebih mahal dari headphone" — ini valid karena ada nol absolut.
            </div>
        """, unsafe_allow_html=True)

with col_d:
    st.markdown("""
        <div class='chart-container'>
            <div class='chart-title'>4. Distribusi Jumlah Terjual</div>
            <div class='chart-desc'>Numerik Diskrit (Rasio) • Histogram</div>
        </div>
    """, unsafe_allow_html=True)
    fig_qty = px.histogram(
        df_filtered, x='Jumlah Terjual', nbins=40,
        marginal='box',
        color_discrete_sequence=['#10b981']
    )
    fig_qty.update_traces(
        marker_line_width=0, opacity=0.85,
        hovertemplate='Jumlah: %{x} unit<br>Frekuensi: %{y}<extra></extra>'
    )
    fig_qty.update_layout(
        showlegend=False,
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(family='Poppins', size=12, color='#0f172a'),
        margin=dict(t=20, b=20, l=20, r=20),
        height=380,
        xaxis=dict(showgrid=False, title='Jumlah Terjual (unit)'),
        yaxis=dict(showgrid=True, gridcolor='#f0f0f0', title=None)
    )
    st.plotly_chart(fig_qty, use_container_width=True, config={'displayModeBar': False})

    if total_trx > 0:
        med_q = df_filtered['Jumlah Terjual'].median()
        max_q = df_filtered['Jumlah Terjual'].max()
        st.markdown(f"""
            <div class='explain-box'>
                <b>Cara Membaca:</b> Sumbu X hanya berisi <b>bilangan bulat</b> (1, 2, 3, ...) 
                karena Jumlah Terjual adalah <b>Diskrit</b>. Tidak ada nilai 3.5 unit.<br>
                <b>Statistik:</b> Median = <b>{med_q:.0f} unit</b> • Maksimum = <b>{max_q} unit</b><br>
                <b>Insight:</b> Distribusi bersifat <i>right-skewed</i> — banyak transaksi kecil, 
                sedikit transaksi besar. Ini pola umum di dunia retail (fenomena Pareto).
            </div>
        """, unsafe_allow_html=True)

# ============================================================
# SECTION 3: TIME SERIES
# ============================================================
st.markdown("<div class='section-title'>📈 Analisis Tren Waktu</div>", unsafe_allow_html=True)
st.markdown("<div class='section-subtitle'>Pergerakan pendapatan harian sepanjang periode</div>", unsafe_allow_html=True)

st.markdown("""
    <div class='chart-container'>
        <div class='chart-title'>5. Tren Pendapatan Harian (dengan Moving Average 7 hari)</div>
        <div class='chart-desc'>Waktu Interval • Line Chart</div>
    </div>
""", unsafe_allow_html=True)

if total_trx > 0:
    daily = df_filtered.groupby('Tanggal')['Total Pendapatan'].sum().reset_index()
    daily['MA7'] = daily['Total Pendapatan'].rolling(7, min_periods=1).mean()

    fig_line = go.Figure()
    fig_line.add_trace(go.Scatter(
        x=daily['Tanggal'], y=daily['Total Pendapatan'],
        mode='lines', name='Harian',
        line=dict(color='rgba(16, 185, 129, 0.3)', width=1),
        hovertemplate='<b>%{x|%d %b %Y}</b><br>Pendapatan: Rp %{y:,.0f}<extra></extra>'
    ))
    fig_line.add_trace(go.Scatter(
        x=daily['Tanggal'], y=daily['MA7'],
        mode='lines', name='MA 7 hari',
        line=dict(color='#10b981', width=2.5),
        hovertemplate='<b>%{x|%d %b %Y}</b><br>MA7: Rp %{y:,.0f}<extra></extra>'
    ))
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
        yaxis=dict(showgrid=True, gridcolor='#f0f0f0', title='Pendapatan (Rp)')
    )
    st.plotly_chart(fig_line, use_container_width=True, config={'displayModeBar': False})

    st.markdown(f"""
        <div class='explain-box'>
            <b>Cara Membaca:</b> Garis hijau tipis = pendapatan harian (fluktuatif). 
            Garis hijau tebal = moving average 7 hari (tren halus).<br>
            <b>Insight:</b> Moving average membantu kita melihat <i>tren sebenarnya</i> dengan 
            menghilangkan noise harian. Jika garis MA naik, berarti penjualan sedang tumbuh 
            secara konsisten.
        </div>
    """, unsafe_allow_html=True)

# ============================================================
# SECTION 4: SCATTER
# ============================================================
st.markdown("<div class='section-title'>🔍 Hubungan Harga vs Jumlah Terjual</div>", unsafe_allow_html=True)
st.markdown("<div class='section-subtitle'>Apakah harga yang lebih murah selalu terjual lebih banyak?</div>", unsafe_allow_html=True)

st.markdown("""
    <div class='chart-container'>
        <div class='chart-title'>6. Scatter Plot: Harga vs Jumlah Terjual per Transaksi</div>
        <div class='chart-desc'>2 Numerik + 1 Kategorik • Scatter Plot</div>
    </div>
""", unsafe_allow_html=True)

if total_trx > 0:
    fig_scatter = px.scatter(
        df_filtered, x='Harga (Rp)', y='Jumlah Terjual',
        color='Kategori',
        color_discrete_map=KATEGORI_COLORS,
        hover_data=['Produk'],
        opacity=0.65
    )
    fig_scatter.update_traces(marker=dict(size=8, line=dict(width=0.5, color='white')))
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
        xaxis=dict(showgrid=True, gridcolor='#f0f0f0', title='Harga (Rp)'),
        yaxis=dict(showgrid=True, gridcolor='#f0f0f0', title='Jumlah Terjual (unit)')
    )
    st.plotly_chart(fig_scatter, use_container_width=True, config={'displayModeBar': False})

    corr = df_filtered[['Harga (Rp)', 'Jumlah Terjual']].corr().iloc[0, 1]
    def interpretasi_corr(val):
        abs_val = abs(val)
        if abs_val < 0.2: return "sangat lemah / tidak ada"
        elif abs_val < 0.4: return "lemah"
        elif abs_val < 0.6: return "sedang"
        elif abs_val < 0.8: return "kuat"
        else: return "sangat kuat"

    st.markdown(f"""
        <div class='explain-box'>
            <b>Cara Membaca:</b> Setiap titik = 1 transaksi. Sumbu X = harga produk, 
            sumbu Y = jumlah yang terjual.<br>
            <b>Korelasi Pearson:</b> <b>{corr:.3f}</b> ({interpretasi_corr(corr)})<br>
            <b>Insight:</b> Terdapat korelasi <b>negatif</b>, artinya semakin mahal harga produk, 
            semakin sedikit jumlah terjual. Contoh: Laptop (harga tinggi) hanya terjual beberapa unit, 
            sementara Snack (harga murah) bisa terjual puluhan unit per transaksi. 
            Pola ini konsisten dengan hukum permintaan (<i>law of demand</i>) di ekonomi.
        </div>
    """, unsafe_allow_html=True)

# ============================================================
# SECTION 5: BOX PLOT
# ============================================================
st.markdown("<div class='section-title'>📦 Perbandingan Kategori</div>", unsafe_allow_html=True)
st.markdown("<div class='section-subtitle'>Sebaran harga dan jumlah terjual antar kategori</div>", unsafe_allow_html=True)

col_e, col_f = st.columns(2)

with col_e:
    st.markdown("""
        <div class='chart-container'>
            <div class='chart-title'>7. Box Plot Harga per Kategori</div>
            <div class='chart-desc'>Numerik vs Kategorik • Box Plot</div>
        </div>
    """, unsafe_allow_html=True)
    fig_box_h = px.box(
        df_filtered, x='Kategori', y='Harga (Rp)',
        color='Kategori',
        color_discrete_map=KATEGORI_COLORS,
        points='outliers'
    )
    fig_box_h.update_traces(line_width=1.5)
    fig_box_h.update_layout(
        showlegend=False,
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(family='Poppins', size=12, color='#0f172a'),
        margin=dict(t=20, b=20, l=20, r=20),
        height=380,
        xaxis=dict(showgrid=False, title=None),
        yaxis=dict(showgrid=True, gridcolor='#f0f0f0', title='Harga (Rp)')
    )
    st.plotly_chart(fig_box_h, use_container_width=True, config={'displayModeBar': False})

with col_f:
    st.markdown("""
        <div class='chart-container'>
            <div class='chart-title'>8. Box Plot Jumlah Terjual per Kategori</div>
            <div class='chart-desc'>Numerik vs Kategorik • Box Plot</div>
        </div>
    """, unsafe_allow_html=True)
    fig_box_q = px.box(
        df_filtered, x='Kategori', y='Jumlah Terjual',
        color='Kategori',
        color_discrete_map=KATEGORI_COLORS,
        points='outliers'
    )
    fig_box_q.update_traces(line_width=1.5)
    fig_box_q.update_layout(
        showlegend=False,
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(family='Poppins', size=12, color='#0f172a'),
        margin=dict(t=20, b=20, l=20, r=20),
        height=380,
        xaxis=dict(showgrid=False, title=None),
        yaxis=dict(showgrid=True, gridcolor='#f0f0f0', title='Jumlah Terjual')
    )
    st.plotly_chart(fig_box_q, use_container_width=True, config={'displayModeBar': False})

# ============================================================
# KESIMPULAN OTOMATIS
# ============================================================
st.markdown("<div class='section-title'>💡 Kesimpulan Otomatis</div>", unsafe_allow_html=True)
st.markdown("<div class='section-subtitle'>Rangkuman temuan berdasarkan filter aktif</div>", unsafe_allow_html=True)

if total_trx > 0:
    top_kat = df_filtered.groupby('Kategori')['Total Pendapatan'].sum().idxmax()
    top_kat_rev = df_filtered.groupby('Kategori')['Total Pendapatan'].sum().max()
    top_prod_q = df_filtered.groupby('Produk')['Jumlah Terjual'].sum().idxmax()
    top_prod_qn = int(df_filtered.groupby('Produk')['Jumlah Terjual'].sum().max())
    top_prod_rev = df_filtered.groupby('Produk')['Total Pendapatan'].sum().idxmax()

    st.markdown(f"""
        <div class='insight-box'>
            ✅ Berdasarkan <b>{total_trx:,} transaksi</b> yang lolos filter:<br><br>
            💰 Total pendapatan: <b>{format_rp(total_rev)}</b> dari <b>{total_unit:,} unit</b> terjual<br>
            🏆 Kategori paling menguntungkan: <b>{top_kat}</b> ({format_rp(top_kat_rev)})<br>
            📦 Produk terlaris: <b>{top_prod_q}</b> ({top_prod_qn} unit)<br>
            💎 Produk paling cuan: <b>{top_prod_rev}</b><br>
            🧾 Rata-rata nilai transaksi: <b>{format_rp(avg_trx)}</b><br><br>
            <b>Pelajaran Tipe Data:</b> Perhatikan bahwa <b>Harga</b> dan <b>Jumlah Terjual</b> 
            sama-sama numerik dengan skala Rasio, tapi sub-tipe-nya berbeda! Harga adalah 
            <b>Kontinu</b> (bisa pecahan), sedangkan Jumlah Terjual adalah <b>Diskrit</b> (harus bulat). 
            Memahami perbedaan ini penting agar tidak salah memilih visualisasi dan analisis statistik.
        </div>
    """, unsafe_allow_html=True)

# ============================================================
# FOOTER
# ============================================================
st.markdown("""
    <div class='footer'>
        <p style='margin: 0;'>🛒 <b>Dashboard Operasional Penjualan</b> • Dibuat dengan Streamlit & Plotly</p>
        <p style='margin: 6px 0 0 0; font-size: 12px;'>Bedah Kasus 1 • Visualisasi Data • Program Studi Sistem Informasi</p>
    </div>
""", unsafe_allow_html=True)