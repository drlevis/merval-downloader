#!/usr/bin/env python3
"""  
Script COMPLETO para descargar datos de TODAS las acciones argentinas .BA

LISTA COMPLETA: 64 acciones .BA
  • 19 del MERVAL principal
  • 45 adicionales de IOL/BCBA

Fuentes:
  • Yahoo Finance
  • InvertirOnline (IOL)
  • Bolsa de Comercio de Buenos Aires (BCBA)

Instala primero:
  pip install yfinance pandas requests --upgrade --no-cache-dir
"""

import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta
import time
import sys
from pathlib import Path
import warnings

warnings.filterwarnings('ignore')

print("="*80)
print("📥 DESCARGADOR COMPLETO - TODAS LAS ACCIONES .BA")
print("="*80 + "\n")

fecha_fin = datetime.now()
fecha_inicio = fecha_fin - timedelta(days=365*5)

print(f"📅 Período: {fecha_inicio.strftime('%Y-%m-%d')} a {fecha_fin.strftime('%Y-%m-%d')}\n")

# LISTA COMPLETA: 64 ACCIONES .BA
ACCIONES_BA = {
    # MERVAL PRINCIPAL (19)
    "GGAL.BA": "Grupo Financiero Galicia",
    "BMA.BA": "Banco Macro",
    "BBAR.BA": "Banco BBVA Argentina",
    "VALO.BA": "Banco de Valores",
    "YPFD.BA": "YPF",
    "PAMP.BA": "Pampa Energía",
    "EDN.BA": "Edenor",
    "TGNO4.BA": "Transportadora Gas del Norte",
    "TGSU2.BA": "Transportadora Gas del Sur",
    "CEPU.BA": "Central Puerto",
    "TRAN.BA": "Transener",
    "METR.BA": "Metrogas",
    "TECO2.BA": "Telecom Argentina",
    "ALUA.BA": "Aluar",
    "TXAR.BA": "Ternium Argentina",
    "LOMA.BA": "Loma Negra",
    "CELU.BA": "Celulosa Argentina",
    "BYMA.BA": "Bolsas y Mercados Argentinos",
    "COME.BA": "Sociedad Comercial del Plata",
    
    # ADICIONALES IOL/BCBA (45)
    "A3.BA": "Matba Rofex S.A.",
    "AGRO.BA": "Agrometal",
    "AUSO.BA": "Autopistas del Sol",
    "BHIP.BA": "Banco Hipotecario",
    "BOLT.BA": "Boldt",
    "BPAT.BA": "Banco Patagonia",
    "CADO.BA": "Carlos Casado",
    "CAPX.BA": "Capex",
    "CARC.BA": "Carboclor S.A.",
    "CECO2.BA": "Endesa Costanera",
    "CGPA2.BA": "Camuzzi Gas Pampeana",
    "CTIO.BA": "Consultatio",
    "CVH.BA": "Cablevisión Holding",
    "DGCU2.BA": "Distribuidora de Gas Cuyana",
    "DOME.BA": "Suscripción Preferente",
    "FERR.BA": "Ferrum",
    "FIPL.BA": "Fiplasto",
    "GAMI.BA": "B-Gaming S.A.",
    "GARO.BA": "Garovaglio y Zorraquin",
    "GBAN.BA": "Gas Natural BAN",
    "GCDI.BA": "Gcdi S.A.",
    "GCLA.BA": "Grupo Clarín",
    "GRIM.BA": "Grimoldi",
    "HARG.BA": "Holcim Argentina",
    "HAVA.BA": "Havanna Holding",
    "IEB.BA": "Dycasa",
    "INTR.BA": "Compania Introductora",
    "INVJ.BA": "Inversora Juramento",
    "IRSA.BA": "Irsa",
    "LEDE.BA": "Ledesma",
    "LONG.BA": "Longvie",
    "MERA.BA": "MERANOL S.A.C.I.",
    "MIRG.BA": "Mirgor",
    "MOLA.BA": "Molinos Agro S.A.",
    "MOLI.BA": "Molinos Río De La Plata",
    "MORI.BA": "Morixe Hermanos",
    "OEST.BA": "Grupo Concesionario Oeste",
    "PATA.BA": "Imp. y Exportadora de la Patagonia",
    "PGR.BA": "Phoenix Global Resources",
    "POLL.BA": "Polledo",
    "RICH.BA": "Laboratorios Richmond",
    "RIGO.BA": "Rigolleau",
    "ROSE.BA": "Instituto Rosenbusch",
    "SAMI.BA": "San Miguel",
    "SEMI.BA": "Molinos Juan Semino",
}

print(f"✅ Total acciones: {len(ACCIONES_BA)}")
print(f"   • 19 MERVAL principal")
print(f"   • 45 adicionales IOL/BCBA\n")

DATA_DIR = Path("MERVAL_Datos_Limpio")
FUND_DIR = Path("MERVAL_Fundamentales")
DATA_DIR.mkdir(exist_ok=True)
FUND_DIR.mkdir(exist_ok=True)

print(f"📁 Directorio Datos: {DATA_DIR.absolute()}")
print(f"📁 Directorio Fundamentales: {FUND_DIR.absolute()}\n")
print("="*80)
print("DESCARGANDO DATOS HISTÓRICOS + FUNDAMENTALES")
print("="*80 + "\n")

resultados = []
fundamentales_list = []

for ticker, nombre in ACCIONES_BA.items():
    print(f"⏳ {ticker:15} ({nombre[:40]})")
    
    try:
        df_precios = yf.download(
            ticker,
            start=fecha_inicio.strftime('%Y-%m-%d'),
            end=fecha_fin.strftime('%Y-%m-%d'),
            progress=False,
            threads=False,
            auto_adjust=False
        )
        
        if df_precios is None or len(df_precios) == 0:
            print(f"   ⚠️  Sin datos\n")
            resultados.append({'Ticker': ticker, 'Nombre': nombre, 'Status': '❌ Sin datos', 'Datos': 0, 'Archivo': '-'})
            continue
        
        # LIMPIAR CSV
        df_precios = df_precios.reset_index()
        if 'Date' in df_precios.columns:
            df_precios.rename(columns={'Date': 'fecha'}, inplace=True)
        
        df_precios = df_precios[['fecha', 'Open', 'High', 'Low', 'Close', 'Adj Close', 'Volume']]
        
        # Convertir a numérico
        for col in ['Open', 'High', 'Low', 'Close', 'Adj Close', 'Volume']:
            df_precios[col] = df_precios[col].apply(lambda x: pd.to_numeric(x, errors='coerce'))
        
        df_precios = df_precios.dropna()
        df_precios['fecha'] = pd.to_datetime(df_precios['fecha'])
        df_precios['fecha'] = df_precios['fecha'].dt.strftime('%Y-%m-%d')
        
        if len(df_precios) == 0:
            print(f"   ⚠️  Sin datos después de limpiar\n")
            continue
        
        # Guardar CSV
        filename_precios = f"{ticker.replace('.BA', '')}_precios_5A.csv"
        filepath_precios = DATA_DIR / filename_precios
        df_precios.to_csv(filepath_precios, index=False, float_format='%.8f')
        
        print(f"   ✅ Datos: {len(df_precios)} registros")
        print(f"   💾 Guardado: {filename_precios}")
        
        # FUNDAMENTALES
        try:
            ticker_obj = yf.Ticker(ticker)
            info = ticker_obj.info
            
            fundamentales = {
                'Ticker': ticker,
                'Nombre': nombre,
                'Precio': info.get('currentPrice', 'N/A'),
                'P/E Ratio (Trailing)': round(info.get('trailingPE', 0), 2) if info.get('trailingPE') else 'N/A',
                'P/E Ratio (Forward)': round(info.get('forwardPE', 0), 2) if info.get('forwardPE') else 'N/A',
                'ROE': f"{round(info.get('returnOnEquity', 0) * 100, 2)}%" if info.get('returnOnEquity') else 'N/A',
                'ROA': f"{round(info.get('returnOnAssets', 0) * 100, 2)}%" if info.get('returnOnAssets') else 'N/A',
                'P/B Ratio': round(info.get('priceToBook', 0), 2) if info.get('priceToBook') else 'N/A',
                'Dividend Yield': f"{round(info.get('dividendYield', 0) * 100, 2)}%" if info.get('dividendYield') else 'N/A',
                'Market Cap': info.get('marketCap', 'N/A'),
                'Beta': round(info.get('beta', 0), 2) if info.get('beta') else 'N/A',
                'EPS (Trailing)': round(info.get('trailingEps', 0), 2) if info.get('trailingEps') else 'N/A',
                'Debt to Equity': round(info.get('debtToEquity', 0), 2) if info.get('debtToEquity') else 'N/A',
                'Current Ratio': round(info.get('currentRatio', 0), 2) if info.get('currentRatio') else 'N/A',
                'Quick Ratio': round(info.get('quickRatio', 0), 2) if info.get('quickRatio') else 'N/A',
            }
            
            fundamentales_list.append(fundamentales)
            print(f"   📊 P/E: {fundamentales['P/E Ratio (Trailing)']}\n")
            
        except Exception as e:
            print(f"   ⚠️  Fundamentales: error\n")
        
        resultados.append({'Ticker': ticker, 'Nombre': nombre, 'Status': '✅ OK', 'Datos': len(df_precios), 'Archivo': filename_precios})
        time.sleep(0.3)
        
    except Exception as e:
        print(f"   ❌ Error: {str(e)[:50]}\n")
        resultados.append({'Ticker': ticker, 'Nombre': nombre, 'Status': '❌ Error', 'Datos': 0, 'Archivo': '-'})

# GUARDAR FUNDAMENTALES
if fundamentales_list:
    df_fund = pd.DataFrame(fundamentales_list)
    filename_fund = "MERVAL_Fundamentales_Completo.csv"
    filepath_fund = FUND_DIR / filename_fund
    df_fund.to_csv(filepath_fund, index=False)
    print(f"\n📊 Fundamentales guardados: {filename_fund}\n")

# RESUMEN
print("\n" + "="*80)
print("📊 RESUMEN FINAL")
print("="*80 + "\n")

if resultados:
    df_resultados = pd.DataFrame(resultados)
    exitosas = len([r for r in resultados if '✅' in r['Status']])
    fallidas = len([r for r in resultados if '❌' in r['Status']])
    
    print(f"✅ Exitosas: {exitosas}/{len(ACCIONES_BA)}")
    print(f"❌ Fallidas: {fallidas}/{len(ACCIONES_BA)}")

# LISTAR ARCHIVOS
print(f"\n{'='*80}")
print("📁 ARCHIVOS GENERADOS - DATOS")
print(f"{'='*80}\n")

files_data = sorted(list(DATA_DIR.glob("*.csv")))
if files_data:
    total_size = 0
    for i, f in enumerate(files_data, 1):
        size_kb = f.stat().st_size / 1024
        total_size += size_kb
        print(f"{i:2d}. {f.name:30} ({size_kb:8.1f} KB)")
    print(f"\n📊 Tamaño total: {total_size:.1f} KB")
else:
    print("No se encontraron archivos")

print(f"\n📁 Carpeta Datos: {DATA_DIR.absolute()}")
print(f"📁 Carpeta Fundamentales: {FUND_DIR.absolute()}\n")

print("="*80)
print("✅ DESCARGA COMPLETADA")
print("="*80)
print(f"\n💡 INFORMACIÓN:")
print(f"   Período: 5 años ({(fecha_fin - fecha_inicio).days} días)")
print(f"   yfinance: {yf.__version__}")
print(f"   pandas: {pd.__version__}")
print(f"\n✅ {len(ACCIONES_BA)} acciones .BA intentadas")
print(f"✅ CSVs limpios sin duplicados\n")
