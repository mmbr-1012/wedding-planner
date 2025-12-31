# Modelos de datos del sistema

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import List, Tuple, Optional, Dict

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

class TipoRecurso(Enum):
    """Tipos de recursos disponibles"""
    CEREMONIA = "Ceremonia"
    RECEPCION = "Recepción"
    PERSONAL = "Personal"
    DECORACION = "Decoración"
    CATERING = "Catering"

class TipoRestriccion(Enum):
    """Tipos de restricciones entre recursos"""
    CO_REQUISITO = "co-requisito"
    EXCLUSION = "exclusion"
    DEPENDENCIA = "dependencia"

@dataclass
class Recurso:
    """Representa un recurso disponible para bodas"""
    id: int
    nombre: str
    tipo: TipoRecurso
    capacidad: int = 1
    precio: float = 0.0
    disponible: bool = True
    descripcion: str = ""
    eventos_asignados: List[Tuple[int, datetime, datetime]] = field(default_factory=list)
    
    def __post_init__(self):
        # Convertir string a TipoRecurso si es necesario
        if isinstance(self.tipo, str):
            try:
                self.tipo = TipoRecurso(self.tipo)
            except ValueError:
                self.tipo = TipoRecurso.PERSONAL
    
    def esta_disponible(self, inicio: datetime, fin: datetime) -> bool:
        """Verifica si el recurso está disponible en un horario específico"""
        if not self.disponible:
            return False
        
        for _, inicio_existente, fin_existente in self.eventos_asignados:
            # Detectar solapamiento de intervalos
            if max(inicio, inicio_existente) < min(fin, fin_existente):
                return False
        return True
    
    def asignar_evento(self, evento_id: int, inicio: datetime, fin: datetime) -> bool:
        """Asigna un evento al recurso si está disponible"""
        if self.esta_disponible(inicio, fin):
            self.eventos_asignados.append((evento_id, inicio, fin))
            return True
        return False
    
    def liberar_evento(self, evento_id: int) -> bool:
        """Libera un evento del recurso"""
        eventos_filtrados = [e for e in self.eventos_asignados if e[0] != evento_id]
        if len(eventos_filtrados) < len(self.eventos_asignados):
            self.eventos_asignados = eventos_filtrados
            return True
        return False
    
    def to_dict(self) -> Dict:
        """Convierte el recurso a diccionario para JSON"""
        return {
            'id': self.id,
            'nombre': self.nombre,
            'tipo': self.tipo.value,
            'capacidad': self.capacidad,
            'precio': self.precio,
            'disponible': self.disponible,
            'descripcion': self.descripcion,
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
    tipo_boda: TipoBoda = TipoBoda.PERSONALIZADA
    presupuesto: float = 0.0
    estado: EstadoEvento = EstadoEvento.PENDIENTE
    num_invitados: int = 0
    fecha_creacion: datetime = field(default_factory=datetime.now)
    
    def __post_init__(self):
        # Convertir strings a Enums si es necesario
        if isinstance(self.tipo_boda, str):
            try:
                self.tipo_boda = TipoBoda(self.tipo_boda)
            except ValueError:
                self.tipo_boda = TipoBoda.PERSONALIZADA
        
        if isinstance(self.estado, str):
            try:
                self.estado = EstadoEvento(self.estado)
            except ValueError:
                self.estado = EstadoEvento.PENDIENTE
        
        # Validar fechas
        if self.inicio >= self.fin:
            raise ValueError("La fecha de inicio debe ser anterior a la fecha de fin")
    
    def duracion(self) -> float:
        """Retorna la duración del evento en horas"""
        return (self.fin - self.inicio).total_seconds() / 3600
    
    def cambiar_estado(self, nuevo_estado: EstadoEvento) -> None:
        """Cambia el estado del evento"""
        self.estado = nuevo_estado
    
    def to_dict(self) -> Dict:
        """Convierte el evento a diccionario para JSON"""
        return {
            'id': self.id,
            'nombre': self.nombre,
            'inicio': self.inicio.isoformat(),
            'fin': self.fin.isoformat(),
            'recursos_solicitados': self.recursos_solicitados,
            'descripcion': self.descripcion,
            'tipo_boda': self.tipo_boda.value,
            'presupuesto': self.presupuesto,
            'estado': self.estado.value,
            'num_invitados': self.num_invitados,
            'fecha_creacion': self.fecha_creacion.isoformat()
        }

@dataclass
class Restriccion:
    """Representa una restricción entre recursos"""
    tipo: TipoRestriccion
    recursos_involucrados: List[int]
    descripcion: str
    
    def __post_init__(self):
        # Convertir string a TipoRestriccion si es necesario
        if isinstance(self.tipo, str):
            try:
                self.tipo = TipoRestriccion(self.tipo)
            except ValueError:
                self.tipo = TipoRestriccion.EXCLUSION
        
        # Validar que hay al menos 2 recursos
        if len(self.recursos_involucrados) < 2:
            raise ValueError("Una restricción debe involucrar al menos 2 recursos")
    
    def valida_para(self, recursos_solicitados: List[int]) -> Tuple[bool, str]:
        """
        Verifica si los recursos solicitados cumplen esta restricción
        Retorna (es_valido, mensaje_error)
        """
        if self.tipo == TipoRestriccion.CO_REQUISITO:
            # Si el primer recurso está presente, el segundo también debe estarlo
            r1, r2 = self.recursos_involucrados[0], self.recursos_involucrados[1]
            if r1 in recursos_solicitados and r2 not in recursos_solicitados:
                return False, f"Violación de co-requisito: {self.descripcion}"
            return True, ""
        
        elif self.tipo == TipoRestriccion.EXCLUSION:
            # Los recursos no pueden estar juntos
            r1, r2 = self.recursos_involucrados[0], self.recursos_involucrados[1]
            if r1 in recursos_solicitados and r2 in recursos_solicitados:
                return False, f"Violación de exclusión: {self.descripcion}"
            return True, ""
        
        return True, ""
    
    def to_dict(self) -> Dict:
        """Convierte la restricción a diccionario para JSON"""
        return {
            'tipo': self.tipo.value,
            'recursos_involucrados': self.recursos_involucrados,
            'descripcion': self.descripcion
        }