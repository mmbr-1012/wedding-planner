# Gestor principal del sistema

from datetime import datetime, timedelta
from typing import List, Dict, Tuple, Optional, Any
import os
import json
from .models import Recurso, Evento, Restriccion, EstadoEvento

class DreamWeddingPlanner:
    """Gestor principal de la aplicación"""
    
    def __init__(self, data_dir: str = "data"):
        self.data_dir = data_dir
        self.recursos: List[Recurso] = []
        self.eventos: List[Evento] = []
        self.restricciones: List[Restriccion] = []
        self.proximo_id_evento = 1
        self._cargar_datos()
    
    def _cargar_datos(self):
        """Carga datos iniciales o desde archivo"""
        os.makedirs(self.data_dir, exist_ok=True)
        data_file = os.path.join(self.data_dir, "weddings.json")
        
        if os.path.exists(data_file):
            self._cargar_desde_json(data_file)
        else:
            self._crear_datos_iniciales()
            self._guardar_json(data_file)
    
    def _crear_datos_iniciales(self):
        """Crea datos iniciales predeterminados"""
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
        
        self.restricciones = [
            Restriccion("co-requisito", [9, 10], "Chef requiere equipo de meseros"),
            Restriccion("exclusion", [1, 2], "Jardín y Salón no pueden usarse simultáneamente"),
            Restriccion("exclusion", [3, 4], "Capilla y Playa no pueden usarse simultáneamente"),
        ]
    
    def _cargar_desde_json(self, archivo: str):
        """Carga datos desde archivo JSON"""
        try:
            with open(archivo, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # Cargar recursos
            self.recursos = []
            for r in data.get('recursos', []):
                recurso = Recurso(**r)
                if 'eventos_asignados' in r:
                    recurso.eventos_asignados = [
                        (eid, datetime.fromisoformat(inicio), datetime.fromisoformat(fin))
                        for eid, inicio, fin in r['eventos_asignados']
                    ]
                self.recursos.append(recurso)
            
            # Cargar eventos
            self.eventos = []
            for e in data.get('eventos', []):
                evento = Evento(
                    id=e['id'],
                    nombre=e['nombre'],
                    inicio=datetime.fromisoformat(e['inicio']),
                    fin=datetime.fromisoformat(e['fin']),
                    recursos_solicitados=e['recursos_solicitados'],
                    descripcion=e.get('descripcion', ''),
                    tipo_boda=e.get('tipo_boda', 'Personalizada'),
                    presupuesto=e.get('presupuesto', 0.0),
                    estado=e.get('estado', EstadoEvento.PENDIENTE.value),
                    fecha_creacion=datetime.fromisoformat(e.get('fecha_creacion', datetime.now().isoformat()))
                )
                self.eventos.append(evento)
                if evento.id >= self.proximo_id_evento:
                    self.proximo_id_evento = evento.id + 1
            
            # Cargar restricciones
            self.restricciones = [Restriccion(**r) for r in data.get('restricciones', [])]
            
        except Exception as e:
            print(f"Error cargando datos: {e}")
            self._crear_datos_iniciales()
    
    def _guardar_json(self, archivo: str) -> bool:
        """Guarda datos en archivo JSON"""
        try:
            data = {
                'recursos': [r.to_dict() for r in self.recursos],
                'eventos': [e.to_dict() for e in self.eventos],
                'restricciones': [r.to_dict() for r in self.restricciones]
            }
            
            with open(archivo, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            
            return True
        except Exception as e:
            print(f"Error guardando datos: {e}")
            return False
    
    # ========== MÉTODOS PÚBLICOS ==========
    
    def crear_evento(self, nombre: str, inicio: datetime, fin: datetime,
                    recursos: List[int], tipo_boda: str = "Personalizada",
                    presupuesto: float = 0.0, descripcion: str = "") -> Tuple[bool, str]:
        """Crea un nuevo evento de boda"""
        
        # Validar recursos
        for recurso_id in recursos:
            recurso = self._obtener_recurso(recurso_id)
            if not recurso:
                return False, f"Recurso ID {recurso_id} no encontrado"
            if not recurso.esta_disponible(inicio, fin):
                return False, f"Recurso {recurso.nombre} no disponible"
        
        # Crear evento
        evento = Evento(
            id=self.proximo_id_evento,
            nombre=nombre,
            inicio=inicio,
            fin=fin,
            recursos_solicitados=recursos,
            tipo_boda=tipo_boda,
            presupuesto=presupuesto,
            descripcion=descripcion,
            estado=EstadoEvento.CONFIRMADO.value
        )
        
        # Asignar recursos
        for recurso_id in recursos:
            recurso = self._obtener_recurso(recurso_id)
            if recurso:
                recurso.eventos_asignados.append((evento.id, inicio, fin))
        
        self.eventos.append(evento)
        self.proximo_id_evento += 1
        
        # Guardar cambios
        self._guardar_json(os.path.join(self.data_dir, "weddings.json"))
        
        return True, "Evento creado exitosamente"
    
    def obtener_eventos_proximos(self, dias: int = 30) -> List[Evento]:
        """Obtiene eventos próximos dentro de X días"""
        fecha_limite = datetime.now() + timedelta(days=dias)
        return [
            e for e in self.eventos
            if e.inicio <= fecha_limite and e.estado == EstadoEvento.CONFIRMADO.value
        ]
    
    def obtener_estadisticas(self) -> Dict[str, Any]:
        """Obtiene estadísticas del sistema"""
        return {
            "total_eventos": len(self.eventos),
            "eventos_confirmados": sum(1 for e in self.eventos if e.estado == EstadoEvento.CONFIRMADO.value),
            "eventos_pendientes": sum(1 for e in self.eventos if e.estado == EstadoEvento.PENDIENTE.value),
            "ingresos_totales": sum(e.presupuesto for e in self.eventos if e.estado == EstadoEvento.CONFIRMADO.value),
            "recursos_totales": len(self.recursos),
            "recursos_disponibles": sum(1 for r in self.recursos if r.disponible)
        }
    
    def _obtener_recurso(self, recurso_id: int) -> Optional[Recurso]:
        """Busca un recurso por ID"""
        for recurso in self.recursos:
            if recurso.id == recurso_id:
                return recurso
        return None
    
    def obtener_recurso_por_nombre(self, nombre: str) -> Optional[Recurso]:
        """Busca un recurso por nombre"""
        for recurso in self.recursos:
            if recurso.nombre.lower() == nombre.lower():
                return recurso
        return None
    
    def obtener_todos_recursos(self) -> List[Recurso]:
        """Devuelve todos los recursos"""
        return self.recursos