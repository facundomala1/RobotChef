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