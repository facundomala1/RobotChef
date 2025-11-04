"""
Archivo integrador generado automaticamente
Directorio: /home/facundo/RoboChef/robochef/entidades/robots
Fecha: 2025-11-04 15:42:21
Total de archivos integrados: 5
"""

# ================================================================================
# ARCHIVO 1/5: __init__.py
# Ruta: /home/facundo/RoboChef/robochef/entidades/robots/__init__.py
# ================================================================================



# ================================================================================
# ARCHIVO 2/5: robot.py
# Ruta: /home/facundo/RoboChef/robochef/entidades/robots/robot.py
# ================================================================================

from abc import ABC, abstractmethod
from robochef.entidades.robots.tipo_robot import TipoRobot

class Robot(ABC):
    
    _id_counter = 0

    def __init__(self, tipo: TipoRobot, bateria_maxima: int):
        Robot._id_counter += 1
        self._id = Robot._id_counter
        self._tipo = tipo
        self._bateria_maxima = bateria_maxima
        self._bateria_actual = bateria_maxima
        self._operativo = True

    def get_id(self) -> int:
        return self._id

    def get_tipo(self) -> TipoRobot:
        return self._tipo

    def get_bateria_actual(self) -> int:
        return self._bateria_actual

    def esta_operativo(self) -> bool:
        return self._operativo and self._bateria_actual > 0

    def consumir_bateria(self, cantidad: int):
        self._bateria_actual -= cantidad
        if self._bateria_actual <= 0:
            self._bateria_actual = 0
            self._operativo = False
            print(f"Robot {self._id} batería agotada. Enviando a recargar.")

    def recargar(self):
        self._bateria_actual = self._bateria_maxima
        self._operativo = True
        print(f"Robot {self._id} recargado.")

    @abstractmethod
    def trabajar(self):
        pass

    def __repr__(self) -> str:
        return f"Robot(id={self._id}, tipo='{self._tipo.name}', bateria={self._bateria_actual})"

# ================================================================================
# ARCHIVO 3/5: robot_camarero.py
# Ruta: /home/facundo/RoboChef/robochef/entidades/robots/robot_camarero.py
# ================================================================================

from typing import Optional, TYPE_CHECKING
from robochef.entidades.robots.robot import Robot
from robochef.entidades.robots.tipo_robot import TipoRobot

if TYPE_CHECKING:
    from robochef.entidades.cocina.pedido import Pedido

class RobotCamarero(Robot):

    def __init__(self, bateria_maxima: int):
        super().__init__(TipoRobot.CAMARERO, bateria_maxima)
        self._pedido_asignado: Optional['Pedido'] = None
        self._ocupado = False

    def esta_ocupado(self) -> bool:
        return self._ocupado

    def asignar_entrega(self, pedido: 'Pedido'):
        if not self._ocupado:
            self._pedido_asignado = pedido
            self._ocupado = True
            print(f"Robot Camarero {self.get_id()} asignado para entregar Pedido {pedido.get_id()}.")
        else:
            raise Exception(f"Robot {self.get_id()} ya está ocupado.")

    def trabajar(self):
        if not self._ocupado or self._pedido_asignado is None:
            print(f"Robot Camarero {self.get_id()} no tiene entrega asignada.")
            return

        if not self.esta_operativo():
            print(f"Robot Camarero {self.get_id()} no puede trabajar, batería baja.")
            return

        print(f"Robot Camarero {self.get_id()} recogiendo Pedido {self._pedido_asignado.get_id()}...")
        
        costo_bateria = 10 
        self.consumir_bateria(costo_bateria)
        
        print(f"Robot Camarero {self.get_id()} entregó Pedido {self._pedido_asignado.get_id()} en mesa {self._pedido_asignado.get_numero_mesa()}.")
        
        self._pedido_asignado = None
        self._ocupado = False

# ================================================================================
# ARCHIVO 4/5: robot_cocinero.py
# Ruta: /home/facundo/RoboChef/robochef/entidades/robots/robot_cocinero.py
# ================================================================================

from typing import Optional, TYPE_CHECKING
from robochef.entidades.robots.robot import Robot
from robochef.entidades.robots.tipo_robot import TipoRobot

if TYPE_CHECKING:
    from robochef.entidades.cocina.pedido import Pedido
class RobotCocinero(Robot):
    
    def __init__(self, tipo: TipoRobot, bateria_maxima: int, estrategia: object):
        super().__init__(tipo, bateria_maxima)
        self._estrategia_cocina = estrategia
        self._pedido_actual: Optional['Pedido'] = None
        self._ocupado = False

    def set_estrategia(self, estrategia: object):
        self._estrategia_cocina = estrategia

    def asignar_pedido(self, pedido: 'Pedido'):
        if not self._ocupado:
            self._pedido_actual = pedido
            self._ocupado = True
            print(f"Robot Cocinero {self.get_id()} asignado al Pedido {pedido.get_id()}.")
        else:
            raise Exception(f"Robot {self.get_id()} ya está ocupado.")

    def esta_ocupado(self) -> bool:
        return self._ocupado

    def trabajar(self):
        if not self._ocupado or self._pedido_actual is None:
            print(f"Robot Cocinero {self.get_id()} no tiene pedido asignado.")
            return

        if not self.esta_operativo():
            print(f"Robot Cocinero {self.get_id()} no puede trabajar, batería baja.")
            return

        print(f"Robot Cocinero {self.get_id()} (Tipo: {self.get_tipo().name}) iniciando trabajo en Pedido {self._pedido_actual.get_id()}.")
        
        # Python usará "duck typing" aquí. No le importa el tipo,
        # solo le importa si tiene un método .ejecutar().
        costo_bateria = self._estrategia_cocina.ejecutar(self._pedido_actual)
        
        self.consumir_bateria(costo_bateria)
        
        print(f"Robot Cocinero {self.get_id()} terminó el Pedido {self._pedido_actual.get_id()}. Batería restante: {self.get_bateria_actual()}%.")
        
        self._pedido_actual = None
        self._ocupado = False

# ================================================================================
# ARCHIVO 5/5: tipo_robot.py
# Ruta: /home/facundo/RoboChef/robochef/entidades/robots/tipo_robot.py
# ================================================================================

from enum import Enum, auto

class TipoRobot(Enum):
    COCINERO_PARRILLERO = auto()
    COCINERO_REPOSTERO = auto()
    CAMARERO = auto()

