"""
INTEGRADOR FINAL - CONSOLIDACION COMPLETA DEL PROYECTO
============================================================================
Directorio raiz: /home/facundo/RoboChef/robochef
Fecha de generacion: 2025-11-04 15:42:21
Total de archivos integrados: 30
Total de directorios procesados: 10
============================================================================
"""

# ==============================================================================
# TABLA DE CONTENIDOS
# ==============================================================================

# DIRECTORIO: .
#   1. constantes.py
#   2. main.py
#
# DIRECTORIO: entidades/cocina
#   3. __init__.py
#   4. estado_pedido.py
#   5. ingrediente.py
#   6. pedido.py
#   7. plato.py
#
# DIRECTORIO: entidades/robots
#   8. __init__.py
#   9. robot.py
#   10. robot_camarero.py
#   11. robot_cocinero.py
#   12. tipo_robot.py
#
# DIRECTORIO: excepciones
#   13. __init__.py
#   14. ingredientes_insuficientes_exception.py
#   15. robochef_exception.py
#   16. robot_no_disponible_exception.py
#
# DIRECTORIO: patrones/factory
#   17. __init__.py
#   18. robot_factory.py
#
# DIRECTORIO: patrones/observer
#   19. observable.py
#   20. observer.py
#
# DIRECTORIO: patrones/strategy
#   21. __init__.py
#   22. estrategia_cocina.py
#
# DIRECTORIO: patrones/strategy/impl
#   23. __init__.py
#   24. estrategia_gourmet.py
#   25. estrategia_rapida.py
#
# DIRECTORIO: servicios/cocina
#   26. __init__.py
#   27. inventario_service.py
#   28. menu_service.py
#
# DIRECTORIO: servicios/robotsservicios
#   29. __init__.py
#   30. jefe_cocina_service.py
#



################################################################################
# DIRECTORIO: .
################################################################################

# ==============================================================================
# ARCHIVO 1/30: constantes.py
# Directorio: .
# Ruta completa: /home/facundo/RoboChef/robochef/constantes.py
# ==============================================================================

# Batería
BATERIA_MAX_COCINERO = 100
BATERIA_MAX_CAMARERO = 120
COSTO_BATERIA_ENTREGA = 10
COSTO_BATERIA_RAPIDA = 15
COSTO_BATERIA_GOURMET = 25

# Tiempos
TIEMPO_SIMULACION_REINTENTO = 5
TIEMPO_SIMULACION_FINAL = 3
TIEMPO_PREPARACION_GOURMET = 0.1

# Stock Inicial
STOCK_INICIAL_DEFAULT = 1000

# ==============================================================================
# ARCHIVO 2/30: main.py
# Directorio: .
# Ruta completa: /home/facundo/RoboChef/robochef/main.py
# ==============================================================================

import time
from robochef.servicios.cocina.menu_service import MenuService
from robochef.servicios.cocina.inventario_service import InventarioService
from robochef.servicios.robotsservicios.jefe_cocina_service import JefeCocinaService
from robochef.entidades.cocina.pedido import Pedido
from robochef.constantes import STOCK_INICIAL_DEFAULT, TIEMPO_SIMULACION_REINTENTO, TIEMPO_SIMULACION_FINAL

def run_simulation():
    
    print("="*60 + "\n         SIMULACIÓN DE RESTAURANTE ROBOCHEF\n" + "="*60)

    # --- 1. Inicialización del Sistema ---
    print("\n[PASO 1]: Inicializando servicios centrales (Singleton y Menú)...")
    inventario = InventarioService.get_instance()
    menu = MenuService()
    jefe_cocina = JefeCocinaService()

    # --- 2. Abastecimiento de Inventario (Singleton) ---
    print("\n[PASO 2]: Abasteciendo el inventario...")
    for ingrediente in menu.get_ingredientes_base():
        inventario.agregar_stock(ingrediente, STOCK_INICIAL_DEFAULT)

    # --- 3. Inicialización de la Flota de Robots (Factory) ---
    print("\n[PASO 3]: Contratando flota de robots (Factory)...")
    jefe_cocina.inicializar_flota(num_cocineros=2, num_camareros=1)

    # --- 4. Llegada de Pedidos (Observer) ---
    print("\n[PASO 4]: Abriendo puertas... Llegan los pedidos.")
    
    plato_hamburguesa = menu.buscar_plato_por_nombre("Hamburguesa Clásica")
    plato_volcan = menu.buscar_plato_por_nombre("Volcán de Chocolate")

    pedido_1 = Pedido(numero_mesa=1, platos=[plato_hamburguesa])
    jefe_cocina.recibir_pedido(pedido_1)
    
    time.sleep(0.5)
    
    pedido_2 = Pedido(numero_mesa=3, platos=[plato_hamburguesa, plato_volcan])
    jefe_cocina.recibir_pedido(pedido_2)

    # --- 5. Simulación de Operación (Strategy) ---
    print(f"\n[PASO 5]: Cocina en operación. Esperando {TIEMPO_SIMULACION_REINTENTO} segundos...")
    time.sleep(TIEMPO_SIMULACION_REINTENTO)

    # --- 6. Llegada de más pedidos mientras otros están en espera ---
    print("\n[PASO 6]: Llega un pedido grande...")
    pedido_3 = Pedido(numero_mesa=2, platos=[plato_hamburguesa, plato_hamburguesa, plato_volcan])
    jefe_cocina.recibir_pedido(pedido_3)
    
    print(f"\n[PASO 7]: Esperando {TIEMPO_SIMULACION_FINAL} segundos más a que se liberen robots...")
    time.sleep(TIEMPO_SIMULACION_FINAL)
    
    jefe_cocina.reintentar_pedidos_pendientes()

    print("\n" + "="*60 + "\n              SIMULACIÓN COMPLETADA\n" + "="*60)

if __name__ == "__main__":
    run_simulation()


################################################################################
# DIRECTORIO: entidades/cocina
################################################################################

# ==============================================================================
# ARCHIVO 3/30: __init__.py
# Directorio: entidades/cocina
# Ruta completa: /home/facundo/RoboChef/robochef/entidades/cocina/__init__.py
# ==============================================================================



# ==============================================================================
# ARCHIVO 4/30: estado_pedido.py
# Directorio: entidades/cocina
# Ruta completa: /home/facundo/RoboChef/robochef/entidades/cocina/estado_pedido.py
# ==============================================================================

from enum import Enum, auto

class EstadoPedido(Enum):
    RECIBIDO = auto()
    EN_PREPARACION = auto()
    LISTO_PARA_SERVIR = auto()
    ENTREGADO = auto()
    CANCELADO = auto()

# ==============================================================================
# ARCHIVO 5/30: ingrediente.py
# Directorio: entidades/cocina
# Ruta completa: /home/facundo/RoboChef/robochef/entidades/cocina/ingrediente.py
# ==============================================================================

class Ingrediente:
    def __init__(self, nombre: str, unidad_medida: str):
        self._nombre = nombre
        self._unidad_medida = unidad_medida

    def get_nombre(self) -> str:
        return self._nombre

    def get_unidad_medida(self) -> str:
        return self._unidad_medida

    def __repr__(self) -> str:
        return f"Ingrediente(nombre='{self._nombre}')"

# ==============================================================================
# ARCHIVO 6/30: pedido.py
# Directorio: entidades/cocina
# Ruta completa: /home/facundo/RoboChef/robochef/entidades/cocina/pedido.py
# ==============================================================================

from typing import List, TYPE_CHECKING
from robochef.entidades.cocina.estado_pedido import EstadoPedido
from robochef.patrones.observer.observable import Observable

if TYPE_CHECKING:
    from robochef.entidades.cocina.plato import Plato

class Pedido(Observable['Pedido']):
    
    _id_counter = 0

    def __init__(self, numero_mesa: int, platos: List['Plato']):
        super().__init__()
        Pedido._id_counter += 1
        self._id = Pedido._id_counter
        self._numero_mesa = numero_mesa
        self._platos = platos
        self._estado = EstadoPedido.RECIBIDO

    def get_id(self) -> int:
        return self._id

    def get_numero_mesa(self) -> int:
        return self._numero_mesa

    def get_platos(self) -> List['Plato']:
        return self._platos.copy()

    def get_estado(self) -> EstadoPedido:
        return self._estado

    def set_estado(self, nuevo_estado: EstadoPedido) -> None:
        if self._estado != nuevo_estado:
            print(f"[Pedido {self._id}]: Estado cambiando a -> {nuevo_estado.name}")
            self._estado = nuevo_estado
            self.notificar_observadores(self)

    def calcular_costo_total(self) -> float:
        total = 0.0
        for plato in self._platos:
            total += plato.get_precio()
        return total

    def __repr__(self) -> str:
        return f"Pedido(id={self._id}, mesa={self._numero_mesa}, estado='{self._estado.name}')"

# ==============================================================================
# ARCHIVO 7/30: plato.py
# Directorio: entidades/cocina
# Ruta completa: /home/facundo/RoboChef/robochef/entidades/cocina/plato.py
# ==============================================================================

from typing import Dict, TYPE_CHECKING

if TYPE_CHECKING:
    from robochef.entidades.cocina.ingrediente import Ingrediente

class Plato:
    def __init__(self, nombre: str, precio: float, receta: Dict['Ingrediente', int]):
        self._nombre = nombre
        self._precio = precio
        self._receta = receta

    def get_nombre(self) -> str:
        return self._nombre

    def get_precio(self) -> float:
        return self._precio

    def get_receta(self) -> Dict['Ingrediente', int]:
        # Devolvemos una copia para proteger la receta original (encapsulación)
        return self._receta.copy()

    def __repr__(self) -> str:
        return f"Plato(nombre='{self._nombre}', precio={self._precio})"


################################################################################
# DIRECTORIO: entidades/robots
################################################################################

# ==============================================================================
# ARCHIVO 8/30: __init__.py
# Directorio: entidades/robots
# Ruta completa: /home/facundo/RoboChef/robochef/entidades/robots/__init__.py
# ==============================================================================



# ==============================================================================
# ARCHIVO 9/30: robot.py
# Directorio: entidades/robots
# Ruta completa: /home/facundo/RoboChef/robochef/entidades/robots/robot.py
# ==============================================================================

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

# ==============================================================================
# ARCHIVO 10/30: robot_camarero.py
# Directorio: entidades/robots
# Ruta completa: /home/facundo/RoboChef/robochef/entidades/robots/robot_camarero.py
# ==============================================================================

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

# ==============================================================================
# ARCHIVO 11/30: robot_cocinero.py
# Directorio: entidades/robots
# Ruta completa: /home/facundo/RoboChef/robochef/entidades/robots/robot_cocinero.py
# ==============================================================================

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

# ==============================================================================
# ARCHIVO 12/30: tipo_robot.py
# Directorio: entidades/robots
# Ruta completa: /home/facundo/RoboChef/robochef/entidades/robots/tipo_robot.py
# ==============================================================================

from enum import Enum, auto

class TipoRobot(Enum):
    COCINERO_PARRILLERO = auto()
    COCINERO_REPOSTERO = auto()
    CAMARERO = auto()


################################################################################
# DIRECTORIO: excepciones
################################################################################

# ==============================================================================
# ARCHIVO 13/30: __init__.py
# Directorio: excepciones
# Ruta completa: /home/facundo/RoboChef/robochef/excepciones/__init__.py
# ==============================================================================



# ==============================================================================
# ARCHIVO 14/30: ingredientes_insuficientes_exception.py
# Directorio: excepciones
# Ruta completa: /home/facundo/RoboChef/robochef/excepciones/ingredientes_insuficientes_exception.py
# ==============================================================================

from typing import TYPE_CHECKING
from robochef.excepciones.robochef_exception import RoboChefException

if TYPE_CHECKING:
    from robochef.entidades.cocina.ingrediente import Ingrediente

class IngredientesInsuficientesException(RoboChefException):
    
    def __init__(self, ingrediente: 'Ingrediente', cantidad_requerida: int, cantidad_disponible: int):
        mensaje = f"No hay suficiente '{ingrediente.get_nombre()}'. Requerido: {cantidad_requerida}, Disponible: {cantidad_disponible}"
        super().__init__(mensaje)
        self._ingrediente = ingrediente
        self._cantidad_requerida = cantidad_requerida
        self._cantidad_disponible = cantidad_disponible

# ==============================================================================
# ARCHIVO 15/30: robochef_exception.py
# Directorio: excepciones
# Ruta completa: /home/facundo/RoboChef/robochef/excepciones/robochef_exception.py
# ==============================================================================

class RoboChefException(Exception):
    
    def __init__(self, mensaje: str):
        self._mensaje = mensaje
        super().__init__(self._mensaje)

    def get_mensaje(self) -> str:
        return self._mensaje

# ==============================================================================
# ARCHIVO 16/30: robot_no_disponible_exception.py
# Directorio: excepciones
# Ruta completa: /home/facundo/RoboChef/robochef/excepciones/robot_no_disponible_exception.py
# ==============================================================================

from robochef.excepciones.robochef_exception import RoboChefException
from robochef.entidades.robots.tipo_robot import TipoRobot

class RobotNoDisponibleException(RoboChefException):
    def __init__(self, tipo_robot: TipoRobot):
        mensaje = f"No hay robots de tipo '{tipo_robot.name}' disponibles en este momento."
        super().__init__(mensaje)
        self._tipo_robot_requerido = tipo_robot


################################################################################
# DIRECTORIO: patrones/factory
################################################################################

# ==============================================================================
# ARCHIVO 17/30: __init__.py
# Directorio: patrones/factory
# Ruta completa: /home/facundo/RoboChef/robochef/patrones/factory/__init__.py
# ==============================================================================



# ==============================================================================
# ARCHIVO 18/30: robot_factory.py
# Directorio: patrones/factory
# Ruta completa: /home/facundo/RoboChef/robochef/patrones/factory/robot_factory.py
# ==============================================================================

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


################################################################################
# DIRECTORIO: patrones/observer
################################################################################

# ==============================================================================
# ARCHIVO 19/30: observable.py
# Directorio: patrones/observer
# Ruta completa: /home/facundo/RoboChef/robochef/patrones/observer/observable.py
# ==============================================================================

from typing import Generic, TypeVar, List
from robochef.patrones.observer.observer import Observer

T = TypeVar('T')

class Observable(Generic[T]):
    
    def __init__(self):
        self._observadores: List[Observer[T]] = []

    def agregar_observador(self, observador: Observer[T]) -> None:
        if observador not in self._observadores:
            self._observadores.append(observador)

    def eliminar_observador(self, observador: Observer[T]) -> None:
        try:
            self._observadores.remove(observador)
        except ValueError:
            pass 

    def notificar_observadores(self, evento: T) -> None:
        for observador in self._observadores:
            observador.actualizar(evento)

# ==============================================================================
# ARCHIVO 20/30: observer.py
# Directorio: patrones/observer
# Ruta completa: /home/facundo/RoboChef/robochef/patrones/observer/observer.py
# ==============================================================================

from abc import ABC, abstractmethod
from typing import Generic, TypeVar

T = TypeVar('T')

class Observer(Generic[T], ABC):

    @abstractmethod
    def actualizar(self, evento: T) -> None:
        pass


################################################################################
# DIRECTORIO: patrones/strategy
################################################################################

# ==============================================================================
# ARCHIVO 21/30: __init__.py
# Directorio: patrones/strategy
# Ruta completa: /home/facundo/RoboChef/robochef/patrones/strategy/__init__.py
# ==============================================================================



# ==============================================================================
# ARCHIVO 22/30: estrategia_cocina.py
# Directorio: patrones/strategy
# Ruta completa: /home/facundo/RoboChef/robochef/patrones/strategy/estrategia_cocina.py
# ==============================================================================

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from robochef.entidades.cocina.pedido import Pedido

class EstrategiaCocina(ABC):

    @abstractmethod
    def ejecutar(self, pedido: 'Pedido') -> int:
        pass


################################################################################
# DIRECTORIO: patrones/strategy/impl
################################################################################

# ==============================================================================
# ARCHIVO 23/30: __init__.py
# Directorio: patrones/strategy/impl
# Ruta completa: /home/facundo/RoboChef/robochef/patrones/strategy/impl/__init__.py
# ==============================================================================



# ==============================================================================
# ARCHIVO 24/30: estrategia_gourmet.py
# Directorio: patrones/strategy/impl
# Ruta completa: /home/facundo/RoboChef/robochef/patrones/strategy/impl/estrategia_gourmet.py
# ==============================================================================

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

# ==============================================================================
# ARCHIVO 25/30: estrategia_rapida.py
# Directorio: patrones/strategy/impl
# Ruta completa: /home/facundo/RoboChef/robochef/patrones/strategy/impl/estrategia_rapida.py
# ==============================================================================

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


################################################################################
# DIRECTORIO: servicios/cocina
################################################################################

# ==============================================================================
# ARCHIVO 26/30: __init__.py
# Directorio: servicios/cocina
# Ruta completa: /home/facundo/RoboChef/robochef/servicios/cocina/__init__.py
# ==============================================================================



# ==============================================================================
# ARCHIVO 27/30: inventario_service.py
# Directorio: servicios/cocina
# Ruta completa: /home/facundo/RoboChef/robochef/servicios/cocina/inventario_service.py
# ==============================================================================

from threading import Lock
from typing import Dict, TYPE_CHECKING
from robochef.excepciones.ingredientes_insuficientes_exception import IngredientesInsuficientesException

if TYPE_CHECKING:
    from robochef.entidades.cocina.ingrediente import Ingrediente
    from robochef.entidades.cocina.plato import Plato

class InventarioService:
    
    _instance = None
    _lock = Lock()

    def __new__(cls):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
                    cls._instance._inicializar_inventario()
        return cls._instance

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls()
        return cls._instance

    def _inicializar_inventario(self):
        self._stock: Dict['Ingrediente', int] = {}

    def agregar_stock(self, ingrediente: 'Ingrediente', cantidad: int):
        if ingrediente not in self._stock:
            self._stock[ingrediente] = 0
        self._stock[ingrediente] += cantidad
        print(f"[Inventario]: Añadido {cantidad} de {ingrediente.get_nombre()}. Stock actual: {self._stock[ingrediente]}")

    def verificar_y_consumir_stock(self, plato: 'Plato'):
        receta = plato.get_receta()
        
        for ingrediente, cantidad_requerida in receta.items():
            cantidad_disponible = self._stock.get(ingrediente, 0)
            if cantidad_disponible < cantidad_requerida:
                raise IngredientesInsuficientesException(ingrediente, cantidad_requerida, cantidad_disponible)
        
        for ingrediente, cantidad_requerida in receta.items():
            self._stock[ingrediente] -= cantidad_requerida
            print(f"[Inventario]: Consumido {cantidad_requerida} de {ingrediente.get_nombre()}. Stock restante: {self._stock[ingrediente]}")

    def get_stock_actual(self, ingrediente: 'Ingrediente') -> int:
        return self._stock.get(ingrediente, 0)

# ==============================================================================
# ARCHIVO 28/30: menu_service.py
# Directorio: servicios/cocina
# Ruta completa: /home/facundo/RoboChef/robochef/servicios/cocina/menu_service.py
# ==============================================================================

from typing import List, Dict, TYPE_CHECKING
from robochef.entidades.cocina.ingrediente import Ingrediente

if TYPE_CHECKING:
    from robochef.entidades.cocina.plato import Plato

class MenuService:

    def __init__(self):
        self._ingredientes_base: Dict[str, 'Ingrediente'] = {}
        self._menu: List['Plato'] = []
        self._inicializar_menu()

    def _crear_ingrediente(self, nombre: str, unidad: str) -> 'Ingrediente':
        ing = Ingrediente(nombre, unidad)
        self._ingredientes_base[nombre] = ing
        return ing

    def _inicializar_menu(self):
        from robochef.entidades.cocina.plato import Plato
        
        pan = self._crear_ingrediente("Pan de Hamburguesa", "unidades")
        carne = self._crear_ingrediente("Carne Molida", "gramos")
        queso = self._crear_ingrediente("Queso Cheddar", "fetas")
        harina = self._crear_ingrediente("Harina", "gramos")
        huevo = self._crear_ingrediente("Huevo", "unidades")
        chocolate = self._crear_ingrediente("Chocolate", "gramos")
        
        receta_hamburguesa = {pan: 2, carne: 150, queso: 1}
        hamburguesa = Plato("Hamburguesa Clásica", 10.50, receta_hamburguesa)
        
        receta_volcan = {harina: 50, huevo: 1, chocolate: 70}
        volcan = Plato("Volcán de Chocolate", 7.00, receta_volcan)
        
        self._menu = [hamburguesa, volcan]

    def get_ingredientes_base(self) -> List['Ingrediente']:
        return list(self._ingredientes_base.values())

    def get_menu(self) -> List['Plato']:
        return self._menu.copy()

    def buscar_plato_por_nombre(self, nombre: str) -> 'Plato':
        for plato in self._menu:
            if plato.get_nombre().lower() == nombre.lower():
                return plato
        raise ValueError(f"Plato '{nombre}' no encontrado en el menú.")


################################################################################
# DIRECTORIO: servicios/robotsservicios
################################################################################

# ==============================================================================
# ARCHIVO 29/30: __init__.py
# Directorio: servicios/robotsservicios
# Ruta completa: /home/facundo/RoboChef/robochef/servicios/robotsservicios/__init__.py
# ==============================================================================



# ==============================================================================
# ARCHIVO 30/30: jefe_cocina_service.py
# Directorio: servicios/robotsservicios
# Ruta completa: /home/facundo/RoboChef/robochef/servicios/robotsservicios/jefe_cocina_service.py
# ==============================================================================

import threading 
import time
from typing import List, Dict, TYPE_CHECKING, Optional
from robochef.entidades.robots.tipo_robot import TipoRobot
from robochef.entidades.cocina.estado_pedido import EstadoPedido
from robochef.patrones.observer.observer import Observer
from robochef.patrones.factory.robot_factory import RobotFactory
from robochef.servicios.cocina.inventario_service import InventarioService
from robochef.excepciones.robot_no_disponible_exception import RobotNoDisponibleException
from robochef.excepciones.ingredientes_insuficientes_exception import IngredientesInsuficientesException

if TYPE_CHECKING:
    from robochef.entidades.robots.robot import Robot
    from robochef.entidades.robots.robot_cocinero import RobotCocinero
    from robochef.entidades.robots.robot_camarero import RobotCamarero
    from robochef.entidades.cocina.pedido import Pedido

class JefeCocinaService(Observer['Pedido']):
    
    def __init__(self):
        self._inventario = InventarioService.get_instance()
        self._robots_cocina: List['RobotCocinero'] = []
        self._robots_camareros: List['RobotCamarero'] = []
        self._pedidos_pendientes: List['Pedido'] = []
        self._lock = threading.RLock()

    def inicializar_flota(self, num_cocineros: int, num_camareros: int):
        print(f"[JefeCocina]: Inicializando flota con {num_cocineros} cocineros y {num_camareros} camareros.")
        for _ in range(num_cocineros):
            self._robots_cocina.append(RobotFactory.crear_robot(TipoRobot.COCINERO_PARRILLERO))
        for _ in range(num_camareros):
            self._robots_camareros.append(RobotFactory.crear_robot(TipoRobot.CAMARERO))

    def recibir_pedido(self, pedido: 'Pedido'):
        with self._lock:
            print(f"[JefeCocina]: Recibido Pedido {pedido.get_id()} para mesa {pedido.get_numero_mesa()}.")
            pedido.agregar_observador(self)
            self._pedidos_pendientes.append(pedido)
            self._asignar_pedido_cocinero(pedido)

    def _asignar_pedido_cocinero(self, pedido: 'Pedido'):
        robot_disponible = self._buscar_robot_libre(self._robots_cocina)
        
        if robot_disponible:
            try:
                for plato in pedido.get_platos():
                    self._inventario.verificar_y_consumir_stock(plato)
                
                pedido.set_estado(EstadoPedido.EN_PREPARACION)
                robot_disponible.asignar_pedido(pedido)
                
                threading.Thread(target=self._procesar_cocina, args=(robot_disponible,)).start()
                
            except IngredientesInsuficientesException as e:
                print(f"[JefeCocina]: ERROR Pedido {pedido.get_id()}: {e.get_mensaje()}")
                pedido.set_estado(EstadoPedido.CANCELADO)
                
        else:
            print(f"[JefeCocina]: No hay cocineros disponibles. Pedido {pedido.get_id()} en espera.")

    def _procesar_cocina(self, robot_cocinero: 'RobotCocinero'):
        robot_cocinero.trabajar()
        
        if robot_cocinero._pedido_actual:
            robot_cocinero._pedido_actual.set_estado(EstadoPedido.LISTO_PARA_SERVIR)

    def _asignar_entrega_camarero(self, pedido: 'Pedido'):
        robot_disponible = self._buscar_robot_libre(self._robots_camareros)
        
        if robot_disponible:
            robot_disponible.asignar_entrega(pedido)
            threading.Thread(target=self._procesar_entrega, args=(robot_disponible,)).start()
            if pedido in self._pedidos_pendientes:
                self._pedidos_pendientes.remove(pedido)
        else:
            print(f"[JefeCocina]: No hay camareros disponibles. Pedido {pedido.get_id()} en espera de entrega.")
            if pedido not in self._pedidos_pendientes:
                self._pedidos_pendientes.append(pedido)

    def _procesar_entrega(self, robot_camarero: 'RobotCamarero'):
        robot_camarero.trabajar()
        
        if robot_camarero._pedido_asignado:
            robot_camarero._pedido_asignado.set_estado(EstadoPedido.ENTREGADO)

    def _buscar_robot_libre(self, flota: List['Robot']) -> Optional['Robot']:
        for robot in flota:
            if not robot.esta_ocupado() and robot.esta_operativo():
                return robot
        return None

    def actualizar(self, pedido: 'Pedido') -> None:
        with self._lock:
            estado = pedido.get_estado()
            print(f"[JefeCocina]: NOTIFICACIÓN - Pedido {pedido.get_id()} cambió a estado {estado.name}")
            
            if estado == EstadoPedido.LISTO_PARA_SERVIR:
                self._asignar_entrega_camarero(pedido)
            
            elif estado == EstadoPedido.CANCELADO or estado == EstadoPedido.ENTREGADO:
                if pedido in self._pedidos_pendientes:
                    self._pedidos_pendientes.remove(pedido)
                pedido.eliminar_observador(self)

    def reintentar_pedidos_pendientes(self):
        with self._lock:
            if not self._pedidos_pendientes:
                return

            print(f"[JefeCocina]: Reintentando {len(self._pedidos_pendientes)} pedidos pendientes...")
            pedidos_a_reintentar = self._pedidos_pendientes[:]
            for pedido in pedidos_a_reintentar:
                if pedido.get_estado() == EstadoPedido.RECIBIDO:
                    self._asignar_pedido_cocinero(pedido)
                elif pedido.get_estado() == EstadoPedido.LISTO_PARA_SERVIR:
                    self._asignar_entrega_camarero(pedido)


################################################################################
# FIN DEL INTEGRADOR FINAL
# Total de archivos: 30
# Generado: 2025-11-04 15:42:21
################################################################################
