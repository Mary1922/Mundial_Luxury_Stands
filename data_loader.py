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
    # Carga inicial
    df = pd.read_csv(path_csv)
    
    # 1. Limpieza de Año de producción (yop)
    if 'yop' in df.columns:
        df['yop'] = pd.to_numeric(df['yop'], errors='coerce').astype('Int64')
        
    # 2. Limpieza de Precio original (sobrescribiendo sobre 'price')
    columna_precio_origen = 'price_raw' if 'price_raw' in df.columns else 'price'
    if columna_precio_origen in df.columns:
        df['price'] = df[columna_precio_origen].apply(limpiar_precio).astype('Float64')
    
    # 3. Filtrado metodológico estricto: Solo mercado de relojes NUEVOS
    # Excluimos de raíz los NaN y estados usados para evitar sesgos comerciales
    condiciones_nuevas = ['New', 'Unworn']
    if 'cond' in df.columns:
        df_nuevos = df[df['cond'].isin(condiciones_nuevas)].copy()
    elif 'condition' in df.columns:
        df_nuevos = df[df['condition'].isin(condiciones_nuevas)].copy()
        df_nuevos = df_nuevos.rename(columns={'condition': 'cond'})
    else:
        df_nuevos = df.copy()
        
    # Eliminamos columnas fantasma duplicadas si existieran
    df_nuevos = df_nuevos.loc[:, ~df_nuevos.columns.duplicated()]
    
    return df_nuevos