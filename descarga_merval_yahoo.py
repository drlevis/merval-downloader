#!/usr/bin/env python3
"""
Script para descargar datos históricos de acciones MERVAL desde Yahoo Finance
Período: Últimos 6 meses (configurable)
Funciona: 100% automático, sin JavaScript requerido
Instala primero:
  pip install yfinance pandas requests
"""

import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta
import time
import sys
from pathlib import Path

print("="*80)
print("📥 DESCARGADOR MERVAL - YAHOO FINANCE")
print("="*80 + "\n")

# Período: últimos 6 meses
fecha_fin = datetime.now()
fecha_inicio = fecha_fin - timedelta(days=180)

print(f"📅 Período: {fecha_inicio.strftime('%Y-%m-%d')} a {fecha_fin.strftime('%Y-%m-%d')}\n")

# Acciones MERVAL disponibles en Yahoo Finance
ACCIONES_MERVAL = {
    "GGAL": "Grupo Galicia (ADR)",
    "YPFD.BA": "YPF",
    "BMA": "Banco Macro (ADR)",
    "LOMA": "Loma Negra (ADR)",
    "CEPU": "Central Puerto (ADR)",
    "EDN": "Edenor (ADR)",
    "SUPV": "Grupo Supervielle (ADR)",
    "PAMP.BA": "Pampa Energía",
    "ALUA.BA": "Aluar (ADR)",
    "BBAR": "BBVA Argentina (ADR)",
    "AGRO": "Adecoagro (ADR)",
}

# Crear carpeta para descargas
DOWNLOAD_DIR = Path("MERVAL_Datos")
DOWNLOAD_DIR.mkdir(exist_ok=True)

print(f"📁 Directorio: {DOWNLOAD_DIR.absolute()}\n")
print("="*80)
print("DESCARGANDO ACCIONES")
print("="*80 + "\n")

resultados = []
delay_segundos = 2  # Delay entre descargas para evitar rate limiting

for ticker, nombre in ACCIONES_MERVAL.items():
    print(f"⏳ {ticker:12} ({nombre})")
    
    try:
        # Descarga datos con yfinance
        df = yf.download(
            ticker,
            start=fecha_inicio.strftime('%Y-%m-%d'),
            end=fecha_fin.strftime('%Y-%m-%d'),
            progress=False,
            threads=False
        )
        
        if len(df) > 0:
            # Información descargada
            precio_actual = df['Close'].iloc[-1]
            precio_min = df['Low'].min()
            precio_max = df['High'].max()
            variacion_6m = ((precio_actual - df['Close'].iloc[0]) / df['Close'].iloc[0]) * 100
            
            print(f"   ✅ OK - {len(df)} datos")
            print(f"   📊 Rango: ${precio_min:.2f} - ${precio_max:.2f}")
            print(f"   💹 Variación 6M: {variacion_6m:+.2f}%")
            
            # Guardar CSV
            filename = f"{ticker.replace('.BA', '')}_6M.csv"
            filepath = DOWNLOAD_DIR / filename
            df.to_csv(filepath)
            
            print(f"   💾 Guardado: {filename}\n")
            
            resultados.append({
                'Ticker': ticker,
                'Nombre': nombre,
                'Status': '✅ OK',
                'Datos': len(df),
                'Inicio': df.index.min().strftime('%Y-%m-%d'),
                'Fin': df.index.max().strftime('%Y-%m-%d'),
                'Precio': f"${precio_actual:.2f}",
                'Var6M': f"{variacion_6m:+.2f}%",
                'Archivo': filename
            })
            
        else:
            print(f"   ⚠️ Sin datos\n")
            resultados.append({
                'Ticker': ticker,
                'Nombre': nombre,
                'Status': '⚠️ Sin datos',
                'Datos': 0,
                'Inicio': '-',
                'Fin': '-',
                'Precio': '-',
                'Var6M': '-',
                'Archivo': '-'
            })
        
        # Delay para evitar rate limiting
        time.sleep(delay_segundos)
        
    except Exception as e:
        print(f"   ❌ Error: {str(e)[:60]}\n")
        resultados.append({
            'Ticker': ticker,
            'Nombre': nombre,
            'Status': '❌ Error',
            'Datos': 0,
            'Inicio': '-',
            'Fin': '-',
            'Precio': '-',
            'Var6M': '-',
            'Archivo': '-'
        })

# Resumen final
print("\n" + "="*80)
print("📊 RESUMEN FINAL")
print("="*80 + "\n")

df_resultados = pd.DataFrame(resultados)
print(df_resultados.to_string(index=False))

# Estadísticas
exitosas = len([r for r in resultados if r['Status'] == '✅ OK'])
fallidas = len([r for r in resultados if '❌' in r['Status']])

print(f"\n✅ Exitosas: {exitosas}/{len(ACCIONES_MERVAL)}")
print(f"❌ Fallidas: {fallidas}/{len(ACCIONES_MERVAL)}")

# Listar archivos
print(f"\n{'='*80}")
print("📁 ARCHIVOS GENERADOS")
print(f"{'='*80}\n")

files = sorted(list(DOWNLOAD_DIR.glob("*.csv")))
if files:
    for i, f in enumerate(files, 1):
        size_kb = f.stat().st_size / 1024
        print(f"{i:2d}. {f.name:20} ({size_kb:8.1f} KB)")
else:
    print("No se encontraron archivos")

print(f"\n📁 Carpeta: {DOWNLOAD_DIR.absolute()}\n")

print("="*80)
print("✅ DESCARGA COMPLETADA")
print("="*80)