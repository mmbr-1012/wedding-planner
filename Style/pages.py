# Definición de todas las páginas de la interfaz

import streamlit as st
from datetime import datetime, timedelta
from Logic.models import TipoBoda, TipoRecurso
from Logic.config import obtener_paquetes, obtener_temas, ConfiguracionApp
from Style.components import (
    mostrar_metricas_dashboard,
    mostrar_tarjeta_evento,
    mostrar_tarjeta_paquete,
    mostrar_tarjeta_recurso,
    mostrar_tarjeta_tema,
    mostrar_resumen_presupuesto,
    mostrar_horario_disponible
)

def pagina_dashboard(planner):
    """Página principal del dashboard"""
    st.title("🏠 Dashboard - Dream Wedding Planner")
    
    # Estadísticas
    stats = planner.obtener_estadisticas()
    mostrar_metricas_dashboard(stats)
    
    st.markdown("---")
    
    # Próximos eventos
    st.subheader("📅 Próximas Bodas (30 días)")
    eventos_proximos = planner.obtener_eventos_proximos(30)
    
    if eventos_proximos:
        for evento in eventos_proximos:
            evento_id = mostrar_tarjeta_evento(evento)
            
            # Botón de eliminar dentro del expander
            col_btn1, col_btn2 = st.columns(2)
            with col_btn1:
                if st.button(f"🗑️ Eliminar", key=f"del_{evento_id}"):
                    exito, mensaje = planner.eliminar_evento(evento_id)
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
        btn_crear = st.button("💍 Crear Nueva Boda", use_container_width=True, 
                             type="primary", key="btn_dashboard_crear")
    
    with col2:
        btn_calc = st.button("💰 Calcular Presupuesto", use_container_width=True, 
                            key="btn_dashboard_calc")
    
    with col3:
        btn_recursos = st.button("🛏️ Ver Recursos", use_container_width=True, 
                                key="btn_dashboard_recursos")
    
    # Manejar clics DESPUÉS de crear todos los botones
    if btn_crear:
        st.session_state.pagina = "crear_boda"
        st.rerun()
    elif btn_calc:
        st.session_state.pagina = "calculadora"
        st.rerun()
    elif btn_recursos:
        st.session_state.pagina = "recursos"
        st.rerun()

def pagina_crear_boda(planner):
    """Página para crear una nueva boda"""
    st.title("✨ Crear Boda de Ensueño")
    
    # Selector de paquete
    st.subheader("1️⃣ Selecciona un Paquete")
    paquetes = obtener_paquetes()
    
    col1, col2, col3 = st.columns(3)
    
    for idx, paquete in enumerate(paquetes):
        with [col1, col2, col3][idx]:
            mostrar_tarjeta_paquete(paquete)
            
            if st.button("Seleccionar", key=f"btn_{paquete.nombre}", 
                        use_container_width=True):
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
                nombre_novia = st.text_input("👰 Nombre de la Novia*")
                fecha = st.date_input("📅 Fecha de la Boda*", min_value=datetime.today())
                hora_inicio = st.time_input("🕐 Hora de Inicio*", 
                                           value=datetime.strptime("14:00", "%H:%M").time())
                
            with col2:
                nombre_novio = st.text_input("🤵 Nombre del Novio*")
                num_invitados = st.number_input("👥 Número de Invitados*", 
                                              min_value=paquete.invitados_min,
                                              max_value=paquete.invitados_max,
                                              value=paquete.invitados_min)
                duracion = st.number_input("⏱️ Duración (horas)*", 
                                         min_value=1, max_value=12, value=6)
            
            # Selección de recursos
            st.subheader("3️⃣ Selecciona los Recursos")
            
            col_cer, col_rec, col_per = st.columns(3)
            
            with col_cer:
                st.write("**🛏️ Ceremonia:**")
                recursos_ceremonia = planner.obtener_recursos_por_tipo(TipoRecurso.CEREMONIA)
                recurso_ceremonia = st.selectbox(
                    "Lugar de ceremonia",
                    options=[r.id for r in recursos_ceremonia],
                    format_func=lambda x: next((r.nombre for r in recursos_ceremonia 
                                               if r.id == x), "")
                )
            
            with col_rec:
                st.write("**🎉 Recepción:**")
                recursos_recepcion = planner.obtener_recursos_por_tipo(TipoRecurso.RECEPCION)
                recurso_recepcion = st.selectbox(
                    "Lugar de recepción",
                    options=[r.id for r in recursos_recepcion],
                    format_func=lambda x: next((r.nombre for r in recursos_recepcion 
                                               if r.id == x), "")
                )
            
            with col_per:
                st.write("**👥 Personal:**")
                recursos_personal = planner.obtener_recursos_por_tipo(TipoRecurso.PERSONAL)
                recursos_personal_sel = st.multiselect(
                    "Selecciona el personal",
                    options=[r.id for r in recursos_personal],
                    format_func=lambda x: next((r.nombre for r in recursos_personal 
                                               if r.id == x), ""),
                    default=[5, 6]
                )
            
            notas = st.text_area("📝 Notas adicionales")
            
            submitted = st.form_submit_button("💍 Crear Boda", 
                                            type="primary", use_container_width=True)
            
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
                                    st.info(f"💡 Horario alternativo disponible: "
                                          f"{inicio_alt.strftime('%d/%m/%Y %H:%M')} - "
                                          f"{fin_alt.strftime('%H:%M')}")
                                else:
                                    st.warning("⚠️ No se encontraron horarios alternativos")

def pagina_calculadora(planner, calculadora):
    """Calculadora de presupuesto"""
    st.title("💰 Calculadora de Presupuesto Personalizado")
    
    if 'selecciones_calc' not in st.session_state:
        st.session_state.selecciones_calc = {}
    
    tab1, tab2, tab3 = st.tabs(["🛏️ Lugares", "👥 Personal y Servicios", "💎 Extras"])
    
    with tab1:
        st.subheader("Lugares para Ceremonia y Recepción")
        
        col1, col2 = st.columns(2)
        with col1:
            st.write("**Ceremonia:**")
            recursos_ceremonia = planner.obtener_recursos_por_tipo(TipoRecurso.CEREMONIA)
            for recurso in recursos_ceremonia:
                if st.checkbox(f"{recurso.nombre} - ${recurso.precio:,}", 
                             key=f"calc_cer_{recurso.id}"):
                    st.session_state.selecciones_calc[recurso.nombre] = recurso.precio
                elif recurso.nombre in st.session_state.selecciones_calc:
                    del st.session_state.selecciones_calc[recurso.nombre]
        
        with col2:
            st.write("**Recepción:**")
            recursos_recepcion = planner.obtener_recursos_por_tipo(TipoRecurso.RECEPCION)
            for recurso in recursos_recepcion:
                if st.checkbox(f"{recurso.nombre} - ${recurso.precio:,}", 
                             key=f"calc_rec_{recurso.id}"):
                    st.session_state.selecciones_calc[recurso.nombre] = recurso.precio
                elif recurso.nombre in st.session_state.selecciones_calc:
                    del st.session_state.selecciones_calc[recurso.nombre]
    
    with tab2:
        st.subheader("Personal y Servicios")
        recursos_personal = planner.obtener_recursos_por_tipo(TipoRecurso.PERSONAL)
        
        col1, col2 = st.columns(2)
        for idx, recurso in enumerate(recursos_personal):
            with col1 if idx % 2 == 0 else col2:
                if st.checkbox(f"{recurso.nombre} - ${recurso.precio:,}", 
                             key=f"calc_per_{recurso.id}"):
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
            keys_to_remove = [k for k in st.session_state.selecciones_calc.keys() 
                            if k.startswith("Tema")]
            for k in keys_to_remove:
                del st.session_state.selecciones_calc[k]
    
    st.markdown("---")
    
    # Calcular y mostrar total
    if st.button("🧮 Calcular Presupuesto Total", type="primary", use_container_width=True):
        if st.session_state.selecciones_calc:
            total = sum(st.session_state.selecciones_calc.values())
            impuestos = total * (ConfiguracionApp.IMPUESTOS / 100)
            total_con_impuestos = total + impuestos
            
            mostrar_resumen_presupuesto(total, impuestos, total_con_impuestos)
            
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
            mostrar_tarjeta_tema(tema)
            
            if st.button(f"Seleccionar", key=f"tema_{tema.nombre}", 
                        use_container_width=True):
                st.session_state.tema_seleccionado = tema.nombre
                st.success(f"✅ Tema '{tema.nombre}' seleccionado")
    
    if 'tema_seleccionado' in st.session_state:
        st.markdown("---")
        st.subheader(f"🎯 Tema seleccionado: {st.session_state.tema_seleccionado}")
        if st.button("💍 Crear Boda con este Tema", type="primary", 
                    use_container_width=True):
            st.session_state.pagina = "crear_boda"
            st.rerun()

def pagina_recursos(planner):
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
            recursos_filtrados = [r for r in recursos_filtrados 
                                if r.tipo.value in tipo_filter]
        
        if disponible_filter == "Disponibles":
            recursos_filtrados = [r for r in recursos_filtrados if r.disponible]
        elif disponible_filter == "No Disponibles":
            recursos_filtrados = [r for r in recursos_filtrados if not r.disponible]
        
        # Mostrar recursos
        st.markdown("---")
        for recurso in recursos_filtrados:
            eventos_asignados = mostrar_tarjeta_recurso(recurso)
            
            # Mostrar eventos asignados
            if eventos_asignados:
                st.write("**📅 Eventos asignados:**")
                for evento_id, inicio, fin in eventos_asignados:
                    evento = planner.obtener_evento_por_id(evento_id)
                    if evento:
                        st.write(f"• {evento.nombre}: "
                               f"{inicio.strftime('%d/%m/%Y %H:%M')} - "
                               f"{fin.strftime('%H:%M')}")
        
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

def pagina_buscar_horario(planner):
    """Página para buscar horarios disponibles"""
    st.title("🔍 Buscar Horario Disponible")
    
    st.write("Esta herramienta te ayuda a encontrar el próximo horario disponible "
            "para los recursos que necesitas.")
    
    with st.form("form_buscar_horario"):
        st.subheader("Selecciona los recursos necesarios")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.write("**🛏️ Ceremonia:**")
            recursos_ceremonia = planner.obtener_recursos_por_tipo(TipoRecurso.CEREMONIA)
            recurso_cer_sel = st.selectbox(
                "Lugar de ceremonia",
                options=[r.id for r in recursos_ceremonia],
                format_func=lambda x: next((r.nombre for r in recursos_ceremonia 
                                           if r.id == x), "")
            )
            
            st.write("**🎉 Recepción:**")
            recursos_recepcion = planner.obtener_recursos_por_tipo(TipoRecurso.RECEPCION)
            recurso_rec_sel = st.selectbox(
                "Lugar de recepción",
                options=[r.id for r in recursos_recepcion],
                format_func=lambda x: next((r.nombre for r in recursos_recepcion 
                                           if r.id == x), "")
            )
        
        with col2:
            st.write("**👥 Personal:**")
            recursos_personal = planner.obtener_recursos_por_tipo(TipoRecurso.PERSONAL)
            recursos_per_sel = st.multiselect(
                "Selecciona el personal",
                options=[r.id for r in recursos_personal],
                format_func=lambda x: next((r.nombre for r in recursos_personal 
                                           if r.id == x), ""),
                default=[5, 6]
            )
        
        duracion = st.number_input("⏱️ Duración del evento (horas)", 
                                  min_value=1, max_value=12, value=6)
        fecha_inicio_busqueda = st.date_input("📅 Buscar desde", 
                                             min_value=datetime.today())
        
        submitted = st.form_submit_button("🔍 Buscar Horario", 
                                        type="primary", use_container_width=True)
        
        if submitted:
            recursos_totales = [recurso_cer_sel, recurso_rec_sel] + recursos_per_sel
            
            with st.spinner("Buscando horario disponible..."):
                horario = planner.buscar_horario_disponible(
                    recursos=recursos_totales,
                    duracion=timedelta(hours=duracion),
                    fecha_inicio=datetime.combine(fecha_inicio_busqueda, 
                                                 datetime.min.time())
                )
            
            if horario:
                inicio, fin = horario
                st.success("✅ ¡Horario disponible encontrado!")
                
                mostrar_horario_disponible(inicio, fin)
                
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
                st.error("❌ No se encontró ningún horario disponible en el próximo año.")
                st.info("💡 Intenta con otros recursos o una fecha diferente.")