from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Text, DECIMAL
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base


class Producto(Base):
    __tablename__ = "productos"
    
    id = Column(Integer, primary_key=True, index=True)
    
    # Datos del producto en Gescom
    gescom_producto_id = Column(String(50), nullable=False, index=True)
    codigo = Column(String(100), nullable=False, index=True)
    nombre = Column(String(255), nullable=False)
    descripcion = Column(Text)
    
    # Relación con mayorista
    mayorista_id = Column(Integer, ForeignKey("mayoristas.id"), nullable=False)
    
    # Información del producto
    categoria = Column(String(255))
    marca = Column(String(255))
    precio = Column(DECIMAL(10, 2))
    stock = Column(Integer, default=0)
    imagen_url = Column(String(500))
    
    # Configuraciones para recomendaciones
    es_destacado = Column(Boolean, default=False)
    orden_recomendacion = Column(Integer, default=0)  # Para ordenar recomendaciones
    activo_recomendaciones = Column(Boolean, default=True)
    
    # Estadísticas
    veces_vendido = Column(Integer, default=0)
    veces_recomendado = Column(Integer, default=0)
    conversion_recomendacion = Column(DECIMAL(5, 2), default=0)  # Porcentaje
    
    # Estado y fechas
    activo = Column(Boolean, default=True)
    fecha_creacion = Column(DateTime(timezone=True), server_default=func.now())
    fecha_actualizacion = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    mayorista = relationship("Mayorista")
    items_pedido = relationship("ItemPedido", back_populates="producto") 