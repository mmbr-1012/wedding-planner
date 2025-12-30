# Calculadora de presupuestos para bodas

from typing import Dict, Tuple, List, Any
from .config import Config

class CalculadoraPresupuesto:
    """Calculadora de presupuesto para bodas"""
    
    @staticmethod
    def calcular(selecciones: Dict[str, Any]) -> Tuple[float, List[str]]:
        """Calcula el presupuesto basado en selecciones"""
        total = 0
        detalles = []
        
        for item, cantidad in selecciones.items():
            if item in Config.PRECIOS:
                if isinstance(Config.PRECIOS[item], dict):
                    precio = Config.PRECIOS[item]["precio"]
                else:
                    precio = Config.PRECIOS[item]
                
                if isinstance(cantidad, (int, float)) and cantidad > 0:
                    subtotal = precio * cantidad
                else:
                    subtotal = precio
                
                total += subtotal
                nombre = CalculadoraPresupuesto._formatear_nombre(item)
                
                if cantidad > 1:
                    detalles.append(f"{nombre}: ${precio:,} x {cantidad} = ${subtotal:,}")
                else:
                    detalles.append(f"{nombre}: ${precio:,}")
        
        return total, detalles
    
    @staticmethod
    def _formatear_nombre(item: str) -> str:
        """Formatea nombres de items para mostrar"""
        nombres = {
            "jardin": "Jardín para Ceremonia",
            "salon": "Salón Principal",
            "capilla": "Capilla Privada",
            "playa": "Playa Privada",
            "coordinador_bodas": "Coordinador de Bodas",
            "fotografo_principal": "Fotógrafo Principal",
            "video_profesional": "Video Profesional",
            "dj_musica": "DJ/Música",
            "chef_ejecutivo": "Chef Ejecutivo",
            "meseros": "Equipo de Meseros",
            "florista": "Florista",
            "pastelero": "Pastelero",
            "salon_principal": "Salón Principal Recepción",
            "terraza": "Terraza VIP",
            "jardin_exterior": "Jardín Exterior",
            "carpa_lujo": "Carpa de Lujo",
            "arco_floral": "Arco Floral Premium",
            "centro_mesa": "Centros de Mesa",
            "candelabros": "Candelabros Elegantes",
            "cortinas_telones": "Cortinas y Telones",
            "alfombras": "Alfombra Roja",
            "letreros": "Letreros Personalizados",
            "globos": "Decoración con Globos",
            "fuente_chocolate": "Fuente de Chocolate",
            "fuente_champan": "Fuente de Champán",
            "tarta_nupcial": "Tarta Nupcial Premium",
            "libro_firmas_lujo": "Libro de Firmas de Lujo",
            "transporte_especial": "Transporte Especial",
            "pirotecnia": "Espectáculo de Pirotecnia"
        }
        return nombres.get(item, item.replace('_', ' ').title())