import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import json
import os
import sys

# Importar módulos de lógica
from wedding_manager import WeddingManager, WeddingBudgetCalculator
from data_handler import DataHandler
from config import WeddingThemes, WeddingPackages, WeddingColors
from budget_calculator import BudgetCalculatorLogic

# Configuración de la página
st.set_page_config(
    page_title="💍 Dream Wedding Planner",
    page_icon="💍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Inicializar el manager de bodas
@st.cache_resource
def get_manager():
    manager = WeddingManager()
    if os.path.exists("data/wedding_data.json"):
        DataHandler.cargar_datos("data/wedding_data.json", manager)
    else:
        DataHandler.crear_archivo_ejemplo("data/wedding_data.json")
        DataHandler.cargar_datos("data/wedding_data.json", manager)
    return manager

# Inicializar estado de sesión
if 'state' not in st.session_state:
    st.session_state.state = {
        'manager': get_manager(),
        'calculator': BudgetCalculatorLogic(),
        'selecciones_calculadora': {},
        'paquete_seleccionado': None,
        'tema_seleccionado': None,
        'current_page': '🏠 Dashboard'
    }

# Obtener referencias
state = st.session_state.state
manager = state['manager']
calculator = state['calculator']

# CSS personalizado
st.markdown(f"""
<style>
    .stApp {{
        background-color: {WeddingColors.BLANCO_NIEVE};
    }}
    
    .wedding-card {{
        background-color: {WeddingColors.ROSADO_PASTEL};
        border-radius: 10px;
        padding: 20px;
        margin: 10px 0;
        border-left: 5px solid {WeddingColors.DORADO_OPACO};
    }}
    
    .metric-card {{
        background-color: {WeddingColors.BLANCO_HUESO};
        border-radius: 10px;
        padding: 15px;
        text-align: center;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }}
    
    .package-card {{
        background-color: {WeddingColors.ROSADO_PASTEL};
        border-radius: 10px;
        padding: 20px;
        margin: 10px;
        border: 2px solid {WeddingColors.ROSADO_PROFUNDO};
    }}
    
    h1, h2, h3 {{
        color: {WeddingColors.DORADO_OPACO} !important;
    }}
    
    .stButton button {{
        background-color: {WeddingColors.ROSADO_SUAVE};
        color: white;
        border: none;
        padding: 10px 20px;
        border-radius: 5px;
    }}
    
    .stButton button:hover {{
        background-color: {WeddingColors.ROSADO_PROFUNDO};
    }}
</style>
""", unsafe_allow_html=True)

# Sidebar - Navegación
with st.sidebar:
    # Icono de boda grande
    st.markdown(f"""
        <div style="text-align: center; font-size: 60px; margin-bottom: 10px;">
            💍
        </div>
        <div style="text-align: center; color: {WeddingColors.DORADO_OPACO}; font-size: 24px; font-weight: bold; margin-bottom: 5px;">
            Dream Wedding
        </div>
        <div style="text-align: center; color: {WeddingColors.ROJO_PASTEL}; font-size: 14px; margin-bottom: 20px;">
            Planner Suite
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Menú de navegación
    menu_options = {
        "🏠 Dashboard": "dashboard",
        "💰 Calculadora de Presupuesto": "budget_calculator", 
        "💒 Crear Nueva Boda": "create_wedding",
        "🎨 Temas de Boda": "wedding_themes",
        "📅 Calendario de Eventos": "calendar",
        "🏛️ Recursos": "resources",
        "📊 Estadísticas": "statistics",
        "⚙️ Configuración": "settings"
    }
    
    selected_option = st.radio(
        "Navegación",
        list(menu_options.keys()),
        index=0
    )
    
    # Actualizar página actual
    state['current_page'] = selected_option
    
    st.markdown("---")
    st.caption("✨ Tus sueños, nuestra misión")

# Función para mostrar el dashboard
def show_dashboard():
    st.title("🏠 Dashboard - Dream Wedding Planner")
    
    # Estadísticas en cards
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f"""
        <div class="metric-card">
            <h3>💒</h3>
            <h2>3</h2>
            <p>Bodas en Progreso</p>
            <small>📈 +2 esta semana</small>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="metric-card">
            <h3>📅</h3>
            <h2>5</h2>
            <p>Bodas Próximas</p>
            <small>🎯 2 confirmadas</small>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class="metric-card">
            <h3>✅</h3>
            <h2>85%</h2>
            <p>Recursos Disponibles</p>
            <small>🔄 15% ocupados</small>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown(f"""
        <div class="metric-card">
            <h3>💰</h3>
            <h2>$150,000</h2>
            <p>Presupuesto Total</p>
            <small>💵 Promedio $30k</small>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Próximas bodas
    st.subheader("📅 Próximas Bodas")
    
    weddings = [
        {"nombre": "Boda María & Juan", "fecha": "2024-12-15", "tipo": "Grande", "estado": "✅ Confirmada", "presupuesto": "$65,000"},
        {"nombre": "Boda Ana & Carlos", "fecha": "2024-12-20", "tipo": "Mediana", "estado": "🔄 En planificación", "presupuesto": "$32,000"},
        {"nombre": "Boda Sofia & David", "fecha": "2024-12-22", "tipo": "Pequeña", "estado": "✅ Confirmada", "presupuesto": "$18,000"}
    ]
    
    for wedding in weddings:
        with st.expander(f"{wedding['nombre']} - {wedding['fecha']}"):
            col1, col2 = st.columns(2)
            with col1:
                st.write(f"**Tipo:** {wedding['tipo']}")
                st.write(f"**Estado:** {wedding['estado']}")
            with col2:
                st.write(f"**Presupuesto:** {wedding['presupuesto']}")
    
    # Acciones rápidas
    st.subheader("🚀 Acciones Rápidas")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        if st.button("💒 Nueva Boda", use_container_width=True):
            state['paquete_seleccionado'] = None
            state['current_page'] = "💒 Crear Nueva Boda"
            st.rerun()
    
    with col2:
        if st.button("💰 Calcular Presupuesto", use_container_width=True):
            state['current_page'] = "💰 Calculadora de Presupuesto"
            st.rerun()
    
    with col3:
        if st.button("📅 Ver Calendario", use_container_width=True):
            state['current_page'] = "📅 Calendario de Eventos"
            st.rerun()
    
    with col4:
        if st.button("🎨 Temas", use_container_width=True):
            state['current_page'] = "🎨 Temas de Boda"
            st.rerun()

# Función para mostrar la calculadora de presupuesto
def show_budget_calculator():
    st.title("💰 Calculadora de Presupuesto Personalizado")
    
    # Inicializar selecciones si no existen
    if 'selecciones' not in st.session_state:
        st.session_state.selecciones = {}
    
    # Crear pestañas para diferentes secciones
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "🏛️ Ceremonia", 
        "👥 Personal", 
        "🎉 Recepción", 
        "🎨 Decoración", 
        "📊 Resumen"
    ])
    
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
    
    with tab5:
        st.subheader("📊 Resumen del Presupuesto")
        
        if st.button("🧮 Calcular Presupuesto Total", type="primary", use_container_width=True):
            if st.session_state.selecciones:
                total, detalles = calculator.calcular_presupuesto(st.session_state.selecciones)
                
                # Mostrar total
                st.markdown(f"""
                <div style="background-color: {WeddingColors.ROSADO_PASTEL}; padding: 20px; border-radius: 10px; text-align: center;">
                    <h2 style="color: {WeddingColors.DORADO_OPACO}; margin: 0;">Total: ${total:,}</h2>
                </div>
                """, unsafe_allow_html=True)
                
                # Mostrar detalles
                st.subheader("📋 Detalles del Cálculo:")
                for detalle in detalles:
                    st.write(f"• {detalle}")
                
                # Botones de acción
                col1, col2 = st.columns(2)
                with col1:
                    if st.button("💾 Guardar Presupuesto", use_container_width=True):
                        st.success(f"Presupuesto de ${total:,} guardado exitosamente")
                        
                with col2:
                    if st.button("🔄 Reiniciar", use_container_width=True):
                        st.session_state.selecciones = {}
                        st.rerun()
            else:
                st.warning("Por favor, selecciona al menos una opción en las pestañas anteriores")
        
        # Mostrar selecciones actuales
        if st.session_state.selecciones:
            st.write("**Selecciones actuales:**")
            for key, value in st.session_state.selecciones.items():
                st.write(f"• {calculator._formatear_nombre_item(key)}: {value}")

# Función para mostrar creación de boda
def show_create_wedding():
    st.title("✨ Crear Boda de Ensueño")
    
    st.markdown("Selecciona un paquete predefinido o personaliza tu boda perfecta")
    
    # Mostrar paquetes
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown(f"""
        <div class="package-card">
            <h3>💒 Boda Pequeña</h3>
            <h2 style="color: {WeddingColors.DORADO_OPACO};">$15,000</h2>
            <p><strong>Invitados:</strong> 50-80 personas</p>
            <ul>
                <li>Ceremonia íntima</li>
                <li>Coctel básico</li>
                <li>Fotógrafo (4h)</li>
                <li>Decoración simple</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("Seleccionar Boda Pequeña", key="btn_pequena", use_container_width=True):
            state['paquete_seleccionado'] = "Boda Pequeña"
            st.success("✅ Paquete Boda Pequeña seleccionado")
    
    with col2:
        st.markdown(f"""
        <div class="package-card">
            <h3>💒 Boda Mediana</h3>
            <h2 style="color: {WeddingColors.DORADO_OPACO};">$30,000</h2>
            <p><strong>Invitados:</strong> 80-150 personas</p>
            <ul>
                <li>Ceremonia principal</li>
                <li>Coctel premium</li>
                <li>Fotógrafo (6h) + Video</li>
                <li>Decoración temática</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("Seleccionar Boda Mediana", key="btn_mediana", use_container_width=True):
            state['paquete_seleccionado'] = "Boda Mediana"
            st.success("✅ Paquete Boda Mediana seleccionado")
    
    with col3:
        st.markdown(f"""
        <div class="package-card">
            <h3>💒 Boda Grande</h3>
            <h2 style="color: {WeddingColors.DORADO_OPACO};">$60,000</h2>
            <p><strong>Invitados:</strong> 150-300 personas</p>
            <ul>
                <li>Ceremonia espectacular</li>
                <li>Coctel de lujo</li>
                <li>Banquete gourmet</li>
                <li>Equipo fotográfico completo</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("Seleccionar Boda Grande", key="btn_grande", use_container_width=True):
            state['paquete_seleccionado'] = "Boda Grande"
            st.success("✅ Paquete Boda Grande seleccionado")
    
    st.markdown("---")
    
    # Botón para personalizar
    if st.button("🎨 Personalizar Boda Completa", type="primary", use_container_width=True):
        state['current_page'] = "💰 Calculadora de Presupuesto"
        st.rerun()
    
    # Mostrar información del paquete seleccionado
    if state['paquete_seleccionado']:
        st.success(f"**Paquete seleccionado:** {state['paquete_seleccionado']}")
        info = WeddingPackages.PAQUETES.get(state['paquete_seleccionado'], {})
        
        col1, col2 = st.columns(2)
        with col1:
            st.subheader("📋 Detalles del Paquete")
            st.write(f"**Invitados:** {info.get('invitados', '')}")
            st.write(f"**Precio base:** ${info.get('precio_base', 0):,}")
        
        with col2:
            st.subheader("✅ Incluye:")
            for item in info.get('incluye', []):
                st.write(f"• {item}")
        
        # Formulario para detalles de la boda
        with st.form("detalles_boda_form"):
            st.subheader("📝 Detalles de la Boda")
            
            col1, col2 = st.columns(2)
            with col1:
                nombre_novia = st.text_input("Nombre de la Novia")
                fecha = st.date_input("Fecha de la Boda", min_value=datetime.today())
            
            with col2:
                nombre_novio = st.text_input("Nombre del Novio")
                num_invitados = st.number_input("Número de Invitados", min_value=10, max_value=500, value=100)
            
            notas = st.text_area("Notas adicionales o requerimientos especiales")
            
            submitted = st.form_submit_button("💾 Confirmar Boda", type="primary")
            if submitted:
                if nombre_novia and nombre_novio:
                    st.success("🎉 ¡Boda confirmada exitosamente!")
                    
                    # Mostrar resumen
                    with st.expander("Ver resumen de la boda"):
                        st.write(f"**Pareja:** {nombre_novia} & {nombre_novio}")
                        st.write(f"**Fecha:** {fecha}")
                        st.write(f"**Paquete:** {state['paquete_seleccionado']}")
                        st.write(f"**Invitados:** {num_invitados}")
                        st.write(f"**Presupuesto base:** ${info.get('precio_base', 0):,}")
                        if notas:
                            st.write(f"**Notas:** {notas}")
                else:
                    st.error("Por favor, completa los nombres de la novia y el novio")

# Función para mostrar temas de boda
def show_wedding_themes():
    st.title("🎨 Temas de Boda")
    
    temas = list(WeddingThemes.ESTILOS_BODA.keys())
    
    # Mostrar todos los temas
    cols = st.columns(2)
    for i, tema in enumerate(temas):
        with cols[i % 2]:
            with st.container():
                st.markdown(f"""
                <div style="background-color: {WeddingColors.ROSADO_PASTEL}; 
                            border-radius: 10px; padding: 20px; margin-bottom: 20px;
                            border: 2px solid {WeddingColors.ROSADO_PROFUNDO}">
                    <h3 style="color: {WeddingColors.DORADO_OPACO};">{tema}</h3>
                </div>
                """, unsafe_allow_html=True)
                
                info = WeddingThemes.ESTILOS_BODA[tema]
                
                col1, col2 = st.columns([1, 2])
                with col1:
                    st.write("**🎨 Colores:**")
                    for color in info['colores']:
                        st.write(f"• {color}")
                    
                    st.write(f"**💰 Precio base:** ${info['precio_base']:,}")
                
                with col2:
                    st.write("**🏛️ Decoración:**")
                    st.info(info['decoracion'])
                
                if st.button(f"Seleccionar {tema}", key=f"btn_{tema}", use_container_width=True):
                    state['tema_seleccionado'] = tema
                    st.success(f"✅ Tema '{tema}' seleccionado")
    
    # Mostrar tema seleccionado
    if state['tema_seleccionado']:
        st.markdown("---")
        st.subheader(f"🎯 Tema seleccionado: {state['tema_seleccionado']}")
        
        if st.button("💍 Crear Boda con este Tema", type="primary", use_container_width=True):
            state['current_page'] = "💒 Crear Nueva Boda"
            st.rerun()

# Función para mostrar calendario
def show_calendar():
    st.title("📅 Calendario de Eventos")
    
    # Obtener eventos del manager
    eventos_manager = manager.obtener_bodas_proximas(90)
    
    if eventos_manager:
        st.write("**Bodas programadas:**")
        for evento in eventos_manager:
            with st.expander(f"{evento.nombre} - {evento.inicio.strftime('%Y-%m-%d')}"):
                col1, col2 = st.columns(2)
                with col1:
                    st.write(f"**Fecha:** {evento.inicio.strftime('%d/%m/%Y')}")
                    st.write(f"**Hora:** {evento.inicio.strftime('%H:%M')} - {evento.fin.strftime('%H:%M')}")
                    st.write(f"**Tipo:** {evento.tipo_boda}")
                with col2:
                    st.write(f"**Presupuesto:** ${evento.presupuesto:,}")
                    st.write(f"**Estado:** {evento.estado}")
                    if evento.descripcion:
                        st.write(f"**Descripción:** {evento.descripcion}")
    else:
        st.info("No hay bodas programadas en los próximos 90 días")
    
    # Botón para agregar nuevo evento
    st.markdown("---")
    if st.button("➕ Agregar Nuevo Evento", type="primary"):
        with st.form("nuevo_evento_form"):
            st.subheader("Nuevo Evento")
            
            col1, col2 = st.columns(2)
            with col1:
                nombre_evento = st.text_input("Nombre del Evento")
                fecha_evento = st.date_input("Fecha", min_value=datetime.today())
                hora_inicio = st.time_input("Hora de Inicio", value=datetime.strptime("15:00", "%H:%M").time())
            
            with col2:
                tipo_evento = st.selectbox("Tipo de Evento", ["Ceremonia", "Coctel", "Cena", "Recepcion", "Otro"])
                duracion = st.number_input("Duración (horas)", min_value=1, max_value=24, value=4)
                presupuesto = st.number_input("Presupuesto ($)", min_value=0, value=10000)
            
            descripcion = st.text_area("Descripción")
            
            if st.form_submit_button("Guardar Evento"):
                st.success("Evento guardado exitosamente")

# Función para mostrar recursos
def show_resources():
    st.title("🏛️ Recursos Disponibles")
    
    # Mostrar recursos del manager
    if manager.recursos:
        # Crear DataFrame
        recursos_data = []
        for recurso in manager.recursos:
            recursos_data.append({
                "ID": recurso.id,
                "Nombre": recurso.nombre,
                "Tipo": recurso.tipo,
                "Capacidad": recurso.capacidad,
                "Precio": f"${recurso.precio:,}",
                "Disponible": "✅" if recurso.disponible else "❌",
                "Eventos Asignados": len(recurso.eventos_asignados)
            })
        
        df = pd.DataFrame(recursos_data)
        
        # Filtros
        col1, col2, col3 = st.columns(3)
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
        
        with col3:
            st.write("")
            st.write("")
            if st.button("🔄 Actualizar Recursos", use_container_width=True):
                st.rerun()
        
        # Aplicar filtros
        if tipo_filter:
            df = df[df['Tipo'].isin(tipo_filter)]
        
        if disponible_filter == "Disponibles":
            df = df[df['Disponible'] == "✅"]
        elif disponible_filter == "No Disponibles":
            df = df[df['Disponible'] == "❌"]
        
        # Mostrar tabla
        st.dataframe(
            df,
            use_container_width=True,
            hide_index=True,
            column_config={
                "ID": st.column_config.NumberColumn(width="small"),
                "Disponible": st.column_config.TextColumn(width="small"),
                "Eventos Asignados": st.column_config.NumberColumn(width="small")
            }
        )
        
        # Estadísticas
        st.subheader("📊 Estadísticas de Recursos")
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Total Recursos", len(manager.recursos))
        with col2:
            disponibles = sum(1 for r in manager.recursos if r.disponible)
            st.metric("Disponibles", disponibles)
        with col3:
            ocupados = len(manager.recursos) - disponibles
            st.metric("Ocupados", ocupados)
        with col4:
            tasa_ocupacion = (ocupados / len(manager.recursos)) * 100 if manager.recursos else 0
            st.metric("Tasa Ocupación", f"{tasa_ocupacion:.1f}%")
    else:
        st.info("No hay recursos cargados en el sistema.")

# Función para mostrar estadísticas
def show_statistics():
    st.title("📊 Estadísticas del Sistema")
    
    # Obtener estadísticas del manager
    stats = manager.obtener_estadisticas()
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Total de Eventos", stats["total_eventos"])
        st.metric("Eventos Confirmados", stats["eventos_confirmados"])
        st.metric("Eventos Pendientes", stats["eventos_pendientes"])
    
    with col2:
        st.metric("Ingresos Totales", f"${stats['ingresos_totales']:,}")
        st.metric("Recursos Totales", stats["recursos_totales"])
        st.metric("Recursos Disponibles", stats["recursos_disponibles"])
    
    with col3:
        st.subheader("Distribución por Tipo")
        if stats["distribucion_tipos_boda"]:
            tipos = list(stats["distribucion_tipos_boda"].keys())
            valores = list(stats["distribucion_tipos_boda"].values())
            
            fig = px.pie(
                names=tipos,
                values=valores,
                title="Tipos de Boda"
            )
            st.plotly_chart(fig, use_container_width=True)

# Función para mostrar configuración
def show_settings():
    st.title("⚙️ Configuración del Sistema")
    
    tab1, tab2, tab3 = st.tabs(["General", "Backup", "Acerca de"])
    
    with tab1:
        st.subheader("Configuración General")
        
        col1, col2 = st.columns(2)
        with col1:
            nombre_empresa = st.text_input("Nombre de la Empresa", value="Dream Wedding Planner")
            moneda = st.selectbox("Moneda", ["USD", "EUR", "MXN", "COP"])
        
        with col2:
            idioma = st.selectbox("Idioma", ["Español", "English", "Português"])
            zona_horaria = st.selectbox("Zona Horaria", ["UTC-5", "UTC-6", "UTC-7", "UTC-8"])
        
        notificaciones = st.checkbox("Activar notificaciones", value=True)
        
        if st.button("💾 Guardar Configuración", type="primary"):
            st.success("Configuración guardada exitosamente")
    
    with tab2:
        st.subheader("Backup y Restauración")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.info("Crear copia de seguridad de todos los datos")
            if st.button("📀 Crear Backup", use_container_width=True):
                if DataHandler.guardar_datos("data/backup_wedding_data.json", manager):
                    st.success("Backup creado exitosamente")
                else:
                    st.error("Error al crear backup")
        
        with col2:
            st.warning("Restaurar datos desde archivo")
            archivo_backup = st.file_uploader("Seleccionar archivo de backup", type=['json'])
            if st.button("🔄 Restaurar desde Backup", use_container_width=True, disabled=not archivo_backup):
                st.warning("Esta acción sobrescribirá todos los datos actuales")

# Navegación principal
current_page = state['current_page']

if current_page == "🏠 Dashboard":
    show_dashboard()
elif current_page == "💰 Calculadora de Presupuesto":
    show_budget_calculator()
elif current_page == "💒 Crear Nueva Boda":
    show_create_wedding()
elif current_page == "🎨 Temas de Boda":
    show_wedding_themes()
elif current_page == "📅 Calendario de Eventos":
    show_calendar()
elif current_page == "🏛️ Recursos":
    show_resources()
elif current_page == "📊 Estadísticas":
    show_statistics()
elif current_page == "⚙️ Configuración":
    show_settings()
