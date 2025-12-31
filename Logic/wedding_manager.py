# Gestor principal del sistema

from datetime import datetime, timedelta
from typing import List, Dict, Tuple, Optional
import os
import json
from .models import Recurso, Evento, Restriccion, EstadoEvento, TipoRecurso, TipoRestriccion, TipoBoda

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
            Recurso(1, "Jardín para Ceremonia", TipoRecurso.CEREMONIA, 200, 2000, True, 
                   "Hermoso jardín al aire libre con capacidad para 200 personas"),
            Recurso(2, "Salón Principal", TipoRecurso.CEREMONIA, 250, 3000, True,
                   "Salón elegante con aire acondicionado"),
            Recurso(3, "Capilla Privada", TipoRecurso.CEREMONIA, 300, 4000, True,
                   "Capilla tradicional con vitrales"),
            Recurso(4, "Playa Privada", TipoRecurso.CEREMONIA, 120, 5000, True,
                   "Playa exclusiva con vista al mar"),
            Recurso(5, "Coordinador de Bodas", TipoRecurso.PERSONAL, 1, 2500, True,
                   "Coordinador profesional con 10+ años de experiencia"),
            Recurso(6, "Fotógrafo Principal", TipoRecurso.PERSONAL, 1, 3000, True,
                   "Fotógrafo profesional con equipo completo"),
            Recurso(7, "Video Profesional", TipoRecurso.PERSONAL, 1, 2000, True,
                   "Videógrafo con drones y cámaras 4K"),
            Recurso(8, "DJ/Música", TipoRecurso.PERSONAL, 1, 1500, True,
                   "DJ profesional con equipo de sonido"),
            Recurso(9, "Chef Ejecutivo", TipoRecurso.CATERING, 1, 4000, True,
                   "Chef con especialidad en banquetes"),
            Recurso(10, "Equipo de Meseros", TipoRecurso.CATERING, 10, 800, True,
                   "Equipo profesional de meseros"),
            Recurso(11, "Florista", TipoRecurso.DECORACION, 1, 2000, True,
                   "Florista especializada en bodas"),
            Recurso(12, "Pastelero", TipoRecurso.CATERING, 1, 1000, True,
                   "Pastelero especializado en tartas nupciales"),
            Recurso(13, "Salón Principal Recepción", TipoRecurso.RECEPCION, 400, 5000, True,
                   "Salón amplio para recepciones grandes"),
            Recurso(14, "Terraza VIP", TipoRecurso.RECEPCION, 150, 3000, True,
                   "Terraza exclusiva con vista panorámica"),
            Recurso(15, "Jardín Exterior", TipoRecurso.RECEPCION, 300, 4000, True,
                   "Jardín espacioso para recepciones al aire libre"),
            Recurso(16, "Carpa de Lujo", TipoRecurso.RECEPCION, 250, 4500, True,
                   "Carpa elegante climatizada"),
        ]
        
        self.restricciones = [
            Restriccion(
                TipoRestriccion.CO_REQUISITO,
                [9, 10],
                "El Chef Ejecutivo requiere el Equipo de Meseros para operar"
            ),
            Restriccion(
                TipoRestriccion.EXCLUSION,
                [1, 2],
                "Jardín para Ceremonia y Salón Principal no pueden usarse simultáneamente"
            ),
            Restriccion(
                TipoRestriccion.EXCLUSION,
                [3, 4],
                "Capilla Privada y Playa Privada no pueden usarse simultáneamente"
            ),
        ]
    
    def _cargar_desde_json(self, archivo: str):
        """Carga datos desde archivo JSON"""
        try:
            with open(archivo, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # Cargar recursos
            self.recursos = []
            for r in data.get('recursos', []):
                recurso = Recurso(
                    id=r['id'],
                    nombre=r['nombre'],
                    tipo=TipoRecurso(r['tipo']),
                    capacidad=r.get('capacidad', 1),
                    precio=r.get('precio', 0.0),
                    disponible=r.get('disponible', True),
                    descripcion=r.get('descripcion', '')
                )
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
                    tipo_boda=TipoBoda(e.get('tipo_boda', 'Personalizada')),
                    presupuesto=e.get('presupuesto', 0.0),
                    estado=EstadoEvento(e.get('estado', EstadoEvento.PENDIENTE.value)),
                    num_invitados=e.get('num_invitados', 0),
                    fecha_creacion=datetime.fromisoformat(e.get('fecha_creacion', datetime.now().isoformat()))
                )
                self.eventos.append(evento)
                if evento.id >= self.proximo_id_evento:
                    self.proximo_id_evento = evento.id + 1
            
            # Cargar restricciones
            self.restricciones = []
            for r in data.get('restricciones', []):
                restriccion = Restriccion(
                    tipo=TipoRestriccion(r['tipo']),
                    recursos_involucrados=r['recursos_involucrados'],
                    descripcion=r['descripcion']
                )
                self.restricciones.append(restriccion)
            
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
    
    def validar_restricciones(self, recursos_solicitados: List[int]) -> Tuple[bool, str]:
        """
        Valida que los recursos cumplan todas las restricciones
        Retorna (es_valido, mensaje_error)
        """
        for restriccion in self.restricciones:
            es_valido, mensaje = restriccion.valida_para(recursos_solicitados)
            if not es_valido:
                return False, mensaje
        
        return True, "Restricciones validadas correctamente"
    
    def crear_evento(self, nombre: str, inicio: datetime, fin: datetime,
                    recursos: List[int], tipo_boda: TipoBoda = TipoBoda.PERSONALIZADA,
                    presupuesto: float = 0.0, descripcion: str = "",
                    num_invitados: int = 0) -> Tuple[bool, str, Optional[int]]:
        """
        Crea un nuevo evento de boda
        Retorna (exito, mensaje, id_evento)
        """
        
        # Validar fechas
        if inicio >= fin:
            return False, "La fecha de inicio debe ser anterior a la fecha de fin", None
        
        if inicio < datetime.now():
            return False, "No se pueden crear eventos en el pasado", None
        
        # Validar recursos existen
        for recurso_id in recursos:
            recurso = self._obtener_recurso(recurso_id)
            if not recurso:
                return False, f"Recurso ID {recurso_id} no encontrado", None
        
        # Validar disponibilidad de recursos
        for recurso_id in recursos:
            recurso = self._obtener_recurso(recurso_id)
            if not recurso.esta_disponible(inicio, fin):
                conflictos = self._obtener_conflictos_recurso(recurso_id, inicio, fin)
                return False, f"Recurso '{recurso.nombre}' no disponible. Conflictos: {conflictos}", None
        
        # Validar restricciones
        es_valido, mensaje = self.validar_restricciones(recursos)
        if not es_valido:
            return False, mensaje, None
        
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
            num_invitados=num_invitados,
            estado=EstadoEvento.CONFIRMADO
        )
        
        # Asignar recursos
        for recurso_id in recursos:
            recurso = self._obtener_recurso(recurso_id)
            if recurso:
                recurso.asignar_evento(evento.id, inicio, fin)
        
        self.eventos.append(evento)
        evento_id = self.proximo_id_evento
        self.proximo_id_evento += 1
        
        # Guardar cambios
        self._guardar_json(os.path.join(self.data_dir, "weddings.json"))
        
        return True, f"Evento '{nombre}' creado exitosamente con ID {evento_id}", evento_id
    
    def eliminar_evento(self, evento_id: int) -> Tuple[bool, str]:
        """Elimina un evento y libera sus recursos"""
        evento = self.obtener_evento_por_id(evento_id)
        if not evento:
            return False, f"Evento ID {evento_id} no encontrado"
        
        # Liberar recursos
        for recurso_id in evento.recursos_solicitados:
            recurso = self._obtener_recurso(recurso_id)
            if recurso:
                recurso.liberar_evento(evento_id)
        
        # Eliminar evento
        self.eventos = [e for e in self.eventos if e.id != evento_id]
        
        # Guardar cambios
        self._guardar_json(os.path.join(self.data_dir, "weddings.json"))
        
        return True, f"Evento '{evento.nombre}' eliminado exitosamente"
    
    def buscar_horario_disponible(self, recursos: List[int], duracion: timedelta,
                                  fecha_inicio: datetime = None,
                                  fecha_limite: datetime = None) -> Optional[Tuple[datetime, datetime]]:
        """
        Encuentra el próximo horario disponible para los recursos solicitados
        
        Args:
            recursos: Lista de IDs de recursos necesarios
            duracion: Duración del evento
            fecha_inicio: Fecha desde donde empezar a buscar (por defecto: ahora)
            fecha_limite: Fecha límite para la búsqueda (por defecto: 1 año)
        
        Returns:
            Tupla (inicio, fin) del horario encontrado, o None si no hay disponibilidad
        """
        if fecha_inicio is None:
            fecha_inicio = datetime.now() + timedelta(days=1)
        
        if fecha_limite is None:
            fecha_limite = fecha_inicio + timedelta(days=365)
        
        # Validar restricciones antes de buscar
        es_valido, mensaje = self.validar_restricciones(recursos)
        if not es_valido:
            return None
        
        # Buscar horario disponible
        busqueda_actual = fecha_inicio
        incremento = timedelta(hours=1)  # Buscar cada hora
        
        while busqueda_actual < fecha_limite:
            fin_propuesto = busqueda_actual + duracion
            
            # Verificar si todos los recursos están disponibles
            todos_disponibles = True
            for recurso_id in recursos:
                recurso = self._obtener_recurso(recurso_id)
                if recurso and not recurso.esta_disponible(busqueda_actual, fin_propuesto):
                    todos_disponibles = False
                    break
            
            if todos_disponibles:
                return (busqueda_actual, fin_propuesto)
            
            busqueda_actual += incremento
        
        return None
    
    def _obtener_conflictos_recurso(self, recurso_id: int, inicio: datetime, fin: datetime) -> str:
        """Obtiene información sobre los conflictos de un recurso"""
        recurso = self._obtener_recurso(recurso_id)
        if not recurso:
            return "Recurso no encontrado"
        
        conflictos = []
        for evento_id, inicio_evento, fin_evento in recurso.eventos_asignados:
            if max(inicio, inicio_evento) < min(fin, fin_evento):
                evento = self.obtener_evento_por_id(evento_id)
                if evento:
                    conflictos.append(f"{evento.nombre} ({inicio_evento.strftime('%d/%m/%Y %H:%M')})")
        
        return ", ".join(conflictos) if conflictos else "Sin conflictos"
    
    def obtener_eventos_proximos(self, dias: int = 30) -> List[Evento]:
        """Obtiene eventos próximos dentro de X días"""
        fecha_actual = datetime.now()
        fecha_limite = fecha_actual + timedelta(days=dias)
        return [
            e for e in self.eventos
            if fecha_actual <= e.inicio <= fecha_limite 
            and e.estado == EstadoEvento.CONFIRMADO
        ]
    
    def obtener_evento_por_id(self, evento_id: int) -> Optional[Evento]:
        """Busca un evento por ID"""
        for evento in self.eventos:
            if evento.id == evento_id:
                return evento
        return None
    
    def obtener_estadisticas(self) -> Dict:
        """Obtiene estadísticas del sistema"""
        confirmados = [e for e in self.eventos if e.estado == EstadoEvento.CONFIRMADO]
        return {
            "total_eventos": len(self.eventos),
            "eventos_confirmados": len(confirmados),
            "eventos_pendientes": sum(1 for e in self.eventos if e.estado == EstadoEvento.PENDIENTE),
            "eventos_completados": sum(1 for e in self.eventos if e.estado == EstadoEvento.COMPLETADO),
            "ingresos_totales": sum(e.presupuesto for e in confirmados),
            "recursos_totales": len(self.recursos),
            "recursos_disponibles": sum(1 for r in self.recursos if r.disponible),
            "promedio_presupuesto": sum(e.presupuesto for e in confirmados) / len(confirmados) if confirmados else 0
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
    
    def obtener_recursos_por_tipo(self, tipo: TipoRecurso) -> List[Recurso]:
        """Obtiene recursos filtrados por tipo"""
        return [r for r in self.recursos if r.tipo == tipo]