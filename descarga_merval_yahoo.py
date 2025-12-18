#!/usr/bin/env python3
"""
Script para descargar datos históricos de acciones MERVAL desde Yahoo Finance
Período: Últimos 6 meses (configurable)
Funciona: 100% automático, sin JavaScript requerido

SOLUCIÓN (2025): Usa auto_adjust=False (ver video: youtube.com/watch?v=kVgthlO6T28)
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
print("📥 DESCARGADOR MERVAL - YAHOO FINANCE (CORREGIDO 2025)")
print("="*80 + "\n")

# Período: últimos 6 meses
fecha_fin = datetime.now()
fecha_inicio = fecha_fin - timedelta(days=180)

print(f"📅 Período: {fecha_inicio.strftime('%Y-%m-%d')} a {fecha_fin.strftime('%Y-%m-%d')}\n")

# Acciones MERVAL disponibles en Yahoo Finance
# IMPORTANTE: Usar ADR sin sufijo (GGAL, BMA, etc) o .BA para Buenos Aires
ACCIONES_MERVAL = {
    # ADR (mercado USA)
    "GGAL": "Grupo Galicia (ADR USA)",
    "BMA": "Banco Macro (ADR USA)",
    "LOMA": "Loma Negra (ADR USA)",
    "CEPU": "Central Puerto (ADR USA)",
    "EDN": "Edenor (ADR USA)",
    "SUPV": "Grupo Supervielle (ADR USA)",
    "BBAR": "BBVA Argentina (ADR USA)",
    "AGRO": "Adecoagro (ADR USA)",
    
    # Buenos Aires (si funcionan en tu entorno)
    "YPFD.BA": "YPF (Buenos Aires)",
    "PAMP.BA": "Pampa Energía (Buenos Aires)",
    "ALUA.BA": "Aluar (Buenos Aires)",
}

# Crear carpeta para descargas
DOWNLOAD_DIR = Path("MERVAL_Datos")
DOWNLOAD_DIR.mkdir(exist_ok=True)

print(f"📁 Directorio: {DOWNLOAD_DIR.absolute()}\n")
print("="*80)
print("DESCARGANDO ACCIONES")
print("="*80 + "\n")

resultados = []
delay_segundos = 1  # Delay entre descargas
max_retries = 2     # Intentos máximos

for ticker, nombre in ACCIONES_MERVAL.items():
    print(f"⏳ {ticker:15} ({nombre})")
    
    exito = False
    retry_count = 0
    
    while not exito and retry_count < max_retries:
        try:
            # SOLUCIÓN (2025): auto_adjust=False es crucial para versiones nuevas de yfinance
            df = yf.download(
                ticker,
                start=fecha_inicio.strftime('%Y-%m-%d'),
                end=fecha_fin.strftime('%Y-%m-%d'),
                progress=False,
                threads=False,
                auto_adjust=False  # ← CLAVE: esto arregla el error de timezone
            )
            
            if len(df) > 0:
                # Información descargada
                precio_actual = df['Adj Close'].iloc[-1] if 'Adj Close' in df.columns else df['Close'].iloc[-1]
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
                
                exito = True
                
            else:
                print(f"   ⚠️ Sin datos (intento {retry_count + 1}/{max_retries})\n")
                retry_count += 1
                if retry_count < max_retries:
                    time.sleep(delay_segundos)
                    continue
                else:
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
            
        except Exception as e:
            error_msg = str(e)[:60]
            retry_count += 1
            
            if retry_count < max_retries:
                print(f"   ⚠️ Error (intento {retry_count}/{max_retries}): {error_msg}")
                time.sleep(delay_segundos)
            else:
                print(f"   ❌ Error: {error_msg}\n")
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
        
        # Delay para evitar rate limiting
        if not exito and retry_count < max_retries:
            time.sleep(delay_segundos)
        elif exito:
            time.sleep(delay_segundos)

# Resumen final
print("\n" + "="*80)
print("📊 RESUMEN FINAL")
print("="*80 + "\n")

df_resultados = pd.DataFrame(resultados)
print(df_resultados.to_string(index=False))

# Estadísticas
exitosas = len([r for r in resultados if r['Status'] == '✅ OK'])
fallidas = len([r for r in resultados if '❌' in r['Status']])
sin_datos = len([r for r in resultados if '⚠️' in r['Status']])

print(f"\n✅ Exitosas: {exitosas}/{len(ACCIONES_MERVAL)}")
print(f"⚠️ Sin datos: {sin_datos}/{len(ACCIONES_MERVAL)}")
print(f"❌ Fallidas: {fallidas}/{len(ACCIONES_MERVAL)}")

# Listar archivos
print(f"\n{'='*80}")
print("📁 ARCHIVOS GENERADOS")
print(f"{'='*80}\n")

files = sorted(list(DOWNLOAD_DIR.glob("*.csv")))
if files:
    total_size = 0
    for i, f in enumerate(files, 1):
        size_kb = f.stat().st_size / 1024
        total_size += size_kb
        print(f"{i:2d}. {f.name:20} ({size_kb:8.1f} KB)")
    print(f"\n📊 Tamaño total: {total_size:.1f} KB")
else:
    print("No se encontraron archivos")

print(f"\n📁 Carpeta: {DOWNLOAD_DIR.absolute()}\n")

print("="*80)
print("✅ DESCARGA COMPLETADA")
print("="*80)
print(f"\n💡 NOTA IMPORTANTE:")
print(f"   Este script usa auto_adjust=False (solución 2025)")
print(f"   Si aún obtiene errores, ver: youtube.com/watch?v=kVgthlO6T28\n")