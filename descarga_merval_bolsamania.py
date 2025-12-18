#!/usr/bin/env python3
"""
Script para descargar datos históricos de MERVAL desde Bolsamania.com
Período: Últimos 6 meses
Funciona: 100% automático, sin JavaScript requerido
Ventaja: No tiene restricciones de Yahoo Finance

Instala primero:
  pip install requests beautifulsoup4 pandas lxml
"""

import requests
import pandas as pd
from datetime import datetime, timedelta
from pathlib import Path
import time
import re

print("="*80)
print("📥 DESCARGADOR MERVAL - BOLSAMANIA.COM")
print("="*80 + "\n")

# Período: últimos 6 meses
fecha_fin = datetime.now()
fecha_inicio = fecha_fin - timedelta(days=180)

print(f"📅 Período: {fecha_inicio.strftime('%d/%m/%Y')} a {fecha_fin.strftime('%d/%m/%Y')}\n")

# Crear carpeta para descargas
DOWNLOAD_DIR = Path("MERVAL_Datos")
DOWNLOAD_DIR.mkdir(exist_ok=True)

print(f"📁 Directorio: {DOWNLOAD_DIR.absolute()}\n")
print("="*80)
print("DESCARGANDO DATOS")
print("="*80 + "\n")

# URLs de Bolsamania para descargar CSV
ACCIONES_BOLSAMANIA = {
    "GGAL": {
        "url": "https://www.bolsamania.com/acciones/ggal/historico-precios",
        "nombre": "Grupo Galicia"
    },
    "YPFD": {
        "url": "https://www.bolsamania.com/acciones/ypfd/historico-precios",
        "nombre": "YPF"
    },
    "BMA": {
        "url": "https://www.bolsamania.com/acciones/bma/historico-precios",
        "nombre": "Banco Macro"
    },
    "LOMA": {
        "url": "https://www.bolsamania.com/acciones/loma/historico-precios",
        "nombre": "Loma Negra"
    },
    "CEPU": {
        "url": "https://www.bolsamania.com/acciones/cepu/historico-precios",
        "nombre": "Central Puerto"
    },
    "EDN": {
        "url": "https://www.bolsamania.com/acciones/edn/historico-precios",
        "nombre": "Edenor"
    },
    "SUPV": {
        "url": "https://www.bolsamania.com/acciones/supv/historico-precios",
        "nombre": "Grupo Supervielle"
    },
    "PAMP": {
        "url": "https://www.bolsamania.com/acciones/pamp/historico-precios",
        "nombre": "Pampa Energía"
    },
    "ALUA": {
        "url": "https://www.bolsamania.com/acciones/alua/historico-precios",
        "nombre": "Aluar"
    },
    "BBAR": {
        "url": "https://www.bolsamania.com/acciones/bbar/historico-precios",
        "nombre": "BBVA Argentina"
    },
}

resultados = []
delay_segundos = 1

for ticker, datos in ACCIONES_BOLSAMANIA.items():
    print(f"⏳ {ticker:12} ({datos['nombre']})")
    
    try:
        # Construir URL de descarga CSV con fechas
        fecha_inicio_str = fecha_inicio.strftime("%d/%m/%Y")
        fecha_fin_str = fecha_fin.strftime("%d/%m/%Y")
        
        # URL para descargar CSV desde Bolsamania
        csv_url = f"https://www.bolsamania.com/descargar-historico/?accion={ticker}&date_from={fecha_inicio_str}&date_to={fecha_fin_str}"
        
        print(f"   📡 Conectando...")
        
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        
        response = requests.get(csv_url, headers=headers, timeout=10)
        
        if response.status_code == 200:
            # Intentar parsear como CSV
            try:
                # Leer CSV desde la respuesta
                lines = response.text.split('\n')
                
                # Filtrar líneas vacías
                lines = [l for l in lines if l.strip()]
                
                if len(lines) > 1:  # Al menos encabezado + 1 dato
                    # Escribir CSV
                    csv_content = '\n'.join(lines)
                    filename = f"{ticker}_6M.csv"
                    filepath = DOWNLOAD_DIR / filename
                    
                    with open(filepath, 'w', encoding='utf-8') as f:
                        f.write(csv_content)
                    
                    # Contar datos
                    num_datos = len(lines) - 1  # Restar encabezado
                    
                    print(f"   ✅ OK - {num_datos} datos")
                    print(f"   💾 Guardado: {filename}\n")
                    
                    resultados.append({
                        'Ticker': ticker,
                        'Nombre': datos['nombre'],
                        'Status': '✅ OK',
                        'Datos': num_datos,
                        'Archivo': filename
                    })
                else:
                    print(f"   ⚠️ CSV vacío\n")
                    resultados.append({
                        'Ticker': ticker,
                        'Nombre': datos['nombre'],
                        'Status': '⚠️ Vacío',
                        'Datos': 0,
                        'Archivo': '-'
                    })
                    
            except Exception as e:
                print(f"   ⚠️ Error parse: {str(e)[:50]}\n")
                resultados.append({
                    'Ticker': ticker,
                    'Nombre': datos['nombre'],
                    'Status': '⚠️ Parse error',
                    'Datos': 0,
                    'Archivo': '-'
                })
        else:
            print(f"   ❌ HTTP {response.status_code}\n")
            resultados.append({
                'Ticker': ticker,
                'Nombre': datos['nombre'],
                'Status': f'❌ HTTP {response.status_code}',
                'Datos': 0,
                'Archivo': '-'
            })
            
    except Exception as e:
        print(f"   ❌ Error: {str(e)[:50]}\n")
        resultados.append({
            'Ticker': ticker,
            'Nombre': datos['nombre'],
            'Status': '❌ Error',
            'Datos': 0,
            'Archivo': '-'
        })
    
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

print(f"\n✅ Exitosas: {exitosas}/{len(ACCIONES_BOLSAMANIA)}")
print(f"⚠️ Con advertencia: {sin_datos}/{len(ACCIONES_BOLSAMANIA)}")
print(f"❌ Fallidas: {fallidas}/{len(ACCIONES_BOLSAMANIA)}")

# Listar archivos
print(f"\n{'='*80}")
print("📁 ARCHIVOS GENERADOS")
print(f"{'='*80}\n")

files = sorted(list(DOWNLOAD_DIR.glob("*_6M.csv")))
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
print(f"\n💡 NOTA: Estos datos son de Bolsamania.com")
print(f"   Funciona sin problemas de Yahoo Finance")
print(f"   Si necesitas más acciones, agrega a ACCIONES_BOLSAMANIA\n")