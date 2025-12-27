from typing import Dict, Tuple, List

class BudgetCalculatorLogic:
    
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
    
    @classmethod
    def calcular_presupuesto(cls, selecciones: Dict) -> Tuple[float, List[str]]:
        total = 0
        detalles = []
        
        for item, cantidad in selecciones.items():
            if item in cls.PRECIOS:
                if isinstance(cls.PRECIOS[item], dict):
                    precio = cls.PRECIOS[item]["precio"]
                else:
                    precio = cls.PRECIOS[item]
                
                subtotal = precio * (cantidad if isinstance(cantidad, (int, float)) and cantidad > 0 else 1)
                total += subtotal
                
                nombre_formateado = cls._formatear_nombre_item(item)
                
                if cantidad > 1:
                    detalles.append(f"{nombre_formateado}: ${precio:,} x {cantidad} = ${subtotal:,}")
                else:
                    detalles.append(f"{nombre_formateado}: ${precio:,}")
        
        return total, detalles
    
    @classmethod
    def _formatear_nombre_item(cls, item: str) -> str:
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