# Aplicación principal de Dream Wedding Planner

import streamlit as st
import sys
import os

# Añadir directorio padre al path para importar Logic
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Importaciones de lógica
from Logic.wedding_manager import DreamWeddingPlanner
from Logic.budget_calculator import CalculadoraPresupuesto

# Importaciones de estilo
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
    pagina_buscar_horario
)

# CONFIGURACIÓN DE PÁGINA
st.set_page_config(
    page_title="💍 Dream Wedding Planner",
    page_icon="💍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# INICIALIZACIÓN
def inicializar_sesion():
    """Inicializa las variables de sesión necesarias"""
    if 'planner' not in st.session_state:
        st.session_state.planner = DreamWeddingPlanner()
    
    if 'calculadora' not in st.session_state:
        st.session_state.calculadora = CalculadoraPresupuesto()
    
    if 'pagina' not in st.session_state:
        st.session_state.pagina = "dashboard"

# MENÚ LATERAL
def renderizar_sidebar(planner):
    """Renderiza todo el contenido del sidebar"""
    # Logo y cabecera
    renderizar_logo_cabecera()
    st.sidebar.markdown("---")
    
    # Menú de navegación
    pagina_seleccionada = renderizar_menu_navegacion(st.session_state.pagina)
    st.sidebar.markdown("---")
    
    # Estadísticas
    try:
        stats = planner.obtener_estadisticas()
        renderizar_estadisticas_sidebar(stats)
    except Exception as e:
        st.sidebar.caption(f"📊 Estadísticas no disponibles: {str(e)}")
    
    st.sidebar.markdown("---")
    
    # Información de versión
    renderizar_info_version()
    
    return pagina_seleccionada

# ENRUTADOR DE PÁGINAS
def renderizar_pagina(pagina: str, planner, calculadora):
    """Renderiza la página seleccionada"""
    paginas = {
        "dashboard": lambda: pagina_dashboard(planner),
        "calculadora": lambda: pagina_calculadora(planner, calculadora),
        "crear_boda": lambda: pagina_crear_boda(planner),
        "temas": lambda: pagina_temas(),
        "recursos": lambda: pagina_recursos(planner),
        "buscar_horario": lambda: pagina_buscar_horario(planner)
    }
    
    if pagina in paginas:
        paginas[pagina]()
    else:
        # Página por defecto
        pagina_dashboard(planner)

# APLICACIÓN PRINCIPAL
def main():
    """Función principal de la aplicación"""
    
    # Inicializar sesión
    inicializar_sesion()
    
    # Obtener instancias
    planner = st.session_state.planner
    calculadora = st.session_state.calculadora
    
    # Aplicar estilos
    aplicar_estilos()
    
    # Renderizar sidebar y obtener página seleccionada
    pagina_seleccionada = renderizar_sidebar(planner)
    
    # Actualizar página en session_state
    st.session_state.pagina = pagina_seleccionada
    
    # Renderizar página
    renderizar_pagina(st.session_state.pagina, planner, calculadora)

# PUNTO DE ENTRADA
if __name__ == "__main__":
    main()