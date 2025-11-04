import time
from typing import TYPE_CHECKING
from robochef.patrones.strategy.estrategia_cocina import EstrategiaCocina

if TYPE_CHECKING:
    from robochef.entidades.cocina.pedido import Pedido

class EstrategiaGourmet(EstrategiaCocina):

    def ejecutar(self, pedido: 'Pedido') -> int:
        print(f"  > [Estrategia Gourmet]: Preparando pedido {pedido.get_id()} priorizando calidad.")
        
        costo_bateria = 0
        for plato in pedido.get_platos():
            print(f"  > Cocinando (Gourmet): {plato.get_nombre()}...")
            time.sleep(0.1) 
            print(f"  > ...emplatado de precisión para {plato.get_nombre()}.")
            costo_bateria += 25
        
        return costo_bateria