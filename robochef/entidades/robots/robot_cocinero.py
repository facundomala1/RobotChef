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