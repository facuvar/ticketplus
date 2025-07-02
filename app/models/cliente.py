from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base


class Cliente(Base):
    __tablename__ = "clientes"
    
    id = Column(Integer, primary_key=True, index=True)
    
    # Datos del cliente en Gescom
    gescom_cliente_id = Column(String(50), nullable=False, index=True)
    nombre = Column(String(255), nullable=False)
    email = Column(String(255))
    telefono = Column(String(50))
    direccion = Column(Text)
    
    # Relación con mayorista
    mayorista_id = Column(Integer, ForeignKey("mayoristas.id"), nullable=False)
    
    # WhatsApp info
    whatsapp_numero = Column(String(50))
    acepta_whatsapp = Column(Boolean, default=True)
    
    # Configuraciones y estado
    activo = Column(Boolean, default=True)
    fecha_ultimo_pedido = Column(DateTime(timezone=True))
    total_pedidos = Column(Integer, default=0)
    ticket_promedio = Column(Integer, default=0)  # En centavos
    
    # Fechas
    fecha_creacion = Column(DateTime(timezone=True), server_default=func.now())
    fecha_actualizacion = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    mayorista = relationship("Mayorista")
    pedidos = relationship("Pedido", back_populates="cliente") 