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