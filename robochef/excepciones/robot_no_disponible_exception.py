from robochef.excepciones.robochef_exception import RoboChefException
from robochef.entidades.robots.tipo_robot import TipoRobot

class RobotNoDisponibleException(RoboChefException):
    def __init__(self, tipo_robot: TipoRobot):
        mensaje = f"No hay robots de tipo '{tipo_robot.name}' disponibles en este momento."
        super().__init__(mensaje)
        self._tipo_robot_requerido = tipo_robot