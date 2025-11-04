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