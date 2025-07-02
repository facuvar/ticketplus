from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Text, DECIMAL, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base
import enum


class EstadoPedido(str, enum.Enum):
    PENDIENTE = "pendiente"
    PROCESANDO = "procesando"
    ENVIADO = "enviado"
    ENTREGADO = "entregado"
    CANCELADO = "cancelado"


class TipoPedido(str, enum.Enum):
    ORIGINAL = "original"  # Pedido original del cliente
    UPSELL = "upsell"     # Pedido complementario por recomendación


class Pedido(Base):
    __tablename__ = "pedidos"
    
    id = Column(Integer, primary_key=True, index=True)
    
    # Datos del pedido en Gescom
    gescom_pedido_id = Column(String(50), nullable=False, index=True)
    numero_pedido = Column(String(100), nullable=False)
    
    # Relaciones
    mayorista_id = Column(Integer, ForeignKey("mayoristas.id"), nullable=False)
    cliente_id = Column(Integer, ForeignKey("clientes.id"), nullable=False)
    
    # Información del pedido
    tipo = Column(Enum(TipoPedido), default=TipoPedido.ORIGINAL)
    estado = Column(Enum(EstadoPedido), default=EstadoPedido.PENDIENTE)
    
    # Referencia al pedido original (solo para UPSELL)
    pedido_original_id = Column(Integer, ForeignKey("pedidos.id"), nullable=True)
    codigo_referencia = Column(String(200), nullable=True)  # Código del pedido original referenciado
    
    # Montos
    subtotal = Column(DECIMAL(10, 2), nullable=False)
    descuento = Column(DECIMAL(10, 2), default=0)
    impuestos = Column(DECIMAL(10, 2), default=0)
    total = Column(DECIMAL(10, 2), nullable=False)
    
    # Información adicional
    observaciones = Column(Text)
    direccion_envio = Column(Text)
    
    # Control de recomendaciones
    recomendaciones_enviadas = Column(Boolean, default=False)
    fecha_envio_recomendaciones = Column(DateTime(timezone=True))
    token_carrito = Column(String(255), unique=True, index=True)  # Token único para el carrito
    token_expiracion = Column(DateTime(timezone=True))
    
    # Métricas de conversión
    click_whatsapp = Column(Boolean, default=False)
    fecha_click_whatsapp = Column(DateTime(timezone=True))
    conversion_upsell = Column(Boolean, default=False)
    monto_upsell = Column(DECIMAL(10, 2), default=0)
    
    # Fechas
    fecha_pedido = Column(DateTime(timezone=True), nullable=False)
    fecha_creacion = Column(DateTime(timezone=True), server_default=func.now())
    fecha_actualizacion = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    mayorista = relationship("Mayorista", back_populates="pedidos")
    cliente = relationship("Cliente", back_populates="pedidos")
    items = relationship("ItemPedido", back_populates="pedido", cascade="all, delete-orphan")
    recomendaciones = relationship("Recomendacion", back_populates="pedido")
    
    # Auto-referencia para pedidos UPSELL
    pedido_original = relationship("Pedido", remote_side=[id], back_populates="pedidos_upsell")
    pedidos_upsell = relationship("Pedido", back_populates="pedido_original") 