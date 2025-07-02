from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base


class Mayorista(Base):
    __tablename__ = "mayoristas"
    
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(255), nullable=False)
    email = Column(String(255), unique=True, nullable=False, index=True)
    telefono = Column(String(50))
    
    # Configuración de base de datos Gescom
    gescom_db_host = Column(String(255))
    gescom_db_port = Column(Integer, default=3306)
    gescom_db_name = Column(String(255))
    gescom_db_user = Column(String(255))
    gescom_db_password = Column(String(255))
    
    # WhatsApp API configuration
    whatsapp_api_key = Column(String(500))
    whatsapp_phone_number = Column(String(50))
    
    # Branding
    logo_url = Column(String(500))
    color_primario = Column(String(7), default="#007bff")  # Hex color
    color_secundario = Column(String(7), default="#6c757d")
    
    # Configuraciones del sistema
    recomendaciones_activas = Column(Boolean, default=True)
    tiempo_espera_horas = Column(Integer, default=24)  # Tiempo antes de enviar WhatsApp
    max_productos_recomendados = Column(Integer, default=5)
    
    # Reglas personalizadas (JSON)
    reglas_recomendacion = Column(JSON, default={})
    
    # Estado y fechas
    activo = Column(Boolean, default=True)
    fecha_creacion = Column(DateTime(timezone=True), server_default=func.now())
    fecha_actualizacion = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    usuarios = relationship("Usuario", back_populates="mayorista")
    pedidos = relationship("Pedido", back_populates="mayorista") 