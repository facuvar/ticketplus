from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base


class Usuario(Base):
    __tablename__ = "usuarios"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, nullable=False, index=True)
    nombre = Column(String(255), nullable=False)
    apellido = Column(String(255))
    hashed_password = Column(String(255), nullable=False)
    
    # Relación con mayorista
    mayorista_id = Column(Integer, ForeignKey("mayoristas.id"), nullable=False)
    
    # Roles y permisos
    es_admin = Column(Boolean, default=False)
    activo = Column(Boolean, default=True)
    
    # Fechas
    fecha_creacion = Column(DateTime(timezone=True), server_default=func.now())
    fecha_ultimo_acceso = Column(DateTime(timezone=True))
    
    # Relationships
    mayorista = relationship("Mayorista", back_populates="usuarios") 