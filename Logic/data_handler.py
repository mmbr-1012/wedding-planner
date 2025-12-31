# Guardar/cargar JSON y exportar datos

import json
import csv
from datetime import datetime
from typing import Optional
from .models import Recurso, Evento, Restriccion, EstadoEvento, TipoRecurso, TipoRestriccion, TipoBoda
from .wedding_manager import DreamWeddingPlanner

class DataHandler:
    """Manejador de datos para persistencia en JSON y exportación"""
    
    @staticmethod
    def cargar_datos(archivo: str, manager: DreamWeddingPlanner) -> bool:
        """Carga datos desde un archivo JSON"""
        try:
            with open(archivo, 'r', encoding='utf-8') as f:
                datos = json.load(f)
            
            # Cargar recursos
            manager.recursos = []
            for r in datos.get('recursos', []):
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
                    tipo_boda=TipoBoda(e.get('tipo_boda', 'Personalizada')),
                    presupuesto=e.get('presupuesto', 0.0),
                    estado=EstadoEvento(e.get('estado', EstadoEvento.PENDIENTE.value)),
                    num_invitados=e.get('num_invitados', 0),
                    fecha_creacion=datetime.fromisoformat(e.get('fecha_creacion', datetime.now().isoformat()))
                )
                manager.eventos.append(evento)
                if evento.id >= manager.proximo_id_evento:
                    manager.proximo_id_evento = evento.id + 1
            
            # Cargar restricciones
            manager.restricciones = []
            for r in datos.get('restricciones', []):
                restriccion = Restriccion(
                    tipo=TipoRestriccion(r['tipo']),
                    recursos_involucrados=r['recursos_involucrados'],
                    descripcion=r['descripcion']
                )
                manager.restricciones.append(restriccion)
            
            return True
            
        except FileNotFoundError:
            print(f"Archivo {archivo} no encontrado")
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
            # Exportar eventos
            with open(f"{archivo_salida}_eventos.csv", 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow(['ID', 'Nombre', 'Fecha Inicio', 'Fecha Fin', 'Tipo', 'Presupuesto', 'Invitados', 'Estado'])
                for evento in manager.eventos:
                    writer.writerow([
                        evento.id,
                        evento.nombre,
                        evento.inicio.strftime('%Y-%m-%d %H:%M'),
                        evento.fin.strftime('%Y-%m-%d %H:%M'),
                        evento.tipo_boda.value,
                        evento.presupuesto,
                        evento.num_invitados,
                        evento.estado.value
                    ])
            
            # Exportar recursos
            with open(f"{archivo_salida}_recursos.csv", 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow(['ID', 'Nombre', 'Tipo', 'Capacidad', 'Precio', 'Disponible', 'Eventos Asignados'])
                for recurso in manager.recursos:
                    writer.writerow([
                        recurso.id,
                        recurso.nombre,
                        recurso.tipo.value,
                        recurso.capacidad,
                        recurso.precio,
                        'Sí' if recurso.disponible else 'No',
                        len(recurso.eventos_asignados)
                    ])
            
            # Exportar restricciones
            with open(f"{archivo_salida}_restricciones.csv", 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow(['Tipo', 'Recursos Involucrados', 'Descripción'])
                for restriccion in manager.restricciones:
                    writer.writerow([
                        restriccion.tipo.value,
                        ', '.join(map(str, restriccion.recursos_involucrados)),
                        restriccion.descripcion
                    ])
            
            return True
        except Exception as e:
            print(f"Error exportando a CSV: {e}")
            return False
    
    @staticmethod
    def generar_reporte_completo(manager: DreamWeddingPlanner, archivo_salida: str) -> bool:
        """Genera un reporte completo en formato texto"""
        try:
            with open(archivo_salida, 'w', encoding='utf-8') as f:
                f.write("=" * 60 + "\n")
                f.write("REPORTE COMPLETO - DREAM WEDDING PLANNER\n")
                f.write("=" * 60 + "\n\n")
                
                # Estadísticas generales
                stats = manager.obtener_estadisticas()
                f.write("ESTADÍSTICAS GENERALES\n")
                f.write("-" * 60 + "\n")
                f.write(f"Total de eventos: {stats['total_eventos']}\n")
                f.write(f"Eventos confirmados: {stats['eventos_confirmados']}\n")
                f.write(f"Eventos pendientes: {stats['eventos_pendientes']}\n")
                f.write(f"Ingresos totales: ${stats['ingresos_totales']:,.2f}\n")
                f.write(f"Recursos totales: {stats['recursos_totales']}\n")
                f.write(f"Recursos disponibles: {stats['recursos_disponibles']}\n\n")
                
                # Eventos
                f.write("LISTADO DE EVENTOS\n")
                f.write("-" * 60 + "\n")
                for evento in manager.eventos:
                    f.write(f"\nID: {evento.id}\n")
                    f.write(f"Nombre: {evento.nombre}\n")
                    f.write(f"Fecha: {evento.inicio.strftime('%d/%m/%Y %H:%M')} - {evento.fin.strftime('%H:%M')}\n")
                    f.write(f"Tipo: {evento.tipo_boda.value}\n")
                    f.write(f"Invitados: {evento.num_invitados}\n")
                    f.write(f"Presupuesto: ${evento.presupuesto:,.2f}\n")
                    f.write(f"Estado: {evento.estado.value}\n")
                    f.write("-" * 40 + "\n")
                
                # Recursos
                f.write("\nLISTADO DE RECURSOS\n")
                f.write("-" * 60 + "\n")
                for recurso in manager.recursos:
                    f.write(f"\nID: {recurso.id}\n")
                    f.write(f"Nombre: {recurso.nombre}\n")
                    f.write(f"Tipo: {recurso.tipo.value}\n")
                    f.write(f"Precio: ${recurso.precio:,.2f}\n")
                    f.write(f"Disponible: {'Sí' if recurso.disponible else 'No'}\n")
                    f.write(f"Eventos asignados: {len(recurso.eventos_asignados)}\n")
                    f.write("-" * 40 + "\n")
            
            return True
        except Exception as e:
            print(f"Error generando reporte: {e}")
            return False