"""
Archivo integrador generado automaticamente
Directorio: /home/facundo/RoboChef/robochef/excepciones
Fecha: 2025-11-04 15:42:21
Total de archivos integrados: 4
"""

# ================================================================================
# ARCHIVO 1/4: __init__.py
# Ruta: /home/facundo/RoboChef/robochef/excepciones/__init__.py
# ================================================================================



# ================================================================================
# ARCHIVO 2/4: ingredientes_insuficientes_exception.py
# Ruta: /home/facundo/RoboChef/robochef/excepciones/ingredientes_insuficientes_exception.py
# ================================================================================

from typing import TYPE_CHECKING
from robochef.excepciones.robochef_exception import RoboChefException

if TYPE_CHECKING:
    from robochef.entidades.cocina.ingrediente import Ingrediente

class IngredientesInsuficientesException(RoboChefException):
    
    def __init__(self, ingrediente: 'Ingrediente', cantidad_requerida: int, cantidad_disponible: int):
        mensaje = f"No hay suficiente '{ingrediente.get_nombre()}'. Requerido: {cantidad_requerida}, Disponible: {cantidad_disponible}"
        super().__init__(mensaje)
        self._ingrediente = ingrediente
        self._cantidad_requerida = cantidad_requerida
        self._cantidad_disponible = cantidad_disponible

# ================================================================================
# ARCHIVO 3/4: robochef_exception.py
# Ruta: /home/facundo/RoboChef/robochef/excepciones/robochef_exception.py
# ================================================================================

class RoboChefException(Exception):
    
    def __init__(self, mensaje: str):
        self._mensaje = mensaje
        super().__init__(self._mensaje)

    def get_mensaje(self) -> str:
        return self._mensaje

# ================================================================================
# ARCHIVO 4/4: robot_no_disponible_exception.py
# Ruta: /home/facundo/RoboChef/robochef/excepciones/robot_no_disponible_exception.py
# ================================================================================

from robochef.excepciones.robochef_exception import RoboChefException
from robochef.entidades.robots.tipo_robot import TipoRobot

class RobotNoDisponibleException(RoboChefException):
    def __init__(self, tipo_robot: TipoRobot):
        mensaje = f"No hay robots de tipo '{tipo_robot.name}' disponibles en este momento."
        super().__init__(mensaje)
        self._tipo_robot_requerido = tipo_robot

