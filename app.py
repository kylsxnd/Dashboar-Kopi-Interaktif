import streamlit as st
import pandas as pd
from streamlit_echarts import st_echarts

# 1. Konfigurasi Halaman (Wide Mode)
st.set_page_config(
    page_title="Dashboard Analitik EduGrowth",
    page_icon="☕",
    layout="wide"
)

# 2. Menyuntikkan CSS Lokal Asli Kamu ke dalam Streamlit
st.markdown("""
    <style>
    /* Styling Dasar Mengikuti CSS Asli Kamu */
    .stApp {
        background: linear-gradient(135deg, #0f2027, #203a43, #2c5364);
        color: #e0e0e0;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }
    
    /* Sembunyikan Header Bawaan Streamlit */
    header {visibility: hidden;}
    
    /* Styling Sidebar Logo & Navigasi */
    .custom-logo {
        font-size: 22px; font-weight: 800;
        background: -webkit-linear-gradient(#f1c40f, #e67e22);
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
        margin-bottom: 30px;
    }
    
    /* Styling Kartu KPI */
    .kpi-section { display: grid; grid-template-columns: repeat(3, 1fr); gap: 25px; margin-bottom: 30px; }
    .kpi-card {
        background: rgba(255, 255, 255, 0.05); padding: 25px 30px; border-radius: 16px;
        backdrop-filter: blur(12px); border: 1px solid rgba(255, 255, 255, 0.1);
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.3); position: relative;
    }
    .kpi-card h3 { font-size: 13px; color: #b0bec5; text-transform: uppercase; margin-bottom: 10px; letter-spacing: 1px; }
    .kpi-card h2 { font-size: 32px; color: #fff; font-weight: 700; margin: 0; }
    .badge { position: absolute; top: 25px; right: 25px; background: rgba(255, 255, 255, 0.1); color: #e0e0e0; padding: 5px 10px; border-radius: 20px; font-size: 11px; font-weight: bold; }

    /* Kartu Grafik & Insight */
    .card-container {
        background: rgba(255, 255, 255, 0.05); padding: 25px; border-radius: 16px; 
        backdrop-filter: blur(12px); border: 1px solid rgba(255, 255, 255, 0.1);
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.3); margin-bottom: 25px;
    }
    </style>
""", unsafe_allow_html=True)

# 3. Fungsi Load & Pembersihan Data (Logika Pandas dari Backend Kamu)
@st.cache_data
def load_and_clean_data():
    df = pd.read_excel('Dataset_Kopi_Nasional_Wide_Format_2021_2026.xlsx')
    df['Produksi Robusta (Ton)'] = pd.to_numeric(df['Produksi Robusta (Ton)'], errors='coerce').fillna(0)
    df['Produksi Arabika (Ton)'] = pd.to_numeric(df['Produksi Arabika (Ton)'], errors='coerce').fillna(0)
    return df

try:
    df = load_and_clean_data()
except Exception as e:
    st.error(f"Gagal memuat dataset Excel: {e}")
    st.stop()

# 4. Sidebar & Filter Tahun (Menyerupai Header & Navigasi Lokal)
with st.sidebar:
    st.markdown('<div class="custom-logo">EduGrowth<br><span style="font-size: 14px; font-weight: normal; color: #fff;">Creative Analytics</span></div>', unsafe_allow_html=True)
    
    # Navigasi Tab
    menu = st.radio("Menu Navigasi", ["📊 Overview & Provinsi", "📈 Tren Tahunan", "📄 Data Spreadsheet"], label_visibility="collapsed")
    
    st.markdown("---")
    st.markdown("### 🎛️ Filter Tahun")
    years = sorted(df['Tahun'].dropna().unique().astype(int).tolist())
    selected_year = st.selectbox("Pilih Tahun", ["Semua Tahun (2021-2026)"] + years)

# Logika Filter Berdasarkan Tahun
if selected_year != "Semua Tahun (2021-2026)":
    filtered_df = df[df['Tahun'] == selected_year]
    trend_df = df[df['Tahun'] <= selected_year]
    periode_teks = f"pada tahun <strong>{selected_year}</strong>"
else:
    filtered_df = df
    trend_df = df
    periode_teks = "selama periode <strong>2021-2026</strong>"

# Hitung KPI
total_robusta = filtered_df['Produksi Robusta (Ton)'].sum()
total_arabika = filtered_df['Produksi Arabika (Ton)'].sum()
total_semua = total_robusta + total_arabika

# Format Angka ala JavaScript (ID Locale)
def fmt(num):
    return f"{num:,.0f}".replace(",", ".")

# --- KONTEN UTAMA HALAMAN ---

# Header Judul
col_h1, col_h2 = st.columns([3, 1])
with col_h1:
    st.markdown("<h1 style='font-size: 32px; color: #fff; margin-bottom: 0;'>Produksi Kopi Nasional</h1>", unsafe_allow_html=True)
    st.markdown("<p style='color: #90a4ae; margin-top: 5px;'>Dashboard Interaktif Perkebunan Indonesia</p>", unsafe_allow_html=True)

st.markdown("<hr style='border-color: rgba(255,255,255,0.1); margin-bottom: 25px;'>", unsafe_allow_html=True)

# ----------------- TAB 1: OVERVIEW & PROVINSI -----------------
if menu == "📊 Overview & Provinsi":
    # KPI Section (3 Kartu)
    st.markdown(f"""
        <div class="kpi-section">
            <div class="kpi-card" style="border-bottom: 4px solid #3498db;">
                <h3>Total Keseluruhan</h3>
                <h2>{fmt(total_semua)}</h2>
                <span class="badge">Ton</span>
            </div>
            <div class="kpi-card" style="border-bottom: 4px solid #f1c40f;">
                <h3>Total Robusta</h3>
                <h2>{fmt(total_robusta)}</h2>
                <span class="badge">Ton</span>
            </div>
            <div class="kpi-card" style="border-bottom: 4px solid #e67e22;">
                <h3>Total Arabika</h3>
                <h2>{fmt(total_arabika)}</h2>
                <span class="badge">Ton</span>
            </div>
        </div>
    """, unsafe_allow_html=True)

    # Chart & Insight Layout (2 Kolom)
    c_chart, c_insight = st.columns([2, 1])

    with c_chart:
        st.markdown('<div class="card-container">', unsafe_allow_html=True)
        st.markdown("<h3 style='color: #fff; font-size: 18px; margin-bottom: 20px;'>🏆 Top 10 Provinsi Penghasil Kopi</h3>", unsafe_allow_html=True)
        
        # Kalkulasi Top 10 Provinsi (Sesuai Logika JS / Backend Kamu)
        filtered_df['Total Produksi'] = filtered_df['Produksi Robusta (Ton)'] + filtered_df['Produksi Arabika (Ton)']
        prov_grouped = filtered_df.groupby('Provinsi')[['Produksi Robusta (Ton)', 'Produksi Arabika (Ton)', 'Total Produksi']].sum().reset_index()
        prov_top10 = prov_grouped.sort_values(by='Total Produksi', ascending=False).head(10)

        labels = prov_top10['Provinsi'].tolist()
        robusta_vals = prov_top10['Produksi Robusta (Ton)'].tolist()
        arabika_vals = prov_top10['Produksi Arabika (Ton)'].tolist()

        # Render ECharts Provinsi (Persis seperti script.js kamu)
        prov_option = {
            "backgroundColor": "transparent",
            "tooltip": {"trigger": "axis", "axisPointer": {"type": "shadow"}},
            "legend": {"data": ["Robusta", "Arabika"], "textStyle": {"color": "#e0e0e0"}, "top": 0},
            "grid": {"left": "3%", "right": "4%", "bottom": "15%", "containLabel": True},
            "xAxis": {"type": "category", "data": labels, "axisLabel": {"color": "#e0e0e0", "rotate": 25}},
            "yAxis": {"type": "value", "axisLabel": {"color": "#e0e0e0"}, "splitLine": {"lineStyle": {"color": "rgba(255,255,255,0.05)"}}},
            "series": [
                {"name": "Robusta", "type": "bar", "data": robusta_vals, "itemStyle": {"color": "#f1c40f", "borderRadius": [4, 4, 0, 0]}},
                {"name": "Arabika", "type": "bar", "data": arabika_vals, "itemStyle": {"color": "#e67e22", "borderRadius": [4, 4, 0, 0]}}
            ]
        }
        st_echarts(options=prov_option, height="400px")
        st.markdown('</div>', unsafe_allow_html=True)

    with c_insight:
        st.markdown('<div class="card-container" style="display: flex; flex-direction: column; justify-content: center;">', unsafe_allow_html=True)
        st.markdown("<h3 style='color: #f1c40f; margin-bottom: 20px;'>💡 Analisis EduGrowth</h3>", unsafe_allow_html=True)
        
        # Logika Dinamis Insight Otomatis (AI-Generated Simulation dari JS kamu)
        if len(labels) > 0:
            top_rob_prov = labels[robusta_vals.index(max(robusta_vals))] if robusta_vals else "N/A"
            top_rob_val = max(robusta_vals) if robusta_vals else 0
            top_ara_prov = labels[arabika_vals.index(max(arabika_vals))] if arabika_vals else "N/A"
            top_ara_val = max(arabika_vals) if arabika_vals else 0

            st.markdown(f"""
                <div style="color: #e0e0e0; line-height: 1.7; font-size: 14.5px; text-align: justify;">
                    <p>Berdasarkan data {periode_teks}, <strong>{top_rob_prov}</strong> memimpin sebagai produsen <strong>Kopi Robusta</strong> terbesar dengan total produksi mencapai <strong style="color: #f1c40f;">{fmt(top_rob_val)} Ton</strong>.</p>
                    <p>Di sisi lain, untuk pasar <strong>Kopi Arabika</strong>, wilayah <strong>{top_ara_prov}</strong> mendominasi dengan angka produksi sebesar <strong style="color: #e67e22;">{fmt(top_ara_val)} Ton</strong>.</p>
                    <p>Secara umum, provinsi-provinsi di Pulau Sumatera mendominasi 10 besar sentra kopi nasional, menjadikannya tulang punggung suplai komoditas kopi di Indonesia.</p>
                    <hr style="border-color: rgba(255,255,255,0.1); margin: 15px 0;">
                    <p style="font-size: 12.5px; color: #90a4ae;"><em>*Teks analisis ini dihasilkan secara otomatis (AI-Generated) berdasarkan filter data yang dipilih.</em></p>
                </div>
            """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

# ----------------- TAB 2: TREN TAHUNAN -----------------
elif menu == "📈 Tren Tahunan":
    st.markdown('<div class="card-container">', unsafe_allow_html=True)
    st.markdown("<h3 style='color: #fff; font-size: 18px; margin-bottom: 20px;'>📈 Tren Produksi Kopi (Tahun ke Tahun)</h3>", unsafe_allow_html=True)
    
    trend_grouped = trend_df.groupby('Tahun')[['Produksi Robusta (Ton)', 'Produksi Arabika (Ton)']].sum().reset_index()
    trend_labels = trend_grouped['Tahun'].astype(int).tolist()
    trend_rob = trend_grouped['Produksi Robusta (Ton)'].tolist()
    trend_ara = trend_grouped['Produksi Arabika (Ton)'].tolist()

    trend_option = {
        "backgroundColor": "transparent",
        "tooltip": {"trigger": "axis"},
        "legend": {"data": ["Robusta", "Arabika"], "textStyle": {"color": "#e0e0e0"}},
        "grid": {"left": "3%", "right": "4%", "bottom": "10%", "containLabel": True},
        "xAxis": {"type": "category", "boundaryGap": False, "data": trend_labels, "axisLabel": {"color": "#e0e0e0"}},
        "yAxis": {"type": "value", "axisLabel": {"color": "#e0e0e0"}, "splitLine": {"lineStyle": {"color": "rgba(255,255,255,0.05)"}}},
        "series": [
            {"name": "Robusta", "type": "line", "data": trend_rob, "smooth": True, "lineStyle": {"width": 3, "color": "#f1c40f"}, "itemStyle": {"color": "#f1c40f"}},
            {"name": "Arabika", "type": "line", "data": trend_ara, "smooth": True, "lineStyle": {"width": 3, "color": "#e67e22"}, "itemStyle": {"color": "#e67e22"}}
        ]
    }
    st_echarts(options=trend_option, height="500px")
    st.markdown('</div>', unsafe_allow_html=True)

# ----------------- TAB 3: DATA SPREADSHEET -----------------
elif menu == "📄 Data Spreadsheet":
    st.markdown('<div class="card-container">', unsafe_allow_html=True)
    st.markdown("<h3 style='color: #fff; font-size: 18px; margin-bottom: 20px;'>📄 Data Spreadsheet Mentah (Dataset Kopi Nasional)</h3>", unsafe_allow_html=True)
    
    # Tampilkan tabel data bersih ala spreadsheet
    st.dataframe(filtered_df, use_container_width=True, height=500)
    st.markdown('</div>', unsafe_allow_html=True)
