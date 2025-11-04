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