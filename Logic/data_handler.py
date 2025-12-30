# Guardar/cargar JSON

import json
from datetime import datetime
from typing import Optional
from .models import Recurso, Evento, Restriccion, EstadoEvento
from .wedding_manager import DreamWeddingPlanner

class DataHandler:
    """Manejador de datos para persistencia en JSON"""
    
    @staticmethod
    def cargar_datos(archivo: str, manager: DreamWeddingPlanner) -> bool:
        """Carga datos desde un archivo JSON"""
        try:
            with open(archivo, 'r', encoding='utf-8') as f:
                datos = json.load(f)
            
            # Cargar recursos
            manager.recursos = []
            for r in datos.get('recursos', []):
                recurso = Recurso(**r)
                if 'eventos_asignados' in r:
                    recurso.eventos_asignados = [
                        (eid, datetime.fromisoformat(inicio), datetime.fromisoformat(fin))
                        for eid, inicio, fin in r['eventos_asignados']
                    ]
                manager.recursos.append(recurso)
            
            # Cargar eventos
            manager.eventos = []
            for e in datos.get('eventos', []):
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
                manager.eventos.append(evento)
                if evento.id >= manager.proximo_id_evento:
                    manager.proximo_id_evento = evento.id + 1
            
            # Cargar restricciones
            manager.restricciones = [Restriccion(**r) for r in datos.get('restricciones', [])]
            
            return True
            
        except FileNotFoundError:
            print("Archivo no encontrado, usando datos iniciales...")
            return False
        except Exception as e:
            print(f"Error cargando datos: {e}")
            return False
    
    @staticmethod
    def guardar_datos(archivo: str, manager: DreamWeddingPlanner) -> bool:
        """Guarda los datos en un archivo JSON"""
        try:
            datos = {
                'recursos': [recurso.to_dict() for recurso in manager.recursos],
                'eventos': [evento.to_dict() for evento in manager.eventos],
                'restricciones': [restriccion.to_dict() for restriccion in manager.restricciones]
            }
            
            with open(archivo, 'w', encoding='utf-8') as f:
                json.dump(datos, f, indent=2, ensure_ascii=False)
                
            return True
        except Exception as e:
            print(f"Error guardando datos: {e}")
            return False
    
    @staticmethod
    def crear_archivo_ejemplo(archivo: str):
        """Crea un archivo de datos de ejemplo"""
        manager = DreamWeddingPlanner()
        datos = {
            'recursos': [recurso.to_dict() for recurso in manager.recursos],
            'eventos': [],
            'restricciones': [restriccion.to_dict() for restriccion in manager.restricciones]
        }
        
        with open(archivo, 'w', encoding='utf-8') as f:
            json.dump(datos, f, indent=2, ensure_ascii=False)
    
    @staticmethod
    def exportar_datos_csv(manager: DreamWeddingPlanner, archivo_salida: str) -> bool:
        """Exporta datos a CSV para análisis"""
        try:
            import csv
            
            # Exportar eventos
            with open(f"{archivo_salida}_eventos.csv", 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow(['ID', 'Nombre', 'Fecha', 'Tipo', 'Presupuesto', 'Estado'])
                for evento in manager.eventos:
                    writer.writerow([
                        evento.id,
                        evento.nombre,
                        evento.inicio.strftime('%Y-%m-%d'),
                        evento.tipo_boda,
                        evento.presupuesto,
                        evento.estado
                    ])
            
            # Exportar recursos
            with open(f"{archivo_salida}_recursos.csv", 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow(['ID', 'Nombre', 'Tipo', 'Capacidad', 'Precio', 'Disponible'])
                for recurso in manager.recursos:
                    writer.writerow([
                        recurso.id,
                        recurso.nombre,
                        recurso.tipo,
                        recurso.capacidad,
                        recurso.precio,
                        recurso.disponible
                    ])
            
            return True
        except Exception as e:
            print(f"Error exportando a CSV: {e}")
            return False 