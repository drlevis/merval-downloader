# 📊 MERVAL Downloader

> Scripts para descargar datos históricos de acciones MERVAL (últimos 6 meses)

## 🎯 Características

✅ **Descarga automática** de acciones MERVAL  
✅ **Período**: Últimos 6 meses (configurable)  
✅ **Formato**: CSV directo  
✅ **Sin JavaScript** requerido  
✅ **Retry automático** con delay para evitar rate limiting  
✅ **12 acciones** MERVAL soportadas  
✅ **CORREGIDO**: Tickers con .BA para Yahoo Finance

## ⚠️ IMPORTANTE - CORREGIDO

**Problema anterior:** Error `'No timezone found, symbol may be delisted'`  
**Causa:** Tickers sin el sufijo `.BA` (Buenos Aires)  
**Solución:** ACTUALIZADO - Ahora usa tickers correctos con `.BA`

```python
# ANTES (INCORRECTO)
ACCIONES = {
    "GGAL": "Grupo Galicia",     # ❌ No funciona
    "BMA": "Banco Macro",         # ❌ No funciona
}

# AHORA (CORRECTO)
ACCIONES = {
    "GGAL.BA": "Grupo Galicia",   # ✅ Funciona
    "BMA.BA": "Banco Macro",       # ✅ Funciona
}
```

## 📥 Opciones de Descarga

### Opción 1: Yahoo Finance (RECOMENDADO) ⭐ ACTUALIZADO

**Ventajas:**
- ✅ 100% automático
- ✅ Funciona sin JavaScript
- ✅ Delay integrado para evitar rate limit
- ✅ CSV directo
- ✅ Retry automático si falla
- ✅ CORREGIDO: Ahora con tickers .BA

**Instalación:**
```bash
pip install -r requirements.txt
```

**Uso:**
```bash
python descarga_merval_yahoo.py
```

**Resultado esperado:**
```
================================================================================
📥 DESCARGADOR MERVAL - YAHOO FINANCE
================================================================================
📅 Período: 2025-06-20 a 2025-12-18
📁 Directorio: /home/usuario/MERVAL_Datos

================================================================================
DESCARGANDO ACCIONES
================================================================================

⏳ GGAL.BA        (Grupo Galicia (Buenos Aires))
   ✅ OK - 122 datos
   📊 Rango: $1,234.50 - $1,450.75
   💹 Variación 6M: +12.45%
   💾 Guardado: GGAL_6M.csv
⏳ YPFD.BA        (YPF (Buenos Aires))
   ✅ OK - 122 datos
   ...

✅ Exitosas: 12/12
```

### Opción 2: Selenium + Investing.com

**Ventajas:**
- ✅ Acceso a todas las acciones MERVAL
- ✅ Datos más completos
- ✅ Totalmente automático

**Limitaciones:**
- ⚠️ Requiere Firefox instalado
- ⚠️ Más lento que Yahoo (~2-3 minutos)

**Instalación:**
```bash
pip install -r requirements.txt
```

**Uso:**
```bash
python descarga_merval_selenium.py
```

## 📋 Acciones Soportadas

| Ticker | Nombre | Ubicación | Status |
|--------|--------|-----------|--------|
| GGAL.BA | Grupo Galicia | Buenos Aires | ✅ |
| YPFD.BA | YPF | Buenos Aires | ✅ |
| BMA.BA | Banco Macro | Buenos Aires | ✅ |
| LOMA.BA | Loma Negra | Buenos Aires | ✅ |
| CEPU.BA | Central Puerto | Buenos Aires | ✅ |
| EDN.BA | Edenor | Buenos Aires | ✅ |
| SUPV.BA | Grupo Supervielle | Buenos Aires | ✅ |
| PAMP.BA | Pampa Energía | Buenos Aires | ✅ |
| ALUA.BA | Aluar | Buenos Aires | ✅ |
| BBAR.BA | BBVA Argentina | Buenos Aires | ✅ |
| MERC.BA | Mercado Libre Argentina | Buenos Aires | ✅ |
| COME.BA | Comercial del Plata | Buenos Aires | ✅ |

## 📂 Estructura de Archivos

Después de ejecutar el script se crea:

```
MERVAL_Datos/
├── GGAL_6M.csv
├── YPFD_6M.csv
├── BMA_6M.csv
├── LOMA_6M.csv
├── CEPU_6M.csv
├── EDN_6M.csv
├── SUPV_6M.csv
├── PAMP_6M.csv
├── ALUA_6M.csv
├── BBAR_6M.csv
├── MERC_6M.csv
└── COME_6M.csv
```

## 📊 Columnas en CSV

```csv
Date,Open,High,Low,Close,Volume,Adj Close
2025-06-20,1234.50,1247.25,1230.30,1246.80,125000,1246.80
2025-06-23,1246.90,1248.50,1246.70,1247.50,98000,1247.50
...
```

## ⚙️ Configuración

### Cambiar período (no solo 6 meses)

En `descarga_merval_yahoo.py`, línea ~18:
```python
# Cambiar esta línea:
fecha_inicio = fecha_fin - timedelta(days=180)  # 180 = 6 meses

# A:
fecha_inicio = fecha_fin - timedelta(days=365)  # 1 año
fecha_inicio = fecha_fin - timedelta(days=30)   # 1 mes
fecha_inicio = fecha_fin - timedelta(days=90)   # 3 meses
```

### Cambiar delay entre descargas

En `descarga_merval_yahoo.py`, línea ~45:
```python
# Aumentar si obtiene errores 429:
delay_segundos = 2   # Cambiar a 3 o 5
max_retries = 3      # Cambiar a 5 o más
```

### Agregar más acciones

En `descarga_merval_yahoo.py`, línea ~25:
```python
ACCIONES_MERVAL = {
    "GGAL.BA": "Grupo Galicia (Buenos Aires)",
    "TU_TICKER.BA": "Tu Acción",  # ← Agregar aquí
    # ...
}
```

## 🔧 Troubleshooting

### Error: "ModuleNotFoundError: No module named 'yfinance'"
```bash
pip install --upgrade yfinance pandas requests
```

### Error: "429 Too Many Requests"
**Solución:** Aumentar el delay
```python
delay_segundos = 5  # Cambiar a 5-10 segundos
max_retries = 5     # Aumentar reintentos
```

### Error: "No timezone found, symbol may be delisted"
**Causas posibles:**
- ❌ Ticker sin `.BA` (SOLUCIONADO en versión nueva)
- ❌ La acción fue deslistada
- ❌ Ticker incorrecto

**Solución:**
1. Verificar que el ticker tenga `.BA` al final
2. Verificar en Yahoo Finance: https://es.finance.yahoo.com/quote/GGAL.BA/
3. Usar Selenium como alternativa

### No descarga datos para cierto ticker
1. Abre en navegador: `https://es.finance.yahoo.com/quote/TICKER.BA/`
2. Si no aparece, la acción puede estar deslistada
3. Usa el script Selenium + Investing.com como alternativa

### Timeout o conexión lenta
```python
# Aumentar timeout en yf.download():
yf.download(
    ticker,
    start=fecha_inicio,
    end=fecha_fin,
    progress=False,
    timeout=30,  # Agregar esta línea
    threads=False
)
```

## 📈 Ejemplo Completo de Uso

```bash
# 1. Clonar repositorio
git clone https://github.com/drlevis/merval-downloader.git
cd merval-downloader

# 2. Instalar dependencias
pip install -r requirements.txt

# 3. Ejecutar script
python descarga_merval_yahoo.py

# 4. Verificar archivos
ls -lah MERVAL_Datos/

# 5. Abrir en Excel o analizar con Python
import pandas as pd
df = pd.read_csv('MERVAL_Datos/GGAL_6M.csv')
print(df.head())
print(df.describe())
```

## 📈 Exportar a Excel

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

## 📝 Cambios Recientes

**v2.0 - Corrección de tickers (2025-12-18)**
- ✅ CORREGIDO: Tickers ahora con sufijo `.BA`
- ✅ Añadidas 12 acciones MERVAL
- ✅ Mejorada manejo de errores con retry automático
- ✅ Añadido delay configurable
- ✅ Mejor feedback en consola

**v1.0 - Versión inicial**
- Descarga básica de acciones MERVAL

## 📝 Licencia

MIT

## 👨‍💻 Autor

Creado por drlevis

## 🔗 Enlaces

- [Yahoo Finance](https://finance.yahoo.com/)
- [Investing.com](https://es.investing.com/)
- [MERVAL Índice](https://es.finance.yahoo.com/quote/%5EMERV/)
- [yfinance Documentation](https://yfinance.readthedocs.io/)

---

**¿Errores?** 🐛 Abre un issue en GitHub  
**¿Sugerencias?** 👍 Contribuciones bienvenidas