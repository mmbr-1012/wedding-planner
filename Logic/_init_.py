# Exporta todas las clases y funciones principales.

from .models import TipoBoda, EstadoEvento, Recurso, Evento, Restriccion
from .config import Config, obtener_temas, obtener_paquetes, obtener_colores, obtener_precios
from .budget_calculator import CalculadoraPresupuesto
from .wedding_manager import DreamWeddingPlanner
from .data_handler import DataHandler

__version__ = "1.0.0"
__author__ = "Dream Wedding Planner"

# Instancias globales para fácil acceso
planner = DreamWeddingPlanner()
calculadora = CalculadoraPresupuesto()

__all__ = [
    'TipoBoda',
    'EstadoEvento',
    'Recurso',
    'Evento',
    'Restriccion',
    'Config',
    'obtener_temas',
    'obtener_paquetes',
    'obtener_colores',
    'obtener_precios',
    'CalculadoraPresupuesto',
    'DreamWeddingPlanner',
    'DataHandler',
    'planner',
    'calculadora',
    '__version__',
    '__author__'
]