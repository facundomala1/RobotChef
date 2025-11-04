from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from robochef.entidades.cocina.pedido import Pedido

class EstrategiaCocina(ABC):

    @abstractmethod
    def ejecutar(self, pedido: 'Pedido') -> int:
        pass