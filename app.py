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

# Cargar los datos limpios y filtrados (df_nuevos)
try:
    df_campaign = cargar_y_limpiar_datos("Watches.csv")
except Exception as e:
    st.error(f"Error al cargar 'Watches.csv'. Asegúrate de que el archivo está en la raíz: {e}")
    st.stop()

# ============================================================
# SECCIÓN DE GOBERNANZA Y ADVERTENCIA DE SESGOS
# ============================================================
st.title("🎯 Estrategia de Campaña: Mundial Luxury Stands")

st.warning("""
### ⚠️ ADVERTENCIA METODOLÓGICA Y MITIGACIÓN DE SESGOS
**Análisis de Calidad de Datos (Gobernanza y Data Ethics):**
El dataset original presentaba un **74.73% de valores nulos (NaN)** en la columna de condición del reloj. 

Asumir arbitrariamente que los registros vacíos corresponden a unidades nuevas para incrementar artificialmente el volumen de la campaña representaría un **Sesgo de Selección Masivo**. La lógica de mercado demuestra que los vendedores omiten la condición principalmente en piezas de segunda mano o vintage. 

**Acción de Mitigación:** Este cuadro de mando trabaja **únicamente** con los registros con etiquetado explícito `New` y `Unworn` (universo de **23,146 anuncios seguros**), garantizando la integridad de las proyecciones financieras de la campaña.
""")

st.write("---")

# ============================================================
# BARRA LATERAL: FILTROS CRUZADOS DINÁMICOS
# ============================================================
st.sidebar.header("🎛️ Filtros de Campaña")

# Filtro interactivo de Marcas (Inicializado con las TOP 12 automáticas)
top12_marcas_auto = list(df_campaign['brand'].value_counts().head(12).index)
marcas_disponibles = sorted(df_campaign['brand'].dropna().unique())

marcas_seleccionadas = st.sidebar.multiselect(
    "Selecciona las Marcas para el Análisis:", 
    options=marcas_disponibles, 
    default=top12_marcas_auto
)

# Aplicamos el filtro dinámico intermedio
df_filtrado = df_campaign[df_campaign['brand'].isin(marcas_seleccionadas)]

# Filtro secundario cruzado: Tier de Lujo
if 'tier_lujo' in df_filtrado.columns:
    tiers_disponibles = sorted(df_filtrado['tier_lujo'].dropna().unique())
    tiers_seleccionados = st.sidebar.multiselect("Filtrar por Tier de Lujo:", options=tiers_disponibles, default=tiers_disponibles)
    df_filtrado = df_filtrado[df_filtrado['tier_lujo'].isin(tiers_seleccionados)]

# ============================================================
# MAQUETACIÓN DE LAS PESTAÑAS DEL EDA (TUS 5 VISUALIZACIONES)
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
    st.subheader("Análisis de Dispersión y Rangos de Precio")
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
            height=600
        )
        fig1.update_layout(
            template='plotly_white',
            showlegend=False,
            xaxis_tickangle=-45,
            margin=dict(b=80)
        )
        st.plotly_chart(fig1, use_container_width=True)
        st.caption("⚠️ **Escala logarítmica activa:** Cada división multiplica el precio por 10. Permite comparar visualmente marcas con rangos de precio muy distintos sin deformar las cajas.")
    else:
        st.info("Selecciona marcas en la barra lateral para generar la visualización.")

# ------------------------------------------------------------
# PESTAÑA 2: Gráfico 2 (Barras Horizontales de Volumen)
# ------------------------------------------------------------
with tab2:
    st.subheader("Volumen y Participación de la Oferta")
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
            height=550
        )
        fig2.update_layout(
            template='plotly_white',
            yaxis={'categoryorder': 'total ascending'}
        )
        st.plotly_chart(fig2, use_container_width=True)
    else:
        st.info("Sin datos disponibles para generar el ranking de volumen.")

# ------------------------------------------------------------
# PESTAÑA 3: Gráfico 3 (Burbujas y Cuadrantes Estratégicos)
# ------------------------------------------------------------
with tab3:
    st.subheader("Matriz Estratégica: Antigüedad vs. Pricing")
    
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
        
        # Filtro de seguridad metodológico
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
                title='¿Qué marcas combinan catálogo reciente y precio premium? (tamaño = nº de modelos nuevos disponibles)',
                labels={'anio_medio': 'Año medio de fabricación', 'precio_medio': 'Precio medio (USD)', 'brand': 'Marca'},
                size_max=40,
                height=600
            )
            fig3.update_traces(textposition='top center')
            fig3.add_vline(x=mediana_anio, line_dash='dash', line_color='gray')
            fig3.add_hline(y=mediana_precio, line_dash='dash', line_color='gray')
            fig3.update_layout(template='plotly_white', showlegend=False)
            
            st.plotly_chart(fig3, use_container_width=True)
            
            # --- OUTPUT DE APOYO DEL GRÁFICO 3 (KPIs y Tabla de Oportunidad) ---
            col_kpi1, col_kpi2 = st.columns(2)
            col_kpi1.metric("Mediana Global de Año", f"{mediana_anio:.1f}")
            col_kpi2.metric("Mediana Global de Precio", f"${mediana_precio:,.0f}")
            
            st.write("#### 🚀 Marcas en el Cuadrante de Oportunidad (Catálogo Reciente + Precio Alto):")
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
    st.subheader("Estructura de Mercado por Niveles de Lujo")
    
    if 'tier_lujo' in df_filtrado.columns and len(df_filtrado) > 0:
        conteo_tier_marca = (
            df_filtrado
            .groupby(['brand', 'tier_lujo'])
            .size()
            .reset_index(name='n_modelos')
        )
        
        orden_tiers = ['1. Entrada', '2. Premium', '3. Alta Gama', '4. Ultra-Lujo']
        
        # Gráfico 4: Barras Apiladas
        fig4 = px.bar(
            conteo_tier_marca,
            x='brand',
            y='n_modelos',
            color='tier_lujo',
            category_orders={'tier_lujo': orden_tiers},
            title='¿Qué rango de precios ofrece cada marca? (nº de modelos nuevos por Tier de Lujo)',
            labels={'brand': 'Marca', 'n_modelos': 'Número de modelos', 'tier_lujo': 'Tier de Lujo'},
            height=550
        )
        fig4.update_layout(template='plotly_white', xaxis_tickangle=-30, barmode='stack')
        st.plotly_chart(fig4, use_container_width=True)
        
        # --- NUEVO OUTPUT (EL QUINTO ELEMENTO): TABLA INTERACTIVA DE APOYO ---
        st.write("### 📈 Tabla de Potencial: % de Modelos en Alta Gama o Superior")
        
        tabla_pct = conteo_tier_marca.pivot(index='brand', columns='tier_lujo', values='n_modelos').fillna(0)
        
        for tier in orden_tiers:
            if tier not in tabla_pct.columns:
                tabla_pct[tier] = 0
                
        tabla_pct['total'] = tabla_pct[orden_tiers].sum(axis=1)
        
        # Evitamos divisiones por cero por si acaso
        tabla_pct['% Alta Gama o superior'] = 0.0
        mask = tabla_pct['total'] > 0
        tabla_pct.loc[mask, '% Alta Gama o superior'] = (
            (tabla_pct.loc[mask, '3. Alta Gama'] + tabla_pct.loc[mask, '4. Ultra-Lujo']) / tabla_pct.loc[mask, 'total'] * 100
        ).round(1)
        
        tabla_reporte = tabla_pct.sort_values('% Alta Gama o superior', ascending=False)[['total', '% Alta Gama o superior']]
        tabla_reporte.index.name = "Marca"
        tabla_reporte.columns = ["Total Modelos", "% Alta Gama o Superior"]
        
        # Renderizado interactivo y elegante en la web de Streamlit
        st.dataframe(tabla_reporte, use_container_width=True)
        
    else:
        st.info("La columna 'tier_lujo' no está disponible o el DataFrame está vacío.")