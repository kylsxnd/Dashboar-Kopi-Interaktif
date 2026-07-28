from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

def load_and_clean_data():
    df = pd.read_excel('Dataset_Kopi_Nasional_Wide_Format_2021_2026.xlsx')
    df['Produksi Robusta (Ton)'] = pd.to_numeric(df['Produksi Robusta (Ton)'], errors='coerce').fillna(0)
    df['Produksi Arabika (Ton)'] = pd.to_numeric(df['Produksi Arabika (Ton)'], errors='coerce').fillna(0)
    return df

@app.get("/api/years")
def get_years():
    df = load_and_clean_data()
    years = sorted(df['Tahun'].dropna().unique().astype(int).tolist())
    return {"years": years}

@app.get("/api/kpi")
def get_kpi(year: int = Query(None)):
    df = load_and_clean_data()
    if year:
        df = df[df['Tahun'] == year]
        
    total_robusta = df['Produksi Robusta (Ton)'].sum()
    total_arabika = df['Produksi Arabika (Ton)'].sum()
    return {
        "total_robusta": round(total_robusta),
        "total_arabika": round(total_arabika),
        "total_semua": round(total_robusta + total_arabika)
    }

@app.get("/api/chart/provinsi")
def get_chart_provinsi(year: int = Query(None)):
    df = load_and_clean_data()
    if year:
        df = df[df['Tahun'] == year]
        
    df['Total Produksi'] = df['Produksi Robusta (Ton)'] + df['Produksi Arabika (Ton)']
    df_grouped = df.groupby('Provinsi')[['Produksi Robusta (Ton)', 'Produksi Arabika (Ton)', 'Total Produksi']].sum().reset_index()
    df_top10 = df_grouped.sort_values(by='Total Produksi', ascending=False).head(10)
    
    return {
        "labels": df_top10['Provinsi'].tolist(),
        "robusta": df_top10['Produksi Robusta (Ton)'].tolist(),
        "arabika": df_top10['Produksi Arabika (Ton)'].tolist()
    }

# API Tren Progresif (Tampil dari awal hingga tahun yang difilter)
@app.get("/api/chart/trend")
def get_chart_trend(year: int = Query(None)):
    df = load_and_clean_data()
    if year:
        df = df[df['Tahun'] <= year]
        
    df_grouped = df.groupby('Tahun')[['Produksi Robusta (Ton)', 'Produksi Arabika (Ton)']].sum().reset_index()
    
    return {
        "labels": df_grouped['Tahun'].astype(int).tolist(),
        "robusta": df_grouped['Produksi Robusta (Ton)'].tolist(),
        "arabika": df_grouped['Produksi Arabika (Ton)'].tolist()
    }

@app.get("/api/raw-data")
def get_raw_data(year: int = Query(None)):
    df = load_and_clean_data()
    if year:
        df = df[df['Tahun'] == year]
        
    df = df.fillna("") 
    return df.to_dict(orient="records")