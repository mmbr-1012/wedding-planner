# Configuración del sistema - Temas, colores, precios, etc.
class Config:
    """Configuración principal de la aplicación"""
    
    # Colores para la interfaz
    COLORES = {
        "ROSADO_PASTEL": "#FFE4E6",
        "ROSADO_SUAVE": "#F8C8D0",
        "ROSADO_PROFUNDO": "#F4A6B8",
        "ROJO_PASTEL": "#FF6B6B",
        "BLANCO_NIEVE": "#FFFFFF",
        "BLANCO_HUESO": "#FFF8F0",
        "DORADO_SUAVE": "#FFD700",
        "PLATEADO_SUAVE": "#C0C0C0",
        "DORADO_OPACO": "#D4AF37",
        "PLATEADO_OPACO": "#A8A8A8"
    }
    
    # Temas de boda predefinidos
    TEMAS = {
        "Romántico Vintage": {
            "colores": ["Blanco", "Marfil", "Rosa pálido", "Dorado"],
            "decoracion": "Flores vintage, candelabros, muebles antiguos",
            "precio_base": 5000
        },
        "Boho Chic": {
            "colores": ["Marfil", "Terracota", "Verde salvia", "Dorado"],
            "decoracion": "Macramé, plantas, detalles naturales",
            "precio_base": 4500
        },
        "Moderno Minimalista": {
            "colores": ["Blanco", "Negro", "Gris", "Verde"],
            "decoracion": "Líneas limpias, geometrías, espacios abiertos",
            "precio_base": 4000
        },
        "Glamour": {
            "colores": ["Negro", "Blanco", "Dorado", "Plateado"],
            "decoracion": "Cristales, espejos, lujos brillantes",
            "precio_base": 7000
        },
        "Rústico": {
            "colores": ["Madera", "Verde", "Blanco", "Terracota"],
            "decoracion": "Madera natural, hierro, elementos naturales",
            "precio_base": 3500
        },
        "Playero": {
            "colores": ["Azul", "Blanco", "Dorado", "Turquesa"],
            "decoracion": "Conchas, arena, velas, telas ligeras",
            "precio_base": 6000
        }
    }
    
    # Paquetes de boda predefinidos
    PAQUETES = {
        "Boda Pequeña": {
            "invitados": "50-80 personas",
            "precio_base": 15000,
            "incluye": ["Ceremonia íntima", "Coctel básico", "Fotógrafo (4h)", "Decoración simple"]
        },
        "Boda Mediana": {
            "invitados": "80-150 personas",
            "precio_base": 30000,
            "incluye": ["Ceremonia principal", "Coctel premium", "Fotógrafo (6h)", "Video", "Decoración temática"]
        },
        "Boda Grande": {
            "invitados": "150-300 personas",
            "precio_base": 60000,
            "incluye": ["Ceremonia espectacular", "Coctel de lujo", "Banquete gourmet", "Equipo fotográfico completo"]
        }
    }
    
    # Precios de recursos
    PRECIOS = {
        "jardin": {"precio": 2000, "capacidad": "150-200"},
        "salon": {"precio": 3000, "capacidad": "100-250"},
        "capilla": {"precio": 4000, "capacidad": "100-300"},
        "playa": {"precio": 5000, "capacidad": "80-120"},
        "coordinador_bodas": 2500,
        "fotografo_principal": 3000,
        "video_profesional": 2000,
        "dj_musica": 1500,
        "chef_ejecutivo": 4000,
        "meseros": 800,
        "florista": 2000,
        "pastelero": 1000,
        "salon_principal": 5000,
        "terraza": 3000,
        "jardin_exterior": 4000,
        "carpa_lujo": 4500,
        "arco_floral": 800,
        "centro_mesa": 50,
        "candelabros": 300,
        "cortinas_telones": 600,
        "alfombras": 400,
        "letreros": 200,
        "globos": 150,
        "fuente_chocolate": 700,
        "fuente_champan": 600,
        "tarta_nupcial": 500,
        "libro_firmas_lujo": 150,
        "transporte_especial": 800,
        "pirotecnia": 1200,
    }

# Funciones de conveniencia para acceder a la configuración
def obtener_temas() -> dict:
    """Devuelve todos los temas disponibles"""
    return Config.TEMAS

def obtener_paquetes() -> dict:
    """Devuelve todos los paquetes disponibles"""
    return Config.PAQUETES

def obtener_colores() -> dict:
    """Devuelve todos los colores disponibles"""
    return Config.COLORES

def obtener_precios() -> dict:
    """Devuelve todos los precios de recursos"""
    return Config.PRECIOS