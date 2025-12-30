# INTERFAZ PRINCIPAL

import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import Logic  # Cambiado de dream_wedding a Logic

# Configuración de página
st.set_page_config(
    page_title="💍 Dream Wedding Planner",
    page_icon="💍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==================== ESTILOS CSS ====================
def aplicar_estilos():
    """Aplica estilos CSS personalizados"""
    colores = Logic.obtener_colores()  # Cambiado aquí
    
    st.markdown(f"""
    <style>
        .stApp {{
            background-color: {colores['BLANCO_NIEVE']};
        }}
        
        .wedding-card {{
            background-color: {colores['ROSADO_PASTEL']};
            border-radius: 10px;
            padding: 20px;
            margin: 10px 0;
            border-left: 5px solid {colores['DORADO_OPACO']};
        }}
        
        .metric-card {{
            background-color: {colores['BLANCO_HUESO']};
            border-radius: 10px;
            padding: 15px;
            text-align: center;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }}
        
        .package-card {{
            background-color: {colores['ROSADO_PASTEL']};
            border-radius: 10px;
            padding: 20px;
            margin: 10px;
            border: 2px solid {colores['ROSADO_PROFUNDO']};
        }}
        
        h1, h2, h3 {{
            color: {colores['DORADO_OPACO']} !important;
        }}
        
        .stButton > button {{
            background-color: {colores['ROSADO_SUAVE']};
            color: white;
            border: none;
            padding: 10px 20px;
            border-radius: 5px;
        }}
        
        .stButton > button:hover {{
            background-color: {colores['ROSADO_PROFUNDO']};
        }}
    </style>
    """, unsafe_allow_html=True)

# ==================== PÁGINAS ====================
def pagina_dashboard():
    """Página principal del dashboard"""
    st.title("🏠 Dashboard - Dream Wedding Planner")
    
    # Estadísticas
    stats = Logic.planner.obtener_estadisticas()  # Cambiado aquí
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Eventos", stats["total_eventos"])
    with col2:
        st.metric("Eventos Confirmados", stats["eventos_confirmados"])
    with col3:
        st.metric("Ingresos Totales", f"${stats['ingresos_totales']:,}")
    with col4:
        st.metric("Recursos Disponibles", f"{stats['recursos_disponibles']}/{stats['recursos_totales']}")
    
    # Próximos eventos
    st.subheader("📅 Próximas Bodas")
    eventos_proximos = Logic.planner.obtener_eventos_proximos(30)  # Cambiado aquí
    
    if eventos_proximos:
        for evento in eventos_proximos:
            with st.expander(f"{evento.nombre} - {evento.inicio.strftime('%d/%m/%Y')}"):
                col1, col2 = st.columns(2)
                with col1:
                    st.write(f"**Fecha:** {evento.inicio.strftime('%d/%m/%Y')}")
                    st.write(f"**Hora:** {evento.inicio.strftime('%H:%M')}")
                    st.write(f"**Tipo:** {evento.tipo_boda}")
                with col2:
                    st.write(f"**Presupuesto:** ${evento.presupuesto:,}")
                    st.write(f"**Estado:** {evento.estado}")
    else:
        st.info("No hay bodas programadas en los próximos 30 días")
    
    # Acciones rápidas
    st.subheader("🚀 Acciones Rápidas")
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("💒 Crear Nueva Boda", use_container_width=True):
            st.session_state.pagina = "crear_boda"
            st.rerun()
    with col2:
        if st.button("💰 Calcular Presupuesto", use_container_width=True):
            st.session_state.pagina = "calculadora"
            st.rerun()
    with col3:
        if st.button("🏛️ Ver Recursos", use_container_width=True):
            st.session_state.pagina = "recursos"
            st.rerun()

def pagina_calculadora():
    """Calculadora de presupuesto"""
    st.title("💰 Calculadora de Presupuesto Personalizado")
    
    # Inicializar selecciones
    if 'selecciones' not in st.session_state:
        st.session_state.selecciones = {}
    
    # Pestañas para diferentes categorías
    tab1, tab2, tab3, tab4 = st.tabs(["🏛️ Ceremonia", "👥 Personal", "🎉 Recepción", "🎨 Decoración"])
    
    with tab1:
        st.subheader("Lugar de Ceremonia")
        
        opciones_ceremonia = {
            "jardin": "Jardín (150-200 personas) - $2,000",
            "salon": "Salón (100-250 personas) - $3,000", 
            "capilla": "Capilla (100-300 personas) - $4,000",
            "playa": "Playa (80-120 personas) - $5,000"
        }
        
        ceremonia = st.radio(
            "Selecciona el lugar de ceremonia:",
            options=list(opciones_ceremonia.keys()),
            format_func=lambda x: opciones_ceremonia[x],
            index=None
        )
        
        if ceremonia:
            st.session_state.selecciones['ceremonia'] = ceremonia
    
    with tab2:
        st.subheader("Personal de Servicio")
        
        personal_opciones = {
            "coordinador_bodas": ("Coordinador de Bodas", 2500),
            "fotografo_principal": ("Fotógrafo Principal", 3000),
            "video_profesional": ("Video Profesional", 2000),
            "dj_musica": ("DJ/Música", 1500),
            "chef_ejecutivo": ("Chef Ejecutivo", 4000),
            "meseros": ("Equipo de Meseros", 800),
            "florista": ("Florista", 2000),
            "pastelero": ("Pastelero", 1000)
        }
        
        for key, (nombre, precio) in personal_opciones.items():
            if st.checkbox(f"{nombre} - ${precio:,}", key=f"personal_{key}"):
                st.session_state.selecciones[key] = 1
            elif key in st.session_state.selecciones:
                del st.session_state.selecciones[key]
    
    with tab3:
        st.subheader("Lugar de Recepción")
        
        opciones_recepcion = {
            "salon_principal": "Salón Principal - $5,000",
            "terraza": "Terraza - $3,000",
            "jardin_exterior": "Jardín Exterior - $4,000", 
            "carpa_lujo": "Carpa de Lujo - $4,500"
        }
        
        recepcion = st.radio(
            "Selecciona el lugar de recepción:",
            options=list(opciones_recepcion.keys()),
            format_func=lambda x: opciones_recepcion[x],
            index=None
        )
        
        if recepcion:
            st.session_state.selecciones['recepcion'] = recepcion
    
    with tab4:
        st.subheader("Decoración y Elementos Especiales")
        
        decoracion_opciones = {
            "arco_floral": ("Arco Floral", 800),
            "centro_mesa": ("Centros de Mesa", 50),
            "candelabros": ("Candelabros", 300),
            "cortinas_telones": ("Cortinas y Telones", 600),
            "alfombras": ("Alfombra Roja", 400),
            "letreros": ("Letreros Personalizados", 200),
            "globos": ("Decoración con Globos", 150),
            "fuente_chocolate": ("Fuente de Chocolate", 700),
            "fuente_champan": ("Fuente de Champán", 600)
        }
        
        for key, (nombre, precio) in decoracion_opciones.items():
            cantidad = st.number_input(
                f"{nombre} - ${precio:,}",
                min_value=0,
                max_value=100,
                value=st.session_state.selecciones.get(key, 0),
                key=f"decor_{key}"
            )
            if cantidad > 0:
                st.session_state.selecciones[key] = cantidad
            elif key in st.session_state.selecciones:
                del st.session_state.selecciones[key]
    
    # Cálculo del presupuesto
    st.markdown("---")
    col1, col2 = st.columns([1, 3])
    
    with col1:
        if st.button("🧮 Calcular Presupuesto Total", type="primary", use_container_width=True):
            if st.session_state.selecciones:
                total, detalles = Logic.calculadora.calcular(st.session_state.selecciones)  # Cambiado
                st.session_state.resultado_calculo = {"total": total, "detalles": detalles}
            else:
                st.warning("Por favor, selecciona al menos una opción")
    
    if 'resultado_calculo' in st.session_state:
        resultado = st.session_state.resultado_calculo
        colores = Logic.obtener_colores()  # Cambiado
        
        st.markdown(f"""
        <div style="background-color: {colores['ROSADO_PASTEL']}; padding: 20px; border-radius: 10px; text-align: center;">
            <h2 style="color: {colores['DORADO_OPACO']}; margin: 0;">Total: ${resultado['total']:,}</h2>
        </div>
        """, unsafe_allow_html=True)
        
        with st.expander("📋 Ver detalles del cálculo"):
            for detalle in resultado['detalles']:
                st.write(f"• {detalle}")
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("💾 Guardar Presupuesto", use_container_width=True):
                st.success(f"Presupuesto de ${resultado['total']:,} guardado exitosamente")
        with col2:
            if st.button("🔄 Reiniciar", use_container_width=True):
                st.session_state.selecciones = {}
                st.session_state.pop('resultado_calculo', None)
                st.rerun()

def pagina_crear_boda():
    """Página para crear una nueva boda"""
    st.title("✨ Crear Boda de Ensueño")
    
    # Mostrar paquetes
    col1, col2, col3 = st.columns(3)
    paquetes = Logic.obtener_paquetes()  # Cambiado
    
    with col1:
        st.markdown(f"""
        <div class="package-card">
            <h3>💒 Boda Pequeña</h3>
            <h2>${paquetes['Boda Pequeña']['precio_base']:,}</h2>
            <p><strong>Invitados:</strong> {paquetes['Boda Pequeña']['invitados']}</p>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("Seleccionar", key="btn_pequena", use_container_width=True):
            st.session_state.paquete_seleccionado = "Boda Pequeña"
            st.success("✅ Paquete seleccionado")
    
    with col2:
        st.markdown(f"""
        <div class="package-card">
            <h3>💒 Boda Mediana</h3>
            <h2>${paquetes['Boda Mediana']['precio_base']:,}</h2>
            <p><strong>Invitados:</strong> {paquetes['Boda Mediana']['invitados']}</p>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("Seleccionar", key="btn_mediana", use_container_width=True):
            st.session_state.paquete_seleccionado = "Boda Mediana"
            st.success("✅ Paquete seleccionado")
    
    with col3:
        st.markdown(f"""
        <div class="package-card">
            <h3>💒 Boda Grande</h3>
            <h2>${paquetes['Boda Grande']['precio_base']:,}</h2>
            <p><strong>Invitados:</strong> {paquetes['Boda Grande']['invitados']}</p>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("Seleccionar", key="btn_grande", use_container_width=True):
            st.session_state.paquete_seleccionado = "Boda Grande"
            st.success("✅ Paquete seleccionado")
    
    st.markdown("---")
    
    # Formulario para detalles
    if 'paquete_seleccionado' in st.session_state:
        st.subheader(f"📝 Detalles de la Boda - {st.session_state.paquete_seleccionado}")
        
        with st.form("formulario_boda"):
            col1, col2 = st.columns(2)
            with col1:
                nombre_novia = st.text_input("Nombre de la Novia")
                fecha = st.date_input("Fecha de la Boda", min_value=datetime.today())
            with col2:
                nombre_novio = st.text_input("Nombre del Novio")
                num_invitados = st.number_input("Número de Invitados", min_value=10, max_value=500, value=100)
            
            notas = st.text_area("Notas adicionales")
            
            if st.form_submit_button("💍 Confirmar Boda", type="primary"):
                if nombre_novia and nombre_novio:
                    st.success("🎉 ¡Boda confirmada exitosamente!")
                    
                    # Mostrar resumen
                    with st.expander("Ver resumen de la boda"):
                        st.write(f"**Pareja:** {nombre_novia} & {nombre_novio}")
                        st.write(f"**Fecha:** {fecha}")
                        st.write(f"**Paquete:** {st.session_state.paquete_seleccionado}")
                        st.write(f"**Invitados:** {num_invitados}")
                        st.write(f"**Presupuesto:** ${paquetes[st.session_state.paquete_seleccionado]['precio_base']:,}")
                        if notas:
                            st.write(f"**Notas:** {notas}")
                else:
                    st.error("Por favor, completa los nombres de la novia y el novio")

def pagina_temas():
    """Página para explorar temas de boda"""
    st.title("🎨 Temas de Boda")
    
    temas = Logic.obtener_temas()  # Cambiado
    
    for nombre, info in temas.items():
        with st.expander(f"🎯 {nombre}"):
            col1, col2 = st.columns(2)
            with col1:
                st.write("**🎨 Colores principales:**")
                for color in info['colores']:
                    st.write(f"• {color}")
                st.write(f"**💰 Precio base:** ${info['precio_base']:,}")
            with col2:
                st.write("**🏛️ Estilo de decoración:**")
                st.info(info['decoracion'])
            
            if st.button(f"Seleccionar '{nombre}'", key=f"btn_{nombre}"):
                st.session_state.tema_seleccionado = nombre
                st.success(f"✅ Tema '{nombre}' seleccionado")
    
    # Mostrar tema seleccionado
    if 'tema_seleccionado' in st.session_state:
        st.markdown("---")
        st.subheader(f"🎯 Tema seleccionado: {st.session_state.tema_seleccionado}")
        
        if st.button("💍 Crear Boda con este Tema", type="primary", use_container_width=True):
            st.session_state.pagina = "crear_boda"
            st.rerun()

def pagina_recursos():
    """Página para ver y gestionar recursos"""
    st.title("🏛️ Recursos Disponibles")
    
    recursos = Logic.planner.obtener_todos_recursos()  # Cambiado
    
    if recursos:
        # Crear DataFrame
        data = []
        for recurso in recursos:
            data.append({
                "ID": recurso.id,
                "Nombre": recurso.nombre,
                "Tipo": recurso.tipo,
                "Capacidad": recurso.capacidad,
                "Precio": f"${recurso.precio:,}",
                "Disponible": "✅" if recurso.disponible else "❌",
                "Eventos Asignados": len(recurso.eventos_asignados)
            })
        
        df = pd.DataFrame(data)
        
        # Filtros
        col1, col2 = st.columns(2)
        with col1:
            tipo_filter = st.multiselect(
                "Filtrar por Tipo",
                options=df['Tipo'].unique(),
                default=[]
            )
        with col2:
            disponible_filter = st.selectbox(
                "Disponibilidad",
                options=["Todos", "Disponibles", "No Disponibles"]
            )
        
        # Aplicar filtros
        if tipo_filter:
            df = df[df['Tipo'].isin(tipo_filter)]
        
        if disponible_filter == "Disponibles":
            df = df[df['Disponible'] == "✅"]
        elif disponible_filter == "No Disponibles":
            df = df[df['Disponible'] == "❌"]
        
        # Mostrar tabla
        st.dataframe(df, use_container_width=True, hide_index=True)
        
        # Estadísticas
        st.subheader("📊 Estadísticas")
        col1, col2, col3 = st.columns(3)
        with col1:
            disponibles = sum(1 for r in recursos if r.disponible)
            st.metric("Disponibles", disponibles)
        with col2:
            ocupados = len(recursos) - disponibles
            st.metric("Ocupados", ocupados)
        with col3:
            tasa = (ocupados / len(recursos)) * 100 if recursos else 0
            st.metric("Tasa Ocupación", f"{tasa:.1f}%")
    else:
        st.info("No hay recursos cargados en el sistema.")

# ==================== MENÚ LATERAL ====================
def menu_lateral():
    """Renderiza el menú lateral de navegación"""
    colores = Logic.obtener_colores()  # Cambiado
    
    st.sidebar.markdown(f"""
    <div style="text-align: center; font-size: 60px; margin-bottom: 10px;">
        💍
    </div>
    <div style="text-align: center; color: {colores['DORADO_OPACO']}; font-size: 24px; font-weight: bold; margin-bottom: 5px;">
        Dream Wedding
    </div>
    <div style="text-align: center; color: {colores['ROJO_PASTEL']}; font-size: 14px; margin-bottom: 20px;">
        Planner Suite v{Logic.__version__}
    </div>
    """, unsafe_allow_html=True)
    
    st.sidebar.markdown("---")
    
    # Opciones de navegación
    opciones = {
        "🏠 Dashboard": "dashboard",
        "💰 Calculadora": "calculadora",
        "💒 Crear Boda": "crear_boda",
        "🎨 Temas": "temas",
        "🏛️ Recursos": "recursos"
    }
    
    seleccion = st.sidebar.radio(
        "Navegación",
        list(opciones.keys())
    )
    
    st.sidebar.markdown("---")
    
    # Información del sistema
    stats = Logic.planner.obtener_estadisticas()  # Cambiado
    st.sidebar.caption(f"📊 **Estadísticas:**")
    st.sidebar.caption(f"• Eventos: {stats['total_eventos']}")
    st.sidebar.caption(f"• Recursos: {stats['recursos_disponibles']}/{stats['recursos_totales']} disp.")
    
    st.sidebar.markdown("---")
    st.sidebar.caption("✨ Tus sueños, nuestra misión")
    
    # Actualizar página en session_state
    st.session_state.pagina = opciones[seleccion]

# ==================== APLICACIÓN PRINCIPAL ====================
def main():
    """Función principal de la aplicación"""
    
    # Inicializar session_state
    if 'pagina' not in st.session_state:
        st.session_state.pagina = "dashboard"
    
    # Aplicar estilos
    aplicar_estilos()
    
    # Mostrar menú lateral
    menu_lateral()
    
    # Navegar a página seleccionada
    pagina = st.session_state.pagina
    
    if pagina == "dashboard":
        pagina_dashboard()
    elif pagina == "calculadora":
        pagina_calculadora()
    elif pagina == "crear_boda":
        pagina_crear_boda()
    elif pagina == "temas":
        pagina_temas()
    elif pagina == "recursos":
        pagina_recursos()

if __name__ == "__main__":
    main()