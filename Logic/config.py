# Configuración del sistema 

from dataclasses import dataclass
from typing import List
from enum import Enum

class ColorPaleta(Enum):
    """Paleta de colores para la interfaz"""
    ROSADO_PASTEL = "#FFE4E6"
    ROSADO_SUAVE = "#F8C8D0"
    ROSADO_PROFUNDO = "#F4A6B8"
    ROJO_PASTEL = "#FF6B6B"
    BLANCO_NIEVE = "#FFFFFF"
    BLANCO_HUESO = "#FFF8F0"
    DORADO_SUAVE = "#FFD700"
    PLATEADO_SUAVE = "#C0C0C0"
    DORADO_OPACO = "#D4AF37"
    PLATEADO_OPACO = "#A8A8A8"
    GRIS_OSCURO = "#2C3E50"
    NEGRO = "#000000"

@dataclass
class TemaBoada:
    """Representa un tema de boda"""
    nombre: str
    colores: List[str]
    decoracion: str
    precio_base: float
    
    def __str__(self) -> str:
        return f"{self.nombre} - ${self.precio_base:,}"

@dataclass
class PaqueteBoda:
    """Representa un paquete de boda"""
    nombre: str
    invitados_min: int
    invitados_max: int
    precio_base: float
    incluye: List[str]
    
    def rango_invitados(self) -> str:
        return f"{self.invitados_min}-{self.invitados_max} personas"
    
    def __str__(self) -> str:
        return f"{self.nombre}: {self.rango_invitados()} - ${self.precio_base:,}"

@dataclass
class PrecioRecurso:
    """Representa el precio de un recurso"""
    nombre: str
    precio: float
    capacidad: str = ""
    unidad: str = "evento"
    
    def precio_formateado(self) -> str:
        if self.capacidad:
            return f"${self.precio:,} ({self.capacidad})"
        return f"${self.precio:,}"

class ConfiguracionApp:
    """Configuración principal de la aplicación"""
    
    EMPRESA = "Dream Wedding Planner"
    VERSION = "2.0.0"
    MONEDA = "USD"
    MAX_INVITADOS = 500
    IMPUESTOS = 16.0
    DEPOSITO_CONFIRMACION = 30.0
    
    # Temas predefinidos
    TEMAS = [
        TemaBoada(
            nombre="Romántico Vintage",
            colores=["Blanco", "Marfil", "Rosa pálido", "Dorado"],
            decoracion="Flores vintage, candelabros, muebles antiguos",
            precio_base=5000
        ),
        TemaBoada(
            nombre="Boho Chic",
            colores=["Marfil", "Terracota", "Verde salvia", "Dorado"],
            decoracion="Macramé, plantas, detalles naturales",
            precio_base=4500
        ),
        TemaBoada(
            nombre="Moderno Minimalista",
            colores=["Blanco", "Negro", "Gris", "Verde"],
            decoracion="Líneas limpias, geometrías, espacios abiertos",
            precio_base=4000
        ),
        TemaBoada(
            nombre="Glamour",
            colores=["Negro", "Blanco", "Dorado", "Plateado"],
            decoracion="Cristales, espejos, lujos brillantes",
            precio_base=7000
        ),
        TemaBoada(
            nombre="Rústico",
            colores=["Madera", "Verde", "Blanco", "Terracota"],
            decoracion="Madera natural, hierro, elementos naturales",
            precio_base=3500
        ),
        TemaBoada(
            nombre="Playero",
            colores=["Azul", "Blanco", "Dorado", "Turquesa"],
            decoracion="Conchas, arena, velas, telas ligeras",
            precio_base=6000
        )
    ]
    
    # Paquetes predefinidos
    PAQUETES = [
        PaqueteBoda(
            nombre="Boda Pequeña",
            invitados_min=50,
            invitados_max=80,
            precio_base=15000,
            incluye=[
                "Ceremonia íntima",
                "Coctel básico",
                "Fotógrafo (4h)",
                "Decoración simple",
                "Coordinador de bodas"
            ]
        ),
        PaqueteBoda(
            nombre="Boda Mediana",
            invitados_min=80,
            invitados_max=150,
            precio_base=30000,
            incluye=[
                "Ceremonia principal",
                "Coctel premium",
                "Fotógrafo (6h)",
                "Video profesional",
                "Decoración temática",
                "DJ/Música en vivo"
            ]
        ),
        PaqueteBoda(
            nombre="Boda Grande",
            invitados_min=150,
            invitados_max=300,
            precio_base=60000,
            incluye=[
                "Ceremonia espectacular",
                "Coctel de lujo",
                "Banquete gourmet",
                "Equipo fotográfico completo",
                "Video cinematográfico",
                "Banda en vivo",
                "Decoración premium"
            ]
        )
    ]
    
    # Precios de recursos
    PRECIOS_RECURSOS = [
        PrecioRecurso("Jardín para Ceremonia", 2000, "150-200 personas"),
        PrecioRecurso("Salón Principal", 3000, "100-250 personas"),
        PrecioRecurso("Capilla Privada", 4000, "100-300 personas"),
        PrecioRecurso("Playa Privada", 5000, "80-120 personas"),
        PrecioRecurso("Coordinador de Bodas", 2500),
        PrecioRecurso("Fotógrafo Principal", 3000),
        PrecioRecurso("Video Profesional", 2000),
        PrecioRecurso("DJ/Música", 1500),
        PrecioRecurso("Chef Ejecutivo", 4000),
        PrecioRecurso("Equipo de Meseros", 800, "hasta 10 meseros"),
        PrecioRecurso("Florista", 2000),
        PrecioRecurso("Pastelero", 1000),
        PrecioRecurso("Salón Principal Recepción", 5000, "hasta 400 personas"),
        PrecioRecurso("Terraza VIP", 3000, "hasta 150 personas"),
        PrecioRecurso("Jardín Exterior", 4000, "hasta 300 personas"),
        PrecioRecurso("Carpa de Lujo", 4500, "hasta 250 personas"),
        PrecioRecurso("Arco Floral Premium", 800, "unidad"),
        PrecioRecurso("Centros de Mesa", 50, "por unidad"),
        PrecioRecurso("Candelabros Elegantes", 300, "set"),
        PrecioRecurso("Cortinas y Telones", 600, "set"),
        PrecioRecurso("Alfombra Roja", 400, "unidad"),
        PrecioRecurso("Letreros Personalizados", 200, "set"),
        PrecioRecurso("Decoración con Globos", 150, "paquete"),
        PrecioRecurso("Fuente de Chocolate", 700, "unidad"),
        PrecioRecurso("Fuente de Champán", 600, "unidad"),
        PrecioRecurso("Tarta Nupcial Premium", 500, "base"),
        PrecioRecurso("Libro de Firmas de Lujo", 150, "unidad"),
        PrecioRecurso("Transporte Especial", 800, "vehículo"),
        PrecioRecurso("Espectáculo de Pirotecnia", 1200, "show")
    ]
    
    @classmethod
    def obtener_tema_por_nombre(cls, nombre: str) -> TemaBoada:
        """Obtiene un tema por su nombre"""
        for tema in cls.TEMAS:
            if tema.nombre == nombre:
                return tema
        return cls.TEMAS[0]
    
    @classmethod
    def obtener_paquete_por_nombre(cls, nombre: str) -> PaqueteBoda:
        """Obtiene un paquete por su nombre"""
        for paquete in cls.PAQUETES:
            if paquete.nombre == nombre:
                return paquete
        return cls.PAQUETES[0]
    
    @classmethod
    def obtener_precio_recurso(cls, nombre: str) -> float:
        """Obtiene el precio de un recurso por su nombre"""
        for recurso in cls.PRECIOS_RECURSOS:
            if recurso.nombre == nombre:
                return recurso.precio
        return 0.0

# Funciones de conveniencia
def obtener_temas() -> List[TemaBoada]:
    """Devuelve todos los temas disponibles"""
    return ConfiguracionApp.TEMAS

def obtener_paquetes() -> List[PaqueteBoda]:
    """Devuelve todos los paquetes disponibles"""
    return ConfiguracionApp.PAQUETES

def obtener_colores() -> dict:
    """Devuelve diccionario de colores para compatibilidad"""
    return {color.name: color.value for color in ColorPaleta}

def obtener_precios() -> List[PrecioRecurso]:
    """Devuelve todos los precios de recursos"""
    return ConfiguracionApp.PRECIOS_RECURSOS