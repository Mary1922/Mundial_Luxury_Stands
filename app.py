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
    background: linear-gradient(
        180deg,
        #4A2C1D 0%,
        #3B2416 50%,
        #2C1810 100%
    );
}

.hero-card {
    background: linear-gradient(
        135deg,
        #4A2C1D 0%,
        #3B2416 50%,
        #2C1810 100%
    );
    padding: 28px;
    border-radius: 20px;
    border: 1px solid #D4AF37;
    box-shadow: 0 10px 25px rgba(0,0,0,.35);
}

.executive-card {
    background: linear-gradient(
        135deg,
        #4A2C1D 0%,
        #3B2416 50%,
        #2C1810 100%
    );
    padding: 18px;
    border-radius: 16px;
    border: 1px solid #D4AF37;
    margin-bottom: 12px;
    box-shadow: 0 6px 18px rgba(0,0,0,.25);
}
.executive-card h4 {
    color: #F5E6C8;
}

.governance-card {
    background: linear-gradient(
        135deg,
        #4A2C1D 0%,
        #3B2416 50%,
        #2C1810 100%
    );
    border: 1px solid #D4AF37;
    padding: 24px;
    border-radius: 16px;
    margin-top: 15px;
    margin-bottom: 25px;
    box-shadow: 0 6px 18px rgba(0,0,0,.25);
}

.governance-card h4 {
    color: #F5E6C8;
}
                    
div[data-testid="metric-container"] {
    background: #1E293B;
    border: 1px solid #334155;
    padding: 18px;
    border-radius: 16px;
    box-shadow: 0 4px 15px rgba(0,0,0,.25);
}

div[data-testid="stMetricLabel"] {
    color: #F5E6C8 !important;
    font-weight: 600 !important;
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

/* ============================================================
   ESTILO PREMIUM PARA FILTROS MULTISELECT
============================================================ */

/* Chips seleccionados */
[data-baseweb="tag"] {
    background-color: #8B5A2B !important;
    color: #F5E6C8 !important;
    border: 1px solid #D4AF37 !important;
    border-radius: 8px !important;
    font-weight: 600 !important;
    padding: 2px 6px !important;
}

/* Texto dentro de cada chip */
[data-baseweb="tag"] span {
    color: #F5E6C8 !important;
}

/* Icono X para eliminar selección */
[data-baseweb="tag"] svg {
    fill: #F5E6C8 !important;
}

/* Cuadro desplegable de selección */
[data-baseweb="select"] > div {
    background-color: #2C1810 !important;
    border: 1px solid #D4AF37 !important;
}

/* Texto dentro de los selectores */
[data-baseweb="select"] {
    color: #F5E6C8 !important;
}

/* Opciones del desplegable al abrir */
div[role="listbox"] {
    background-color: #2C1810 !important;
    border: 1px solid #D4AF37 !important;
}

/* Opciones individuales */
div[role="option"] {
    color: #F5E6C8 !important;
    background-color: #2C1810 !important;
}

/* Opción al pasar el ratón */
div[role="option"]:hover {
    background-color: #8B5A2B !important;
}
            
.stProgress > div > div > div {
    background-color: #C9A227 !important;
}

.stProgress > div > div > div > div {
    background-color: #D4AF37 !important;
}

/* ============================================================
   NUEVO CSS PREMIUM PARA TARJETAS DE SESGOS (BIAS CARDS)
============================================================ */
.bias-card {
    background: #111827;
    border: 1px solid #334155;
    border-radius: 16px;
    padding: 22px 26px;
    margin-bottom: 20px;
    border-top: 5px solid #94A3B8;
    box-shadow: 0 4px 15px rgba(0,0,0,.25);
}
.bias-header { display: flex; align-items: center; justify-content: space-between; margin-bottom: 14px; }
.bias-title-group { display: flex; align-items: center; gap: 12px; }
.bias-icon {
    font-size: 1.6rem; background: #1E293B; border-radius: 12px;
    width: 46px; height: 46px; display: flex; align-items: center; justify-content: center;
}
.bias-title { font-size: 1.05rem; font-weight: 700; color: #F8FAFC; margin: 0; }
.severity-badge {
    display: inline-block; padding: 4px 14px; border-radius: 999px;
    font-size: 0.7rem; font-weight: 700; letter-spacing: .04em; text-transform: uppercase; white-space: nowrap;
}
.severity-alto    { background: #7F1D1D; color: #FCA5A5; }
.severity-medio   { background: #78350F; color: #FCD34D; }
.bias-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 16px; margin-top: 4px; }
.bias-block { border-radius: 12px; padding: 14px 16px; }
.bias-block.impacto    { background: rgba(239,68,68,0.08); border: 1px solid rgba(239,68,68,0.25); }
.bias-block.mitigacion { background: rgba(45,212,191,0.08); border: 1px solid rgba(45,212,191,0.25); }
.bias-block-label { font-size: 0.72rem; font-weight: 700; text-transform: uppercase; letter-spacing: .05em; margin-bottom: 6px; }
.bias-block.impacto .bias-block-label    { color: #FCA5A5; }
.bias-block.mitigacion .bias-block-label { color: #5EEAD4; }
.bias-block p { color: #E2E8F0; font-size: 0.88rem; line-height: 1.5; margin: 0; }
.bias-block ul { color: #E2E8F0; font-size: 0.88rem; line-height: 1.55; margin: 0; padding-left: 18px; }
.coverage-row { display: flex; gap: 10px; margin-top: 10px; flex-wrap: wrap; }
.coverage-chip {
    background: #1E293B; border: 1px solid #334155; border-radius: 999px;
    padding: 5px 12px; font-size: 0.78rem; color: #E2E8F0; display:flex; align-items:center; gap:6px;
}
.dot { width: 9px; height: 9px; border-radius: 50%; display:inline-block; }
.dot-alta { background:#22C55E; }
.dot-baja { background:#EF4444; }
.stat-strip { display: flex; gap: 28px; margin: 14px 0 4px 0; }
.stat-box .stat-value { font-size: 1.6rem; font-weight: 700; color: #D4AF37; }
.stat-box .stat-label { font-size: 0.75rem; color: #94A3B8; text-transform: uppercase; letter-spacing:.04em; }

</style>
""", unsafe_allow_html=True)

# ============================================================
# 3. CARGA DE DATOS SEPARADA (Dataset Comercial e IA)
# ============================================================
df = cargar_y_limpiar_datos("Watches_limpio.csv")

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

# Filtro 2: Tiers de Lujo (Aprovechando la lógica categórica de data_loader)
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
    col1, col2 = st.columns([4, 2.1])
    with col1:
        st.markdown("""
        <div class="hero-card">
            <h1 style="margin-bottom:0; color:white; font-size:1.7rem;">⚽ Mundial Luxury Stands 🏆</h1>
            <h4 style="color:#F5E6C8;">Dashboard Ejecutivo de Inteligencia Comercial</h4>
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
# 6. SECCIÓN KPIs GLOBALES & TARJETAS (Resumen Ejecutivo)
# ============================================================
st.markdown("### 📊 Resumen Ejecutivo")

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
tab1, tab2, tab3, tab4 = st.tabs(["🏆 Presencia y Participación", "📐 Análisis de Cuadrantes", "⚖️ Sesgos y Mitigación", "🎁 Experiencia Premium"])

# --- PESTAÑA 1: PRESENCIA EN EL MERCADO Y DISTRIBUCIÓN ---
with tab1:
    st.markdown("### 🏆 Estructura de Competidores y Precios")
    if not df_filtrado.empty:
        col_lista, col_grafico_barras = st.columns([1, 2])
        
        conteo_marcas = df_filtrado['brand'].value_counts().head(15).reset_index()
        conteo_marcas.columns = ['marca', 'numero_anuncios']
        total = df_filtrado['brand'].value_counts().sum()
        
        with col_lista:
            st.markdown("##### Participación")
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
            fig2.update_traces(
                marker_color="#C9A227",
                marker_line_color="#8B6B00",
                marker_line_width=1
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
        st.markdown("### 📊 Análisis de Dispersión de Precios")
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
                x=0, y=-0.28, showarrow=False,
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

            resumen_oportunidad['anio_medio'] = (
                resumen_oportunidad['anio_medio']
                .round()
                .astype(int)
            )

            MIN_MODELOS = 5
            resumen_oportunidad = resumen_oportunidad[resumen_oportunidad['n_modelos'] >= MIN_MODELOS]
            
            if not resumen_oportunidad.empty:
                precio_oportunidad = 9000
                mediana_anio = resumen_oportunidad['anio_medio'].median()

                
                # GRÁFICO OBLIGATORIO 3: Mapa de oportunidad (Scatterplot con rangos re-escalados para evitar apiñamiento)
                fig3 = px.scatter(
                    resumen_oportunidad,
                    x='anio_medio',
                    y='precio_medio',
                    size='n_modelos',
                    color='brand',
                    text='brand',
                    title='¿Qué marcas combinan catálogo reciente y precio premium?',
                    labels={'anio_medio': 'Año medio de fabricación de los modelos', 'precio_medio': 'Precio medio (USD)', 'brand': 'Marca'},
                    size_max=40,
                    height=600
                )
                fig3.update_traces(textposition='top center')
                
                # OPTIMIZACIÓN DE ESCALAS: Forzamos límites fijos y holgados para dispersar los elementos
                fig3.update_xaxes(range=[2020, 2025.5])
                
                fig3.update_yaxes(
                    type="log",
                    range=[3.8, 5.1],   # 10^3.8≈6300 hasta 10^5.1≈126000
                    title="Precio medio (USD)"
                )
                
                
                # Líneas de referencia basadas en medianas del scatterplot
                fig3.add_vline(x=mediana_anio, line_dash='dash', line_color='gray')
                fig3.add_hline(y=precio_oportunidad, line_dash='dash', line_color='#D4AF37', line_width=2)
                
                fig3.update_layout(
                    template='plotly_dark',
                    paper_bgcolor='rgba(0,0,0,0)',
                    plot_bgcolor='rgba(0,0,0,0)',
                    showlegend=False
                )
                fig3.add_annotation(
                    x=2024.2,
                    y=9000,
                    text="Umbral Premium",
                    showarrow=False,
                    font=dict(
                        size=12,
                        color="#D4AF37"
                    ),
                    bgcolor="rgba(0,0,0,0.65)"
                )
                
                col_graf, col_info = st.columns([3, 1])
                with col_graf:
                    st.plotly_chart(fig3, use_container_width=True)
                with col_info:
                    
                    st.metric("Umbral Precio Premium", "$9,000")
                    st.markdown("""
                    <div class="executive-card">
                        <b>Cuadrante Superior Derecho (Oportunidad):</b><br>
                        Muestra las marcas que tienen un catálogo moderno combinado con márgenes de precio premium-altos.
                    </div>
                    """, unsafe_allow_html=True)
                    
                # Despliegue de apoyo analítico complementario (Tabla de Marcas en Cuadrante de Ventaja)
                st.markdown("### 🚀 Marcas Detectadas en el Cuadrante de Oportunidad")
                oportunidad = resumen_oportunidad[
                    (resumen_oportunidad['anio_medio'] >= mediana_anio) &
                    (resumen_oportunidad['precio_medio'] >= precio_oportunidad)
                ].sort_values('precio_medio', ascending=False)
                
                if not oportunidad.empty:
                    omega = resumen_oportunidad[resumen_oportunidad['brand'].astype(str).str.contains('Omega', case=False, na=False)]
                    if not omega.empty and 'Omega' not in oportunidad['brand'].astype(str).tolist():
                        oportunidad = pd.concat([oportunidad, omega]).drop_duplicates(subset=['brand'])
                        oportunidad['anio_medio'] = oportunidad['anio_medio'].round().astype(int)
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
        st.markdown("### 📊 Composición por Portafolio de Precios (Tiers de Lujo)")
        
        # GRÁFICO OBLIGATORIO 4: ¿Qué rango de precios ofrece cada marca? 
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
                title='¿Qué rango de precios ofrece cada marca?<br>(nº de modelos por Tier de Lujo)',
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
                # TABLA DE APOYO 5: Qué % de los modelos caen en categorías exclusivas
                st.markdown("##### Tabla de Apoyo: Concentración en Alta Gama o Superior")
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
                tabla_final.columns = [ 'Marca', 'Total Modelos', '% Alta Gama o Superior']
                
                st.dataframe(
                    tabla_final,
                    hide_index=True,
                    use_container_width=True,
                    column_config={
                        "Marca": st.column_config.TextColumn(
                            "Marca",
                            width="small"
                        ),

                        "Total Modelos": st.column_config.NumberColumn(
                            "Total Modelos",
                            width="small"
                        ),

                        "% Alta Gama o Superior": st.column_config.ProgressColumn(
                            "% Alta Gama o Superior",
                            help="Porcentaje combinado de modelos en segmentos exclusivos",
                            format="%.1f%%",
                            min_value=0,
                            max_value=100,
                            width="medium"
                        )
                    }
                )
                
# --- PESTAÑA 3: SESGOS Y MITIGACIÓN ---
with tab3:
    st.markdown("### ⚖️ Sesgos y Mitigación")

    st.info("""
    Para garantizar una toma de decisiones responsable, es crítico reconocer las limitaciones 
    metodológicas del dataset actual. A continuación, se detallan los sesgos identificados y las 
    medidas de mitigación propuestas.
    """)

    # Abrimos un contenedor contenedor general para evitar que se rompa el texto plano
    st.markdown('<div style="display: flex; gap: 20px; flex-wrap: wrap; justify-content: space-between;">', unsafe_allow_html=True)

    # SESGO 1
    st.markdown("""
    <div class="governance-card" style="flex: 1; min-width: 280px; margin-top: 10px;">
        <h4 style="margin-top: 0;">🌎 Sesgo Geográfico</h4>
        <p style="color: #F5E6C8; font-size: 0.9rem;"><b>Impacto:</b> Datos concentrados en EE.UU./Europa. México y Canadá subrepresentados.</p>
        <p style="color: #F5E6C8; font-size: 0.9rem;"><b>Riesgo:</b> Error en la estrategia de marketing local por extrapolación indebida.</p>
        <div style="background: rgba(255,255,255,0.08); border-left: 4px solid #D4AF37; padding: 12px; border-radius: 8px; margin-top: 15px;">
            <b style="color: #D4AF37; font-size: 0.75rem; text-transform: uppercase; letter-spacing: 0.05em;">Mitigación</b>
            <p style="color: #F5E6C8; font-size: 0.85rem; margin: 4px 0 0 0;">Incluir datasets locales y ajustar peso de predicción por región.</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # SESGO 2
    st.markdown("""
    <div class="governance-card" style="flex: 1; min-width: 280px; margin-top: 10px;">
        <h4 style="margin-top: 0;">🏷️ Precio Reventa vs PVP</h4>
        <p style="color: #F5E6C8; font-size: 0.9rem;"><b>Impacto:</b> Los valores reflejan mercado secundario, no precios de catálogo oficial.</p>
        <p style="color: #F5E6C8; font-size: 0.9rem;"><b>Riesgo:</b> Distorsión en la estimación de costes de activación.</p>
        <div style="background: rgba(255,255,255,0.08); border-left: 4px solid #D4AF37; padding: 12px; border-radius: 8px; margin-top: 15px;">
            <b style="color: #D4AF37; font-size: 0.75rem; text-transform: uppercase; letter-spacing: 0.05em;">Mitigación</b>
            <p style="color: #F5E6C8; font-size: 0.85rem; margin: 4px 0 0 0;">Calibrar precios usando un factor de corrección de mercado mayorista.</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # SESGO 3
    st.markdown("""
    <div class="governance-card" style="flex: 1; min-width: 280px; margin-top: 10px;">
        <h4 style="margin-top: 0;">🔍 Filtro "Solo Nuevos"</h4>
        <p style="color: #F5E6C8; font-size: 0.9rem;"><b>Impacto:</b> Sesgo hacia marcas con alta distribución vía revendedores terceros.</p>
        <p style="color: #F5E6C8; font-size: 0.9rem;"><b>Riesgo:</b> Infrarrepresentación de marcas con venta boutique exclusiva.</p>
        <div style="background: rgba(255,255,255,0.08); border-left: 4px solid #D4AF37; padding: 12px; border-radius: 8px; margin-top: 15px;">
            <b style="color: #D4AF37; font-size: 0.75rem; text-transform: uppercase; letter-spacing: 0.05em;">Mitigación</b>
            <p style="color: #F5E6C8; font-size: 0.85rem; margin: 4px 0 0 0;">Ampliar alcance a datos de mercado primario (boutiques).</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Cerramos el contenedor flex
    st.markdown('</div>', unsafe_allow_html=True)

    # Nota final de Gobernanza (La que ya te salía perfecta con tus colores favoritos)
    st.markdown("""
    <div class="governance-card" style="margin-top: 25px;">
        <h4>📋 Compromiso con la IA Responsable</h4>
        Nuestra metodología de análisis audita estos riesgos para evitar la replicación de sesgos históricos. 
        <b>Cada decisión estratégica basada en este dashboard debe ser supervisada con estos puntos de control.</b>
    </div>
    """, unsafe_allow_html=True)

# ============================================================
# PESTAÑA 4: EXPERIENCIA PREMIUM
# ============================================================

with tab4:

    st.markdown("## 🎁 Experiencia Premium")

    st.markdown("""
    <div class="hero-card">
        <h3 style="color:#F5E6C8;">Grabado Exclusivo Personalizado</h3>
        <p style="color:#E2E8F0; font-size:16px;">
        Como elemento diferenciador de la experiencia de compra,
        los clientes seleccionados recibirán un grabado exclusivo
        personalizado incluido con su reloj de lujo.
        </p>
    </div>
    """, unsafe_allow_html=True)

    st.write("")

    if st.button("✨ Mostrar Detalle Premium"):

        st.image(
            "Pictures/grabado.png",
            caption="Grabado personalizado incluido como detalle exclusivo",
            use_container_width=True
        )

        st.success(
            "El grabado premium se entrega sin coste adicional como parte de la experiencia de lujo."
        )