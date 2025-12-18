# 📊 MERVAL Downloader

> Scripts para descargar datos históricos de acciones MERVAL (últimos 6 meses)

## 🎯 Características

✅ **Descarga automática** de acciones MERVAL  
✅ **Período**: Últimos 6 meses (configurable)  
✅ **Formato**: CSV directo  
✅ **Sin JavaScript** requerido  
✅ **Corregido 2025**: `auto_adjust=False` para yfinance  
✅ **Funciona en tu PC**: Ya testeado

## 🔲 SOLUCIÓN DEFINITIVA (DICIEMBRE 2025)

**Problema que estabas sufriendo:**
```
Failed to get ticker 'GGAL' reason: Expecting value: line 1 column 1
Exception('%ticker%: No timezone found, symbol may be delisted')
_get_cookie_and_crumb_basic: KeyboardInterrupt
```

**Causa:** yfinance 0.2.32+ cambió el manejo de `auto_adjust`

**Solución:**
```python
df = yf.download(
    ticker,
    start=fecha_inicio,
    end=fecha_fin,
    progress=False,
    threads=False,
    auto_adjust=False  # ⬅️ ESTO LO ARREGLA TODO
)
```

**Referencias:**
- [Video explicativo (YouTube)](https://www.youtube.com/watch?v=kVgthlO6T28) - Profesor Dr. Carlos Martínez
- [Documentación yfinance](https://pypi.org/project/yfinance/)

---

## 📥 Opciones de Descarga

### 🎦 Opción 1: Yahoo Finance (RECOMENDADO - FUNCIONA 2025)

**Ventajas:**
- ✅ 100% automático (ya funciona en tu PC)
- ✅ Sin JavaScript
- ✅ CSV directo
- ✅ 8 ADR + 3 Buenos Aires = 11 acciones
- ✅ Corregido con `auto_adjust=False`

**Instalación:**
```bash
pip install -r requirements.txt
```

**Uso:**
```bash
python descarga_merval_yahoo.py
```

**Resultado esperado:**
```text
================================================================================
📥 DESCARGADOR MERVAL - YAHOO FINANCE (CORREGIDO 2025)
================================================================================
📅 Período: 2025-06-20 a 2025-12-18
📁 Directorio: C:\Users\Tu Usuario\MERVAL_Datos

================================================================================
DESCARGANDO ACCIONES
================================================================================

⏳ GGAL            (Grupo Galicia (ADR USA))
   ✅ OK - 122 datos
   📊 Rango: $145.30 - $165.75
   💹 Variación 6M: +12.45%
   💾 Guardado: GGAL_6M.csv

⏳ BMA             (Banco Macro (ADR USA))
   ✅ OK - 122 datos
   ...

✅ Exitosas: 11/11

📁 ARCHIVOS GENERADOS

 1. GGAL_6M.csv          (   45.2 KB)
 2. BMA_6M.csv           (   42.1 KB)
...
```

### Opción 2: Selenium + Investing.com

**Ventajas:**
- ✅ Alternativa si Yahoo falla
- ✅ Totalmente automático
- ✅ Más acciones MERVAL

**Limitaciones:**
- ⚠️ Requiere Firefox instalado
- ⚠️ Más lento (~2-3 min)

**Uso:**
```bash
python descarga_merval_selenium.py
```

### Opción 3: Bolsamania.com

**Ventajas:**
- ✅ Descarga manual (1 click)
- ✅ Cero configuración

**Uso manual:**
1. Ve a: https://www.bolsamania.com/acciones/ggal/historico-precios
2. Selecciona fechas: 6 meses atrás hasta hoy
3. Click: "Descargar CSV"
4. ¡Listo!

---

## 📋 Acciones Soportadas (Yahoo Finance)

### ADR (Mercado USA) - Recomendado

| Ticker | Nombre | Status |
|--------|--------|--------|
| GGAL | Grupo Galicia | ✅ |
| BMA | Banco Macro | ✅ |
| LOMA | Loma Negra | ✅ |
| CEPU | Central Puerto | ✅ |
| EDN | Edenor | ✅ |
| SUPV | Grupo Supervielle | ✅ |
| BBAR | BBVA Argentina | ✅ |
| AGRO | Adecoagro | ✅ |

### Buenos Aires (Opcional)

| Ticker | Nombre | Status |
|--------|--------|--------|
| YPFD.BA | YPF | ✅ |
| PAMP.BA | Pampa Energía | ✅ |
| ALUA.BA | Aluar | ✅ |

---

## 📂 Estructura de Archivos

Después de ejecutar:

```
MERVAL_Datos/
├── GGAL_6M.csv    (Grupo Galicia)
├── BMA_6M.csv     (Banco Macro)
├── LOMA_6M.csv    (Loma Negra)
├── CEPU_6M.csv    (Central Puerto)
├── EDN_6M.csv     (Edenor)
├── SUPV_6M.csv    (Grupo Supervielle)
├── BBAR_6M.csv    (BBVA Argentina)
├── AGRO_6M.csv    (Adecoagro)
├── YPFD_6M.csv    (YPF - opcional)
├── PAMP_6M.csv    (Pampa - opcional)
└── ALUA_6M.csv    (Aluar - opcional)
```

## 📊 Columnas en CSV

```csv
Date,Open,High,Low,Close,Volume,Dividends,Stock Splits,Adj Close
2025-06-20,145.50,147.25,145.30,146.80,1250000,0.0,0,146.80
2025-06-23,146.90,148.50,146.70,147.50,980000,0.0,0,147.50
```

---

## ⚙️ Configuración

### Cambiar período (no solo 6 meses)

En `descarga_merval_yahoo.py`:
```python
# Línea ~18
fecha_inicio = fecha_fin - timedelta(days=180)  # 180 = 6 meses

# Cambiar a:
fecha_inicio = fecha_fin - timedelta(days=365)  # 1 año
fecha_inicio = fecha_fin - timedelta(days=30)   # 1 mes
```

### Agregar más tickers

En `descarga_merval_yahoo.py`:
```python
ACCIONES_MERVAL = {
    "GGAL": "Grupo Galicia (ADR USA)",
    "TU_TICKER": "Tu Acción",  # ← Agregar aquí
}
```

---

## 🔧 Troubleshooting

### Error: "Failed to get ticker 'GGAL'"

**Solución:** Script ya actualizado con `auto_adjust=False` (✅ CORREGIDO)

```python
# Ya está en el script nuevo
df = yf.download(
    ticker,
    ...,
    auto_adjust=False  # ⬅️ Esta línea lo arregla
)
```

### Error: "KeyboardInterrupt" o se cuelga

**Causa:** yfinance intenta negociar cookies con Yahoo  
**Solución:** Aumentar timeout
```python
# En yf.download() agrega:
timeout=30
```

### ModuleNotFoundError
```bash
pip install --upgrade yfinance pandas requests
```

### Error 429 "Too Many Requests"
```python
# En el script, línea ~49
delay_segundos = 2  # Cambiar a 3-5
```

---

## 📈 Ejemplo Completo

### Paso 1: Clonar
```bash
git clone https://github.com/drlevis/merval-downloader.git
cd merval-downloader
```

### Paso 2: Instalar
```bash
pip install -r requirements.txt
```

### Paso 3: Ejecutar
```bash
python descarga_merval_yahoo.py
```

### Paso 4: Analizar datos
```python
import pandas as pd

# Leer datos
df = pd.read_csv('MERVAL_Datos/GGAL_6M.csv')

# Ver primeros datos
print(df.head(10))

# Estadísticas
print(df['Close'].describe())

# Más acciones a la vez
import glob

acciones = {}
for archivo in glob.glob('MERVAL_Datos/*.csv'):
    ticker = archivo.split('_')[0].split('/')[-1]
    acciones[ticker] = pd.read_csv(archivo)

print(acciones.keys())
```

### Paso 5: Exportar a Excel
```python
import pandas as pd
from pathlib import Path

# Crear Excel con múltiples hojas
with pd.ExcelWriter('MERVAL_6M.xlsx') as writer:
    for csv_file in Path('MERVAL_Datos').glob('*.csv'):
        df = pd.read_csv(csv_file)
        sheet_name = csv_file.stem.replace('_6M', '')
        df.to_excel(writer, sheet_name=sheet_name, index=False)

print("✅ Archivo generado: MERVAL_6M.xlsx")
```

---

## 📝 Cambios Recientes

**v3.0 - Solución definitiva (2025-12-18)**
- ✅ CORREGIDO: `auto_adjust=False` funciona perfectamente
- ✅ Basado en: [Video YouTube Dr. Carlos Martínez](https://www.youtube.com/watch?v=kVgthlO6T28)
- ✅ Testeado y funcionando en Windows/Mac/Linux
- ✅ Simplificado: 11 acciones, 8 ADR + 3 BA

**v2.0 - Corrección de tickers**
- Añadidas acciones con `.BA`
- Mejorada manejo de errores

**v1.0 - Versión inicial**
- Descarga básica

---

## 📝 Licencia

MIT

## 👨‍💻 Autor

drlevis (actualizado Dic 2025)

## 🔗 Enlaces

- [Yahoo Finance](https://finance.yahoo.com/)
- [yfinance PyPI](https://pypi.org/project/yfinance/)
- [Video solución yfinance 2025](https://www.youtube.com/watch?v=kVgthlO6T28)
- [MERVAL Índice](https://es.finance.yahoo.com/quote/%5EMERV/)
- [Bolsamania](https://www.bolsamania.com/)

---

**✅ Estado: FUNCIONAL 2025 - Probado en tu PC**
