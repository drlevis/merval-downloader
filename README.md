# 📊 MERVAL Downloader

> Scripts para descargar datos históricos de acciones MERVAL (últimos 6 meses)

## 🎯 Características

✅ **Descarga automática** de acciones MERVAL  
✅ **Período**: Últimos 6 meses (configurable)  
✅ **Formato**: CSV directo  
✅ **Sin JavaScript** requerido  
✅ **Retry automático** con delay para evitar rate limiting  
✅ **11 acciones** MERVAL soportadas  

## 📥 Opciones de Descarga

### Opción 1: Yahoo Finance (RECOMENDADO)

**Ventajas:**
- ✅ 100% automático
- ✅ Funciona sin JavaScript
- ✅ Delay integrado para evitar rate limit
- ✅ CSV directo

**Instalación:**
```bash
pip install yfinance pandas requests
```

**Uso:**
```bash
python descarga_merval_yahoo.py
```

**Resultado:**
- Crea carpeta `MERVAL_Datos/`
- Descarga 11 acciones MERVAL
- Genera reportes en la consola
- Tiempo total: ~30 segundos

### Opción 2: Selenium + Investing.com

**Ventajas:**
- ✅ Acceso a todas las acciones MERVAL
- ✅ Datos más completos
- ✅ Totalmente automático

**Limitaciones:**
- ⚠️ Requiere Firefox instalado
- ⚠️ Más lento que Yahoo

**Instalación:**
```bash
pip install selenium webdriver-manager
```

**Uso:**
```bash
python descarga_merval_selenium.py
```

## 📋 Acciones Soportadas (Yahoo Finance)

| Ticker | Nombre | Tipo |
|--------|--------|------|
| GGAL | Grupo Galicia | ADR |
| YPFD.BA | YPF | Local |
| BMA | Banco Macro | ADR |
| LOMA | Loma Negra | ADR |
| CEPU | Central Puerto | ADR |
| EDN | Edenor | ADR |
| SUPV | Grupo Supervielle | ADR |
| PAMP.BA | Pampa Energía | Local |
| ALUA.BA | Aluar | Local |
| BBAR | BBVA Argentina | ADR |
| AGRO | Adecoagro | ADR |

## 📂 Estructura de Archivos

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
└── AGRO_6M.csv
```

## 📊 Columnas en CSV

```
Date,Open,High,Low,Close,Volume
2025-06-20,145.50,147.25,145.30,146.80,1250000
2025-06-23,146.90,148.50,146.70,147.50,980000
...
```

## ⚙️ Configuración

### Cambiar período (no solo 6 meses)

En `descarga_merval_yahoo.py`:
```python
# Cambiar esta línea:
fecha_inicio = fecha_fin - timedelta(days=180)  # 180 = 6 meses

# A:
fecha_inicio = fecha_fin - timedelta(days=365)  # 1 año
fecha_inicio = fecha_fin - timedelta(days=30)   # 1 mes
```

### Agregar más acciones

En `descarga_merval_yahoo.py`:
```python
ACCIONES_MERVAL = {
    "GGAL": "Grupo Galicia (ADR)",
    "TU_TICKER": "Tu Acción",  # ← Agregar aquí
    # ...
}
```

## 🔧 Troubleshooting

### Error: "ModuleNotFoundError: No module named 'yfinance'"
```bash
pip install --upgrade yfinance
```

### Error: "429 Too Many Requests"
```python
# Aumentar delay en el script:
delay_segundos = 5  # Cambiar a 5 segundos
```

### No descarga datos para cierto ticker
- El ticker podría no estar disponible en Yahoo Finance
- Intenta con `.BA` al final (ej: `YPFD.BA`)
- Usa la opción Selenium + Investing.com

## 📈 Ejemplo de Uso

```bash
$ python descarga_merval_yahoo.py

================================================================================
📥 DESCARGADOR MERVAL - YAHOO FINANCE
================================================================================

📅 Período: 2025-06-20 a 2025-12-18

📁 Directorio: /home/usuario/MERVAL_Datos

================================================================================
DESCARGANDO ACCIONES
================================================================================

⏳ GGAL         (Grupo Galicia (ADR))
   ✅ OK - 122 datos
   📊 Rango: $145.30 - $165.75
   💹 Variación 6M: +12.45%
   💾 Guardado: GGAL_6M.csv

⏳ YPFD.BA      (YPF)
   ✅ OK - 122 datos
   📊 Rango: $18.50 - $25.30
   💹 Variación 6M: +8.32%
   💾 Guardado: YPFD_6M.csv

...
```

## 📝 Licencia

MIT

## 👨‍💻 Autor

Creado por drlevis

## 🔗 Enlaces

- [Yahoo Finance](https://finance.yahoo.com/)
- [Investing.com](https://es.investing.com/)
- [yfinance Documentation](https://yfinance.readthedocs.io/)

---

**¿Preguntas?** Abre un issue en GitHub 🐛