import json
from datetime import datetime, timedelta
from typing import List, Dict, Tuple, Optional
from enum import Enum

class TipoBoda(Enum):
    PEQUENA = "Pequeña"
    MEDIANA = "Mediana" 
    GRANDE = "Grande"
    PERSONALIZADA = "Personalizada"

class EstadoEvento(Enum):
    PENDIENTE = "pendiente"
    CONFIRMADO = "confirmado"
    CANCELADO = "cancelado"
    EN_PROGRESO = "en_progreso"
    COMPLETADO = "completado"

class Recurso:
    def __init__(self, id: int, nombre: str, tipo: str, capacidad: int = 1, precio: float = 0.0):
        self.id = id
        self.nombre = nombre
        self.tipo = tipo
        self.capacidad = capacidad
        self.precio = precio
        self.eventos_asignados = []
        self.disponible = True

    def to_dict(self):
        return {
            'id': self.id,
            'nombre': self.nombre,
            'tipo': self.tipo,
            'capacidad': self.capacidad,
            'precio': self.precio,
            'disponible': self.disponible,
            'eventos_asignados': [(eid, inicio.isoformat(), fin.isoformat()) 
                                for eid, inicio, fin in self.eventos_asignados]
        }

    @classmethod
    def from_dict(cls, data):
        recurso = cls(
            data['id'], 
            data['nombre'], 
            data['tipo'], 
            data.get('capacidad', 1),
            data.get('precio', 0.0)
        )
        recurso.disponible = data.get('disponible', True)
        recurso.eventos_asignados = [
            (eid, datetime.fromisoformat(inicio), datetime.fromisoformat(fin)) 
            for eid, inicio, fin in data.get('eventos_asignados', [])
        ]
        return recurso

    def esta_disponible(self, inicio: datetime, fin: datetime) -> bool:
        if not self.disponible:
            return False
            
        for evento_id, inicio_existente, fin_existente in self.eventos_asignados:
            if max(inicio, inicio_existente) < min(fin, fin_existente):
                return False
        return True

class Evento:
    def __init__(self, id: int, nombre: str, inicio: datetime, fin: datetime, 
                 recursos_solicitados: List[int], descripcion: str = "", 
                 tipo_boda: str = "Personalizada", presupuesto: float = 0.0):
        self.id = id
        self.nombre = nombre
        self.inicio = inicio
        self.fin = fin
        self.recursos_solicitados = recursos_solicitados
        self.descripcion = descripcion
        self.tipo_boda = tipo_boda
        self.presupuesto = presupuesto
        self.estado = EstadoEvento.PENDIENTE.value
        self.fecha_creacion = datetime.now()

    def to_dict(self):
        return {
            'id': self.id,
            'nombre': self.nombre,
            'inicio': self.inicio.isoformat(),
            'fin': self.fin.isoformat(),
            'recursos_solicitados': self.recursos_solicitados,
            'descripcion': self.descripcion,
            'tipo_boda': self.tipo_boda,
            'presupuesto': self.presupuesto,
            'estado': self.estado,
            'fecha_creacion': self.fecha_creacion.isoformat()
        }

    @classmethod
    def from_dict(cls, data):
        evento = cls(
            data['id'],
            data['nombre'],
            datetime.fromisoformat(data['inicio']),
            datetime.fromisoformat(data['fin']),
            data['recursos_solicitados'],
            data.get('descripcion', ''),
            data.get('tipo_boda', 'Personalizada'),
            data.get('presupuesto', 0.0)
        )
        evento.estado = data.get('estado', EstadoEvento.PENDIENTE.value)
        evento.fecha_creacion = datetime.fromisoformat(data.get('fecha_creacion', datetime.now().isoformat()))
        return evento

class Restriccion:
    def __init__(self, tipo: str, recursos_involucrados: List[int], descripcion: str):
        self.tipo = tipo
        self.recursos_involucrados = recursos_involucrados
        self.descripcion = descripcion

    def to_dict(self):
        return {
            'tipo': self.tipo,
            'recursos_involucrados': self.recursos_involucrados,
            'descripcion': self.descripcion
        }

    @classmethod
    def from_dict(cls, data):
        return cls(data['tipo'], data['recursos_involucrados'], data['descripcion'])

class WeddingBudgetCalculator:
    
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
                
                if cantidad > 1:
                    detalles.append(f"{item}: ${precio:,} x {cantidad} = ${subtotal:,}")
                else:
                    detalles.append(f"{item}: ${precio:,}")
        
        return total, detalles

class WeddingManager:
    def __init__(self):
        self.recursos: List[Recurso] = []
        self.eventos: List[Evento] = []
        self.restricciones: List[Restriccion] = []
        self.proximo_id_evento = 1
        self.cargar_datos_iniciales()

    def cargar_datos_iniciales(self):
        if not self.recursos:
            self.recursos = [
                Recurso(1, "Jardín para Ceremonia", "Ceremonia", 200, 2000),
                Recurso(2, "Salón Principal", "Ceremonia", 250, 3000),
                Recurso(3, "Capilla Privada", "Ceremonia", 300, 4000),
                Recurso(4, "Playa Privada", "Ceremonia", 120, 5000),
                Recurso(5, "Coordinador de Bodas", "Personal", 1, 2500),
                Recurso(6, "Fotógrafo Principal", "Personal", 1, 3000),
                Recurso(7, "Video Profesional", "Personal", 1, 2000),
                Recurso(8, "DJ/Música", "Personal", 1, 1500),
                Recurso(9, "Chef Ejecutivo", "Personal", 1, 4000),
                Recurso(10, "Equipo de Meseros", "Personal", 10, 800),
                Recurso(11, "Florista", "Personal", 1, 2000),
                Recurso(12, "Pastelero", "Personal", 1, 1000),
                Recurso(13, "Salón Principal Recepción", "Recepción", 400, 5000),
                Recurso(14, "Terraza VIP", "Recepción", 150, 3000),
                Recurso(15, "Jardín Exterior", "Recepción", 300, 4000),
                Recurso(16, "Carpa de Lujo", "Recepción", 250, 4500),
            ]

        if not self.restricciones:
            self.restricciones = [
                Restriccion("co-requisito", [9, 10], "Chef requiere equipo de meseros"),
                Restriccion("co-requisito", [8, 17], "DJ requiere sistema de sonido"),
                Restriccion("exclusion", [1, 2], "Jardín y Salón no pueden usarse simultáneamente"),
                Restriccion("exclusion", [3, 4], "Capilla y Playa no pueden usarse simultáneamente"),
            ]

    def obtener_recurso_por_id(self, recurso_id: int) -> Optional[Recurso]:
        for recurso in self.recursos:
            if recurso.id == recurso_id:
                return recurso
        return None

    def obtener_evento_por_id(self, evento_id: int) -> Optional[Evento]:
        for evento in self.eventos:
            if evento.id == evento_id:
                return evento
        return None

    def validar_conflictos_recursos(self, evento: Evento) -> Tuple[bool, str]:
        for recurso_id in evento.recursos_solicitados:
            recurso = self.obtener_recurso_por_id(recurso_id)
            if not recurso:
                return False, f"Recurso ID {recurso_id} no encontrado"
            
            if not recurso.esta_disponible(evento.inicio, evento.fin):
                return False, f"Recurso {recurso.nombre} no disponible en ese horario"
                
        return True, "Sin conflictos"

    def planificar_evento(self, evento: Evento) -> Tuple[bool, str]:
        valido, mensaje = self.validar_conflictos_recursos(evento)
        if not valido:
            return False, mensaje

        for recurso_id in evento.recursos_solicitados:
            recurso = self.obtener_recurso_por_id(recurso_id)
            if recurso:
                recurso.eventos_asignados.append((evento.id, evento.inicio, evento.fin))

        evento.estado = EstadoEvento.CONFIRMADO.value
        self.eventos.append(evento)
        self.proximo_id_evento += 1
        return True, "Evento planificado con éxito"

    def obtener_bodas_proximas(self, dias: int = 30) -> List[Evento]:
        fecha_limite = datetime.now() + timedelta(days=dias)
        return [evento for evento in self.eventos 
                if evento.inicio <= fecha_limite and evento.estado == EstadoEvento.CONFIRMADO.value]

    def obtener_estadisticas(self) -> Dict:
        total_eventos = len(self.eventos)
        eventos_confirmados = sum(1 for e in self.eventos if e.estado == EstadoEvento.CONFIRMADO.value)
        eventos_pendientes = sum(1 for e in self.eventos if e.estado == EstadoEvento.PENDIENTE.value)
        
        ingresos_totales = sum(e.presupuesto for e in self.eventos if e.estado == EstadoEvento.CONFIRMADO.value)
        
        tipos_boda = {}
        for evento in self.eventos:
            if evento.tipo_boda in tipos_boda:
                tipos_boda[evento.tipo_boda] += 1
            else:
                tipos_boda[evento.tipo_boda] = 1
        
        return {
            "total_eventos": total_eventos,
            "eventos_confirmados": eventos_confirmados,
            "eventos_pendientes": eventos_pendientes,
            "ingresos_totales": ingresos_totales,
            "distribucion_tipos_boda": tipos_boda,
            "recursos_totales": len(self.recursos),
            "recursos_disponibles": sum(1 for r in self.recursos if r.disponible)
        }