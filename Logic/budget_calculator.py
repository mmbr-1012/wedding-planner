# Calculadora de presupuestos para bodas

from typing import Dict, Tuple, List, Any
from .config import ConfiguracionApp

class CalculadoraPresupuesto:
    """Calculadora de presupuesto para bodas"""
    
    @staticmethod
    def calcular(selecciones: Dict[str, Any]) -> Tuple[float, List[str]]:
        """
        Calcula el presupuesto basado en selecciones
        
        Args:
            selecciones: Diccionario con nombre_item: precio
        
        Returns:
            Tupla (total, lista_detalles)
        """
        total = 0
        detalles = []
        
        for item, valor in selecciones.items():
            if isinstance(valor, (int, float)):
                if valor > 0:
                    total += valor
                    detalles.append(f"• {item}: ${valor:,.2f}")
        
        return total, detalles
    
    @staticmethod
    def calcular_con_impuestos(subtotal: float, tasa_impuesto: float = None) -> Tuple[float, float, float]:
        """
        Calcula el total con impuestos
        
        Args:
            subtotal: Subtotal sin impuestos
            tasa_impuesto: Tasa de impuesto (si es None, usa la configuración)
        
        Returns:
            Tupla (subtotal, impuestos, total)
        """
        if tasa_impuesto is None:
            tasa_impuesto = ConfiguracionApp.IMPUESTOS
        
        impuestos = subtotal * (tasa_impuesto / 100)
        total = subtotal + impuestos
        
        return subtotal, impuestos, total
    
    @staticmethod
    def calcular_deposito(total: float, porcentaje: float = None) -> float:
        """
        Calcula el depósito de confirmación
        
        Args:
            total: Total del presupuesto
            porcentaje: Porcentaje del depósito (si es None, usa la configuración)
        
        Returns:
            Monto del depósito
        """
        if porcentaje is None:
            porcentaje = ConfiguracionApp.DEPOSITO_CONFIRMACION
        
        return total * (porcentaje / 100)
    
    @staticmethod
    def generar_plan_pagos(total: float, num_cuotas: int = 3) -> List[Dict[str, float]]:
        """
        Genera un plan de pagos en cuotas
        
        Args:
            total: Total a pagar
            num_cuotas: Número de cuotas
        
        Returns:
            Lista de diccionarios con información de cada cuota
        """
        deposito = CalculadoraPresupuesto.calcular_deposito(total)
        restante = total - deposito
        cuota = restante / (num_cuotas - 1) if num_cuotas > 1 else restante
        
        plan = [{"cuota": 1, "concepto": "Depósito inicial", "monto": deposito}]
        
        for i in range(2, num_cuotas + 1):
            plan.append({
                "cuota": i,
                "concepto": f"Cuota {i-1}",
                "monto": cuota if i < num_cuotas else restante - (cuota * (num_cuotas - 2))
            })
        
        return plan
    
    @staticmethod
    def comparar_paquetes(num_invitados: int) -> Dict[str, Any]:
        """
        Compara paquetes según número de invitados
        
        Args:
            num_invitados: Número de invitados
        
        Returns:
            Diccionario con recomendaciones
        """
        paquetes = ConfiguracionApp.PAQUETES
        recomendaciones = []
        
        for paquete in paquetes:
            if paquete.invitados_min <= num_invitados <= paquete.invitados_max:
                recomendaciones.append({
                    "nombre": paquete.nombre,
                    "precio": paquete.precio_base,
                    "match": "perfecto",
                    "incluye": paquete.incluye
                })
            elif num_invitados < paquete.invitados_min:
                recomendaciones.append({
                    "nombre": paquete.nombre,
                    "precio": paquete.precio_base,
                    "match": "sobrepasado",
                    "incluye": paquete.incluye
                })
        
        return {
            "invitados": num_invitados,
            "recomendaciones": recomendaciones
        }