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
# INYECCIÓN DE CSS PARA DETALLES PREMIUM (CON CONTRASTE SEGURO)
# ============================================================
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&display=swap');
    
    /* Forzamos la tipografía Inter en toda la app */
    html, body, [data-testid="stSidebarView"], .stApp {
        font-family: 'Inter', sans-serif;
    }
    
    /* Tarjeta de Gobernanza: Fondo gris oscuro para que resalte tanto en modo claro como oscuro */
    .governance-card {
        background-color: #1E293B;
        border-left: 5px solid #D4AF37;
        padding: 22px;
        border-radius: 8px;
        margin-top: 15px;
        margin-bottom: 25px;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
    }
    .governance-title {
        color: #F59E0B;
        font-weight: 700;
        margin-bottom: 10px;
        font-size: 1.2rem;
        letter-spacing: 0.5px;
    }
    .governance-text {
        color: #F8FAFC;
        font-size: 0.95rem;
        line-height: 1.6;
    }
    
    /* Diseño de las pestañas (Tabs) */
    button[data-baseweb="tab"] {
        font-size: 1rem !important;
        font-weight: 600 !important;
        padding: 12px 20px !important;
    }
    
    /* Ajuste de color para las métricas KPI */
    div[data-testid="stMetricValue"] {
        color: #D4AF37 !important;
        font-weight: 700 !important;
    }
    </style>
""", unsafe_allow_html=True)

# Paletas cromáticas de lujo para los gráficos
PALETA_LUJO_DISCRETA = ['#D4AF37', '#64748B', '#475569', '#94A3B8', '#334155', '#CBD5E1']
PALETA_TIERS_SEQUENTIAL = ['#94A3B8', '#38BDF8', '#F59E0B', '#EF4444'] 

# Cargar los datos
try:
    df_campaign = cargar_y_limpiar_datos("Watches.csv")
except Exception as e:
    st.error(f"Error al cargar 'Watches.csv': {e}")
    st.stop()

# ============================================================
# CABECERA Y TITULARES (Usamos colores nativos para evitar bloqueos visuales)
# ============================================================
st.title("🎯 Estrategia de Campaña: Mundial Luxury Stands")

st.markdown("""
<div class="governance-card">
    <div class="governance-title">⚠️ ADVERTENCIA METODOLÓGICA Y MITIGACIÓN DE SESGOS</div>
    <div class="governance-text">
        <strong>Análisis de Calidad de Datos (Gobernanza y Data Ethics):</strong><br>
        El dataset original presentaba un <strong>74.73% de valores nulos (NaN)</strong> en la columna de condición del reloj. 
        Asumir arbitrariamente que los registros vacíos corresponden a unidades nuevas para incrementar artificialmente el volumen de la campaña representaría un <em>Sesgo de Selección Masivo</em>.<br><br>
        <strong>Acción de Mitigación:</strong> Este cuadro de mando trabaja <strong>únicamente</strong> con los registros con etiquetado explícito <code>New</code> y <code>Unworn</code> (universo de <strong>23,146 anuncios seguros</strong>), garantizará la integridad absoluta de las proyecciones financieras.
    </div>
</div>
""", unsafe_allow_html=True)

# ============================================================
# BARRA LATERAL
# ============================================================
st.sidebar.title("🎛️ Filtros de Campaña")

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
# PESTAÑAS CON CONFIGURACIÓN DE TEMA AUTOMÁTICO
# ============================================================
tab1, tab2, tab3, tab4 = st.tabs([
    "📦 Distribución de Precios", 
    "📊 Presencia en Mercado", 
    "🎯 Cuadrantes de Oportunidad", 
    "💎 Segmentación por Tiers"
])

with tab1:
    st.subheader("Análisis de Dispersión y Rangos de Precio")
    if len(df_filtrado) > 0:
        fig1 = px.box(
            df_filtrado, x='brand', y='price', color='brand', log_y=True,   
            title='Distribución de precios por marca (escala logarítmica)',
            labels={'brand': 'Marca', 'price': 'Precio (USD)'},
            points=False, height=600, color_discrete_sequence=PALETA_LUJO_DISCRETA
        )
        fig1.update_layout(template='plotly_dark', xaxis_tickangle=-45, margin=dict(b=80))
        st.plotly_chart(fig1, use_container_width=True)
    else:
        st.info("Selecciona marcas en la barra lateral.")

with tab2:
    st.subheader("Volumen y Participación de la Oferta")
    if len(df_filtrado) > 0:
        conteo_marcas = df_filtrado['brand'].value_counts().reset_index()
        conteo_marcas.columns = ['marca', 'numero_anuncios']
        
        fig2 = px.bar(
            conteo_marcas.head(15), x='numero_anuncios', y='marca', orientation='h',
            title='¿Qué marcas tienen mayor presencia en el mercado?',
            labels={'numero_anuncios': 'Anuncios activos', 'marca': 'Marca'},
            text='numero_anuncios', height=550, color_discrete_sequence=['#D4AF37']
        )
        fig2.update_layout(template='plotly_dark', yaxis={'categoryorder': 'total ascending'})
        st.plotly_chart(fig2, use_container_width=True)

with tab3:
    st.subheader("Matriz Estratégica: Antigüedad vs. Pricing")
    df_yop_valido = df_filtrado.dropna(subset=['yop', 'price'])
    
    if len(df_yop_valido) > 0:
        resumen_oportunidad = df_yop_valido.groupby('brand').agg(
            anio_medio=('yop', 'mean'), precio_medio=('price', 'mean'), n_modelos=('price', 'count')
        ).reset_index()
        
        resumen_oportunidad = resumen_oportunidad[resumen_oportunidad['n_modelos'] >= 5]
        
        if len(resumen_oportunidad) > 0:
            mediana_anio = resumen_oportunidad['anio_medio'].median()
            mediana_precio = resumen_oportunidad['precio_medio'].median()
            
            fig3 = px.scatter(
                resumen_oportunidad, x='anio_medio', y='precio_medio', size='n_modelos', color='brand', text='brand',
                title='¿Qué marcas combinan catálogo reciente y precio premium?',
                labels={'anio_medio': 'Año medio', 'precio_medio': 'Precio medio (USD)'},
                size_max=40, height=600, color_discrete_sequence=PALETA_LUJO_DISCRETA
            )
            fig3.update_traces(textposition='top center')
            fig3.add_vline(x=mediana_anio, line_dash='dash', line_color='#94A3B8')
            fig3.add_hline(y=mediana_precio, line_dash='dash', line_color='#94A3B8')
            fig3.update_layout(template='plotly_dark', showlegend=False)
            st.plotly_chart(fig3, use_container_width=True)
            
            col_kpi1, col_kpi2 = st.columns(2)
            col_kpi1.metric("Mediana Global de Año", f"{mediana_anio:.1f}")
            col_kpi2.metric("Mediana Global de Precio", f"${mediana_precio:,.0f}")
            
            st.write("#### 🚀 Marcas en el Cuadrante de Oportunidad:")
            oportunidad = resumen_oportunidad[
                (resumen_oportunidad['anio_medio'] >= mediana_anio) & (resumen_oportunidad['precio_medio'] >= mediana_precio)
            ].sort_values('precio_medio', ascending=False)
            
            if not oportunidad.empty:
                st.dataframe(
                    oportunidad[['brand', 'anio_medio', 'precio_medio', 'n_modelos']]
                    .rename(columns={'brand': 'Marca', 'anio_medio': 'Año Medio', 'precio_medio': 'Precio Medio', 'n_modelos': 'Modelos'}),
                    use_container_width=True
                )
        else:
            st.info("No hay suficientes datos para los cuadrantes.")

with tab4:
    st.subheader("Estructura de Mercado por Niveles de Lujo")
    if 'tier_lujo' in df_filtrado.columns and len(df_filtrado) > 0:
        conteo_tier_marca = df_filtrado.groupby(['brand', 'tier_lujo'], observed=False).size().reset_index(name='n_modelos')
        
        fig4 = px.bar(
            conteo_tier_marca, x='brand', y='n_modelos', color='tier_lujo',
            title='Modelos por Tier de Lujo',
            labels={'brand': 'Marca', 'n_modelos': 'Modelos', 'tier_lujo': 'Tier'},
            height=550, color_discrete_sequence=PALETA_TIERS_SEQUENTIAL
        )
        fig4.update_layout(template='plotly_dark', xaxis_tickangle=-30, barmode='stack')
        st.plotly_chart(fig4, use_container_width=True)
        
        st.write("### 📈 Tabla de Potencial: % de Modelos en Alta Gama o Superior")
        tabla_pct = conteo_tier_marca.pivot(index='brand', columns='tier_lujo', values='n_modelos').fillna(0)
        orden_tiers = ['1. Entrada', '2. Premium', '3. Alta Gama', '4. Ultra-Lujo']
        for tier in orden_tiers:
            if tier not in tabla_pct.columns: tabla_pct[tier] = 0
        tabla_pct['total'] = tabla_pct[orden_tiers].sum(axis=1)
        
        tabla_pct['% Alta Gama o superior'] = 0.0
        mask = tabla_pct['total'] > 0
        tabla_pct.loc[mask, '% Alta Gama o superior'] = ((tabla_pct.loc[mask, '3. Alta Gama'] + tabla_pct.loc[mask, '4. Ultra-Lujo']) / tabla_pct.loc[mask, 'total'] * 100).round(1)
        
        st.dataframe(tabla_pct.sort_values('% Alta Gama o superior', ascending=False)[['total', '% Alta Gama o superior']], use_container_width=True)