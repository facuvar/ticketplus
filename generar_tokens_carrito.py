#!/usr/bin/env python3
"""
Script para generar tokens de carrito válidos para pedidos existentes
"""
import secrets
from datetime import datetime, timedelta
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.models.pedido import Pedido
from app.core.config import settings

def generar_tokens_carrito():
    """Generar tokens de carrito para pedidos que no los tienen"""
    
    # Conectar a la base de datos
    engine = create_engine(settings.DATABASE_URL)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    db = SessionLocal()
    
    try:
        # Buscar pedidos sin token_carrito o con tokens inválidos
        pedidos_sin_token = db.query(Pedido).filter(
            (Pedido.token_carrito.is_(None)) | 
            (Pedido.token_carrito == '') |
            (Pedido.token_carrito.like('token-%'))  # Tokens generados por defecto
        ).all()
        
        print(f"🔍 Encontrados {len(pedidos_sin_token)} pedidos sin tokens válidos")
        
        for pedido in pedidos_sin_token:
            # Generar token válido
            token_carrito = secrets.token_urlsafe(32)
            
            # Establecer expiración (48 horas desde ahora)
            token_expiracion = datetime.now() + timedelta(hours=48)
            
            # Actualizar pedido
            pedido.token_carrito = token_carrito
            pedido.token_expiracion = token_expiracion
            
            print(f"✅ Pedido {pedido.numero_pedido}: {token_carrito[:10]}...")
        
        # Commit cambios
        db.commit()
        print(f"🎉 Tokens generados exitosamente para {len(pedidos_sin_token)} pedidos")
        
        # Mostrar algunos tokens de ejemplo
        pedidos_con_token = db.query(Pedido).filter(
            Pedido.token_carrito.isnot(None),
            Pedido.token_carrito != ''
        ).limit(3).all()
        
        print("\n🔗 Ejemplos de tokens generados:")
        for pedido in pedidos_con_token:
            print(f"   Pedido: {pedido.numero_pedido}")
            print(f"   Token: {pedido.token_carrito}")
            print(f"   URL: http://localhost:8000/frontend/carrito.html?token={pedido.token_carrito}")
            print()
        
    except Exception as e:
        print(f"❌ Error generando tokens: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    print("🚀 Generando tokens de carrito para pedidos existentes...")
    generar_tokens_carrito()
    print("✅ Proceso completado!") 