from pydantic import BaseModel, ConfigDict
from typing import List, Optional
from datetime import datetime
from decimal import Decimal
from app.models.recomendacion import TipoRecomendacion, EstadoRecomendacion


class RecomendacionBase(BaseModel):
    producto_id: int
    tipo: TipoRecomendacion
    score: Optional[Decimal] = 0
    razon: Optional[str] = None


class RecomendacionCreate(RecomendacionBase):
    pedido_id: int
    mayorista_id: int
    orden: Optional[int] = 0


class RecomendacionResponse(RecomendacionBase):
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    pedido_id: int
    mayorista_id: int
    estado: EstadoRecomendacion
    orden: int
    producto_nombre: Optional[str]
    producto_precio: Optional[Decimal]
    producto_imagen_url: Optional[str]
    fue_clickeada: bool
    fue_agregada_carrito: bool
    cantidad_agregada: int
    monto_convertido: Decimal
    fecha_generacion: datetime
    fecha_envio: Optional[datetime]


class RecomendacionParaCarrito(BaseModel):
    """Schema para mostrar recomendaciones en el carrito público"""
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    producto_id: int
    producto_nombre: str
    producto_precio: Decimal
    producto_imagen_url: Optional[str]
    razon: Optional[str]
    orden: int


class RecomendacionesRequest(BaseModel):
    """Request para generar recomendaciones"""
    pedido_id: int
    forzar_regeneracion: Optional[bool] = False


class RecomendacionesResponse(BaseModel):
    """Response con las recomendaciones generadas"""
    pedido_id: int
    total_recomendaciones: int
    recomendaciones: List[RecomendacionResponse]
    token_carrito: Optional[str] = None
    url_carrito: Optional[str] = None 