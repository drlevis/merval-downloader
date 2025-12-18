#!/usr/bin/env python3
"""
Script COMPLETO para descargar datos MERVAL desde Yahoo Finance

NOTA IMPORTANTE (2025-12-18):
- Yahoo Finance LIMITÓ acceso a algunos tickers argentinos .BA
- SOLUCIÓN: Usar tickers alternativos que SÍ funcionan:
  • ADRs USA (con conversión ARS → USD si es necesario)
  • Datos de APIs alternativas (en próxima versión)

Acciones DISPONIBLES CONFIRMADAS:
✅ GGAL (ADR USA de GGAL.BA)
✅ BMA (ADR USA de BMA.BA)
✅ AGRO (ADR USA de AGRO.BA)
✅ LOMA (ADR USA de LOMA.BA)
✅ CEPU (ADR USA de CEPU.BA)

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
import traceback

# Silenciar warnings
warnings.filterwarnings('ignore', category=FutureWarning)
warnings.filterwarnings('ignore')

print("="*80)
print("📥 DESCARGADOR MERVAL - ALTERNATIVA")
print("="*80 + "\n")

print("⚠️  NOTA: Yahoo Finance limitó acceso a tickers .BA directos.")
print("   🙅 Solución: Usando ADRs USA (que SÍ funcionan)\n")

# Período: últimos 5 años
fecha_fin = datetime.now()
fecha_inicio = fecha_fin - timedelta(days=365*5)

print(f"📅 Período: {fecha_inicio.strftime('%Y-%m-%d')} a {fecha_fin.strftime('%Y-%m-%d')}\n")

# ACCIONES QUE FUNCIONAN EN YAHOO FINANCE
# Nota: Algunos .BA no tienen datos, pero sus ADRs USA sí
ACCIONES_MERVAL = {
    # BANCOS - FUNCIONAN
    "GGAL": "Grupo Galicia (ADR USA - de GGAL.BA)",
    "BMA": "Banco Macro (ADR USA - de BMA.BA)",
    
    # ENERGÍA
    "YPFD": "YPF (ADR USA - de YPFD.BA)",
    
    # MATERIALES
    "LOMA": "Loma Negra (ADR USA - de LOMA.BA)",
    
    # COMERCIO
    "CEPU": "Central Puerto (ADR USA - de CEPU.BA)",
    
    # AGRONEGOCIOS
    "AGRO": "Adecoagro (ADR USA - de AGRO.BA)",
}

print(f"Acciones confirmadas disponibles: {len(ACCIONES_MERVAL)}")
print("🙅 Usando ADRs USA (cotizan en dólares)\n")
print("⚠️  Para convertir a pesos argentinos: USD × tipo de cambio ARS\n")

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
        print(f"   Descargando desde {fecha_inicio.strftime('%Y-%m-%d')}...")
        
        df_precios = yf.download(
            ticker,
            start=fecha_inicio.strftime('%Y-%m-%d'),
            end=fecha_fin.strftime('%Y-%m-%d'),
            progress=False,
            threads=False,
            auto_adjust=False
        )
        
        if df_precios is None or len(df_precios) == 0:
            print(f"   ❌ Sin datos históricos\n")
            resultados.append({
                'Ticker': ticker,
                'Nombre': nombre,
                'Status': '❌ Error',
                'Datos': 0,
                'Archivo': '-'
            })
            continue
        
        # LIMPIAR CSV: Resetear índice
        if isinstance(df_precios.index, pd.DatetimeIndex):
            df_precios = df_precios.reset_index()
        
        if 'Date' in df_precios.columns:
            df_precios.rename(columns={'Date': 'fecha'}, inplace=True)
        elif df_precios.index.name == 'Date':
            df_precios = df_precios.reset_index()
            df_precios.rename(columns={'Date': 'fecha'}, inplace=True)
        
        # Reordenar columnas OHLCV
        cols_esperadas = ['fecha', 'Open', 'High', 'Low', 'Close', 'Adj Close', 'Volume']
        cols_disponibles = [c for c in cols_esperadas if c in df_precios.columns]
        df_precios = df_precios[cols_disponibles]
        
        # CONVERTIR A NUMÉRICO (fix para el error "arg must be a list...")
        for col in ['Open', 'High', 'Low', 'Close', 'Adj Close', 'Volume']:
            if col in df_precios.columns:
                df_precios[col] = pd.to_numeric(df_precios[col], errors='coerce')
        
        # Eliminar NaN
        df_precios = df_precios.dropna(subset=['Open', 'Close'])
        
        # Formatear fecha
        if 'fecha' in df_precios.columns:
            df_precios['fecha'] = pd.to_datetime(df_precios['fecha'])
            df_precios['fecha'] = df_precios['fecha'].dt.strftime('%Y-%m-%d')
        
        if len(df_precios) == 0:
            print(f"   ❌ Datos vacíos después de limpieza\n")
            continue
        
        # Guardar CSV
        filename_precios = f"{ticker}_precios_5A.csv"
        filepath_precios = DATA_DIR / filename_precios
        df_precios.to_csv(filepath_precios, index=False, float_format='%.8f')
        
        print(f"   ✅ Datos: {len(df_precios)} registros")
        print(f"   💾 Guardado: {filename_precios}")
        
        # 2. OBTENER FUNDAMENTALES
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
            print(f"   📊 P/E: {fundamentales['P/E Ratio (Trailing)']}")
            print(f"   💲 Div Yield: {fundamentales['Dividend Yield']}\n")
            
        except Exception as e:
            print(f"   ⚠️  Fundamentales: {str(e)[:30]}\n")
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
        print(f"      Traceback: {traceback.format_exc()[:100]}\n")
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

if resultados:
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
    print("No se encontraron archivos de datos")

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
print(f"\n⚠️  IMPORTANTE:")
print(f"   • Los precios están en DÓLARES (USD)")
print(f"   • Para convertir a pesos: USD × tipo_cambio_ARS")
print(f"   • Próximamente: Datos en pesos argentinos directos\n")