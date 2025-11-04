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