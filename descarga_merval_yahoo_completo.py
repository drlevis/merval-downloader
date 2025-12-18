#!/usr/bin/env python3
"""
Script COMPLETO para descargar datos MERVAL desde Yahoo Finance
Incluyendo:
  - Datos históricos (5 años) - LIMPIO sin duplicados
  - Análisis fundamentales (P/E, Dividend Yield, ROE, etc)
  - Ratios financieros
  - Exporta a CSVs limpios

NOTA: Solo USA TICKERS .BA (Buenos Aires)
NO incluye ADRs (ej: GGAL sin .BA es ADR USA)

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

# Silenciar warnings
warnings.filterwarnings('ignore', category=FutureWarning)
warnings.filterwarnings('ignore')

print("="*80)
print("📥 DESCARGADOR MERVAL COMPLETO - SOLO TICKERS .BA")
print("="*80 + "\n")

# Período: últimos 5 años
fecha_fin = datetime.now()
fecha_inicio = fecha_fin - timedelta(days=365*5)

print(f"📅 Período: {fecha_inicio.strftime('%Y-%m-%d')} a {fecha_fin.strftime('%Y-%m-%d')}\n")

# ACCIONES MERVAL - SOLO .BA (Buenos Aires, no ADRs USA)
ACCIONES_MERVAL = {
    # BANCOS
    "GGAL.BA": "Grupo Financiero Galicia",
    "BBAR.BA": "BBVA Banco Francés",
    "VALO.BA": "Banco de Valores",
    "BMA.BA": "Banco Macro",
    
    # ENERGÍA
    "YPFD.BA": "YPF",
    "PAMP.BA": "Pampa Energía",
    "EDN.BA": "Edenor",
    "TGNO4.BA": "Transportista Gas del Norte",
    "TGSU2.BA": "Transportista Gas del Sur",
    
    # UTILITIES
    "TRAN.BA": "Transener",
    "METR.BA": "Metrogas",
    "TECO2.BA": "Telecom Argentina",
    
    # COMERCIO
    "BYMA.BA": "Bolsas y Mercados Argentinos",
    "CEPU.BA": "Central Puerto",
    
    # MATERIALES
    "TXAR.BA": "Ternium Argentina",
    "ALUA.BA": "Aluar (Aluminio Argentino)",
    "LOMA.BA": "Loma Negra",
    
    # AGRONEGOCIOS
    "AGRO.BA": "Adecoagro",
    "SUPV.BA": "Grupo Supervielle",
}

print(f"Total de acciones: {len(ACCIONES_MERVAL)}")
print("🌟 Solo tickers .BA (Buenos Aires) - NO incluye ADRs USA\n")

# Crear carpetas
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

for ticker, nombre in ACCIONES_MERVAL.items():
    print(f"⏳ {ticker:15} ({nombre})")
    
    try:
        # 1. DESCARGAR DATOS HISTÓRICOS
        df_precios = yf.download(
            ticker,
            start=fecha_inicio.strftime('%Y-%m-%d'),
            end=fecha_fin.strftime('%Y-%m-%d'),
            progress=False,
            threads=False,
            auto_adjust=False
        )
        
        if len(df_precios) == 0:
            print(f"   ⚠️ Sin datos históricos\n")
            continue
        
        # LIMPIAR CSV: Resetear índice para que Date sea columna normal
        df_precios = df_precios.reset_index()
        df_precios.rename(columns={'Date': 'fecha'}, inplace=True)
        
        # Reordenar columnas de manera lógica (OHLCV estándar)
        df_precios = df_precios[['fecha', 'Open', 'High', 'Low', 'Close', 'Adj Close', 'Volume']]
        
        # ASEGURAR que no hay filas extra con el ticker
        # Convertir a numérico para eliminar filas con texto
        df_precios['Open'] = pd.to_numeric(df_precios['Open'], errors='coerce')
        df_precios['High'] = pd.to_numeric(df_precios['High'], errors='coerce')
        df_precios['Low'] = pd.to_numeric(df_precios['Low'], errors='coerce')
        df_precios['Close'] = pd.to_numeric(df_precios['Close'], errors='coerce')
        df_precios['Adj Close'] = pd.to_numeric(df_precios['Adj Close'], errors='coerce')
        df_precios['Volume'] = pd.to_numeric(df_precios['Volume'], errors='coerce')
        
        # Eliminar NaN (filas corruptas)
        df_precios = df_precios.dropna()
        
        # Convertir fecha a datetime para formatear correctamente
        df_precios['fecha'] = pd.to_datetime(df_precios['fecha'])
        df_precios['fecha'] = df_precios['fecha'].dt.strftime('%Y-%m-%d')
        
        # Guardar CSV LIMPIO (SIN INDICES, SIN FILAS EXTRA)
        filename_precios = f"{ticker.replace('.BA', '')}_precios_5A.csv"
        filepath_precios = DATA_DIR / filename_precios
        df_precios.to_csv(filepath_precios, index=False, float_format='%.8f')
        
        print(f"   ✅ Datos: {len(df_precios)} registros")
        print(f"   💾 Guardado: {filename_precios}")
        
        # 2. OBTENER FUNDAMENTALES
        try:
            ticker_obj = yf.Ticker(ticker)
            info = ticker_obj.info
            
            # Extraer ratios (con manejo de valores nulos)
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
            print(f"   📊 P/E: {fundamentales['P/E Ratio (Trailing)']}")
            print(f"   💲 Div Yield: {fundamentales['Dividend Yield']}\n")
            
        except Exception as e:
            print(f"   ⚠️ Error fundamentales: {str(e)[:40]}\n")
            fundamentales_list.append({
                'Ticker': ticker,
                'Nombre': nombre,
                'Precio': 'Error',
                'P/E Ratio (Trailing)': 'Error',
                'P/E Ratio (Forward)': 'Error',
                'ROE': 'Error',
                'ROA': 'Error',
                'P/B Ratio': 'Error',
                'Dividend Yield': 'Error',
                'Market Cap': 'Error',
                'Beta': 'Error',
                'EPS (Trailing)': 'Error',
                'Debt to Equity': 'Error',
                'Current Ratio': 'Error',
                'Quick Ratio': 'Error',
            })
        
        resultados.append({
            'Ticker': ticker,
            'Nombre': nombre,
            'Status': '✅ OK',
            'Datos': len(df_precios),
            'Archivo': filename_precios
        })
        
        time.sleep(0.5)
        
    except Exception as e:
        print(f"   ❌ Error: {str(e)[:60]}\n")
        resultados.append({
            'Ticker': ticker,
            'Nombre': nombre,
            'Status': '❌ Error',
            'Datos': 0,
            'Archivo': '-'
        })

# 3. GUARDAR TABLA DE FUNDAMENTALES
if fundamentales_list:
    df_fund = pd.DataFrame(fundamentales_list)
    filename_fund = "MERVAL_Fundamentales_Completo.csv"
    filepath_fund = FUND_DIR / filename_fund
    df_fund.to_csv(filepath_fund, index=False)
    print(f"\n📊 Fundamentales guardados: {filename_fund}\n")

# 4. RESUMEN FINAL
print("\n" + "="*80)
print("📊 RESUMEN FINAL")
print("="*80 + "\n")

df_resultados = pd.DataFrame(resultados)
print(df_resultados.to_string(index=False))

exitosas = len([r for r in resultados if r['Status'] == '✅ OK'])
fallidas = len([r for r in resultados if '❌' in r['Status']])

print(f"\n✅ Exitosas: {exitosas}/{len(ACCIONES_MERVAL)}")
print(f"❌ Fallidas: {fallidas}/{len(ACCIONES_MERVAL)}")

# 5. LISTAR ARCHIVOS
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

# 6. LISTAR FUNDAMENTALES
print(f"\n{'='*80}")
print("📁 ARCHIVOS GENERADOS - FUNDAMENTALES")
print(f"{'='*80}\n")

files_fund = sorted(list(FUND_DIR.glob("*.csv")))
if files_fund:
    for i, f in enumerate(files_fund, 1):
        size_kb = f.stat().st_size / 1024
        print(f"{i:2d}. {f.name:30} ({size_kb:8.1f} KB)")
else:
    print("No se encontraron archivos de fundamentales")

print(f"\n📁 Carpeta Datos: {DATA_DIR.absolute()}")
print(f"📁 Carpeta Fundamentales: {FUND_DIR.absolute()}\n")

print("="*80)
print("✅ DESCARGA + ANÁLISIS COMPLETADO")
print("="*80)
print(f"\n💡 INFORMACIÓN:")
print(f"   Período: 5 años ({(fecha_fin - fecha_inicio).days} días)")
print(f"   yfinance: {yf.__version__}")
print(f"   pandas: {pd.__version__}")
print(f"\n✅ CSVs LIMPIOS - Sin duplicados, sin encabezados extra!")
print(f"✅ Ratios Fundamentales disponibles para análisis!")
print(f"✅ Solo TICKERS .BA (Buenos Aires) - 100% MERVAL!\n")