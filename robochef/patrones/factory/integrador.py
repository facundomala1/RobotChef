"""
Archivo integrador generado automaticamente
Directorio: /home/facundo/RoboChef/robochef/patrones/factory
Fecha: 2025-11-04 15:42:21
Total de archivos integrados: 2
"""

# ================================================================================
# ARCHIVO 1/2: __init__.py
# Ruta: /home/facundo/RoboChef/robochef/patrones/factory/__init__.py
# ================================================================================



# ================================================================================
# ARCHIVO 2/2: robot_factory.py
# Ruta: /home/facundo/RoboChef/robochef/patrones/factory/robot_factory.py
# ================================================================================

from typing import TYPE_CHECKING
from robochef.entidades.robots.tipo_robot import TipoRobot

if TYPE_CHECKING:
    from robochef.entidades.robots.robot import Robot
    from robochef.entidades.robots.robot_cocinero import RobotCocinero
    from robochef.entidades.robots.robot_camarero import RobotCamarero
    from robochef.patrones.strategy.estrategia_cocina import EstrategiaCocina
    

class RobotFactory:

    @staticmethod
    def _crear_cocinero_parrillero() -> 'RobotCocinero':
        from robochef.entidades.robots.robot_cocinero import RobotCocinero
        from robochef.patrones.strategy.impl.estrategia_rapida import EstrategiaRapida
        
        return RobotCocinero(
            tipo=TipoRobot.COCINERO_PARRILLERO,
            bateria_maxima=100,
            estrategia=EstrategiaRapida()
        )

    @staticmethod
    def _crear_cocinero_repostero() -> 'RobotCocinero':
        from robochef.entidades.robots.robot_cocinero import RobotCocinero
        from robochef.patrones.strategy.impl.estrategia_gourmet import EstrategiaGourmet
        
        return RobotCocinero(
            tipo=TipoRobot.COCINERO_REPOSTERO,
            bateria_maxima=80,
            estrategia=EstrategiaGourmet()
        )

    @staticmethod
    def _crear_camarero() -> 'RobotCamarero':
        from robochef.entidades.robots.robot_camarero import RobotCamarero
        return RobotCamarero(bateria_maxima=120)

    @staticmethod
    def crear_robot(tipo: TipoRobot) -> 'Robot':
        
        fabricas = {
            TipoRobot.COCINERO_PARRILLERO: RobotFactory._crear_cocinero_parrillero,
            TipoRobot.COCINERO_REPOSTERO: RobotFactory._crear_cocinero_repostero,
            TipoRobot.CAMARERO: RobotFactory._crear_camarero
        }

        if tipo not in fabricas:
            raise ValueError(f"Tipo de robot desconocido: {tipo.name}")

        return fabricas[tipo]()

