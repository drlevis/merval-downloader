# 🔧 SOLUCIÓN DE ERRORES COMUNES

## Problema: "No timezone found, symbol may be delisted"

### Causa
Los tickers de Yahoo Finance para acciones argentinas REQUIEREN el sufijo `.BA`

### Solución

❌ **INCORRECTO:**
```python
ACCIONES = {
    "GGAL": "Grupo Galicia",
    "BMA": "Banco Macro",
    "YPFD": "YPF",
}
```

✅ **CORRECTO:**
```python
ACCIONES = {
    "GGAL.BA": "Grupo Galicia",
    "BMA.BA": "Banco Macro",
    "YPFD.BA": "YPF",
}
```

### Verificación

Puedes verificar si un ticker es válido visitando:
```
https://es.finance.yahoo.com/quote/GGAL.BA/
https://es.finance.yahoo.com/quote/BMA.BA/
https://es.finance.yahoo.com/quote/YPFD.BA/
```

---

## Problema: "429 Too Many Requests"

### Causa
Yahoo Finance está bloqueando por demasiadas solicitudes rápidas

### Solución

Aumento el `delay_segundos` en el script:

```python
# Línea ~45
delay_segundos = 2   # CAMBIAR A 5 o más
max_retries = 3      # CAMBIAR A 5 o más
```

**Ejemplo:**
```python
# Lento pero seguro
delay_segundos = 10  # 10 segundos entre descargas
max_retries = 5      # Reintentar 5 veces si falla
```

---

## Problema: "Socket timeout" o "Connection refused"

### Causa
Problema de conexión a Internet o servidor de Yahoo está lento

### Soluciones

1. **Aumentar timeout:**
```python
df = yf.download(
    ticker,
    start=fecha_inicio,
    end=fecha_fin,
    progress=False,
    timeout=30,  # ← AGREGAR ESTO
    threads=False
)
```

2. **Usar proxy (si estás en una red corporativa):**
```python
import yfinance as yf

proxies = {
    'http': 'http://proxy.ejemplo.com:8080',
    'https': 'https://proxy.ejemplo.com:8080'
}

df = yf.download(
    ticker,
    session=yfinance.utils.get_session(proxies=proxies),
    start=fecha_inicio,
    end=fecha_fin
)
```

3. **Verificar conexión:**
```bash
# Linux/Mac
ping google.com

# Windows
ping google.com
```

---

## Problema: "ModuleNotFoundError"

### Causa
Librerías no instaladas

### Solución

```bash
# Instalar todas las dependencias
pip install -r requirements.txt

# O instalar individualmente
pip install yfinance pandas requests selenium webdriver-manager
```

---

## Problema: "No data found" o "Sin datos"

### Causa Posible 1: Ticker incorrecto o deslistado

**Solución:**
```bash
# Verificar en navegador
https://es.finance.yahoo.com/quote/TICKER.BA/

# Si muestra "Not Found" o error, usa Selenium
python descarga_merval_selenium.py
```

### Causa Posible 2: Rango de fechas fuera de datos disponibles

**Solución:**
```python
# En lugar de 6 meses, intentar con 3
fecha_inicio = fecha_fin - timedelta(days=90)  # 3 meses

# O más reciente
fecha_inicio = fecha_fin - timedelta(days=30)  # 1 mes
```

---

## Problema: "Script se queda colgado"

### Causa
Gran cantidad de tickers o conexión lenta

### Soluciones

1. **Reducir cantidad de acciones temporalmente:**
```python
ACCIONES_MERVAL = {
    "GGAL.BA": "Grupo Galicia",
    "BMA.BA": "Banco Macro",
    # Comentar el resto temporalmente
}
```

2. **Usar timeout con Ctrl+C:**
```bash
python descarga_merval_yahoo.py
# Si se cuelga, presionar Ctrl+C para detener
```

3. **Ejecutar por separado:**
```python
# Script simplificado para un solo ticker
import yfinance as yf

df = yf.download(
    "GGAL.BA",
    start="2025-06-20",
    end="2025-12-18",
    progress=True,
    timeout=30
)

df.to_csv('GGAL_test.csv')
print(df.head())
```

---

## Verificación Paso a Paso

### 1. Verificar instalación de Python
```bash
python --version
# Debe mostrar Python 3.7 o superior
```

### 2. Verificar pip
```bash
pip --version
# Debe mostrar version
```

### 3. Verificar yfinance
```bash
python -c "import yfinance; print(yfinance.__version__)"
# Debe mostrar versión, ej: 0.2.32
```

### 4. Verificar ticker válido
```python
import yfinance as yf

df = yf.download(
    "GGAL.BA",
    start="2025-06-20",
    end="2025-12-18",
    progress=False
)

print(f"Datos descargados: {len(df)}")
print(df.head())
```

### 5. Si funciona el test anterior, ejecutar:
```bash
python descarga_merval_yahoo.py
```

---

## Índice de Tickers Válidos (Verificados)

Todos estos tickers funcionan en Yahoo Finance con `.BA`:

```
✅ GGAL.BA - Grupo Galicia
✅ YPFD.BA - YPF
✅ BMA.BA - Banco Macro
✅ LOMA.BA - Loma Negra
✅ CEPU.BA - Central Puerto
✅ EDN.BA - Edenor
✅ SUPV.BA - Grupo Supervielle
✅ PAMP.BA - Pampa Energía
✅ ALUA.BA - Aluar
✅ BBAR.BA - BBVA Argentina
✅ MERC.BA - Mercado Libre
✅ COME.BA - Comercial del Plata
```

**Si necesitas otros:** Verifica en https://es.finance.yahoo.com/

---

## Alternativa: Usar Selenium

Si Yahoo Finance sigue dando problemas:

```bash
# Instalar Firefox
# Linux: sudo apt-get install firefox
# Mac: brew install firefox
# Windows: Descargar de mozilla.org

# Ejecutar script Selenium
python descarga_merval_selenium.py
```

---

## Contacto / Soporte

- **GitHub Issues:** [drlevis/merval-downloader/issues](https://github.com/drlevis/merval-downloader/issues)
- **Reddit:** r/merval
- **Discord:** Comunidades de inversores argentinos

🙋 Buena suerte con tus descargas!  ✅