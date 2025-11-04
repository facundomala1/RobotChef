from typing import Dict, TYPE_CHECKING

if TYPE_CHECKING:
    from robochef.entidades.cocina.ingrediente import Ingrediente

class Plato:
    def __init__(self, nombre: str, precio: float, receta: Dict['Ingrediente', int]):
        self._nombre = nombre
        self._precio = precio
        self._receta = receta

    def get_nombre(self) -> str:
        return self._nombre

    def get_precio(self) -> float:
        return self._precio

    def get_receta(self) -> Dict['Ingrediente', int]:
        # Devolvemos una copia para proteger la receta original (encapsulación)
        return self._receta.copy()

    def __repr__(self) -> str:
        return f"Plato(nombre='{self._nombre}', precio={self._precio})"