from pydantic import BaseModel, ConfigDict
from typing import List, Optional
from datetime import datetime
from decimal import Decimal
from app.models.pedido import EstadoPedido, TipoPedido


class ItemPedidoBase(BaseModel):
    producto_id: int
    cantidad: int
    precio_unitario: Decimal
    descuento: Optional[Decimal] = 0


class ItemPedidoCreate(ItemPedidoBase):
    pass


class ItemPedidoResponse(ItemPedidoBase):
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    subtotal: Decimal
    producto_codigo: Optional[str]
    producto_nombre: Optional[str]


class PedidoBase(BaseModel):
    gescom_pedido_id: str
    numero_pedido: str
    cliente_id: int
    subtotal: Decimal
    total: Decimal
    fecha_pedido: datetime
    observaciones: Optional[str] = None


class PedidoCreate(PedidoBase):
    items: List[ItemPedidoCreate]


class PedidoNuevo(BaseModel):
    """Schema para recibir pedidos nuevos desde Gescom"""
    mayorista_id: int
    gescom_pedido_id: str
    numero_pedido: str
    gescom_cliente_id: str
    cliente_nombre: str
    cliente_telefono: Optional[str] = None
    cliente_email: Optional[str] = None
    subtotal: Decimal
    total: Decimal
    fecha_pedido: datetime
    items: List[dict]  # Lista de items del pedido


class PedidoResponse(PedidoBase):
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    mayorista_id: int
    tipo: TipoPedido
    estado: EstadoPedido
    descuento: Decimal
    impuestos: Decimal
    token_carrito: Optional[str]
    recomendaciones_enviadas: bool
    fecha_creacion: datetime
    items: List[ItemPedidoResponse] = []


class PedidoListResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    numero_pedido: str
    cliente_nombre: str
    total: Decimal
    estado: EstadoPedido
    fecha_pedido: datetime
    recomendaciones_enviadas: bool 