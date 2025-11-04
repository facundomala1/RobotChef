"""
Archivo integrador generado automaticamente
Directorio: /home/facundo/RoboChef/robochef/entidades/cocina
Fecha: 2025-11-04 15:42:21
Total de archivos integrados: 5
"""

# ================================================================================
# ARCHIVO 1/5: __init__.py
# Ruta: /home/facundo/RoboChef/robochef/entidades/cocina/__init__.py
# ================================================================================



# ================================================================================
# ARCHIVO 2/5: estado_pedido.py
# Ruta: /home/facundo/RoboChef/robochef/entidades/cocina/estado_pedido.py
# ================================================================================

from enum import Enum, auto

class EstadoPedido(Enum):
    RECIBIDO = auto()
    EN_PREPARACION = auto()
    LISTO_PARA_SERVIR = auto()
    ENTREGADO = auto()
    CANCELADO = auto()

# ================================================================================
# ARCHIVO 3/5: ingrediente.py
# Ruta: /home/facundo/RoboChef/robochef/entidades/cocina/ingrediente.py
# ================================================================================

class Ingrediente:
    def __init__(self, nombre: str, unidad_medida: str):
        self._nombre = nombre
        self._unidad_medida = unidad_medida

    def get_nombre(self) -> str:
        return self._nombre

    def get_unidad_medida(self) -> str:
        return self._unidad_medida

    def __repr__(self) -> str:
        return f"Ingrediente(nombre='{self._nombre}')"

# ================================================================================
# ARCHIVO 4/5: pedido.py
# Ruta: /home/facundo/RoboChef/robochef/entidades/cocina/pedido.py
# ================================================================================

from typing import List, TYPE_CHECKING
from robochef.entidades.cocina.estado_pedido import EstadoPedido
from robochef.patrones.observer.observable import Observable

if TYPE_CHECKING:
    from robochef.entidades.cocina.plato import Plato

class Pedido(Observable['Pedido']):
    
    _id_counter = 0

    def __init__(self, numero_mesa: int, platos: List['Plato']):
        super().__init__()
        Pedido._id_counter += 1
        self._id = Pedido._id_counter
        self._numero_mesa = numero_mesa
        self._platos = platos
        self._estado = EstadoPedido.RECIBIDO

    def get_id(self) -> int:
        return self._id

    def get_numero_mesa(self) -> int:
        return self._numero_mesa

    def get_platos(self) -> List['Plato']:
        return self._platos.copy()

    def get_estado(self) -> EstadoPedido:
        return self._estado

    def set_estado(self, nuevo_estado: EstadoPedido) -> None:
        if self._estado != nuevo_estado:
            print(f"[Pedido {self._id}]: Estado cambiando a -> {nuevo_estado.name}")
            self._estado = nuevo_estado
            self.notificar_observadores(self)

    def calcular_costo_total(self) -> float:
        total = 0.0
        for plato in self._platos:
            total += plato.get_precio()
        return total

    def __repr__(self) -> str:
        return f"Pedido(id={self._id}, mesa={self._numero_mesa}, estado='{self._estado.name}')"

# ================================================================================
# ARCHIVO 5/5: plato.py
# Ruta: /home/facundo/RoboChef/robochef/entidades/cocina/plato.py
# ================================================================================

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

