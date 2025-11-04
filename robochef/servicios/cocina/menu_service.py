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