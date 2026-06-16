import streamlit as st
import plotly.express as px
from data_loader import cargar_y_limpiar_datos

# Configuración de la página en modo ancho para expandir los gráficos
st.set_page_config(
    page_title="Dashboard Relojes de Lujo — Campaña Nuevos",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Cargar los datos limpios y filtrados (df_nuevos)
try:
    df_campaign = cargar_y_limpiar_datos("Watches.csv")
except Exception as e:
    st.error(f"No se pudo cargar el archivo CSV. Asegúrate de que 'Watches.csv' está en la raíz. Error: {e}")
    st.stop()

# ============================================================
# MAQUETACIÓN VISUAL DE LA ALERTA DE SESGO (Product Owner View)
# ============================================================
st.title("🎯 Estrategia de Campaña: Mercado de Relojes Nuevos")

st.warning("""
### ⚠️ ADVERTENCIA METODOLÓGICA Y MITIGACIÓN DE SESGOS
**Análisis de Calidad de Datos (Gobernanza y Data Ethics):**
El dataset original presentaba un **74.73% de valores nulos (NaN)** en la columna de condición del reloj. 

Asumir arbitrariamente que los registros vacíos corresponden a unidades nuevas para incrementar el volumen de la campaña representaría un **Sesgo de Selección Masivo** y un riesgo crítico para el negocio. La lógica de mercado demuestra que los vendedores omiten la condición principalmente en piezas de segunda mano o vintage. 

**Acción de Mitigación:** Este cuadro de mando ha sido diseñado aislando **únicamente** los registros con etiquetado explícito `New` y `Unworn` (universo de **23,146 anuncios seguros**), garantizando la integridad de las proyecciones financieras de la campaña.
""")

st.write("---")

# ============================================================
# BARRA LATERAL: FILTROS CRUZADOS DINÁMICOS
# ============================================================
st.sidebar.header("🎛️ Filtros de Campaña")

# Filtro 1: Marca (Top marcas con más volumen)
marcas_disponibles = sorted(df_campaign['brand'].dropna().unique())
marcas_seleccionadas = st.sidebar.multiselect(
    "Filtrar por Marca:", 
    options=marcas_disponibles, 
    default=marcas_disponibles[:5] if len(marcas_disponibles) > 5 else marcas_disponibles
)

# Aplicar primer filtro para dinamizar los siguientes
df_filtrado = df_campaign[df_campaign['brand'].isin(marcas_seleccionadas)]

# Filtro 2: Tier de Lujo (Basado en el df ya filtrado por marca)
tiers_disponibles = sorted(df_filtrado['tier_lujo'].dropna().unique()) if 'tier_lujo' in df_filtrado.columns else []
if Tiers_disponibles:
    tiers_seleccionados = st.sidebar.multiselect("Filtrar por Segmento de Lujo:", options=tiers_disponibles, default=tiers_disponibles)
    df_filtrado = df_filtrado[df_filtrado['tier_lujo'].isin(tiers_seleccionados)]

# Filtro 3: Material de la caja (casem)
materiales_disponibles = sorted(df_filtrado['casem'].dropna().unique()) if 'casem' in df_filtrado.columns else []
if materiales_disponibles:
    materiales_seleccionados = st.sidebar.multiselect("Filtrar por Material de Caja:", options=materiales_disponibles, default=materiales_disponibles)
    df_filtrado = df_filtrado[df_filtrado['casem'].isin(materiales_seleccionados)]

# ============================================================
# KPI's Y VISUALIZACIONES EXPANDIDAS
# ============================================================
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Muestra Filtrada (Anuncios)", f"{len(df_filtrado):,}")
with col2:
    precio_medio = df_filtrado['price'].mean() if len(df_filtrado) > 0 else 0
    st.metric("Precio Medio (USD)", f"${precio_medio:,.2f}" if precio_medio > 0 else "$0.00")
with col3:
    marcas_activas = df_filtrado['brand'].nunique()
    st.metric("Marcas Analizadas", marcas_activas)

st.write("### Distribución Expandida de Precios por Marca")

if len(df_filtrado) > 0:
    # Gráfico de cajas optimizado para ocupar la pantalla completa
    fig1 = px.box(
        df_filtrado,
        x='brand',
        y='price',
        color='brand',
        labels={'brand': 'Marca', 'price': 'Precio de venta (USD)'},
        points=False
    )
    fig1.update_layout(
        template='plotly_white',
        showlegend=False,
        xaxis_tickangle=-45,
        height=600,  # Forzamos altura panorámica
        margin=dict(l=40, r=40, t=20, b=100)
    )
    # Escala logarítmica opcional mediante un checkbox interactivo en la UI
    usar_log = st.checkbox("Aplicar Escala Logarítmica en el Eje Y (Recomendado para mitigar el efecto visual de outliers extremos)")
    if usar_log:
        fig1.update_yaxes(type="log")
        
    st.plotly_chart(fig1, use_container_width=True)
else:
    st.info("Por favor, selecciona al menos una marca en los filtros de la barra lateral para generar los gráficos.")