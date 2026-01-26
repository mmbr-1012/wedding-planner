# Style/components.py
# Componentes visuales reutilizables

import streamlit as st
from Logic.config import ColorPaleta, ConfiguracionApp

def renderizar_logo_cabecera():
    """Renderiza el logo y cabecera de la aplicación"""
    st.sidebar.markdown(f"""
    <div style="text-align: center; font-size: 60px; margin-bottom: 10px;">
        💍
    </div>
    <div style="text-align: center; color: {ColorPaleta.DORADO_OPACO.value}; 
         font-size: 28px; font-weight: bold; margin-bottom: 5px;">
        Dream Wedding
    </div>
    <div style="text-align: center; color: {ColorPaleta.ROJO_PASTEL.value}; 
         font-size: 16px; margin-bottom: 20px; font-weight: 600;">
        Planner Suite
    </div>
    """, unsafe_allow_html=True)

def renderizar_estadisticas_sidebar(stats: dict):
    """Renderiza las estadísticas en el sidebar"""
    st.sidebar.markdown(f"""
    <div style="background-color: {ColorPaleta.ROSADO_PASTEL.value}; 
                padding: 15px; border-radius: 10px;">
        <h4 style="color: {ColorPaleta.GRIS_OSCURO.value}; margin: 0;">📊 Estadísticas</h4>
        <hr style="margin: 10px 0; border-color: {ColorPaleta.DORADO_OPACO.value};">
        <p style="color: {ColorPaleta.GRIS_OSCURO.value}; margin: 5px 0;">
            <strong>Eventos:</strong> {stats.get('total_eventos', 0)}
        </p>
        <p style="color: {ColorPaleta.GRIS_OSCURO.value}; margin: 5px 0;">
            <strong>Confirmados:</strong> {stats.get('eventos_confirmados', 0)}
        </p>
        <p style="color: {ColorPaleta.GRIS_OSCURO.value}; margin: 5px 0;">
            <strong>Recursos:</strong> {stats.get('recursos_disponibles', 0)}/{stats.get('recursos_totales', 0)}
        </p>
        <p style="color: {ColorPaleta.GRIS_OSCURO.value}; margin: 5px 0;">
            <strong>Ingresos:</strong> ${stats.get('ingresos_totales', 0):,.0f}
        </p>
    </div>
    """, unsafe_allow_html=True)

def renderizar_info_version():
    """Renderiza la información de versión en el sidebar"""
    st.sidebar.markdown(f"""
    <div style="text-align: center; color: {ColorPaleta.GRIS_OSCURO.value};">
        <p style="font-size: 12px; margin: 5px 0;">
            <strong>Versión:</strong> {ConfiguracionApp.VERSION}
        </p>
        <p style="font-size: 11px; margin: 5px 0; font-style: italic;">
            ✨ Tus sueños, nuestra misión
        </p>
    </div>
    """, unsafe_allow_html=True)

def renderizar_menu_navegacion(pagina_actual: str) -> str:
    """
    Renderiza el menú de navegación en el sidebar
    
    Args:
        pagina_actual: Nombre de la página actual
    
    Returns:
        Nombre de la página seleccionada
    """
    opciones = {
        "🏠 Salpicadero": "dashboard",
        "💰 Calculadora": "calculadora",
        "💍 Crear Boda": "crear_boda",
        "🎨 Temas": "temas",
        "🛏️ Recursos": "recursos",
        "🔍 Buscar Horario": "buscar_horario"
    }
    
    # Encontrar el índice de la página actual
    opciones_lista = list(opciones.keys())
    valores_lista = list(opciones.values())
    
    try:
        indice_actual = valores_lista.index(pagina_actual)
    except ValueError:
        indice_actual = 0
    
    seleccion = st.sidebar.radio(
        "📍 Navegación", 
        opciones_lista,
        index=indice_actual,
        label_visibility="collapsed",
        key="menu_navegacion"  # ← AGREGADO: Key único para el radio
    )
    
    return opciones[seleccion]

def mostrar_tarjeta_evento(evento):
    """Muestra una tarjeta con información de un evento"""
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
        
        return evento.id

def mostrar_tarjeta_recurso(recurso):
    """Muestra una tarjeta con información de un recurso"""
    estado_icono = "✅" if recurso.disponible else "❌"
    with st.expander(f"{estado_icono} {recurso.nombre} - ${recurso.precio:,}"):
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.write(f"**🏷️ Tipo:** {recurso.tipo.value}")
            st.write(f"**👥 Capacidad:** {recurso.capacidad}")
            st.write(f"**💰 Precio:** ${recurso.precio:,}")
            if recurso.descripcion:
                st.write(f"**📝 Descripción:** {recurso.descripcion}")
        
        with col2:
            estado_texto = "Disponible ✅" if recurso.disponible else "Ocupado ❌"
            color_fondo = "#d4edda" if recurso.disponible else "#f8d7da"
            
            st.markdown(f"""
            <div style="background-color: {color_fondo}; 
                        padding: 15px; border-radius: 10px; text-align: center;">
                <h4 style="color: {ColorPaleta.GRIS_OSCURO.value};">{estado_texto}</h4>
                <p style="color: {ColorPaleta.GRIS_OSCURO.value};">
                    <strong>Eventos:</strong> {len(recurso.eventos_asignados)}
                </p>
            </div>
            """, unsafe_allow_html=True)
        
        return recurso.eventos_asignados

def mostrar_tarjeta_tema(tema):
    """Muestra una tarjeta con información de un tema"""
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.write(f"**🎨 Colores principales:**")
        cols_colores = st.columns(len(tema.colores))
        for idx, color in enumerate(tema.colores):
            with cols_colores[idx]:
                st.markdown(f"""
                <div style="background-color: #e0e0e0; padding: 10px; 
                            border-radius: 5px; text-align: center;">
                    <strong style="color: {ColorPaleta.GRIS_OSCURO.value};">{color}</strong>
                </div>
                """, unsafe_allow_html=True)
        
        st.write(f"**🛏️ Estilo de decoración:**")
        st.info(tema.decoracion)
    
    with col2:
        st.markdown(f"""
        <div style="background-color: {ColorPaleta.ROSADO_PASTEL.value}; 
                    padding: 20px; border-radius: 10px; text-align: center;">
            <h3 style="color: {ColorPaleta.GRIS_OSCURO.value};">Precio Base</h3>
            <h2 style="color: {ColorPaleta.DORADO_OPACO.value};">${tema.precio_base:,}</h2>
        </div>
        """, unsafe_allow_html=True)

def mostrar_tarjeta_paquete(paquete):
    """Muestra una tarjeta con información de un paquete"""
    items_html = "".join([f"<li>{item}</li>" for item in paquete.incluye])
    
    st.markdown(f"""
    <div class="package-card">
        <h3 style="color: {ColorPaleta.DORADO_OPACO.value};">💎 {paquete.nombre}</h3>
        <h2 style="color: {ColorPaleta.GRIS_OSCURO.value};">${paquete.precio_base:,}</h2>
        <p style="color: {ColorPaleta.GRIS_OSCURO.value};">
            <strong>👥 Invitados:</strong> {paquete.rango_invitados()}
        </p>
        <hr>
        <p style="color: {ColorPaleta.GRIS_OSCURO.value};"><strong>Incluye:</strong></p>
        <ul style="text-align: left; color: {ColorPaleta.GRIS_OSCURO.value};">
            {items_html}
        </ul>
    </div>
    """, unsafe_allow_html=True)

def mostrar_metricas_dashboard(stats: dict):
    """Muestra las métricas principales en el dashboard"""
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
            <h1 style="color: {ColorPaleta.GRIS_OSCURO.value};">
                {stats['recursos_disponibles']}/{stats['recursos_totales']}
            </h1>
        </div>
        """, unsafe_allow_html=True)

def mostrar_resumen_presupuesto(total: float, impuestos: float, total_con_impuestos: float):
    """Muestra el resumen del presupuesto calculado"""
    st.markdown(f"""
    <div style="background: linear-gradient(135deg, {ColorPaleta.ROSADO_PASTEL.value} 0%, 
                {ColorPaleta.ROSADO_SUAVE.value} 100%); 
                padding: 30px; border-radius: 15px; text-align: center; margin: 20px 0;
                box-shadow: 0 4px 8px rgba(0,0,0,0.15);">
        <h3 style="color: {ColorPaleta.GRIS_OSCURO.value}; margin: 0;">Subtotal</h3>
        <h1 style="color: {ColorPaleta.DORADO_OPACO.value}; margin: 10px 0;">${total:,.2f}</h1>
        <p style="color: {ColorPaleta.GRIS_OSCURO.value}; margin: 5px;">
            Impuestos ({ConfiguracionApp.IMPUESTOS}%): ${impuestos:,.2f}
        </p>
        <hr style="border-color: {ColorPaleta.DORADO_OPACO.value};">
        <h2 style="color: {ColorPaleta.GRIS_OSCURO.value}; margin: 10px 0;">
            Total: ${total_con_impuestos:,.2f}
        </h2>
    </div>
    """, unsafe_allow_html=True)

def mostrar_horario_disponible(inicio, fin):
    """Muestra el horario disponible encontrado"""
    st.markdown(f"""
    <div style="background-color: {ColorPaleta.BLANCO_NIEVE.value}; 
                padding: 25px; border-radius: 15px; 
                border: 3px solid {ColorPaleta.DORADO_SUAVE.value};
                margin: 20px 0;">
        <h3 style="color: {ColorPaleta.DORADO_OPACO.value}; text-align: center;">
            📅 Horario Disponible
        </h3>
        <h2 style="color: {ColorPaleta.GRIS_OSCURO.value}; text-align: center;">
            {inicio.strftime('%d/%m/%Y')}
        </h2>
        <h3 style="color: {ColorPaleta.GRIS_OSCURO.value}; text-align: center;">
            {inicio.strftime('%H:%M')} - {fin.strftime('%H:%M')}
        </h3>
    </div>
    """, unsafe_allow_html=True)