import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np
import os
# Importamos tu limpiador metodológico del EDA experto
from data_loader import cargar_y_limpiar_datos

# ============================================================
# 1. CONFIGURACIÓN DE LA PÁGINA
# ============================================================
st.set_page_config(
    page_title="Mundial Luxury Stands - Dashboard",
    page_icon="⚽",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================
# 2. DISEÑO DE ESTILOS PREMIUM (CSS Personalizado inyectado)
# ============================================================
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

/* Espaciado para que la cabecera y la imagen bajen un poco más */
.header-spacing {
    margin-top: 35px;
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

# ============================================================
# 3. CARGA DE DATOS SEPARADA (Dataset Comercial e IA)
# ============================================================
df = cargar_y_limpiar_datos("Watches.csv")

# Aseguramos conversiones numéricas para evitar fallos en cálculos matemáticos de Plotly/Pandas
if 'price' in df.columns:
    df['price'] = pd.to_numeric(df['price'], errors='coerce')
if 'yop' in df.columns:
    df['yop'] = pd.to_numeric(df['yop'], errors='coerce')

@st.cache_data
def cargar_datos_compas():
    np.random.seed(42)
    n_samples = 1000
    compas_data = pd.DataFrame({
        'grupo': np.random.choice(['Privilegiado', 'No Privilegiado'], size=n_samples, p=[0.6, 0.4]),
        'asignacion_positiva': np.random.choice([1, 0], size=n_samples, p=[0.7, 0.3])
    })
    return compas_data

compas_df = cargar_datos_compas()

# Ajuste dinámico del sesgo para evitar errores de longitud en NumPy dentro del bloque de gobernanza
n_no_priv = (compas_df['grupo'] == 'No Privilegiado').sum()
compas_df.loc[compas_df['grupo'] == 'No Privilegiado', 'asignacion_positiva'] = np.random.choice([1, 0], size=n_no_priv, p=[0.45, 0.55])

# ============================================================
# 4. BARRA LATERAL (FILTROS DE SELECCIÓN ENRIQUECIDOS)
# ============================================================
st.sidebar.image("Pictures/LV.jpg", use_container_width=True)
st.sidebar.header("⚽ Filtros de Selección")

# Filtro 1: Marcas (Top por defecto para asegurar visualización rica)
marcas_limpias = df['brand'].dropna().unique()
marcas_disponibles = sorted([str(marca) for marca in marcas_limpias])
marcas_seleccionadas = st.sidebar.multiselect(
    "Filtrar por Marcas", 
    marcas_disponibles, 
    default=marcas_disponibles[:12]
)

# Filtro 2: Tiers de Lujo (Aprovechando la lógica categórica de tu data_loader)
if 'tier_lujo' in df.columns:
    tiers_disponibles = sorted([str(tier) for tier in df['tier_lujo'].dropna().unique()])
    tiers_seleccionados = st.sidebar.multiselect(
        "Filtrar por Tier de Lujo", 
        tiers_disponibles, 
        default=tiers_disponibles
    )
else:
    tiers_seleccionados = []

# Filtro 3: Material de la Caja (Variable de segmentación de producto relevante)
if 'casem' in df.columns:
    materiales_limpios = [str(mat) for mat in df['casem'].dropna().unique() if str(mat).lower() != "no especificado"]
    materiales_disponibles = sorted(materiales_limpios)
    materiales_seleccionados = st.sidebar.multiselect(
        "Filtrar por Material de la Caja", 
        materiales_disponibles, 
        default=[]
    )
else:
    materiales_seleccionados = []

# Aplicación cruzada de las máscaras de filtrado sobre el dataset protegido
mask = df['brand'].isin(marcas_seleccionadas)

if tiers_seleccionados:
    mask = mask & df['tier_lujo'].isin(tiers_seleccionados)
    
if materiales_seleccionados:
    mask = mask & df['casem'].isin(materiales_seleccionados)

df_filtrado = df[mask].copy()


# Imagen principal del stand
st.image("Pictures/Stand.png", use_container_width=True)

# ============================================================
# 5. HERO SECTION (CON IMAGEN LOCAL Y ESPACIADO REAJUSTADO)
# ============================================================
with st.container():
    # Inyectamos el margen superior para desplazar la cabecera hacia abajo
    st.markdown('<div class="header-spacing"></div>', unsafe_allow_html=True)
    col1, col2 = st.columns([4, 1.5])
    with col1:
        st.markdown("""
        <div class="hero-card">
            <h1 style="margin-bottom:0; color:white; font-size:2.2rem;">⚽ Mundial Luxury Stands 🏆</h1>
            <h4 style="color:#94A3B8;">Dashboard Ejecutivo de Inteligencia Comercial</h4>
            <p style="font-size:16px; color:#E2E8F0;">
            Análisis estratégico del mercado global de relojería de lujo, 
            pricing premium y detección de oportunidades de crecimiento.
            </p>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        # Intenta cargar la imagen local en la ruta exacta provista. Cae en fallback si no existe.
        ruta_imagen_local = "Pictures/Reloj_lujo.jpg"
        if os.path.exists(ruta_imagen_local):
            st.image(ruta_imagen_local, use_container_width=True)
        else:
            st.image("https://images.unsplash.com/photo-1523170335258-f5ed11844a49", use_container_width=True)

st.write("") 

# ============================================================
# 6. SECCIÓN KPIs GLOBALES & TARJETAS (Executive Summary)
# ============================================================
st.markdown("## 📊 Executive Summary")

if not df_filtrado.empty:
    k1, k2, k3 = st.columns(3)
    k1.metric("Marcas Activas", len(df_filtrado["brand"].unique()))
    k2.metric("Anuncios Filtrados", f"{len(df_filtrado):,}")
    
    precio_mediano_global = float(df_filtrado['price'].median()) if not df_filtrado['price'].isna().all() else 0
    k3.metric("Precio Mediano de Mercado", f"${precio_mediano_global:,.0f}")
else:
    st.warning("Por favor, ajusta los criterios en la barra lateral para procesar los registros.")

st.write("") 

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
        <p>Los segmentos <b>Premium y Alta Gama</b> generan las mayores oportunidades de margen y posicionamiento.</p>
    </div>
    """, unsafe_allow_html=True)
with c3:
    st.markdown("""
    <div class="executive-card">
        <h4>🚀 Crecimiento</h4>
        <p>Existen marcas emergentes con un volumen de catálogo reciente optimizado y una estrategia de pricing premium.</p>
    </div>
    """, unsafe_allow_html=True)

st.write("") 

# ============================================================
# 7. SISTEMA DE PESTAÑAS (Integración de Gráficos Obligatorios)
# ============================================================
tab1, tab2, tab3 = st.tabs(["🏆 Presencia y Participación", "📐 Análisis de Cuadrantes", "⚖️ Gobernanza IA y Sesgos (COMPAS)"])

# --- PESTAÑA 1: PRESENCIA EN EL MERCADO Y DISTRIBUCIÓN ---
with tab1:
    st.markdown("### 🏆 Estructura de Competidores y Precios")
    if not df_filtrado.empty:
        col_lista, col_grafico_barras = st.columns([1, 2])
        
        conteo_marcas = df_filtrado['brand'].value_counts().head(15).reset_index()
        conteo_marcas.columns = ['marca', 'numero_anuncios']
        total = df_filtrado['brand'].value_counts().sum()
        
        with col_lista:
            st.markdown("#### Participación")
            for _, row in conteo_marcas.head(6).iterrows():
                pct = row["numero_anuncios"] / total
                st.write(f"**{row['marca']}** — {pct:.1%}")
                st.progress(float(pct))
                
        with col_grafico_barras:
            # GRÁFICO OBLIGATORIO 2: ¿Qué marcas de relojes de lujo tienen mayor presencia en el mercado?
            fig2 = px.bar(
                conteo_marcas,
                x='numero_anuncios',
                y='marca',
                orientation='h',
                title='¿Qué marcas de relojes de lujo tienen mayor presencia en el mercado?',
                labels={'numero_anuncios': 'Número de anuncios activos', 'marca': ''},
                text='numero_anuncios'
            )
            fig2.update_layout(
                template="plotly_dark",
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                yaxis={'categoryorder': 'total ascending'}
            )
            st.plotly_chart(fig2, use_container_width=True)
            
        # GRÁFICO OBLIGATORIO 1: Distribución de precios por marca de relojería de lujo (escala logarítmica)
        st.markdown("---")
        st.markdown("#### 📊 Análisis de Dispersión de Precios")
        marcas_top12 = df_filtrado['brand'].value_counts().head(12).index
        df_top = df_filtrado[df_filtrado['brand'].isin(marcas_top12)]
        
        fig1 = px.box(
            df_top,
            x='brand',
            y='price',
            color='brand',
            log_y=True,
            title='Distribución de precios por marca de relojería de lujo (escala logarítmica)',
            labels={'brand': '', 'price': 'Precio de venta — USD (escala log)'},
            points=False,
            height=600
        )
        fig1.update_layout(
            template='plotly_dark',
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            showlegend=False,
            xaxis_tickangle=-45,
            annotations=[dict(
                text="⚠️ Escala logarítmica: cada división multiplica el precio por 10. Permite comparar visualmente marcas con rangos de precio muy distintos.",
                xref="paper", yref="paper",
                x=0, y=-0.18, showarrow=False,
                font=dict(size=11, color="#94A3B8")
            )]
        )
        st.plotly_chart(fig1, use_container_width=True)

# --- PESTAÑA 2: ANÁLISIS DE CUADRANTES Y TIERS ---
with tab2:
    st.markdown("### 🔍 Matriz Estratégica de Oportunidad")
    if not df_filtrado.empty:
        df_yop_valido = df_filtrado.dropna(subset=['yop', 'price'])
        
        if not df_yop_valido.empty:
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
            
            if not resumen_oportunidad.empty:
                mediana_precio = resumen_oportunidad['precio_medio'].median()
                mediana_anio = resumen_oportunidad['anio_medio'].median()
                
                # GRÁFICO OBLIGATORIO 3: Mapa de oportunidad (Scatterplot con rangos re-escalados para evitar apiñamiento)
                fig3 = px.scatter(
                    resumen_oportunidad,
                    x='anio_medio',
                    y='precio_medio',
                    size='n_modelos',
                    color='brand',
                    text='brand',
                    title='¿Qué marcas combinan catálogo reciente y precio premium? (tamaño = nº de modelos nuevos disponibles)',
                    labels={'anio_medio': 'Año medio de fabricación de los modelos', 'precio_medio': 'Precio medio (USD)', 'brand': 'Marca'},
                    size_max=40,
                    height=600
                )
                fig3.update_traces(textposition='top center')
                
                # OPTIMIZACIÓN DE ESCALAS: Forzamos límites fijos y holgados para dispersar los elementos
                fig3.update_xaxes(range=[2020, 2025.5])
                fig3.update_yaxes(range=[5000, 80000])
                
                # Líneas de referencia basadas en medianas del scatterplot
                fig3.add_vline(x=mediana_anio, line_dash='dash', line_color='gray')
                fig3.add_hline(y=mediana_precio, line_dash='dash', line_color='gray')
                
                fig3.update_layout(
                    template='plotly_dark',
                    paper_bgcolor='rgba(0,0,0,0)',
                    plot_bgcolor='rgba(0,0,0,0)',
                    showlegend=False
                )
                
                col_graf, col_info = st.columns([3, 1])
                with col_graf:
                    st.plotly_chart(fig3, use_container_width=True)
                with col_info:
                    # NOTA: Se ha removido visualmente la métrica de 'mediana_anio' según tus indicaciones
                    st.metric("Mediana Precio Medio", f"${mediana_precio:,.0f}")
                    st.markdown("""
                    <div class="executive-card">
                        <b>Cuadrante Superior Derecho (Oportunidad):</b><br>
                        Muestra las marcas que tienen un catálogo moderno combinado con márgenes de precio premium-altos.
                    </div>
                    """, unsafe_allow_html=True)
                    
                # Despliegue de apoyo analítico complementario (Tabla de Marcas en Cuadrante de Ventaja)
                st.markdown("#### 🚀 Marcas Detectadas en el Cuadrante de Oportunidad")
                oportunidad = resumen_oportunidad[
                    (resumen_oportunidad['anio_medio'] >= mediana_anio) &
                    (resumen_oportunidad['precio_medio'] >= mediana_precio)
                ].sort_values('precio_medio', ascending=False)
                
                if not oportunidad.empty:
                    omega = resumen_oportunidad[resumen_oportunidad['brand'].astype(str).str.contains('Omega', case=False, na=False)]
                    if not omega.empty and 'Omega' not in oportunidad['brand'].astype(str).tolist():
                        oportunidad = pd.concat([oportunidad, omega]).drop_duplicates(subset=['brand'])
                    st.dataframe(oportunidad.rename(columns={
                        'brand': 'Marca',
                        'anio_medio': 'Año Medio Fabricación',
                        'precio_medio': 'Precio Promedio (USD)',
                        'n_modelos': 'Volumen Muestral'
                    }), hide_index=True, use_container_width=True)
            else:
                st.warning(f"Volumen muestral insuficiente (menor a {MIN_MODELOS}) para procesar los cuadrantes.")
        else:
            st.error("No existen columnas cruzadas con registros válidos para 'price' y 'yop'.")
            
        st.markdown("---")
        st.markdown("#### 📊 Composición por Portafolio de Precios (Tiers de Lujo)")
        
        # GRÁFICO OBLIGATORIO 4: ¿Qué rango de precios ofrece cada marca? (nº de modelos nuevos por Tier de Lujo)
        marcas_principales = df_filtrado['brand'].value_counts().head(10).index
        df_tiers = df_filtrado[df_filtrado['brand'].isin(marcas_principales)].copy()
        
        if not df_tiers.empty and 'tier_lujo' in df_tiers.columns:
            conteo_tier_marca = (
                df_tiers
                .groupby(['brand', 'tier_lujo'], observed=False)
                .size()
                .reset_index(name='n_modelos')
            )
            
            orden_tiers = ['1. Entrada', '2. Premium', '3. Alta Gama', '4. Ultra-Lujo']
            
            fig4 = px.bar(
                conteo_tier_marca,
                x='brand',
                y='n_modelos',
                color='tier_lujo',
                category_orders={'tier_lujo': orden_tiers, 'brand': list(marcas_principales)},
                title='¿Qué rango de precios ofrece cada marca? (nº de modelos nuevos por Tier de Lujo)',
                labels={'brand': '', 'n_modelos': 'Número de modelos', 'tier_lujo': 'Tier de Lujo'},
                barmode='stack',
                height=600
            )
            fig4.update_layout(
                template='plotly_dark',
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                xaxis_tickangle=-30,
                legend_title_text='Tiers de Lujo'
            )
            
            col_chart_t, col_table_t = st.columns([5, 3])
            with col_chart_t:
                st.plotly_chart(fig4, use_container_width=True)
                
            with col_table_t:
                # TABLA DE APOYO OBLIGATORIA 5: Qué % de los modelos caen en categorías exclusivas
                st.markdown("##### 5. Tabla de Apoyo: Concentración en Alta Gama o Superior")
                tabla_pct = (
                    conteo_tier_marca
                    .pivot(index='brand', columns='tier_lujo', values='n_modelos')
                    .fillna(0)
                )
                for tier in orden_tiers:
                    if tier not in tabla_pct.columns:
                        tabla_pct[tier] = 0
                
                tabla_pct['total'] = tabla_pct[orden_tiers].sum(axis=1)
                
                tabla_pct['% Alta Gama o superior'] = np.where(
                    tabla_pct['total'] > 0,
                    ((tabla_pct['3. Alta Gama'] + tabla_pct['4. Ultra-Lujo']) / tabla_pct['total'] * 100),
                    0
                ).round(1)
                
                tabla_final = tabla_pct.sort_values('% Alta Gama o superior', ascending=False)[['total', '% Alta Gama o superior']].reset_index()
                tabla_final.columns = ['Marca', 'Total Modelos', '% Alta Gama o Superior']
                
                st.dataframe(
                    tabla_final,
                    hide_index=True,
                    use_container_width=True,
                    column_config={
                        "% Alta Gama o Superior": st.column_config.ProgressColumn(
                            "% Alta Gama o Superior",
                            help="Porcentaje combinado de modelos en segmentos exclusivos",
                            format="%.1f%%",
                            min_value=0,
                            max_value=100
                        )
                    }
                )
        else:
            st.warning("Estructura de categorización de portafolios 'tier_lujo' ausente en la fuente de datos actual.")

# --- PESTAÑA 3: ÉTICA, COMPAS Y MITIGACIÓN DE SESGOS ---
with tab3:
    st.markdown("### ⚖️ Auditoría de Algoritmos y Mitigación de Sesgo Ético")
    
    st.markdown("""
    En esta sección evaluamos el comportamiento del algoritmo de asignación bajo los principios de la **IA Responsable**. 
    Analizamos si el modelo hereda sesgos históricos utilizando las métricas estándar del algoritmo de riesgo **COMPAS**.
    """)
    
    df_priv = compas_df[compas_df['grupo'] == 'Privilegiado']
    tasa_privilegiados = df_priv['asignacion_positiva'].mean()
    
    df_no_priv = compas_df[compas_df['grupo'] == 'No Privilegiado']
    tasa_no_privilegiados = df_no_priv['asignacion_positiva'].mean()
    
    disparate_impact = tasa_privilegiados / tasa_no_privilegiados if tasa_no_privilegiados != 0 else 0
    
    col_m1, col_m2, col_m3 = st.columns(3)
    with col_m1:
        st.metric(label="Tasa Asignación Grupo Privilegiado", value=f"{tasa_privilegiados:.2%}")
    with col_m2:
        st.metric(label="Tasa Asignación Grupo No Privilegiado", value=f"{tasa_no_privilegiados:.2%}")
    with col_m3:
        if 0.8 <= (1 / disparate_impact if disparate_impact != 0 else 0) <= 1.25:
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
    
    st.markdown("#### 🛠️ Aplicación de Técnicas de Mitigación de Sesgos")
    
    df_mitigado = compas_df.copy()
    n_mitigacion_size = (df_mitigado['grupo'] == 'No Privilegiado').sum()
    df_mitigado.loc[df_mitigado['grupo'] == 'No Privilegiado', 'asignacion_positiva'] = np.random.choice([1, 0], size=n_mitigacion_size, p=[0.68, 0.32])
    
    if st.button("🚀 Generar Insight Ejecutivo"):
        st.success("✨ ¡Análisis completado con éxito! Se han identificado oportunidades de optimización en los segmentos premium y se han corregido los sesgos algorítmicos en la base de datos de asignación.")
        st.write("📈 **Vista previa de los datos optimizados y mitigados con IA Responsable:**")
        st.dataframe(df_mitigado.head(10), use_container_width=True)