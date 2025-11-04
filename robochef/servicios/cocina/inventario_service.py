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