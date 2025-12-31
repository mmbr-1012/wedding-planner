# INTERFAZ PRINCIPAL - VERSIÓN MEJORADA

import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import os
import sys

# Importaciones
from Logic.config import ConfiguracionApp, ColorPaleta, obtener_colores, obtener_temas, obtener_paquetes
from Logic.wedding_manager import DreamWeddingPlanner
from Logic.budget_calculator import CalculadoraPresupuesto
from Logic.models import TipoBoda, EstadoEvento, TipoRecurso

# Crear instancias globales
if 'planner' not in st.session_state:
    st.session_state.planner = DreamWeddingPlanner()
if 'calculadora' not in st.session_state:
    st.session_state.calculadora = CalculadoraPresupuesto()

planner = st.session_state.planner
calculadora = st.session_state.calculadora

# Configuración de página
st.set_page_config(
    page_title="💍 Dream Wedding Planner",
    page_icon="💍",
    layout="wide",
    initial_sidebar_state="expanded"
)

#  ESTILOS CSS MEJORADOS 
def aplicar_estilos():
    """Aplica estilos CSS personalizados mejorados"""
    st.markdown(f"""
    <style>
        /* Estilos generales */
        .stApp {{
            background: linear-gradient(135deg, {ColorPaleta.BLANCO_NIEVE.value} 0%, {ColorPaleta.ROSADO_PASTEL.value} 100%);
        }}
        
        /* Tarjetas de boda */
        .wedding-card {{
            background-color: {ColorPaleta.BLANCO_NIEVE.value};
            border-radius: 15px;
            padding: 25px;
            margin: 15px 0;
            border-left: 6px solid {ColorPaleta.DORADO_OPACO.value};
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
            transition: transform 0.3s ease;
        }}
        
        .wedding-card:hover {{
            transform: translateY(-5px);
            box-shadow: 0 6px 12px rgba(0,0,0,0.15);
        }}
        
        /* Tarjetas de métricas */
        .metric-card {{
            background: linear-gradient(135deg, {ColorPaleta.BLANCO_NIEVE.value} 0%, {ColorPaleta.ROSADO_PASTEL.value} 100%);
            border-radius: 15px;
            padding: 20px;
            text-align: center;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
            border: 2px solid {ColorPaleta.DORADO_SUAVE.value};
        }}
        
        /* Tarjetas de paquetes */
        .package-card {{
            background-color: {ColorPaleta.BLANCO_NIEVE.value};
            border-radius: 15px;
            padding: 25px;
            margin: 15px;
            border: 3px solid {ColorPaleta.ROSADO_PROFUNDO.value};
            box-shadow: 0 4px 8px rgba(0,0,0,0.12);
            transition: all 0.3s ease;
        }}
        
        .package-card:hover {{
            border-color: {ColorPaleta.DORADO_SUAVE.value};
            transform: scale(1.02);
        }}
        
        /* Títulos */
        h1 {{
            color: {ColorPaleta.DORADO_OPACO.value} !important;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
            font-weight: 700 !important;
        }}
        
        h2, h3 {{
            color: {ColorPaleta.GRIS_OSCURO.value} !important;
            font-weight: 600 !important;
        }}
        
        /* Botones mejorados */
        .stButton > button {{
            background: linear-gradient(135deg, {ColorPaleta.ROSADO_SUAVE.value} 0%, {ColorPaleta.ROSADO_PROFUNDO.value} 100%);
            color: {ColorPaleta.NEGRO.value} !important;
            font-weight: 600 !important;
            border: none;
            padding: 12px 24px;
            border-radius: 8px;
            transition: all 0.3s ease;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }}
        
        .stButton > button:hover {{
            background: linear-gradient(135deg, {ColorPaleta.ROSADO_PROFUNDO.value} 0%, {ColorPaleta.ROJO_PASTEL.value} 100%);
            transform: translateY(-2px);
            box-shadow: 0 4px 8px rgba(0,0,0,0.15);
        }}
        
        /* Inputs mejorados */
        .stTextInput > div > div > input,
        .stNumberInput > div > div > input,
        .stDateInput > div > div > input,
        .stTimeInput > div > div > input {{
            border: 2px solid {ColorPaleta.ROSADO_PASTEL.value} !important;
            border-radius: 8px !important;
            font-weight: 500 !important;
        }}
        
        /* Selectbox mejorado */
        .stSelectbox > div > div {{
            border: 2px solid {ColorPaleta.ROSADO_PASTEL.value} !important;
            border-radius: 8px !important;
        }}
        
        /* Texto en contraste */
        p, li, span, label {{
            color: {ColorPaleta.GRIS_OSCURO.value} !important;
            font-weight: 500 !important;
        }}
        
        /* Sidebar mejorado */
        [data-testid="stSidebar"] {{
            background: linear-gradient(180deg, {ColorPaleta.BLANCO_NIEVE.value} 0%, {ColorPaleta.ROSADO_PASTEL.value} 100%);
        }}
        
        /* Alertas */
        .stAlert {{
            border-radius: 10px;
            font-weight: 500;
        }}
        
        /* Expander */
        .streamlit-expanderHeader {{
            background-color: {ColorPaleta.ROSADO_PASTEL.value} !important;
            border-radius: 8px !important;
            font-weight: 600 !important;
        }}
        
        /* DataFrames */
        .dataframe {{
            border: 2px solid {ColorPaleta.ROSADO_PASTEL.value} !important;
            border-radius: 10px !important;
        }}
        
        /* Success/Info boxes con mejor contraste */
        .stSuccess, .stInfo {{
            background-color: {ColorPaleta.BLANCO_NIEVE.value} !important;
            color: {ColorPaleta.GRIS_OSCURO.value} !important;
            border: 2px solid {ColorPaleta.DORADO_SUAVE.value} !important;
        }}
    </style>
    """, unsafe_allow_html=True)

#  PÁGINAS 

def pagina_dashboard():
    """Página principal del dashboard"""
    st.title("🏠 Dashboard - Dream Wedding Planner")
    
    # Estadísticas
    stats = planner.obtener_estadisticas()
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown(f"""
        <div class="metric-card">
            <h3 style="color: {ColorPaleta.DORADO_OPACO.value};">📊 Total Eventos</h3>
            <h1 style="color: {ColorPaleta.GRIS_OSCURO.value};">{stats["total_eventos"]}</h1>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="metric-card">
            <h3 style="color: {ColorPaleta.DORADO_OPACO.value};">✅ Confirmados</h3>
            <h1 style="color: {ColorPaleta.GRIS_OSCURO.value};">{stats["eventos_confirmados"]}</h1>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class="metric-card">
            <h3 style="color: {ColorPaleta.DORADO_OPACO.value};">💰 Ingresos</h3>
            <h1 style="color: {ColorPaleta.GRIS_OSCURO.value};">${stats['ingresos_totales']:,.0f}</h1>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown(f"""
        <div class="metric-card">
            <h3 style="color: {ColorPaleta.DORADO_OPACO.value};">🛏️ Recursos</h3>
            <h1 style="color: {ColorPaleta.GRIS_OSCURO.value};">{stats['recursos_disponibles']}/{stats['recursos_totales']}</h1>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Próximos eventos
    st.subheader("📅 Próximas Bodas (30 días)")
    eventos_proximos = planner.obtener_eventos_proximos(30)
    
    if eventos_proximos:
        for evento in eventos_proximos:
            with st.expander(f"💍 {evento.nombre} - {evento.inicio.strftime('%d/%m/%Y')}"):
                col1, col2 = st.columns(2)
                with col1:
                    st.write(f"**📅 Fecha:** {evento.inicio.strftime('%d/%m/%Y')}")
                    st.write(f"**🕐 Hora:** {evento.inicio.strftime('%H:%M')} - {evento.fin.strftime('%H:%M')}")
                    st.write(f"**🎨 Tipo:** {evento.tipo_boda.value}")
                with col2:
                    st.write(f"**💰 Presupuesto:** ${evento.presupuesto:,.2f}")
                    st.write(f"**👥 Invitados:** {evento.num_invitados}")
                    st.write(f"**📊 Estado:** {evento.estado.value}")
                
                if evento.descripcion:
                    st.write(f"**📝 Descripción:** {evento.descripcion}")
                
                col_btn1, col_btn2 = st.columns(2)
                with col_btn1:
                    if st.button(f"🗑️ Eliminar", key=f"del_{evento.id}"):
                        exito, mensaje = planner.eliminar_evento(evento.id)
                        if exito:
                            st.success(mensaje)
                            st.rerun()
                        else:
                            st.error(mensaje)
    else:
        st.info("📭 No hay bodas programadas en los próximos 30 días")
    
    st.markdown("---")
    
    # Acciones rápidas
    st.subheader("🚀 Acciones Rápidas")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("💍 Crear Nueva Boda", use_container_width=True, type="primary"):
            st.session_state.pagina = "crear_boda"
            st.rerun()
    
    with col2:
        if st.button("💰 Calcular Presupuesto", use_container_width=True):
            st.session_state.pagina = "calculadora"
            st.rerun()
    
    with col3:
        if st.button("🛏️ Ver Recursos", use_container_width=True):
            st.session_state.pagina = "recursos"
            st.rerun()

def pagina_crear_boda():
    """Página para crear una nueva boda - FUNCIONAL"""
    st.title("✨ Crear Boda de Ensueño")
    
    # Selector de paquete
    st.subheader("1️⃣ Selecciona un Paquete")
    paquetes = obtener_paquetes()
    
    col1, col2, col3 = st.columns(3)
    
    for idx, paquete in enumerate(paquetes):
        with [col1, col2, col3][idx]:
            st.markdown(f"""
            <div class="package-card">
                <h3 style="color: {ColorPaleta.DORADO_OPACO.value};">💎 {paquete.nombre}</h3>
                <h2 style="color: {ColorPaleta.GRIS_OSCURO.value};">${paquete.precio_base:,}</h2>
                <p style="color: {ColorPaleta.GRIS_OSCURO.value};"><strong>👥 Invitados:</strong> {paquete.rango_invitados()}</p>
                <hr>
                <p style="color: {ColorPaleta.GRIS_OSCURO.value};"><strong>Incluye:</strong></p>
                <ul style="text-align: left; color: {ColorPaleta.GRIS_OSCURO.value};">
                    {"".join([f"<li>{item}</li>" for item in paquete.incluye])}
                </ul>
            </div>
            """, unsafe_allow_html=True)
            
            if st.button("Seleccionar", key=f"btn_{paquete.nombre}", use_container_width=True):
                st.session_state.paquete_seleccionado = paquete
                st.success(f"✅ Paquete '{paquete.nombre}' seleccionado")
    
    st.markdown("---")
    
    # Formulario de creación
    if 'paquete_seleccionado' in st.session_state:
        paquete = st.session_state.paquete_seleccionado
        
        st.subheader(f"2️⃣ Detalles de la Boda - {paquete.nombre}")
        
        with st.form("formulario_boda"):
            col1, col2 = st.columns(2)
            
            with col1:
                nombre_novia = st.text_input("👰 Nombre de la Novia*", key="novia")
                fecha = st.date_input("📅 Fecha de la Boda*", min_value=datetime.today())
                hora_inicio = st.time_input("🕐 Hora de Inicio*", value=datetime.strptime("14:00", "%H:%M").time())
                
            with col2:
                nombre_novio = st.text_input("🤵 Nombre del Novio*", key="novio")
                num_invitados = st.number_input("👥 Número de Invitados*", 
                                              min_value=paquete.invitados_min,
                                              max_value=paquete.invitados_max,
                                              value=paquete.invitados_min)
                duracion = st.number_input("⏱️ Duración (horas)*", min_value=1, max_value=12, value=6)
            
            # Selección de recursos
            st.subheader("3️⃣ Selecciona los Recursos")
            
            col_cer, col_rec, col_per = st.columns(3)
            
            with col_cer:
                st.write("**🏛️ Ceremonia:**")
                recursos_ceremonia = planner.obtener_recursos_por_tipo(TipoRecurso.CEREMONIA)
                recurso_ceremonia = st.selectbox(
                    "Lugar de ceremonia",
                    options=[r.id for r in recursos_ceremonia],
                    format_func=lambda x: next((r.nombre for r in recursos_ceremonia if r.id == x), ""),
                    key="ceremonia"
                )
            
            with col_rec:
                st.write("**🎉 Recepción:**")
                recursos_recepcion = planner.obtener_recursos_por_tipo(TipoRecurso.RECEPCION)
                recurso_recepcion = st.selectbox(
                    "Lugar de recepción",
                    options=[r.id for r in recursos_recepcion],
                    format_func=lambda x: next((r.nombre for r in recursos_recepcion if r.id == x), ""),
                    key="recepcion"
                )
            
            with col_per:
                st.write("**👥 Personal:**")
                recursos_personal = planner.obtener_recursos_por_tipo(TipoRecurso.PERSONAL)
                recursos_personal_sel = st.multiselect(
                    "Selecciona el personal",
                    options=[r.id for r in recursos_personal],
                    format_func=lambda x: next((r.nombre for r in recursos_personal if r.id == x), ""),
                    default=[5, 6],  # Coordinador y fotógrafo por defecto
                    key="personal"
                )
            
            notas = st.text_area("📝 Notas adicionales", key="notas")
            
            submitted = st.form_submit_button("💍 Crear Boda", type="primary", use_container_width=True)
            
            if submitted:
                if not nombre_novia or not nombre_novio:
                    st.error("❌ Por favor, completa los nombres de la novia y el novio")
                else:
                    # Crear evento
                    inicio = datetime.combine(fecha, hora_inicio)
                    fin = inicio + timedelta(hours=duracion)
                    
                    recursos_totales = [recurso_ceremonia, recurso_recepcion] + recursos_personal_sel
                    
                    # Calcular presupuesto
                    presupuesto_total = paquete.precio_base
                    for recurso_id in recursos_totales:
                        recurso = planner._obtener_recurso(recurso_id)
                        if recurso:
                            presupuesto_total += recurso.precio
                    
                    exito, mensaje, evento_id = planner.crear_evento(
                        nombre=f"Boda {nombre_novia} & {nombre_novio}",
                        inicio=inicio,
                        fin=fin,
                        recursos=recursos_totales,
                        tipo_boda=TipoBoda.PERSONALIZADA,
                        presupuesto=presupuesto_total,
                        descripcion=notas,
                        num_invitados=num_invitados
                    )
                    
                    if exito:
                        st.success(f"🎉 {mensaje}")
                        with st.expander("📋 Ver resumen de la boda"):
                            st.write(f"**💑 Pareja:** {nombre_novia} & {nombre_novio}")
                            st.write(f"**📅 Fecha:** {fecha.strftime('%d/%m/%Y')}")
                            st.write(f"**🕐 Horario:** {hora_inicio} - {fin.strftime('%H:%M')}")
                            st.write(f"**📦 Paquete:** {paquete.nombre}")
                            st.write(f"**👥 Invitados:** {num_invitados}")
                            st.write(f"**💰 Presupuesto Total:** ${presupuesto_total:,.2f}")
                            st.write(f"**🆔 ID del Evento:** {evento_id}")
                            if notas:
                                st.write(f"**📝 Notas:** {notas}")
                        
                        if st.button("🏠 Volver al Dashboard"):
                            st.session_state.pagina = "dashboard"
                            st.rerun()
                    else:
                        st.error(f"❌ {mensaje}")
                        
                        # Ofrecer búsqueda de horario alternativo
                        if "no disponible" in mensaje.lower():
                            if st.button("🔍 Buscar Horario Alternativo"):
                                horario_alt = planner.buscar_horario_disponible(
                                    recursos=recursos_totales,
                                    duracion=timedelta(hours=duracion),
                                    fecha_inicio=inicio
                                )
                                if horario_alt:
                                    inicio_alt, fin_alt = horario_alt
                                    st.info(f"💡 Horario alternativo disponible: {inicio_alt.strftime('%d/%m/%Y %H:%M')} - {fin_alt.strftime('%H:%M')}")
                                else:
                                    st.warning("⚠️ No se encontraron horarios alternativos en el próximo año")

def pagina_calculadora():
    """Calculadora de presupuesto mejorada"""
    st.title("💰 Calculadora de Presupuesto Personalizado")
    
    if 'selecciones_calc' not in st.session_state:
        st.session_state.selecciones_calc = {}
    
    tab1, tab2, tab3 = st.tabs(["🏛️ Lugares", "👥 Personal y Servicios", "💎 Extras"])
    
    with tab1:
        st.subheader("Lugares para Ceremonia y Recepción")
        
        col1, col2 = st.columns(2)
        with col1:
            st.write("**Ceremonia:**")
            recursos_ceremonia = planner.obtener_recursos_por_tipo(TipoRecurso.CEREMONIA)
            for recurso in recursos_ceremonia:
                if st.checkbox(f"{recurso.nombre} - ${recurso.precio:,}", key=f"calc_cer_{recurso.id}"):
                    st.session_state.selecciones_calc[recurso.nombre] = recurso.precio
                elif recurso.nombre in st.session_state.selecciones_calc:
                    del st.session_state.selecciones_calc[recurso.nombre]
        
        with col2:
            st.write("**Recepción:**")
            recursos_recepcion = planner.obtener_recursos_por_tipo(TipoRecurso.RECEPCION)
            for recurso in recursos_recepcion:
                if st.checkbox(f"{recurso.nombre} - ${recurso.precio:,}", key=f"calc_rec_{recurso.id}"):
                    st.session_state.selecciones_calc[recurso.nombre] = recurso.precio
                elif recurso.nombre in st.session_state.selecciones_calc:
                    del st.session_state.selecciones_calc[recurso.nombre]
    
    with tab2:
        st.subheader("Personal y Servicios")
        recursos_personal = planner.obtener_recursos_por_tipo(TipoRecurso.PERSONAL)
        
        col1, col2 = st.columns(2)
        for idx, recurso in enumerate(recursos_personal):
            with col1 if idx % 2 == 0 else col2:
                if st.checkbox(f"{recurso.nombre} - ${recurso.precio:,}", key=f"calc_per_{recurso.id}"):
                    st.session_state.selecciones_calc[recurso.nombre] = recurso.precio
                elif recurso.nombre in st.session_state.selecciones_calc:
                    del st.session_state.selecciones_calc[recurso.nombre]
    
    with tab3:
        st.subheader("Servicios Adicionales")
        temas = obtener_temas()
        tema_seleccionado = st.selectbox(
            "Tema de Boda",
            options=[None] + [t.nombre for t in temas],
            format_func=lambda x: "Ninguno" if x is None else x
        )
        
        if tema_seleccionado:
            tema = ConfiguracionApp.obtener_tema_por_nombre(tema_seleccionado)
            st.session_state.selecciones_calc[f"Tema {tema.nombre}"] = tema.precio_base
        elif "Tema" in str(st.session_state.selecciones_calc):
            keys_to_remove = [k for k in st.session_state.selecciones_calc.keys() if k.startswith("Tema")]
            for k in keys_to_remove:
                del st.session_state.selecciones_calc[k]
    
    st.markdown("---")
    
    # Calcular y mostrar total
    if st.button("🧮 Calcular Presupuesto Total", type="primary", use_container_width=True):
        if st.session_state.selecciones_calc:
            total = sum(st.session_state.selecciones_calc.values())
            impuestos = total * (ConfiguracionApp.IMPUESTOS / 100)
            total_con_impuestos = total + impuestos
            
            st.markdown(f"""
            <div style="background: linear-gradient(135deg, {ColorPaleta.ROSADO_PASTEL.value} 0%, {ColorPaleta.ROSADO_SUAVE.value} 100%); 
                        padding: 30px; border-radius: 15px; text-align: center; margin: 20px 0;
                        box-shadow: 0 4px 8px rgba(0,0,0,0.15);">
                <h3 style="color: {ColorPaleta.GRIS_OSCURO.value}; margin: 0;">Subtotal</h3>
                <h1 style="color: {ColorPaleta.DORADO_OPACO.value}; margin: 10px 0;">${total:,.2f}</h1>
                <p style="color: {ColorPaleta.GRIS_OSCURO.value}; margin: 5px;">Impuestos ({ConfiguracionApp.IMPUESTOS}%): ${impuestos:,.2f}</p>
                <hr style="border-color: {ColorPaleta.DORADO_OPACO.value};">
                <h2 style="color: {ColorPaleta.GRIS_OSCURO.value}; margin: 10px 0;">Total: ${total_con_impuestos:,.2f}</h2>
            </div>
            """, unsafe_allow_html=True)
            
            with st.expander("📋 Ver detalles del cálculo"):
                for nombre, precio in st.session_state.selecciones_calc.items():
                    st.write(f"• {nombre}: ${precio:,.2f}")
            
            col1, col2 = st.columns(2)
            with col1:
                if st.button("💾 Guardar Presupuesto", use_container_width=True):
                    st.success(f"✅ Presupuesto de ${total_con_impuestos:,.2f} guardado")
            with col2:
                if st.button("🔄 Reiniciar", use_container_width=True):
                    st.session_state.selecciones_calc = {}
                    st.rerun()
        else:
            st.warning("⚠️ Por favor, selecciona al menos una opción")

def pagina_temas():
    """Página para explorar temas de boda"""
    st.title("🎨 Temas de Boda")
    
    temas = obtener_temas()
    
    for tema in temas:
        with st.expander(f"🎯 {tema.nombre}", expanded=False):
            col1, col2 = st.columns([2, 1])
            
            with col1:
                st.write(f"**🎨 Colores principales:**")
                cols_colores = st.columns(len(tema.colores))
                for idx, color in enumerate(tema.colores):
                    with cols_colores[idx]:
                        st.markdown(f"""
                        <div style="background-color: #e0e0e0; padding: 10px; border-radius: 5px; text-align: center;">
                            <strong style="color: {ColorPaleta.GRIS_OSCURO.value};">{color}</strong>
                        </div>
                        """, unsafe_allow_html=True)
                
                st.write(f"**🛏️ Estilo de decoración:**")
                st.info(tema.decoracion)
            
            with col2:
                st.markdown(f"""
                <div style="background-color: {ColorPaleta.ROSADO_PASTEL.value}; padding: 20px; 
                            border-radius: 10px; text-align: center;">
                    <h3 style="color: {ColorPaleta.GRIS_OSCURO.value};">Precio Base</h3>
                    <h2 style="color: {ColorPaleta.DORADO_OPACO.value};">${tema.precio_base:,}</h2>
                </div>
                """, unsafe_allow_html=True)
                
                if st.button(f"Seleccionar", key=f"tema_{tema.nombre}", use_container_width=True):
                    st.session_state.tema_seleccionado = tema.nombre
                    st.success(f"✅ Tema '{tema.nombre}' seleccionado")
    
    if 'tema_seleccionado' in st.session_state:
        st.markdown("---")
        st.subheader(f"🎯 Tema seleccionado: {st.session_state.tema_seleccionado}")
        if st.button("💍 Crear Boda con este Tema", type="primary", use_container_width=True):
            st.session_state.pagina = "crear_boda"
            st.rerun()

def pagina_recursos():
    """Página para ver y gestionar recursos"""
    st.title("🛏️ Recursos Disponibles")
    
    recursos = planner.obtener_todos_recursos()
    
    if recursos:
        # Filtros
        col1, col2 = st.columns(2)
        with col1:
            tipos_disponibles = list(set([r.tipo.value for r in recursos]))
            tipo_filter = st.multiselect(
                "🔍 Filtrar por Tipo",
                options=tipos_disponibles,
                default=[]
            )
        
        with col2:
            disponible_filter = st.selectbox(
                "📊 Disponibilidad",
                options=["Todos", "Disponibles", "No Disponibles"]
            )
        
        # Aplicar filtros
        recursos_filtrados = recursos
        if tipo_filter:
            recursos_filtrados = [r for r in recursos_filtrados if r.tipo.value in tipo_filter]
        
        if disponible_filter == "Disponibles":
            recursos_filtrados = [r for r in recursos_filtrados if r.disponible]
        elif disponible_filter == "No Disponibles":
            recursos_filtrados = [r for r in recursos_filtrados if not r.disponible]
        
        # Mostrar recursos en tarjetas
        st.markdown("---")
        for recurso in recursos_filtrados:
            with st.expander(f"{'✅' if recurso.disponible else '❌'} {recurso.nombre} - ${recurso.precio:,}"):
                col1, col2 = st.columns([2, 1])
                
                with col1:
                    st.write(f"**🏷️ Tipo:** {recurso.tipo.value}")
                    st.write(f"**👥 Capacidad:** {recurso.capacidad}")
                    st.write(f"**💰 Precio:** ${recurso.precio:,}")
                    if recurso.descripcion:
                        st.write(f"**📝 Descripción:** {recurso.descripcion}")
                
                with col2:
                    estado = "Disponible ✅" if recurso.disponible else "Ocupado ❌"
                    st.markdown(f"""
                    <div style="background-color: {'#d4edda' if recurso.disponible else '#f8d7da'}; 
                                padding: 15px; border-radius: 10px; text-align: center;">
                        <h4 style="color: {ColorPaleta.GRIS_OSCURO.value};">{estado}</h4>
                        <p style="color: {ColorPaleta.GRIS_OSCURO.value};"><strong>Eventos:</strong> {len(recurso.eventos_asignados)}</p>
                    </div>
                    """, unsafe_allow_html=True)
                
                # Mostrar eventos asignados
                if recurso.eventos_asignados:
                    st.write("**📅 Eventos asignados:**")
                    for evento_id, inicio, fin in recurso.eventos_asignados:
                        evento = planner.obtener_evento_por_id(evento_id)
                        if evento:
                            st.write(f"• {evento.nombre}: {inicio.strftime('%d/%m/%Y %H:%M')} - {fin.strftime('%H:%M')}")
        
        # Estadísticas
        st.markdown("---")
        st.subheader("📊 Estadísticas de Recursos")
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Total", len(recursos))
        with col2:
            disponibles = sum(1 for r in recursos if r.disponible)
            st.metric("Disponibles", disponibles)
        with col3:
            ocupados = len(recursos) - disponibles
            st.metric("Ocupados", ocupados)
        with col4:
            tasa = (ocupados / len(recursos) * 100) if recursos else 0
            st.metric("Tasa Ocupación", f"{tasa:.1f}%")
    else:
        st.info("📭 No hay recursos cargados en el sistema.")

def pagina_buscar_horario():
    """Página para buscar horarios disponibles"""
    st.title("🔍 Buscar Horario Disponible")
    
    st.write("Esta herramienta te ayuda a encontrar el próximo horario disponible para los recursos que necesitas.")
    
    with st.form("form_buscar_horario"):
        st.subheader("Selecciona los recursos necesarios")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.write("**🏛️ Ceremonia:**")
            recursos_ceremonia = planner.obtener_recursos_por_tipo(TipoRecurso.CEREMONIA)
            recurso_cer_sel = st.selectbox(
                "Lugar de ceremonia",
                options=[r.id for r in recursos_ceremonia],
                format_func=lambda x: next((r.nombre for r in recursos_ceremonia if r.id == x), "")
            )
            
            st.write("**🎉 Recepción:**")
            recursos_recepcion = planner.obtener_recursos_por_tipo(TipoRecurso.RECEPCION)
            recurso_rec_sel = st.selectbox(
                "Lugar de recepción",
                options=[r.id for r in recursos_recepcion],
                format_func=lambda x: next((r.nombre for r in recursos_recepcion if r.id == x), "")
            )
        
        with col2:
            st.write("**👥 Personal:**")
            recursos_personal = planner.obtener_recursos_por_tipo(TipoRecurso.PERSONAL)
            recursos_per_sel = st.multiselect(
                "Selecciona el personal",
                options=[r.id for r in recursos_personal],
                format_func=lambda x: next((r.nombre for r in recursos_personal if r.id == x), ""),
                default=[5, 6]
            )
        
        duracion = st.number_input("⏱️ Duración del evento (horas)", min_value=1, max_value=12, value=6)
        fecha_inicio_busqueda = st.date_input("📅 Buscar desde", min_value=datetime.today())
        
        submitted = st.form_submit_button("🔍 Buscar Horario", type="primary", use_container_width=True)
        
        if submitted:
            recursos_totales = [recurso_cer_sel, recurso_rec_sel] + recursos_per_sel
            
            with st.spinner("Buscando horario disponible..."):
                horario = planner.buscar_horario_disponible(
                    recursos=recursos_totales,
                    duracion=timedelta(hours=duracion),
                    fecha_inicio=datetime.combine(fecha_inicio_busqueda, datetime.min.time())
                )
            
            if horario:
                inicio, fin = horario
                st.success("✅ ¡Horario disponible encontrado!")
                
                st.markdown(f"""
                <div style="background-color: {ColorPaleta.BLANCO_NIEVE.value}; 
                            padding: 25px; border-radius: 15px; 
                            border: 3px solid {ColorPaleta.DORADO_SUAVE.value};
                            margin: 20px 0;">
                    <h3 style="color: {ColorPaleta.DORADO_OPACO.value}; text-align: center;">📅 Horario Disponible</h3>
                    <h2 style="color: {ColorPaleta.GRIS_OSCURO.value}; text-align: center;">
                        {inicio.strftime('%d/%m/%Y')}
                    </h2>
                    <h3 style="color: {ColorPaleta.GRIS_OSCURO.value}; text-align: center;">
                        {inicio.strftime('%H:%M')} - {fin.strftime('%H:%M')}
                    </h3>
                </div>
                """, unsafe_allow_html=True)
                
                st.write("**Recursos seleccionados:**")
                for recurso_id in recursos_totales:
                    recurso = planner._obtener_recurso(recurso_id)
                    if recurso:
                        st.write(f"• {recurso.nombre} - ${recurso.precio:,}")
                
                if st.button("💍 Crear Boda con este Horario", type="primary"):
                    st.session_state.horario_sugerido = horario
                    st.session_state.recursos_sugeridos = recursos_totales
                    st.session_state.pagina = "crear_boda"
                    st.rerun()
            else:
                st.error("❌ No se encontró ningún horario disponible en el próximo año para esta combinación de recursos.")
                st.info("💡 Intenta con otros recursos o una fecha diferente.")

#  MENÚ LATERAL 
def menu_lateral():
    """Renderiza el menú lateral de navegación"""
    st.sidebar.markdown(f"""
    <div style="text-align: center; font-size: 60px; margin-bottom: 10px;">
        💍
    </div>
    <div style="text-align: center; color: {ColorPaleta.DORADO_OPACO.value}; font-size: 28px; font-weight: bold; margin-bottom: 5px;">
        Dream Wedding
    </div>
    <div style="text-align: center; color: {ColorPaleta.ROJO_PASTEL.value}; font-size: 16px; margin-bottom: 20px; font-weight: 600;">
        Planner Suite
    </div>
    """, unsafe_allow_html=True)
    
    st.sidebar.markdown("---")
    
    # Menú de navegación
    opciones = {
        "🏠 Dashboard": "dashboard",
        "💰 Calculadora": "calculadora",
        "💍 Crear Boda": "crear_boda",
        "🎨 Temas": "temas",
        "🛏️ Recursos": "recursos",
        "🔍 Buscar Horario": "buscar_horario"
    }
    
    seleccion = st.sidebar.radio("📍 Navegación", list(opciones.keys()), label_visibility="collapsed")
    
    st.sidebar.markdown("---")
    
    # Estadísticas en sidebar
    try:
        stats = planner.obtener_estadisticas()
        st.sidebar.markdown(f"""
        <div style="background-color: {ColorPaleta.ROSADO_PASTEL.value}; 
                    padding: 15px; border-radius: 10px;">
            <h4 style="color: {ColorPaleta.GRIS_OSCURO.value}; margin: 0;">📊 Estadísticas</h4>
            <hr style="margin: 10px 0; border-color: {ColorPaleta.DORADO_OPACO.value};">
            <p style="color: {ColorPaleta.GRIS_OSCURO.value}; margin: 5px 0;">
                <strong>Eventos:</strong> {stats['total_eventos']}
            </p>
            <p style="color: {ColorPaleta.GRIS_OSCURO.value}; margin: 5px 0;">
                <strong>Confirmados:</strong> {stats['eventos_confirmados']}
            </p>
            <p style="color: {ColorPaleta.GRIS_OSCURO.value}; margin: 5px 0;">
                <strong>Recursos:</strong> {stats['recursos_disponibles']}/{stats['recursos_totales']}
            </p>
            <p style="color: {ColorPaleta.GRIS_OSCURO.value}; margin: 5px 0;">
                <strong>Ingresos:</strong> ${stats['ingresos_totales']:,.0f}
            </p>
        </div>
        """, unsafe_allow_html=True)
    except:
        st.sidebar.caption("📊 Estadísticas no disponibles")
    
    st.sidebar.markdown("---")
    
    # Información de la empresa
    st.sidebar.markdown(f"""
    <div style="text-align: center; color: {ColorPaleta.GRIS_OSCURO.value};">
        <p style="font-size: 12px; margin: 5px 0;"><strong>Versión:</strong> {ConfiguracionApp.VERSION}</p>
        <p style="font-size: 11px; margin: 5px 0; font-style: italic;">✨ Tus sueños, nuestra misión</p>
    </div>
    """, unsafe_allow_html=True)
    
    return opciones[seleccion]

#  APLICACIÓN PRINCIPAL 
def main():
    """Función principal de la aplicación"""
    
    # Inicializar página si no existe
    if 'pagina' not in st.session_state:
        st.session_state.pagina = "dashboard"
    
    # Aplicar estilos
    aplicar_estilos()
    
    # Obtener página seleccionada del menú
    pagina_seleccionada = menu_lateral()
    st.session_state.pagina = pagina_seleccionada
    
    # Renderizar página correspondiente
    paginas = {
        "dashboard": pagina_dashboard,
        "calculadora": pagina_calculadora,
        "crear_boda": pagina_crear_boda,
        "temas": pagina_temas,
        "recursos": pagina_recursos,
        "buscar_horario": pagina_buscar_horario
    }
    
    # Ejecutar página
    if st.session_state.pagina in paginas:
        paginas[st.session_state.pagina]()
    else:
        pagina_dashboard()

if __name__ == "__main__":
    main()