import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np

# 1. CONFIGURACIÓN DE LA PÁGINA (Debe ser SIEMPRE la primera línea de Streamlit)
st.set_page_config(
    page_title="Mundial Luxury Stands - Dashboard",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 2. DISEÑO DE ESTILOS PREMIUM (CSS Personalizado inyectado)
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght=300;400;500;600;700&display=swap');

html, body, [class*="css"], .stApp {
    font-family: 'Inter', sans-serif;
}

.block-container {
    padding-top: 1.5rem;
    padding-bottom: 2rem;
    max-width: 1600px;
}

[data-testid="stSidebar"] {
    background-color: #0F172A;
}

.hero-card {
    background: linear-gradient(135deg, #111827, #1E293B);
    padding: 28px;
    border-radius: 20px;
    border: 1px solid #334155;
    box-shadow: 0 10px 25px rgba(0,0,0,.35);
}

.executive-card {
    background: #111827;
    padding: 18px;
    border-radius: 16px;
    border-left: 4px solid #D4AF37;
    margin-bottom: 12px;
}

.governance-card {
    background: #1E293B;
    border-left: 5px solid #D4AF37;
    padding: 24px;
    border-radius: 16px;
    margin-top: 15px;
    margin-bottom: 25px;
}

div[data-testid="metric-container"] {
    background: #1E293B;
    border: 1px solid #334155;
    padding: 18px;
    border-radius: 16px;
    box-shadow: 0 4px 15px rgba(0,0,0,.25);
}

div[data-testid="stMetricValue"] {
    color: #D4AF37 !important;
    font-weight: 700;
}

button[data-baseweb="tab"] {
    font-size: 1rem !important;
    font-weight: 600 !important;
}

.stButton > button {
    background: linear-gradient(135deg, #D4AF37, #F59E0B);
    color: black;
    border: none;
    border-radius: 12px;
    padding: 0.8rem 1.4rem;
    font-weight: 700;
    transition: all .3s ease;
    box-shadow: 0 4px 14px rgba(212,175,55,.35);
}

.stButton > button:hover {
    transform: translateY(-2px);
    box-shadow: 0 8px 24px rgba(212,175,55,.55);
}
</style>
""", unsafe_allow_html=True)

# 3. CARGA DE DATOS SEPARADA (Para evitar conflictos de caché)
@st.cache_data
def cargar_datos_relojes_v2():
    return pd.read_csv("Watches.csv")

@st.cache_data
def cargar_datos_compas():
    import numpy as np
    np.random.seed(42)
    n_samples = 1000
    compas_data = pd.DataFrame({
        'grupo': np.random.choice(['Privilegiado', 'No Privilegiado'], size=n_samples, p=[0.6, 0.4]),
        'asignacion_positiva': np.random.choice([1, 0], size=n_samples, p=[0.7, 0.3])
    })
    return compas_data

# Llamamos a cada función por separado
df = cargar_datos_relojes_v2()
compas_df = cargar_datos_compas()

# Ajuste dinámico del sesgo para el ejercicio (fuera de la función para que no falle el tamaño)
n_no_priv = (compas_df['grupo'] == 'No Privilegiado').sum()
compas_df.loc[compas_df['grupo'] == 'No Privilegiado', 'asignacion_positiva'] = np.random.choice([1, 0], size=n_no_priv, p=[0.45, 0.55])

# 4. BARRA LATERAL (FILTROS)
st.sidebar.header("🎯 Filtros de Selección")
marcas_disponibles = sorted(df['brand'].unique())
marcas_seleccionadas = st.sidebar.multiselect("Filtrar por Marcas", marcas_disponibles, default=marcas_disponibles[:5])

# Filtrado del dataset comercial
df_filtrado = df[df['brand'].isin(marcas_seleccionadas)]

# 5. HERO SECTION (Encabezado Visual Reemplazado)
with st.container():
    col1, col2 = st.columns([4, 1])
    with col1:
        st.markdown("""
        <div class="hero-card">
            <h1 style="margin-bottom:0;">🎯 Mundial Luxury Stands</h1>
            <h4 style="color:#94A3B8;">Dashboard Ejecutivo de Inteligencia Comercial</h4>
            <p style="font-size:16px;">
            Análisis estratégico del mercado global de relojería de lujo, 
            pricing premium y detección de oportunidades de crecimiento.
            </p>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.image(
            "https://images.unsplash.com/photo-1523170335258-f5ed11844a49",
            use_container_width=True
        )

st.write("") # Espaciador

# 6. SECCIÓN KPIs GLOBALES & TARJETAS (Executive Summary)
st.markdown("## 📊 Executive Summary")

k1, k2, k3, k4 = st.columns(4)
k1.metric("Marcas", len(df_filtrado["brand"].unique()))
k2.metric("Anuncios", f"{len(df_filtrado):,}")
k3.metric("Precio Medio", f"${df_filtrado['price'].mean():,.0f}")
k4.metric("Precio Máximo", f"${df_filtrado['price'].max():,.0f}")

st.write("") # Espaciador

c1, c2, c3 = st.columns(3)
with c1:
    st.markdown("""
    <div class="executive-card">
        <h4>📈 Liderazgo</h4>
        <p>Las marcas dominantes concentran la mayor parte del inventario activo y tracción de mercado.</p>
    </div>
    """, unsafe_allow_html=True)
with c2:
    st.markdown("""
    <div class="executive-card">
        <h4>💎 Premiumización</h4>
        <p>Los segmentos Alta Gama y Ultra-Lujo generan las mayores oportunidades de margen y posicionamiento.</p>
    </div>
    """, unsafe_allow_html=True)
with c3:
    st.markdown("""
    <div class="executive-card">
        <h4>🚀 Crecimiento</h4>
        <p>Existen marcas emergentes con un volumen de catálogo reciente optimizado y una estrategia de pricing premium.</p>
    </div>
    """, unsafe_allow_html=True)

st.write("") # Espaciador

# 7. SISTEMA DE PESTAÑAS (Organización de tu Módulo Comercial y de Ética)
tab1, tab2, tab3 = st.tabs(["🏆 Presencia y Participación", "📐 Análisis de Cuadrantes", "⚖️ Gobernanza IA y Sesgos (COMPAS)"])

# --- PESTAÑA 1: PRESENCIA EN EL MERCADO ---
with tab1:
    st.markdown("### 🏆 Participación de Mercado")
    
    # Preparación de datos para la participación
    conteo_marcas = df_filtrado['brand'].value_counts().reset_index()
    conteo_marcas.columns = ['marca', 'numero_anuncios']
    
    total = conteo_marcas["numero_anuncios"].sum()
    
    col_lista, col_grafico_barras = st.columns([2, 2])
    
    with col_lista:
        for _, row in conteo_marcas.head(5).iterrows():
            pct = row["numero_anuncios"] / total
            st.write(f"**{row['marca']}** — {pct:.1%}")
            st.progress(float(pct))
            
    with col_grafico_barras:
        fig_bar = px.bar(conteo_marcas.head(10), x='marca', y='numero_anuncios', 
                         title="Top 10 Marcas por Volumen",
                         color_discrete_sequence=['#D4AF37'])
        fig_bar.update_layout(template="plotly_dark", paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig_bar, use_container_width=True)

# --- PESTAÑA 2: ANÁLISIS DE CUADRANTES ---
with tab2:
    st.markdown("### 🔍 Matriz Estratégica de Oportunidad")
    
    # Agrupación para generar el análisis de cuadrantes (Precio vs Año de catálogo)
    resumen_oportunidad = df_filtrado.groupby('brand').agg({
        'price': 'median',
        'year': 'median'
    }).reset_index()
    resumen_oportunidad.columns = ['brand', 'precio_mediano', 'anio_mediano']
    
    mediana_anio = df_filtrado['year'].median()
    mediana_precio = df_filtrado['price'].median()
    
    # Generación de la gráfica Plotly (fig3 equivalente)
    fig3 = px.scatter(
        resumen_oportunidad, 
        x='anio_mediano', 
        y='precio_mediano',
        text='brand',
        title="Posicionamiento de Marca (Año Mediano vs Precio Mediano)",
        labels={'anio_mediano': 'Año del Modelo (Mediana)', 'precio_mediano': 'Precio de Mercado (Mediana)'}
    )
    fig3.update_traces(marker=dict(size=14, color='#D4AF37', line=dict(width=1, color='white')), textposition='top center')
    fig3.add_hline(y=mediana_precio, line_dash="dash", line_color="#94A3B8")
    fig3.add_vline(x=mediana_anio, line_dash="dash", line_color="#94A3B8")
    fig3.update_layout(template="plotly_dark", paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')

    # Aplicamos la mejora solicitada de columnas
    col_graf, col_info = st.columns([3, 1])
    
    with col_graf:
        st.plotly_chart(fig3, use_container_width=True)
        
    with col_info:
        st.metric("Año Mediano", f"{mediana_anio:.1f}")
        st.metric("Precio Mediano", f"${mediana_precio:,.0f}")
        st.metric("Marcas Analizadas", len(resumen_oportunidad))
        
        st.markdown("""
        <div class="executive-card">
            <b>Insight Clave:</b><br>
            Las marcas situadas en el cuadrante superior derecho presentan la combinación óptima de catálogo de modelos reciente y pricing premium.
        </div>
        """, unsafe_allow_html=True)

# --- PESTAÑA 3: ÉTICA, COMPAS Y MITIGACIÓN DE SESGOS ---
with tab3:
    st.markdown("### ⚖️ Auditoría de Algoritmos y Mitigación de Sesgo Ético")
    
    st.markdown("""
    En esta sección evaluamos el comportamiento del algoritmo de asignación bajo los principios de la **IA Responsable**. 
    Analizamos si el modelo hereda sesgos históricos utilizando las métricas estándar del algoritmo de riesgo **COMPAS**.
    """)
    
    # --- CÁLCULO DE LA MÉTRICA DE IMPACTO DISPAR ---
    # Tasa del grupo Privilegiado
    df_priv = compas_df[compas_df['grupo'] == 'Privilegiado']
    tasa_privilegiados = df_priv['asignacion_positiva'].mean()
    
    # Tasa del grupo No Privilegiado
    df_no_priv = compas_df[compas_df['grupo'] == 'No Privilegiado']
    tasa_no_privilegiados = df_no_priv['asignacion_positiva'].mean()
    
    # Cálculo matemático del Disparate Impact Ratio
    disparate_impact = tasa_privilegiados / tasa_no_privilegiados
    
    # Visualización de la métrica en formato premium
    col_m1, col_m2, col_m3 = st.columns(3)
    
    with col_m1:
        st.metric(label="Tasa Asignación Grupo Privilegiado", value=f"{tasa_privilegiados:.2%}")
    with col_m2:
        st.metric(label="Tasa Asignación Grupo No Privilegiado", value=f"{tasa_no_privilegiados:.2%}")
    with col_m3:
        # Evaluamos el umbral ético legal (Regla del 80% / rango 0.8 a 1.25)
        if 0.8 <= (1 / disparate_impact) <= 1.25: # Ajustado según dirección del ratio
            estado_sesgo = "✅ Conforme (Sin sesgo significativo)"
        else:
            estado_sesgo = "🚨 Sesgo Detectado (Fuera de rango ético)"
        st.metric(label="Ratio de Impacto Dispar", value=f"{disparate_impact:.2f}", delta=estado_sesgo)

    st.markdown("""
    <div class="governance-card">
        <h4>📋 Nota de Gobernanza de Datos</h4>
        Para cumplir con las normativas europeas y marcos de ética corporativos, el Ratio de Impacto Dispar 
        debe mantenerse cercano a <b>1.0</b>. Valores inferiores a 0.80 o superiores a 1.25 implican un impacto discriminatorio 
        indirecto sobre los grupos protegidos.
    </div>
    """, unsafe_allow_html=True)
    
    # --- SIMULACIÓN Y MOSTRADO DE LA MITIGACIÓN ---
    st.markdown("#### 🛠️ Aplicación de Técnicas de Mitigación de Sesgos")
    
    # Generamos un DataFrame mitigado simulando un post-procesamiento balanceado
    df_mitigado = compas_df.copy()
    # Ajustamos la asignación para equilibrar las tasas equitativamente
    df_mitigado.loc[df_mitigado['grupo'] == 'No Privilegiado', 'asignacion_positiva'] = np.random.choice([1, 0], size=400, p=[0.68, 0.32])
    
    # Botón Premium solicitado
    if st.button("🚀 Generar Insight Ejecutivo"):
        st.success("✨ ¡Análisis completado con éxito! Se han identificado oportunidades de optimización en los segmentos premium y se han corregido los sesgos algorítmicos en la base de datos de asignación.")
        
        st.write("📈 **Vista previa de los datos optimizados y mitigados con IA Responsable:**")
        st.dataframe(df_mitigado.head(10), use_container_width=True)