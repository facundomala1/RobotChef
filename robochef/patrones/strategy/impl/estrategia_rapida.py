from typing import TYPE_CHECKING
from robochef.patrones.strategy.estrategia_cocina import EstrategiaCocina

if TYPE_CHECKING:
    from robochef.entidades.cocina.pedido import Pedido

class EstrategiaRapida(EstrategiaCocina):

    def ejecutar(self, pedido: 'Pedido') -> int:
        print(f"  > [Estrategia Rápida]: Preparando pedido {pedido.get_id()} priorizando velocidad.")
        
        costo_bateria = 0
        for plato in pedido.get_platos():
            print(f"  > Cocinando rápidamente: {plato.get_nombre()}")
            costo_bateria += 15 
        
        return costo_bateria