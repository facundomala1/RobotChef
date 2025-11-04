"""
Archivo integrador generado automaticamente
Directorio: /home/facundo/RoboChef/robochef/servicios/cocina
Fecha: 2025-11-04 15:42:21
Total de archivos integrados: 3
"""

# ================================================================================
# ARCHIVO 1/3: __init__.py
# Ruta: /home/facundo/RoboChef/robochef/servicios/cocina/__init__.py
# ================================================================================



# ================================================================================
# ARCHIVO 2/3: inventario_service.py
# Ruta: /home/facundo/RoboChef/robochef/servicios/cocina/inventario_service.py
# ================================================================================

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

# ================================================================================
# ARCHIVO 3/3: menu_service.py
# Ruta: /home/facundo/RoboChef/robochef/servicios/cocina/menu_service.py
# ================================================================================

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

