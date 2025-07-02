# Importar todos los modelos para que SQLAlchemy pueda resolver las relaciones
from .mayorista import Mayorista
from .usuario import Usuario
from .cliente import Cliente
from .producto import Producto
from .pedido import Pedido
from .item_pedido import ItemPedido
from .recomendacion import Recomendacion

__all__ = [
    "Mayorista",
    "Usuario", 
    "Cliente",
    "Producto",
    "Pedido",
    "ItemPedido",
    "Recomendacion"
] 