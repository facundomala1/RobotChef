from enum import Enum, auto

class EstadoPedido(Enum):
    RECIBIDO = auto()
    EN_PREPARACION = auto()
    LISTO_PARA_SERVIR = auto()
    ENTREGADO = auto()
    CANCELADO = auto()