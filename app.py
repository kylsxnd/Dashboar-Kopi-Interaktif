import streamlit as st
import pandas as pd

# Konfigurasi Halaman
st.set_page_config(
    page_title="Dashboard Kinerja Produksi Kopi Nasional",
    page_icon="☕",
    layout="wide"
)

st.title("☕ Dashboard Kinerja Produksi Kopi Nasional (2021–2026)")
st.markdown("Aplikasi web interaktif untuk memantau tren dan statistik produksi komoditas kopi Robusta dan Arabika di Indonesia.")

# Fungsi Load dan Pembersihan Data dengan Pandas
@st.cache_data
def load_and_clean_data():
    df = pd.read_excel('Dataset_Kopi_Nasional_Wide_Format_2021_2026.xlsx')
    df['Produksi Robusta (Ton)'] = pd.to_numeric(df['Produksi Robusta (Ton)'], errors='coerce').fillna(0)
    df['Produksi Arabika (Ton)'] = pd.to_numeric(df['Produksi Arabika (Ton)'], errors='coerce').fillna(0)
    return df

try:
    df = load_and_clean_data()
except Exception as e:
    st.error(f"Gagal memuat dataset: {e}")
    st.stop()

# --- SIDEBAR FILTER ---
st.sidebar.header("🎛️ Panel Kontrol & Filter")
years = sorted(df['Tahun'].dropna().unique().astype(int).tolist())
selected_year = st.sidebar.selectbox("Pilih Tahun Analisis", ["Semua Tahun (2021-2026)"] + years)

# Logika Filter Data
if selected_year != "Semua Tahun (2021-2026)":
    filtered_df = df[df['Tahun'] == selected_year]
    trend_df = df[df['Tahun'] <= selected_year]
    periode_teks = f"pada tahun {selected_year}"
else:
    filtered_df = df
    trend_df = df
    periode_teks = "selama periode 2021-2026"

# --- KPI METRICS ---
total_robusta = filtered_df['Produksi Robusta (Ton)'].sum()
total_arabika = filtered_df['Produksi Arabika (Ton)'].sum()
total_semua = total_robusta + total_arabika

col1, col2, col3 = st.columns(3)
col1.metric("📦 Total Produksi Kopi", f"{total_semua:,.0f} Ton")
col2.metric("🟡 Total Kopi Robusta", f"{total_robusta:,.0f} Ton")
col3.metric("🟤 Total Kopi Arabika", f"{total_arabika:,.0f} Ton")

st.markdown("---")

# --- GRAFIK PROVINSI (BAR CHART) ---
st.subheader(f"📊 Top 10 Provinsi Penghasil Kopi Terbesar {periode_teks}")

filtered_df['Total Produksi'] = filtered_df['Produksi Robusta (Ton)'] + filtered_df['Produksi Arabika (Ton)']
prov_grouped = filtered_df.groupby('Provinsi')[['Produksi Robusta (Ton)', 'Produksi Arabika (Ton)', 'Total Produksi']].sum().reset_index()
prov_top10 = prov_grouped.sort_values(by='Total Produksi', ascending=False).head(10)

chart_data = prov_top10.set_index('Provinsi')[['Produksi Robusta (Ton)', 'Produksi Arabika (Ton)']]
st.bar_chart(chart_data)

# --- GRAFIK TREN (LINE CHART) ---
st.subheader("📈 Tren Perkembangan Produksi Kopi Nasional")
trend_grouped = trend_df.groupby('Tahun')[['Produksi Robusta (Ton)', 'Produksi Arabika (Ton)']].sum()
st.line_chart(trend_grouped)

# --- TABEL DATA MENTAH ---
with st.expander("📋 Lihat Tabel Spreadsheet Data Mentah"):
    st.dataframe(filtered_df, use_container_width=True)
