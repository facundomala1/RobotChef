class RoboChefException(Exception):
    
    def __init__(self, mensaje: str):
        self._mensaje = mensaje
        super().__init__(self._mensaje)

    def get_mensaje(self) -> str:
        return self._mensaje