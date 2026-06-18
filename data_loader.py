import pandas as pd
import numpy as np
import re
import streamlit as st

def limpiar_precio(valor):
    if pd.isna(valor):
        return np.nan
    if isinstance(valor, (int, float)):
        return float(valor)
    texto = str(valor)
    texto_limpio = re.sub(r'[^\d.,]', '', texto)
    texto_limpio = texto_limpio.replace(',', '')
    try:
        return float(texto_limpio) if texto_limpio else np.nan
    except ValueError:
        return np.nan

@st.cache_data
def cargar_y_limpiar_datos(path_csv="Watches_limpio.csv"):

    # Carga inicial con optimización de memoria
    df = pd.read_csv(path_csv, low_memory=False)

    # Si ya existe tier_lujo, no volver a crearla
    if "tier_lujo" not in df.columns:

        def asignar_tier(precio):
            if pd.isna(precio):
                return "1. Entrada"
            if precio < 5000:
                return "1. Entrada"
            elif precio < 15000:
                return "2. Premium"
            elif precio < 50000:
                return "3. Alta Gama"
            else:
                return "4. Ultra-Lujo"

        # 1. Limpieza de Año de producción (yop)
        if 'yop' in df.columns:
            df['yop'] = pd.to_numeric(df['yop'], errors='coerce').astype('Int64')

        # 2. Limpieza de Precio original
        columna_precio_origen = 'price_raw' if 'price_raw' in df.columns else 'price'
        if columna_precio_origen in df.columns:
            df['price'] = df[columna_precio_origen].apply(limpiar_precio).astype('Float64')

        # 3. Filtrado metodológico estricto: Solo mercado de relojes NUEVOS
        condiciones_nuevas = ['New', 'Unworn']
        if 'cond' in df.columns:
            df_nuevos = df[df['cond'].isin(condiciones_nuevas)].copy()
        elif 'condition' in df.columns:
            df_nuevos = df[df['condition'].isin(condiciones_nuevas)].copy()
            df_nuevos = df_nuevos.rename(columns={'condition': 'cond'})
        else:
            df_nuevos = df.copy()

        df_nuevos = df_nuevos.loc[:, ~df_nuevos.columns.duplicated()]

        # ============================================================
        # 🌟 RECREACIÓN AUTOMÁTICA Y ORDENACIÓN CATEGÓRICA DEL TIER
        # ============================================================
        df_nuevos['tier_lujo'] = df_nuevos['price'].apply(asignar_tier)

        # IMPORTANTE: Forzamos a Pandas a entender el orden jerárquico para los gráficos
        orden_tiers = ['1. Entrada', '2. Premium', '3. Alta Gama', '4. Ultra-Lujo']
        df_nuevos['tier_lujo'] = pd.Categorical(df_nuevos['tier_lujo'], categories=orden_tiers, ordered=True)

        df = df_nuevos  # A partir de aquí seguimos trabajando sobre el dataset filtrado

    # ============================================================
    # 🔧 GARANTÍA INCONDICIONAL DE 'casem' (Material de la Caja)
    # ------------------------------------------------------------
    # OJO: este bloque se ejecuta SIEMPRE, tanto si el CSV ya traía
    # 'tier_lujo' precalculado (rama else de arriba) como si no.
    # Antes vivía DENTRO del `if "tier_lujo" not in df.columns:`,
    # así que en cuanto el CSV empezó a incluir 'tier_lujo' de
    # fábrica, esta normalización dejaba de ejecutarse, 'casem'
    # nunca se creaba, y el filtro de Material de la Caja
    # desaparecía de la barra lateral sin ningún error visible.
    # ============================================================
    if 'case_material' in df.columns and 'casem' not in df.columns:
        df['casem'] = df['case_material']
    elif 'casem' not in df.columns:
        df['casem'] = "No especificado"

    return df