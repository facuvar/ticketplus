from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Text, DECIMAL, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base
import enum


class TipoRecomendacion(str, enum.Enum):
    MAS_VENDIDOS = "mas_vendidos"
    HISTORICO_CLIENTE = "historico_cliente"
    CATEGORIA_SIMILAR = "categoria_similar"
    REGLA_PERSONALIZADA = "regla_personalizada"
    MANUAL = "manual"


class EstadoRecomendacion(str, enum.Enum):
    GENERADA = "generada"
    ENVIADA = "enviada"
    CLICKEADA = "clickeada"
    CONVERTIDA = "convertida"
    IGNORADA = "ignorada"


class Recomendacion(Base):
    __tablename__ = "recomendaciones"
    
    id = Column(Integer, primary_key=True, index=True)
    
    # Relaciones
    pedido_id = Column(Integer, ForeignKey("pedidos.id"), nullable=False)
    producto_id = Column(Integer, ForeignKey("productos.id"), nullable=False)
    mayorista_id = Column(Integer, ForeignKey("mayoristas.id"), nullable=False)
    
    # Información de la recomendación
    tipo = Column(Enum(TipoRecomendacion), nullable=False)
    estado = Column(Enum(EstadoRecomendacion), default=EstadoRecomendacion.GENERADA)
    orden = Column(Integer, default=0)  # Orden en la lista de recomendaciones
    
    # Algoritmo y scoring
    score = Column(DECIMAL(5, 2), default=0)  # Puntaje del algoritmo
    razon = Column(Text)  # Explicación de por qué se recomendó
    
    # Información del producto al momento de la recomendación
    producto_nombre = Column(String(255))
    producto_precio = Column(DECIMAL(10, 2))
    producto_imagen_url = Column(String(500))
    
    # Métricas de conversión
    fue_clickeada = Column(Boolean, default=False)
    fecha_click = Column(DateTime(timezone=True))
    fue_agregada_carrito = Column(Boolean, default=False)
    fecha_agregada_carrito = Column(DateTime(timezone=True))
    cantidad_agregada = Column(Integer, default=0)
    monto_convertido = Column(DECIMAL(10, 2), default=0)
    
    # Fechas
    fecha_generacion = Column(DateTime(timezone=True), server_default=func.now())
    fecha_envio = Column(DateTime(timezone=True))
    
    # Relationships
    pedido = relationship("Pedido", back_populates="recomendaciones")
    producto = relationship("Producto")
    mayorista = relationship("Mayorista") 