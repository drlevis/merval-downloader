#!/usr/bin/env python3
"""
Script para descargar automáticamente acciones MERVAL desde Investing.com
Usa: Selenium + Firefox (más estable que Chrome)
Instala primero:
  pip install selenium
  pip install webdriver-manager
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.firefox.service import Service as FirefoxService
import time
import os
from pathlib import Path

print("="*80)
print("📥 DESCARGADOR MERVAL - SELENIUM + INVESTING.COM")
print("="*80 + "\n")

# Acciones MERVAL a descargar
ACCIONES = {
    "GGAL": "https://es.investing.com/equities/grupo-financiero-galicia-sa-adr",
    "YPFD": "https://es.investing.com/equities/ypf-sociedad",
    "BMA": "https://es.investing.com/equities/banco-macro-sa",
    "LOMA": "https://es.investing.com/equities/loma-negra-compania-industrial",
    "CEPU": "https://es.investing.com/equities/central-puerto-sa",
    "EDN": "https://es.investing.com/equities/edenor-sa",
    "SUPV": "https://es.investing.com/equities/grupo-supervielle-sa",
    "PAMP": "https://es.investing.com/equities/pampa-energia-sa",
    "ALUA": "https://es.investing.com/equities/aluar-aluminio-argentino-saic",
    "BBAR": "https://es.investing.com/equities/bbva-argentina-sa",
}

# Crear carpeta para descargas
DOWNLOAD_DIR = Path("MERVAL_Descargadas")
DOWNLOAD_DIR.mkdir(exist_ok=True)

print(f"📁 Directorio: {DOWNLOAD_DIR.absolute()}\n")

# Configurar Firefox
options = webdriver.FirefoxOptions()
options.add_argument("--headless")  # Ejecutar sin interfaz
options.add_argument("--no-sandbox")

# Configurar descarga automática
prefs = {
    "browser.download.folderList": 2,
    "browser.download.manager.showWhenStarting": False,
    "browser.download.dir": str(DOWNLOAD_DIR.absolute()),
    "browser.helperApps.neverAsk.saveToDisk": "text/csv,application/csv"
}
options.set_preference("browser.download.folderList", 2)
options.set_preference("browser.download.manager.showWhenStarting", False)
options.set_preference("browser.download.dir", str(DOWNLOAD_DIR.absolute()))

print("Iniciando Firefox...\n")

try:
    driver = webdriver.Firefox(
        service=FirefoxService(GeckoDriverManager().install()),
        options=options
    )
    print("✅ Firefox iniciado\n")
    
    resultados = []
    
    for ticker, url in ACCIONES.items():
        print(f"⏳ Descargando {ticker}...")
        
        try:
            driver.get(url)
            time.sleep(2)
            
            # Busca y hace click en "Datos Históricos"
            try:
                link_historico = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.LINK_TEXT, "Datos Históricos"))
                )
                link_historico.click()
                time.sleep(2)
                
                # Busca el botón de descargar (puede variar según la página)
                try:
                    # Intenta diferentes formas de encontrar el botón
                    descarga = None
                    
                    # Opción 1: Busca por clase
                    try:
                        descarga = driver.find_element(By.CLASS_NAME, "download-csv")
                        descarga.click()
                    except:
                        pass
                    
                    # Opción 2: Busca por data-test
                    if not descarga:
                        try:
                            descarga = driver.find_element(By.CSS_SELECTOR, "[data-test='download']")
                            descarga.click()
                        except:
                            pass
                    
                    # Opción 3: Busca cualquier botón con "descarga" o "export"
                    if not descarga:
                        try:
                            botones = driver.find_elements(By.TAG_NAME, "button")
                            for btn in botones:
                                if "descarga" in btn.text.lower() or "export" in btn.text.lower() or "csv" in btn.text.lower():
                                    btn.click()
                                    descarga = btn
                                    break
                        except:
                            pass
                    
                    time.sleep(3)
                    print(f"  ✅ Descargando...\n")
                    resultados.append({
                        'Ticker': ticker,
                        'Status': '✅ Descargado',
                        'URL': url
                    })
                    
                except Exception as e:
                    print(f"  ⚠️ No se encontró botón descarga: {str(e)[:50]}\n")
                    resultados.append({
                        'Ticker': ticker,
                        'Status': '⚠️ Sin botón',
                        'URL': url
                    })
                    
            except Exception as e:
                print(f"  ❌ Error: {str(e)[:50]}\n")
                resultados.append({
                    'Ticker': ticker,
                    'Status': '❌ Error',
                    'URL': url
                })
                
        except Exception as e:
            print(f"  ❌ No accesible: {str(e)[:50]}\n")
            resultados.append({
                'Ticker': ticker,
                'Status': '❌ No accesible',
                'URL': url
            })
    
    driver.quit()
    print("\n✅ Descargas completadas")
    print(f"📁 Revisa la carpeta: {DOWNLOAD_DIR.absolute()}\n")
    
    # Listar archivos descargados
    print("="*80)
    print("ARCHIVOS DESCARGADOS:")
    print("="*80)
    
    files = list(DOWNLOAD_DIR.glob("*.csv"))
    if files:
        for f in sorted(files):
            size_kb = f.stat().st_size / 1024
            print(f"  ✅ {f.name} ({size_kb:.1f} KB)")
    else:
        print("  ⚠️ No se encontraron archivos CSV")
        print("     (Puede ser que Firefox no descargó automáticamente)")
        print("     → Descarga manual: Click derecho → Guardar como\n")
    
except Exception as e:
    print(f"❌ Error fatal: {str(e)}\n")
    print("SOLUCIÓN:")
    print("1. Instala Firefox: https://www.mozilla.org/firefox/")
    print("2. Ejecuta este script de nuevo\n")

print("\n" + "="*80)
print("✅ SCRIPT FINALIZADO")
print("="*80)