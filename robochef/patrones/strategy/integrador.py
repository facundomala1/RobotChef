"""
Archivo integrador generado automaticamente
Directorio: /home/facundo/RoboChef/robochef/patrones/strategy
Fecha: 2025-11-04 15:42:21
Total de archivos integrados: 2
"""

# ================================================================================
# ARCHIVO 1/2: __init__.py
# Ruta: /home/facundo/RoboChef/robochef/patrones/strategy/__init__.py
# ================================================================================



# ================================================================================
# ARCHIVO 2/2: estrategia_cocina.py
# Ruta: /home/facundo/RoboChef/robochef/patrones/strategy/estrategia_cocina.py
# ================================================================================

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from robochef.entidades.cocina.pedido import Pedido

class EstrategiaCocina(ABC):

    @abstractmethod
    def ejecutar(self, pedido: 'Pedido') -> int:
        pass

