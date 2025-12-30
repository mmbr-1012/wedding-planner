# Modelos de datos del sistema

from dataclasses import dataclass, asdict
from datetime import datetime
from enum import Enum
from typing import List, Tuple, Optional, Any

class TipoBoda(Enum):
    """Tipos de bodas disponibles"""
    PEQUENA = "Pequeña"
    MEDIANA = "Mediana"
    GRANDE = "Grande"
    PERSONALIZADA = "Personalizada"

class EstadoEvento(Enum):
    """Estados posibles de un evento"""
    PENDIENTE = "pendiente"
    CONFIRMADO = "confirmado"
    CANCELADO = "cancelado"
    EN_PROGRESO = "en_progreso"
    COMPLETADO = "completado"

@dataclass
class Recurso:
    """Representa un recurso disponible para bodas"""
    id: int
    nombre: str
    tipo: str
    capacidad: int = 1
    precio: float = 0.0
    disponible: bool = True
    eventos_asignados: List[Tuple[int, datetime, datetime]] = None
    
    def __post_init__(self):
        if self.eventos_asignados is None:
            self.eventos_asignados = []
    
    def esta_disponible(self, inicio: datetime, fin: datetime) -> bool:
        """Verifica si el recurso está disponible en un horario específico"""
        if not self.disponible:
            return False
        for _, inicio_existente, fin_existente in self.eventos_asignados:
            if max(inicio, inicio_existente) < min(fin, fin_existente):
                return False
        return True
    
    def to_dict(self) -> dict:
        """Convierte el recurso a diccionario para JSON"""
        return {
            'id': self.id,
            'nombre': self.nombre,
            'tipo': self.tipo,
            'capacidad': self.capacidad,
            'precio': self.precio,
            'disponible': self.disponible,
            'eventos_asignados': [
                (eid, inicio.isoformat(), fin.isoformat())
                for eid, inicio, fin in self.eventos_asignados
            ]
        }

@dataclass
class Evento:
    """Representa un evento de boda"""
    id: int
    nombre: str
    inicio: datetime
    fin: datetime
    recursos_solicitados: List[int]
    descripcion: str = ""
    tipo_boda: str = "Personalizada"
    presupuesto: float = 0.0
    estado: str = EstadoEvento.PENDIENTE.value
    fecha_creacion: datetime = None
    
    def __post_init__(self):
        if self.fecha_creacion is None:
            self.fecha_creacion = datetime.now()
    
    def to_dict(self) -> dict:
        """Convierte el evento a diccionario para JSON"""
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

@dataclass
class Restriccion:
    """Representa una restricción entre recursos"""
    tipo: str
    recursos_involucrados: List[int]
    descripcion: str
    
    def to_dict(self) -> dict:
        """Convierte la restricción a diccionario para JSON"""
        return {
            'tipo': self.tipo,
            'recursos_involucrados': self.recursos_involucrados,
            'descripcion': self.descripcion
        }