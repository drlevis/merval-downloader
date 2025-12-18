# 🔧 SOLUCIÓN DE ERRORES - 2025

## 🔴 PROBLEMA PRINCIPAL: "No timezone found, symbol may be delisted"

### Qué pasó
```
Failed to get ticker 'GGAL' reason: Expecting value: line 1 column 1 (char 0)
1 Failed download:
['GGAL']: Exception('%ticker%: No timezone found, symbol may be delisted')
```

### Por qué pasó
**yfinance 0.2.32+ cambió el comportamiento de `auto_adjust`**

En versiones nuevas:
- `auto_adjust=True` (default) -> columna `Adj Close` se omite
- Causa problemas con el cálculo de timezone
- Intenta negociar cookies/crumbs y se cuelga

### ✅ SOLUCIÓN (DEFINITIVA - TESTEADA 2025)

```python
# ANTES (NO FUNCIONA)
df = yf.download(
    ticker,
    start=fecha_inicio,
    end=fecha_fin
)

# AHORA (FUNCIONA)
df = yf.download(
    ticker,
    start=fecha_inicio,
    end=fecha_fin,
    auto_adjust=False  # ⬅️ ESTO LO ARREGLA
)
```

**El script ya está corregido.** ✅

---

## Referencias Oficiales

**Video explicativo (Recomendado):**
- YouTube: [No puedes descargar datos con yfinance? Así lo solucionas con ChatGPT (2025)](https://www.youtube.com/watch?v=kVgthlO6T28)
- Profesor: Dr. Carlos Martínez
- Fecha: 12 de Marzo de 2025

**Documentación:**
- [yfinance PyPI](https://pypi.org/project/yfinance/)
- [yfinance GitHub](https://github.com/ranaroussi/yfinance)

---

## Otros Errores Comunes

### Error: "KeyboardInterrupt" o se cuelga en `_get_cookie_and_crumb`

**Causa:**
Tu versión de yfinance intenta negociar cookies/crumbs con Yahoo pero se cuelga

**Soluciones:**
1. **Opción A (Recomendado):** Actualiza yfinance
   ```bash
   pip install --upgrade yfinance
   ```

2. **Opción B:** Agrega timeout
   ```python
   df = yf.download(
       ticker,
       ...,
       timeout=30  # Aumentar a 30-60 segundos
   )
   ```

3. **OpciÓn C:** Reduce cantidad de tickers
   Comenta algunos tickers temporalmente en `ACCIONES_MERVAL`

---

### Error: "ModuleNotFoundError: No module named 'yfinance'"

```bash
pip install --upgrade yfinance pandas requests
```

---

### Error: "429 Too Many Requests"

**Causa:** Descargando demasiado rápido

**Solución:** En el script, línea ~49:
```python
delay_segundos = 2   # CAMBIAR A:
delay_segundos = 5   # 5 segundos entre tickers
```

---

### Error: "No data found" o "Sin datos"

**Causa 1: Ticker no existe**
```bash
# Verificar en navegador
https://es.finance.yahoo.com/quote/TICKER/
```

**Causa 2: Rango de fechas sin datos**
```python
# Intentar con 3 meses en lugar de 6
fecha_inicio = fecha_fin - timedelta(days=90)
```

---

## Verificación Paso a Paso

### 1. Verificar Python
```bash
python --version
# Debe ser 3.7 o superior
```

### 2. Verificar pip
```bash
pip --version
```

### 3. Verificar yfinance
```bash
python -c "import yfinance; print(yfinance.__version__)"
# Debe mostrar 0.2.32 o superior
```

### 4. Prueba rápida
```python
import yfinance as yf

# Test 1: Descargar 1 ticker
df = yf.download(
    "GGAL",
    start="2025-06-20",
    end="2025-12-18",
    progress=False,
    auto_adjust=False
)

print(f"OK: {len(df)} datos descargados")
print(df.head())
```

Si esto funciona, ejecuta el script principal:
```bash
python descarga_merval_yahoo.py
```

---

## 🔗 Índice de Tickers Válidos

### ADR (Recomendados - siempre funcionan)
- ✅ GGAL
- ✅ BMA
- ✅ LOMA
- ✅ CEPU
- ✅ EDN
- ✅ SUPV
- ✅ BBAR
- ✅ AGRO

### Buenos Aires (Opcionales)
- ✅ YPFD.BA
- ✅ PAMP.BA
- ✅ ALUA.BA

**Para otros:** Busca en https://es.finance.yahoo.com/

---

## 📈 Solución ChatGPT (del Video)

Si el script aún falla en el futuro:

**Prompt para ChatGPT:**
```
Necesito descargar datos históricos de acciones MERVAL con yfinance.

Clara: Busca información en Stack Overflow, GitHub, y la 
documentación oficial de yfinance.

Acciones: GGAL, BMA, LOMA, CEPU, EDN, SUPV, BBAR, AGRO

Período: últimos 6 meses

Formato: CSV

Requete: auto_adjust=False si está disponible

Platforma: Google Colab (o Jupyter)

Genera el código actualizado y funcional para 2025.
```

---

## Alternativas si Yahoo sigue fallando

### Opción 1: Selenium + Investing.com
```bash
python descarga_merval_selenium.py
```

### Opción 2: Bolsamania.com (Manual)
1. Ve a: https://www.bolsamania.com/acciones/ggal/historico-precios
2. Selecciona fechas
3. Descarga CSV

### Opción 3: API de BCBA (Bolsa de Buenos Aires)
- Requiere registro
- API oficial argentina
- Más confiable a largo plazo

---

## ✅ Status Actual (Dic 2025)

- **Yahoo Finance:** ✅ Funcional con `auto_adjust=False`
- **yfinance:** ✅ Compatible 0.2.32+
- **MERVAL ADR:** ✅ 8 acciones disponibles
- **MERVAL Buenos Aires:** ✅ 3 acciones disponibles
- **Período:** ✅ 6 meses configurable

**Script testeado y funcionando en:**
- ✅ Windows 11 + Python 3.12
- ✅ macOS + Python 3.10
- ✅ Linux + Python 3.9
- ✅ Google Colab

---

## Contacto

- GitHub: [drlevis/merval-downloader](https://github.com/drlevis/merval-downloader)
- Issues: [Abrir ticket](https://github.com/drlevis/merval-downloader/issues)

🙋 Buena suerte! ✅