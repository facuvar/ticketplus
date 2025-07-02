from sqlalchemy import Column, Integer, String, ForeignKey, DECIMAL
from sqlalchemy.orm import relationship
from app.core.database import Base


class ItemPedido(Base):
    __tablename__ = "items_pedido"
    
    id = Column(Integer, primary_key=True, index=True)
    
    # Relaciones
    pedido_id = Column(Integer, ForeignKey("pedidos.id"), nullable=False)
    producto_id = Column(Integer, ForeignKey("productos.id"), nullable=False)
    
    # Datos del item
    cantidad = Column(Integer, nullable=False)
    precio_unitario = Column(DECIMAL(10, 2), nullable=False)
    descuento = Column(DECIMAL(10, 2), default=0)
    subtotal = Column(DECIMAL(10, 2), nullable=False)
    
    # Información adicional del producto en el momento del pedido
    producto_codigo = Column(String(100))
    producto_nombre = Column(String(255))
    
    # Relationships
    pedido = relationship("Pedido", back_populates="items")
    producto = relationship("Producto", back_populates="items_pedido") 