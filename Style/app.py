# Aplicación principal de Dream Wedding Planner

import streamlit as st
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from Logic.wedding_manager import DreamWeddingPlanner
from Logic.budget_calculator import CalculadoraPresupuesto
from Style.style import aplicar_estilos
from Style.components import (
    renderizar_logo_cabecera,
    renderizar_estadisticas_sidebar,
    renderizar_info_version,
    renderizar_menu_navegacion
)
from Style.pages import (
    pagina_dashboard,
    pagina_crear_boda,
    pagina_calculadora,
    pagina_temas,
    pagina_recursos,
    pagina_buscar_horario,
    pagina_gestionar_eventos,
)

st.set_page_config(
    page_title="💍 Dream Wedding Planner",
    page_icon="💍",
    layout="wide",
    initial_sidebar_state="expanded"
)

def inicializar_sesion():
    if 'planner' not in st.session_state:
        st.session_state.planner = DreamWeddingPlanner()
    if 'calculadora' not in st.session_state:
        st.session_state.calculadora = CalculadoraPresupuesto()
    if 'pagina' not in st.session_state:
        st.session_state.pagina = "dashboard"
    if '_nav_destino' not in st.session_state:
        st.session_state._nav_destino = None

def renderizar_sidebar(planner):
    renderizar_logo_cabecera()
    st.sidebar.markdown("---")
    pagina_seleccionada = renderizar_menu_navegacion(st.session_state.pagina)
    st.sidebar.markdown("---")
    try:
        stats = planner.obtener_estadisticas()
        renderizar_estadisticas_sidebar(stats)
    except Exception as e:
        st.sidebar.caption(f"📊 Estadísticas no disponibles: {str(e)}")
    st.sidebar.markdown("---")
    renderizar_info_version()
    return pagina_seleccionada

def renderizar_pagina(pagina, planner, calculadora):
    paginas = {
        "dashboard":         lambda: pagina_dashboard(planner),
        "calculadora":       lambda: pagina_calculadora(planner, calculadora),
        "crear_boda":        lambda: pagina_crear_boda(planner),
        "temas":             lambda: pagina_temas(),
        "recursos":          lambda: pagina_recursos(planner),
        "buscar_horario":    lambda: pagina_buscar_horario(planner),
        "gestionar_eventos": lambda: pagina_gestionar_eventos(planner),
    }
    paginas.get(pagina, lambda: pagina_dashboard(planner))()

def main():
    inicializar_sesion()
    planner     = st.session_state.planner
    calculadora = st.session_state.calculadora
    aplicar_estilos()

    # Resolver navegación interna (botones de páginas) ANTES del sidebar.
    # Sin esto el radio del sidebar sobreescribe el destino y hay que hacer
    # doble clic para que el cambio de página surta efecto.
    if st.session_state._nav_destino:
        st.session_state.pagina      = st.session_state._nav_destino
        st.session_state._nav_destino = None
        st.rerun()

    pagina_sidebar = renderizar_sidebar(planner)
    if pagina_sidebar != st.session_state.pagina:
        st.session_state.pagina = pagina_sidebar

    renderizar_pagina(st.session_state.pagina, planner, calculadora)

if __name__ == "__main__":
    main()