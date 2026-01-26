# Paquete Logic - Dream Wedding Planner
# Exporta todas las clases y funciones principales

from .models import (
    TipoBoda, 
    EstadoEvento, 
    TipoRecurso, 
    TipoRestriccion,
    Recurso, 
    Evento, 
    Restriccion
)

from .config import (
    ConfiguracionApp,
    ColorPaleta,
    TemaBoada,
    PaqueteBoda,
    PrecioRecurso,
    obtener_temas,
    obtener_paquetes,
    obtener_colores,
    obtener_precios
)

from .budget_calculator import CalculadoraPresupuesto
from .wedding_manager import DreamWeddingPlanner
from .data_handler import DataHandler

__version__ = "2.0.0"
__author__ = "Dream Wedding Planner Team"

# Instancias globales para fácil acceso (opcional)
planner = None
calculadora = None

def inicializar():
    """Inicializa las instancias globales"""
    global planner, calculadora
    planner = DreamWeddingPlanner()
    calculadora = CalculadoraPresupuesto()
    return planner, calculadora

__all__ = [
    # Enums
    'TipoBoda',
    'EstadoEvento',
    'TipoRecurso',
    'TipoRestriccion',
    
    # Modelos
    'Recurso',
    'Evento',
    'Restriccion',
    
    # Configuración
    'ConfiguracionApp',
    'ColorPaleta',
    'TemaBoada',
    'PaqueteBoda',
    'PrecioRecurso',
    'obtener_temas',
    'obtener_paquetes',
    'obtener_colores',
    'obtener_precios',
    
    # Gestores
    'CalculadoraPresupuesto',
    'DreamWeddingPlanner',
    'DataHandler',
    
    # Funciones
    'inicializar',
    
    # Variables
    'planner',
    'calculadora',
    '__version__',
    '__author__'
]