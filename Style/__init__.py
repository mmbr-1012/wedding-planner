# Paquete de interfaz visual

from .style import aplicar_estilos
from .components import (
    renderizar_logo_cabecera,
    renderizar_estadisticas_sidebar,
    renderizar_info_version,
    renderizar_menu_navegacion
)

__all__ = [
    'aplicar_estilos',
    'renderizar_logo_cabecera',
    'renderizar_estadisticas_sidebar',
    'renderizar_info_version',
    'renderizar_menu_navegacion'
]