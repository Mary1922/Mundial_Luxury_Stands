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
def cargar_y_limpiar_datos(path_csv="Watches.csv"):
    # Carga inicial del archivo original
    df = pd.read_csv(path_csv)
    
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
        
    # Eliminamos duplicados fantasmas de columnas si existieran
    df_nuevos = df_nuevos.loc[:, ~df_nuevos.columns.duplicated()]
    
    # ============================================================
    # 🌟 RECREACIÓN AUTOMÁTICA DE LA VARIABLE DE NEGOCIO: TIER DE LUJO
    # ============================================================
    # Definimos los cortes de precio para clasificar el nivel de lujo del reloj
    # Entrada (< $5,000) | Premium ($5,000 - $15,000) | Alta Gama ($15,000 - $50,000) | Ultra-Lujo (> $50,000)
    
    def asignar_tier(precio):
        if pd.isna(precio):
            return "1. Entrada"  # Por seguridad o manejo de nulos
        if precio < 5000:
            return "1. Entrada"
        elif precio < 15000:
            return "2. Premium"
        elif precio < 50000:
            return "3. Alta Gama"
        else:
            return "4. Ultra-Lujo"
            
    # Creamos la columna sobre la marcha para que Streamlit la tenga disponible siempre
    df_nuevos['tier_lujo'] = df_nuevos['price'].apply(asignar_tier)
    
    # Homogeneizar columnas secundarias si no existen o se llaman diferente
    if 'case_material' in df_nuevos.columns and 'casem' not in df_nuevos.columns:
        df_nuevos['casem'] = df_nuevos['case_material']
    elif 'casem' not in df_nuevos.columns:
        df_nuevos['casem'] = "No especificado"
        
    return df_nuevos