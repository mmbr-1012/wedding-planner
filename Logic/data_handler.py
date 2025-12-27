# Guardar/cargar JSON
import json
from datetime import datetime
from wedding_manager import Recurso, Evento, Restriccion, WeddingManager

class DataHandler:
    @staticmethod
    def cargar_datos(archivo: str, manager: WeddingManager) -> bool:
        try:
            with open(archivo, 'r', encoding='utf-8') as f:
                datos = json.load(f)
            
            manager.recursos = [Recurso.from_dict(r) for r in datos.get('recursos', [])]
            manager.eventos = [Evento.from_dict(e) for e in datos.get('eventos', [])]
            manager.restricciones = [Restriccion.from_dict(r) for r in datos.get('restricciones', [])]
            
            if manager.eventos:
                manager.proximo_id_evento = max(e.id for e in manager.eventos) + 1
            else:
                manager.proximo_id_evento = 1
                
            return True
            
        except FileNotFoundError:
            print("Archivo no encontrado, cargando datos iniciales...")
            manager.cargar_datos_iniciales()
            return False
        except Exception as e:
            print(f"Error cargando datos: {e}")
            manager.cargar_datos_iniciales()
            return False

    @staticmethod
    def guardar_datos(archivo: str, manager: WeddingManager) -> bool:
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
        manager = WeddingManager()
        datos = {
            'recursos': [recurso.to_dict() for recurso in manager.recursos],
            'eventos': [],
            'restricciones': [restriccion.to_dict() for restriccion in manager.restricciones]
        }
        
        with open(archivo, 'w', encoding='utf-8') as f:
            json.dump(datos, f, indent=2, ensure_ascii=False)