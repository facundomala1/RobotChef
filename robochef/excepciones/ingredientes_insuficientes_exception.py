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