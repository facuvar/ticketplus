#!/usr/bin/env python3
"""
Script para corregir fechas de expiración de tokens de carrito
"""
from datetime import datetime, timedelta
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.models.pedido import Pedido
from app.core.config import settings

def corregir_expiracion_tokens():
    """Corregir fechas de expiración de tokens de carrito"""
    
    # Conectar a la base de datos
    engine = create_engine(settings.DATABASE_URL)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    db = SessionLocal()
    
    try:
        # Buscar pedidos con tokens pero con expiración pasada o nula
        ahora = datetime.now()
        pedidos_problema = db.query(Pedido).filter(
            Pedido.token_carrito.isnot(None),
            Pedido.token_carrito != '',
            (Pedido.token_expiracion.is_(None)) | 
            (Pedido.token_expiracion <= ahora)
        ).all()
        
        print(f"🔍 Encontrados {len(pedidos_problema)} pedidos con tokens expirados o sin expiración")
        
        for pedido in pedidos_problema:
            # Establecer nueva expiración (48 horas desde ahora)
            nueva_expiracion = ahora + timedelta(hours=48)
            
            # Actualizar pedido
            pedido.token_expiracion = nueva_expiracion
            
            print(f"✅ Pedido {pedido.numero_pedido}: Nueva expiración {nueva_expiracion.strftime('%Y-%m-%d %H:%M')}")
        
        # Commit cambios
        db.commit()
        print(f"🎉 Fechas de expiración corregidas para {len(pedidos_problema)} pedidos")
        
        # Mostrar algunos tokens válidos
        tokens_validos = db.query(Pedido).filter(
            Pedido.token_carrito.isnot(None),
            Pedido.token_carrito != '',
            Pedido.token_expiracion > ahora
        ).limit(3).all()
        
        print("\n🔗 Tokens válidos disponibles:")
        for pedido in tokens_validos:
            tiempo_restante = pedido.token_expiracion - ahora
            horas_restantes = int(tiempo_restante.total_seconds() / 3600)
            print(f"   Pedido: {pedido.numero_pedido}")
            print(f"   Token: {pedido.token_carrito}")
            print(f"   Expira en: {horas_restantes} horas")
            print(f"   URL: http://localhost:8000/frontend/carrito.html?token={pedido.token_carrito}")
            print()
        
    except Exception as e:
        print(f"❌ Error corrigiendo expiración: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    print("🚀 Corrigiendo fechas de expiración de tokens...")
    corregir_expiracion_tokens()
    print("✅ Proceso completado!") 