import streamlit as st
import plotly.express as px
import pandas as pd
from data_loader import cargar_y_limpiar_datos

# 1. Configuración panorámica de la página
st.set_page_config(
    page_title="Mundial Luxury Stands — Control de Campaña",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================
# INYECCIÓN DE ARQUITECTURA DE DISEÑO CSS (CUSTOM STYLING)
# ============================================================
st.markdown("""
    <style>
    /* Configuración del tema general oscuro y tipografía limpia */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&display=swap');
    
    html, body, [data-testid="stSidebarView"] {
        font-family: 'Inter', sans-serif;
    }
    
    /* Estilización del contenedor de advertencia metodológica */
    .governance-card {
        background-color: #1A1C23;
        border-left: 5px solid #D4AF37;
        padding: 20px;
        border-radius: 8px;
        margin-bottom: 25px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.3);
    }
    .governance-title {
        color: #E5C158;
        font-weight: 600;
        margin-top: 0px;
        font-size: 1.15rem;
    }
    .governance-text {
        color: #E2E8F0;
        font-size: 0.95rem;
        line-height: 1.5;
    }
    
    /* Customización de las pestañas superiores (Tabs) */
    button[data-baseweb="tab"] {
        font-size: 1rem !important;
        font-weight: 600 !important;
        color: #94A3B8 !important;
        border-bottom-width: 2px !important;
    }
    button[data-baseweb="tab"][aria-selected="true"] {
        color: #E5C158 !important;
        border-bottom-color: #D4AF37 !important;
    }
    
    /* Bloques de KPIs Métricas */
    div[data-testid="stMetricValue"] {
        color: #E5C158 !important;
        font-weight: 700 !important;
        font-size: 2.2rem !important;
    }
    div[data-testid="stMetricLabel"] {
        color: #94A3B8 !important;
        text-transform: uppercase;
        font-size: 0.8rem !important;
        letter-spacing: 1px;
    }
    </style>
""", unsafe_unsafe_with_transparent_background=True, unsafe_allow_html=True)

# Paleta cromática corporativa para gráficos de Plotly
PALETA_LUJO_DISCRETA = ['#D4AF37', '#718096', '#4A5568', '#A0AEC0', '#2D3748', '#CBD5E0']
PALETA_TIERS_SEQUENTIAL = ['#A5D6A7', '#64B5F6', '#FB8C00', '#E53935'] # Degradado de menor a mayor valor estricto

# Cargar los datos limpios y filtrados
try:
    df_campaign = cargar_y_limpiar_datos("Watches.csv")
except Exception as e:
    st.error(f"Error al cargar 'Watches.csv'. Asegúrate de que el archivo está en la raíz: {e}")
    st.stop()

# ============================================================
# SECCIÓN DE GOBERNANZA UTILIZANDO INTERFAZ HTML/CSS PREMIUM
# ============================================================
st.markdown('<h1 style="color: #F3F4F6; font-weight: 700; letter-spacing: -0.5px;">🎯 Estrategia de Campaña: Mundial Luxury Stands</h1>', unsafe_allow_html=True)

st.markdown("""
<div class="governance-card">
    <div class="governance-title">⚠️ ADVERTENCIA METODOLÓGICA Y MITIGACIÓN DE SESGOS</div>
    <div class="governance-text">
        <strong>Análisis de Calidad de Datos (Gobernanza y Data Ethics):</strong><br>
        El dataset original presentaba un <strong>74.73% de valores nulos (NaN)</strong> en la columna de condición del reloj. 
        Asumir arbitrariamente que los registros vacíos corresponden a unidades nuevas para incrementar artificialmente el volumen de la campaña representaría un <em>Sesgo de Selección Masivo</em>.<br><br>
        <strong>Acción de Mitigación:</strong> Este cuadro de mando trabaja <strong>únicamente</strong> con los registros con etiquetado explícito <code>New</code> y <code>Unworn</code> (universo de <strong>23,146 anuncios seguros</strong>), garantizando la integridad absoluta de las proyecciones financieras de la campaña.
    </div>
</div>
""", unsafe_allow_html=True)

# ============================================================
# BARRA LATERAL: FILTROS CRUZADOS DINÁMICOS
# ============================================================
st.sidebar.markdown('<h2 style="color: #E5C158; font-size: 1.3rem;">🎛️ Filtros de Campaña</h2>', unsafe_allow_html=True)

top12_marcas_auto = list(df_campaign['brand'].value_counts().head(12).index)
marcas_disponibles = sorted(df_campaign['brand'].dropna().unique())

marcas_seleccionadas = st.sidebar.multiselect(
    "Selecciona las Marcas para el Análisis:", 
    options=marcas_disponibles, 
    default=top12_marcas_auto
)

df_filtrado = df_campaign[df_campaign['brand'].isin(marcas_seleccionadas)]

if 'tier_lujo' in df_filtrado.columns:
    tiers_disponibles = sorted(df_filtrado['tier_lujo'].dropna().unique())
    tiers_seleccionados = st.sidebar.multiselect("Filtrar por Tier de Lujo:", options=tiers_disponibles, default=tiers_disponibles)
    df_filtrado = df_filtrado[df_filtrado['tier_lujo'].isin(tiers_seleccionados)]

# ============================================================
# MAQUETACIÓN DE LAS PESTAÑAS DEL EDA
# ============================================================
tab1, tab2, tab3, tab4 = st.tabs([
    "📦 Distribución de Precios", 
    "📊 Presencia en Mercado", 
    "🎯 Cuadrantes de Oportunidad", 
    "💎 Segmentación por Tiers"
])

# ------------------------------------------------------------
# PESTAÑA 1: Gráfico 1 (Diagrama de Cajas Logarítmico)
# ------------------------------------------------------------
with tab1:
    st.markdown('<h3 style="color: #F3F4F6;">Análisis de Dispersión y Rangos de Precio</h3>', unsafe_allow_html=True)
    if len(df_filtrado) > 0:
        fig1 = px.box(
            df_filtrado,
            x='brand',
            y='price',
            color='brand',
            log_y=True,   
            title='Distribución de precios por marca de relojería de lujo (escala logarítmica)',
            labels={'brand': 'Marca', 'price': 'Precio de venta — USD (escala log)'},
            points=False,
            height=600,
            color_discrete_sequence=PALETA_LUJO_DISCRETA
        )
        fig1.update_layout(
            template='plotly_dark',
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            showlegend=False,
            xaxis_tickangle=-45,
            margin=dict(b=80)
        )
        st.plotly_chart(fig1, width='stretch')
        st.caption("⚠️ **Escala logarítmica activa:** Cada división multiplica el precio por 10. Permite comparar visualmente marcas con rangos de precio muy distintos sin deformar las cajas.")
    else:
        st.info("Selecciona marcas en la barra lateral para generar la visualización.")

# ------------------------------------------------------------
# PESTAÑA 2: Gráfico 2 (Barras Horizontales de Volumen)
# ------------------------------------------------------------
with tab2:
    st.markdown('<h3 style="color: #F3F4F6;">Volumen y Participación de la Oferta</h3>', unsafe_allow_html=True)
    if len(df_filtrado) > 0:
        conteo_marcas = df_filtrado['brand'].value_counts().reset_index()
        conteo_marcas.columns = ['marca', 'numero_anuncios']
        
        fig2 = px.bar(
            conteo_marcas.head(15),
            x='numero_anuncios',
            y='marca',
            orientation='h',
            title='¿Qué marcas de relojes de lujo tienen mayor presencia en el mercado?',
            labels={'numero_anuncios': 'Número de anuncios activos', 'marca': 'Marca'},
            text='numero_anuncios',
            height=550,
            color_discrete_sequence=['#D4AF37'] # Forzamos barra dorada corporativa
        )
        fig2.update_layout(
            template='plotly_dark',
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            yaxis={'categoryorder': 'total ascending'}
        )
        st.plotly_chart(fig2, width='stretch')
    else:
        st.info("Sin datos disponibles para generar el ranking de volumen.")

# ------------------------------------------------------------
# PESTAÑA 3: Gráfico 3 (Burbujas y Cuadrantes Estratégicos)
# ------------------------------------------------------------
with tab3:
    st.markdown('<h3 style="color: #F3F4F6;">Matriz Estratégica: Antigüedad vs. Pricing</h3>', unsafe_allow_html=True)
    
    df_yop_valido = df_filtrado.dropna(subset=['yop', 'price'])
    
    if len(df_yop_valido) > 0:
        resumen_oportunidad = (
            df_yop_valido
            .groupby('brand')
            .agg(
                anio_medio=('yop', 'mean'),
                precio_medio=('price', 'mean'),
                n_modelos=('price', 'count')
            )
            .reset_index()
        )
        
        MIN_MODELOS = 5
        resumen_oportunidad = resumen_oportunidad[resumen_oportunidad['n_modelos'] >= MIN_MODELOS]
        
        if len(resumen_oportunidad) > 0:
            mediana_anio = resumen_oportunidad['anio_medio'].median()
            mediana_precio = resumen_oportunidad['precio_medio'].median()
            
            fig3 = px.scatter(
                resumen_oportunidad,
                x='anio_medio',
                y='precio_medio',
                size='n_modelos',
                color='brand',
                text='brand',
                title='¿Qué marcas combinan catálogo reciente y precio premium? (tamaño = nº de modelos nuevos)',
                labels={'anio_medio': 'Año medio de fabricación', 'precio_medio': 'Precio medio (USD)', 'brand': 'Marca'},
                size_max=40,
                height=600,
                color_discrete_sequence=PALETA_LUJO_DISCRETA
            )
            fig3.update_traces(textposition='top center')
            fig3.add_vline(x=mediana_anio, line_dash='dash', line_color='#A0AEC0')
            fig3.add_hline(y=mediana_precio, line_dash='dash', line_color='#A0AEC0')
            fig3.update_layout(
                template='plotly_dark',
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                showlegend=False
            )
            
            st.plotly_chart(fig3, width='stretch')
            
            # KPIs Estilizados con CSS del header superior
            col_kpi1, col_kpi2 = st.columns(2)
            col_kpi1.metric("Mediana Global de Año", f"{mediana_anio:.1f}")
            col_kpi2.metric("Mediana Global de Precio", f"${mediana_precio:,.0f}")
            
            st.markdown('<h4 style="color: #E5C158; margin-top: 20px;">🚀 Marcas en el Cuadrante de Oportunidad (Catálogo Reciente + Precio Alto):</h4>', unsafe_allow_html=True)
            oportunidad = resumen_oportunidad[
                (resumen_oportunidad['anio_medio'] >= mediana_anio) &
                (resumen_oportunidad['precio_medio'] >= mediana_precio)
            ].sort_values('precio_medio', ascending=False)
            
            if not oportunidad.empty:
                st.dataframe(
                    oportunidad[['brand', 'anio_medio', 'precio_medio', 'n_modelos']]
                    .rename(columns={'brand': 'Marca', 'anio_medio': 'Año Medio', 'precio_medio': 'Precio Medio (USD)', 'n_modelos': 'Modelos Disp.'}),
                    use_container_width=True
                )
            else:
                st.info("Ninguna marca seleccionada cae exactamente en el cuadrante superior derecho.")
        else:
            st.info("No hay suficientes marcas con más de 5 modelos para trazar los cuadrantes.")
    else:
        st.info("Faltan variables críticas ('yop' o 'price') en la selección actual para trazar la matriz.")

# ------------------------------------------------------------
# PESTAÑA 4: Gráfico 4 y Tabla 5 (Composición de Tiers de Lujo)
# ------------------------------------------------------------
with tab4:
    st.markdown('<h3 style="color: #F3F4F6;">Estructura de Mercado por Niveles de Lujo</h3>', unsafe_allow_html=True)
    
    if 'tier_lujo' in df_filtrado.columns and len(df_filtrado) > 0:
        conteo_tier_marca = (
            df_filtrado
            .groupby(['brand', 'tier_lujo'], observed=False)
            .size()
            .reset_index(name='n_modelos')
        )
        
        # Gráfico 4: Barras Apiladas con paleta secuencial elegante
        fig4 = px.bar(
            conteo_tier_marca,
            x='brand',
            y='n_modelos',
            color='tier_lujo',
            title='¿Qué rango de precios ofrece cada marca? (nº de modelos nuevos por Tier de Lujo)',
            labels={'brand': 'Marca', 'n_modelos': 'Número de modelos', 'tier_lujo': 'Tier de Lujo'},
            height=550,
            color_discrete_sequence=PALETA_TIERS_SEQUENTIAL
        )
        fig4.update_layout(
            template='plotly_dark',
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            xaxis_tickangle=-30, 
            barmode='stack'
        )
        st.plotly_chart(fig4, width='stretch')
        
        st.markdown('<h3 style="color: #E5C158; margin-top: 25px;">📈 Tabla de Potencial: % de Modelos en Alta Gama o Superior</h3>', unsafe_allow_html=True)
        
        # Pivote seguro respetando categorías vacías
        tabla_pct = conteo_tier_marca.pivot(index='brand', columns='tier_lujo', values='n_modelos').fillna(0)
        
        orden_tiers = ['1. Entrada', '2. Premium', '3. Alta Gama', '4. Ultra-Lujo']
        for tier in orden_tiers:
            if tier not in tabla_pct.columns:
                tabla_pct[tier] = 0
                
        tabla_pct['total'] = tabla_pct[orden_tiers].sum(axis=1)
        
        tabla_pct['% Alta Gama o superior'] = 0.0
        mask = tabla_pct['total'] > 0
        tabla_pct.loc[mask, '% Alta Gama o superior'] = (
            (tabla_pct.loc[mask, '3. Alta Gama'] + tabla_pct.loc[mask, '4. Ultra-Lujo']) / tabla_pct.loc[mask, 'total'] * 100
        ).round(1)
        
        tabla_reporte = tabla_pct.sort_values('% Alta Gama o superior', ascending=False)[['total', '% Alta Gama o superior']]
        tabla_reporte.index.name = "Marca"
        tabla_reporte.columns = ["Total Modelos", "% Alta Gama o Superior"]
        
        st.dataframe(tabla_reporte, use_container_width=True)
        
    else:
        st.info("La columna 'tier_lujo' no está disponible o el DataFrame está vacío.")