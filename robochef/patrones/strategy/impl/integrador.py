"""
Archivo integrador generado automaticamente
Directorio: /home/facundo/RoboChef/robochef/patrones/strategy/impl
Fecha: 2025-11-04 15:42:21
Total de archivos integrados: 3
"""

# ================================================================================
# ARCHIVO 1/3: __init__.py
# Ruta: /home/facundo/RoboChef/robochef/patrones/strategy/impl/__init__.py
# ================================================================================



# ================================================================================
# ARCHIVO 2/3: estrategia_gourmet.py
# Ruta: /home/facundo/RoboChef/robochef/patrones/strategy/impl/estrategia_gourmet.py
# ================================================================================

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

# ================================================================================
# ARCHIVO 3/3: estrategia_rapida.py
# Ruta: /home/facundo/RoboChef/robochef/patrones/strategy/impl/estrategia_rapida.py
# ================================================================================

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

