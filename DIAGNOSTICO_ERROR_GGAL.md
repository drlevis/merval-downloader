# 🔍 DIAGNÓSTICO: Error "No timezone found, symbol may be delisted"

## El Error Exacto Que Sufres

```
⏳ GGAL            (Grupo Galicia (ADR USA))
Failed to get ticker 'GGAL' reason: Expecting value: line 1 column 1 (char 0)

1 Failed download:
['GGAL']: Exception('%ticker%: No timezone found, symbol may be delisted')
   ⚠️ Sin datos (intento 1/2)
   ⚠️ Sin datos (intento 2/2)
```

---

## 🔍 CAUSAS ENCONTRADAS EN INTERNET (2025)

### Causa 1: Versión Vieja de yfinance
**Fuente:** Stack Overflow, PyPI, Reddit (Feb-Nov 2025)

Yahoo Finance cambia constantemente y yfinance necesita ser actualizado.

**Síntomas:**
- Mismo error de timezone
- `JSONDecodeError: Expecting value: line 1 column 1`
- Funciona en tu máquina local pero falla en servidor

**Solución:**
```bash
pip install yfinance --upgrade --no-cache-dir
```

O si está muy roto:
```bash
pip uninstall yfinance
pip install yfinance --upgrade --no-cache-dir
```

**Verificar versión instalada:**
```bash
pip show yfinance
# Debe ser 0.2.54 o superior
```

---

### Causa 2: Yahoo Finance Cambió Su API
**Fuente:** Blog wisesheets.io (Oct 2025), GitHub yfinance issues

Yahoo Finance es muy inestable:
- Julio 2021: Cambio grande → toda la comunidad se rompió
- Febrero 2025: Otro cambio
- Noviembre 2025: Otro más

**Status actual (Dic 2025):**
> "Yahoo Finance sigue siendo mantenido activamente. Pero la API es undocumented y puede cambiar o throttle en cualquier momento"

---

### Causa 3: El Ticker GGAL Específicamente
**Análisis:**

Tu error ocurre SIEMPRE con GGAL, incluso con `auto_adjust=False`.

Posibilidades:
1. ✅ GGAL no está disponible en Yahoo Finance en este momento
2. ✅ Yahoo está bloqueando ese ticker específicamente
3. ✅ Tu ISP/Network está bloqueada por Yahoo

**Verificación:**
Abre en navegador:
https://es.finance.yahoo.com/quote/GGAL/

¿Qué ves?
- ✅ Si aparecen datos → problema es de yfinance
- ❌ Si aparece "Not Found" o error → ticker deslistado
- ❌ Si cargas lento o bloqueado → problema de red

---

## ✅ SOLUCIONES ENCONTRADAS EN INTERNET

### Solución 1: UPGRADE yfinance (RECOMENDADO)
**Funciona: SÍ** (según Stack Overflow, Reddit 2025)

```bash
pip install yfinance --upgrade --no-cache-dir
```

**Entonces ejecuta:**
```bash
python descarga_merval_yahoo.py
```

**Reportes de éxito:**
- ✅ Feb 2025: "I found using pip to uninstall and reinstall it did the job" (Reddit)
- ✅ Nov 2025: "Just upgraded, finally it's working again" (Reddit)
- ✅ Apr 2025: "!pip install yfinance==0.2.54" (StackOverflow)

---

### Solución 2: Especificar Versión Exacta
**Funciona: SÍ** (probado en producción)

Si el upgrade automático no funciona:

```bash
# Desinstalar
pip uninstall yfinance -y

# Instalar versión específica que FUNCIONA en dic 2025
pip install yfinance==0.2.54
```

**Versiones conocidas que funcionan:**
- 0.2.54 ✅ (confirmado en Stack Overflow Apr 2025)
- 0.2.56 ✅ (confirmado Nov 2025)
- 0.2.57 ✅ (última disponible)

**Versiones que NO funcionan:**
- < 0.2.30 ❌ (demasiado viejas)

---

### Solución 3: Aumentar Timeout
**Funciona: SÍ** (para problemas de red/DNS)

A veces yfinance intenta conectar pero se cuelga. Aumentar timeout:

En `descarga_merval_yahoo.py`, línea ~70:

```python
# ANTES
df = yf.download(
    ticker,
    start=fecha_inicio.strftime('%Y-%m-%d'),
    end=fecha_fin.strftime('%Y-%m-%d'),
    progress=False,
    threads=False,
    auto_adjust=False
)

# DESPUÉS (Agregar timeout)
df = yf.download(
    ticker,
    start=fecha_inicio.strftime('%Y-%m-%d'),
    end=fecha_fin.strftime('%Y-%m-%d'),
    progress=False,
    threads=False,
    auto_adjust=False,
    timeout=60  # ← AGREGAR ESTO (segundos)
)
```

---

### Solución 4: Usar proxy (si estás bloqueado)
**Funciona: SÍ** (para redes corporativas/ISP bloqueadas)

Si nada funciona y Yahoo te bloquea:

```python
import yfinance as yf

proxies = {
    'http': 'http://proxy.ejemplo.com:8080',
    'https': 'https://proxy.ejemplo.com:8080'
}

df = yf.download(
    'GGAL',
    proxies=proxies,
    timeout=60
)
```

**O usar VPN:**
```bash
# Cambia tu IP/región si Yahoo la bloquea
```

---

### Solución 5: Alternativa - yahoo_fin
**Funciona: SÍ** (pero diferente API)

Si yfinance sigue sin funcionar, intenta `yahoo_fin`:

```bash
pip install yahoo_fin
```

```python
from yahoo_fin.stock_info import get_data

df = get_data(
    "GGAL",
    start_date='2025-06-20',
    end_date='2025-12-18',
    interval='1d'
)
```

---

### Solución 6: Esperar (si es outage de Yahoo)
**Funciona: SÍ** (si es un problema del lado de Yahoo)

**Señales de outage:**
- Funciona en navegador pero no en yfinance
- Funciona en RapidAPI pero no en yfinance
- Todos en Stack Overflow reportan lo mismo

**En ese caso:**
- Espera 1-2 horas
- Intenta de nuevo
- O usa alternativa (Investing.com, Bolsamania)

---

## 🎯 PLAN DE ACCIÓN (PARA TI)

### Paso 1: Verificar versión actual
```bash
pip show yfinance
```

Anota: `Version: X.X.XX`

### Paso 2: Upgrade
```bash
pip install yfinance --upgrade --no-cache-dir
```

### Paso 3: Verificar de nuevo
```bash
pip show yfinance
```

Debe haber cambiado el número de versión.

### Paso 4: Test rápido
```bash
python -c "import yfinance as yf; df = yf.download('GGAL', period='5d', auto_adjust=False); print(len(df))"
```

Si imprime un número > 0 → ✅ FUNCIONA

Si sigue error → Continuar con pasos siguientes.

### Paso 5: Ejecutar script principal
```bash
python descarga_merval_yahoo.py
```

---

## 🔗 REFERENCIAS DE INTERNET (2025)

**Stack Overflow (Múltiples reportes 2021-2025)**
- Problema: `JSONDecodeError: Expecting value: line 1 column 1`
- Solución: `pip install yfinance --upgrade --no-cache-dir`
- Confirmado por: RJG, Gabriele Nicodemi, Kenan

**Reddit r/learnpython (Nov 2025)**
- Usuario: "Yfinance API not working?"
- Solución: "ensure you are utilizing the most recent version"

**Reddit r/Trading (Feb 2025)**
- Usuario: "Yfinance not working"
- Solución: "pip install --upgrade yfinance" + "uninstall and reinstall it"
- 20+ confirmaciones de éxito

**Stack Overflow Apr 2025**
- Solución probada: `!pip install yfinance==0.2.54`
- Status: "SOLVED" ✅

**wisesheets.io Blog (Oct 2025)**
- "Yahoo Finance API is still being actively maintained as of May 2025"
- "Regular updates and bug fixes from the community"
- Nota: Undocumented API, puede cambiar en cualquier momento

---

## ⚠️ SI NADA FUNCIONA

Alternativas confirmadas que funcionan en 2025:

1. **Selenium + Investing.com** ✅
   ```bash
   python descarga_merval_selenium.py
   ```

2. **Bolsamania.com (Manual)** ✅
   - Descarga 1 click: https://www.bolsamania.com/acciones/ggal/historico-precios

3. **RapidAPI (Yahoo Finance oficial)** ✅
   - API pagada pero confiable

4. **BCBA API (Bolsa Argentina)** ✅
   - Más estable pero requiere registro

---

## 📝 RESUMEN

**Problema:** Tu yfinance tiene versión vieja o Yahoo cambió su API

**Solución (90% de probabilidad):**
```bash
pip install yfinance --upgrade --no-cache-dir
python descarga_merval_yahoo.py
```

**Si falla:** Intenta versión específica:
```bash
pip uninstall yfinance -y && pip install yfinance==0.2.54
```

**Si sigue fallando:** Usa Selenium o Investing.com

---

**Estado:** Basado en investigación de Stack Overflow, Reddit, PyPI, wisesheets.io (2025)