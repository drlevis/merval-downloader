#!/usr/bin/env python3
"""
Script de ANÁLISIS Y RECOMENDACIÓN para MERVAL
ANALIZA todos los fundamentales y:
  - Rankea por P/E
  - Identifica undervalued
  - Calcula scores de compra
  - Genera recomendaciones

EJECUTA:
  python analizar_y_recomendar.py
"""

import pandas as pd
from pathlib import Path
import warnings

warnings.filterwarnings('ignore')

print("="*90)
print("📊 ANÁLISIS Y RECOMENDACIONES DE COMPRA - MERVAL")
print("="*90 + "\n")

# Cargar fundamentales
FUND_PATH = Path("MERVAL_Fundamentales/MERVAL_Fundamentales_Completo.csv")
DATA_PATH = Path("MERVAL_Datos_Limpio")

if not FUND_PATH.exists():
    print(f"❌ Error: No encontré {FUND_PATH}")
    print(f"Ejecuta primero: python descarga_merval_yahoo_completo.py")
    exit(1)

df_fund = pd.read_csv(FUND_PATH)

print(f"📊 Analizando {len(df_fund)} acciones de MERVAL...\n")
print("="*90)
print("RAW DATA - FUNDAMENTALES DESCARGADOS")
print("="*90 + "\n")
print(df_fund.to_string(index=False))
print("\n" + "="*90)

# Crear función para generar score
def calcular_score(row):
    """
    Score de compra de 0-100
    Basado en fundamentales
    """
    score = 0
    detalles = []
    
    # P/E Score
    pe = row['P/E Ratio (Trailing)']
    if isinstance(pe, str) or pd.isna(pe) or pe == 'N/A' or pe == 'Error':
        pe_score = 0
    else:
        pe = float(str(pe).replace('N/A', '0'))
        if pe < 0:
            pe_score = 0  # Pérdidas
            detalles.append("❌ P/E negativo")
        elif pe < 10:
            pe_score = 25
            detalles.append("✅ P/E muy barato")
        elif pe < 15:
            pe_score = 20
            detalles.append("✅ P/E barato")
        elif pe < 25:
            pe_score = 15
            detalles.append("⚠️  P/E justo")
        else:
            pe_score = 5
            detalles.append("❌ P/E caro")
    score += pe_score
    
    # ROE Score
    roe = row['ROE']
    if isinstance(roe, str) and '%' in str(roe):
        try:
            roe_val = float(str(roe).replace('%', ''))
            if roe_val > 15:
                roe_score = 20
                detalles.append("✅ ROE excelente")
            elif roe_val > 10:
                roe_score = 15
                detalles.append("✅ ROE bueno")
            elif roe_val > 5:
                roe_score = 10
                detalles.append("⚠️  ROE promedio")
            else:
                roe_score = 0
                detalles.append("❌ ROE bajo")
        except:
            roe_score = 0
    else:
        roe_score = 0
    score += roe_score
    
    # Dividend Score
    div = row['Dividend Yield']
    if isinstance(div, str) and '%' in str(div):
        try:
            div_val = float(str(div).replace('%', ''))
            if div_val > 4:
                div_score = 20
                detalles.append("✅ Dividendo alto")
            elif div_val > 2:
                div_score = 15
                detalles.append("✅ Dividendo bueno")
            elif div_val > 1:
                div_score = 10
                detalles.append("⚠️  Dividendo bajo")
            elif div_val > 0:
                div_score = 5
                detalles.append("⚠️  Dividendo muy bajo")
            else:
                div_score = 0
                detalles.append("❌ Sin dividendo")
        except:
            div_score = 0
    else:
        div_score = 0
    score += div_score
    
    # D/E Score
    de = row['Debt to Equity']
    if isinstance(de, str):
        try:
            de_val = float(de)
            if de_val < 0.5:
                de_score = 15
                detalles.append("✅ Deuda baja")
            elif de_val < 1.0:
                de_score = 12
                detalles.append("✅ Deuda normal")
            elif de_val < 1.5:
                de_score = 8
                detalles.append("⚠️  Deuda elevada")
            else:
                de_score = 0
                detalles.append("❌ Deuda muy alta")
        except:
            de_score = 0
    else:
        de_score = 0
    score += de_score
    
    # Current Ratio Score
    cr = row['Current Ratio']
    if isinstance(cr, str):
        try:
            cr_val = float(cr)
            if cr_val > 1.5:
                cr_score = 10
                detalles.append("✅ Liquidez buena")
            elif cr_val > 1.0:
                cr_score = 5
                detalles.append("⚠️  Liquidez ajustada")
            else:
                cr_score = 0
                detalles.append("❌ Liquidez crítica")
        except:
            cr_score = 0
    else:
        cr_score = 0
    score += cr_score
    
    return score, detalles

# Calcular scores
df_fund['Score'] = df_fund.apply(lambda row: calcular_score(row)[0], axis=1)
df_fund['Detalles'] = df_fund.apply(lambda row: calcular_score(row)[1], axis=1)

# Rankear
df_fund_sorted = df_fund.sort_values('Score', ascending=False)

print("\n" + "="*90)
print("🎆 RANKING DE COMPRA - TOP 5")
print("="*90 + "\n")

for i, (idx, row) in enumerate(df_fund_sorted.head(5).iterrows(), 1):
    ticker = row['Ticker']
    nombre = row['Nombre']
    score = row['Score']
    precio = row['Precio']
    pe = row['P/E Ratio (Trailing)']
    roe = row['ROE']
    div = row['Dividend Yield']
    detalles = row['Detalles']
    
    if score >= 60:
        rating = "🟢 COMPRA FUERTE"
    elif score >= 40:
        rating = "🟡 COMPRA MODERADA"
    elif score >= 20:
        rating = "🟠 CONSIDERAR"
    else:
        rating = "🔴 EVITAR"
    
    print(f"{i}. {ticker:10} | {nombre:35} | Score: {score:3.0f}/100 {rating}")
    print(f"   Precio: ${precio:>10} | P/E: {pe:>8} | ROE: {roe:>8} | Div: {div:>8}")
    print(f"   → " + " | ".join(detalles))
    print()

# Análisis por categoría
print("\n" + "="*90)
print("📄 ANÁLISIS DETALLADO POR MÉTRICA")
print("="*90 + "\n")

# P/E ranking
print("📊 P/E RATIO (Más bajo = más barato)")
print("-" * 70)
df_pe = df_fund.copy()
df_pe['P/E_clean'] = df_pe['P/E Ratio (Trailing)'].apply(
    lambda x: float(str(x).replace('N/A', '0')) if isinstance(x, str) or not pd.isna(x) else 0
)
df_pe = df_pe[df_pe['P/E_clean'] > 0].sort_values('P/E_clean')
for idx, row in df_pe.head(5).iterrows():
    if row['P/E_clean'] > 0:
        print(f"  {row['Ticker']:10} | P/E = {row['P/E_clean']:6.2f} | {row['Nombre']}")

# ROE ranking
print("\n💪 ROE (Más alto = mejor gestión)")
print("-" * 70)
df_roe = df_fund.copy()
df_roe['ROE_clean'] = df_roe['ROE'].apply(
    lambda x: float(str(x).replace('%', '')) if isinstance(x, str) and '%' in str(x) else 0
)
df_roe = df_roe[df_roe['ROE_clean'] > 0].sort_values('ROE_clean', ascending=False)
for idx, row in df_roe.head(5).iterrows():
    if row['ROE_clean'] > 0:
        print(f"  {row['Ticker']:10} | ROE = {row['ROE_clean']:6.2f}% | {row['Nombre']}")

# Dividend ranking
print("\n💰 DIVIDEND YIELD (Más alto = mejor ingreso)")
print("-" * 70)
df_div = df_fund.copy()
df_div['Div_clean'] = df_div['Dividend Yield'].apply(
    lambda x: float(str(x).replace('%', '')) if isinstance(x, str) and '%' in str(x) else 0
)
df_div = df_div[df_div['Div_clean'] > 0].sort_values('Div_clean', ascending=False)
for idx, row in df_div.head(5).iterrows():
    if row['Div_clean'] > 0:
        print(f"  {row['Ticker']:10} | Div = {row['Div_clean']:6.2f}% | {row['Nombre']}")

# Solvencia ranking
print("\n🏦 D/E RATIO (Más bajo = menos deuda)")
print("-" * 70)
df_de = df_fund.copy()
df_de['DE_clean'] = df_de['Debt to Equity'].apply(
    lambda x: float(str(x)) if isinstance(x, str) and str(x) not in ['N/A', 'Error'] else 999
)
df_de = df_de[df_de['DE_clean'] < 999].sort_values('DE_clean')
for idx, row in df_de.head(5).iterrows():
    if row['DE_clean'] < 999:
        print(f"  {row['Ticker']:10} | D/E = {row['DE_clean']:6.2f} | {row['Nombre']}")

# Recomendaciones finales
print("\n\n" + "="*90)
print("🌟 RECOMENDACIONES FINALES")
print("="*90 + "\n")

top_buy = df_fund_sorted[df_fund_sorted['Score'] >= 40]
if len(top_buy) > 0:
    print(f"✅ COMPRA RECOMENDADA ({len(top_buy)} stocks):")
    for idx, row in top_buy.iterrows():
        print(f"   • {row['Ticker']:10} - {row['Nombre']} (Score: {row['Score']:.0f}/100)")
else:
    print("⚠️  No hay compras recomendadas actualmente")

moderate = df_fund_sorted[(df_fund_sorted['Score'] >= 20) & (df_fund_sorted['Score'] < 40)]
if len(moderate) > 0:
    print(f"\n⚠️  CONSIDERAR CON CUIDADO ({len(moderate)} stocks):")
    for idx, row in moderate.iterrows():
        print(f"   • {row['Ticker']:10} - {row['Nombre']} (Score: {row['Score']:.0f}/100)")

avoid = df_fund_sorted[df_fund_sorted['Score'] < 20]
if len(avoid) > 0:
    print(f"\n❌ EVITAR POR AHORA ({len(avoid)} stocks):")
    for idx, row in avoid.iterrows():
        print(f"   • {row['Ticker']:10} - {row['Nombre']} (Score: {row['Score']:.0f}/100)")

# Guardar análisis
df_export = df_fund_sorted[['Ticker', 'Nombre', 'Precio', 'P/E Ratio (Trailing)', 
                             'ROE', 'Dividend Yield', 'Debt to Equity', 
                             'Current Ratio', 'Score']]
df_export = df_export.sort_values('Score', ascending=False)
df_export.to_csv('MERVAL_Analisis_Recomendaciones.csv', index=False)

print(f"\n📄 Análisis guardado en: MERVAL_Analisis_Recomendaciones.csv")

print("\n" + "="*90)
print("✅ ANÁLISIS COMPLETADO")
print("="*90 + "\n")
print("""
📌 PRÓXIMOS PASOS:

1. Abre: MERVAL_Analisis_Recomendaciones.csv
   → Ver ranking completo en Excel/Sheets

2. Para cada compra potencial:
   → Abre: MERVAL_Datos_Limpio/[TICKER]_precios_5A.csv
   → Analiza gráficos históricos
   → Verifica soportes y resistencias

3. Antes de invertir:
   → Lee reportes anuales en Yahoo Finance
   → Verifica noticias recientes
   → Calcula margen de seguridad (20-30% descuento)

4. Portfolio sugerido (diversificación):
   → 40% en COMPRA FUERTE (Score > 60)
   → 40% en COMPRA MODERADA (Score 40-60)
   → 20% en Cash o CONSIDERAR (esperando caídas)

¡Estás listo para invertir como profesional! 🚀
""")
