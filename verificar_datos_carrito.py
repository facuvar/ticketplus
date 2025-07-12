#!/usr/bin/env python3
"""
Script para verificar los datos disponibles para los tokens de carrito
"""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.models.pedido import Pedido
from app.models.item_pedido import ItemPedido
from app.models.recomendacion import Recomendacion
from app.models.cliente import Cliente
from app.models.mayorista import Mayorista
from app.core.config import settings
from datetime import datetime

def verificar_datos_carrito():
    """Verificar qué datos están disponibles para los tokens de carrito"""
    
    # Conectar a la base de datos
    engine = create_engine(settings.DATABASE_URL)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    db = SessionLocal()
    
    try:
        # Buscar pedidos con tokens válidos
        ahora = datetime.now()
        pedidos_con_token = db.query(Pedido).filter(
            Pedido.token_carrito.isnot(None),
            Pedido.token_carrito != '',
            Pedido.token_expiracion > ahora
        ).limit(5).all()
        
        print(f"🔍 Encontrados {len(pedidos_con_token)} pedidos con tokens válidos")
        print()
        
        for pedido in pedidos_con_token:
            print(f"📦 Pedido: {pedido.numero_pedido}")
            print(f"   Token: {pedido.token_carrito}")
            print(f"   Total: ${pedido.total}")
            print(f"   Expira: {pedido.token_expiracion}")
            
            # Verificar cliente
            cliente = db.query(Cliente).filter(Cliente.id == pedido.cliente_id).first()
            print(f"   Cliente: {cliente.nombre if cliente else 'No encontrado'}")
            
            # Verificar mayorista
            mayorista = db.query(Mayorista).filter(Mayorista.id == pedido.mayorista_id).first()
            print(f"   Mayorista: {mayorista.nombre if mayorista else 'No encontrado'}")
            
            # Verificar items del pedido
            items = db.query(ItemPedido).filter(ItemPedido.pedido_id == pedido.id).all()
            print(f"   Items del pedido: {len(items)}")
            for item in items:
                print(f"     - {item.producto_nombre}: {item.cantidad} x ${item.precio_unitario}")
            
            # Verificar recomendaciones
            recomendaciones = db.query(Recomendacion).filter(Recomendacion.pedido_id == pedido.id).all()
            print(f"   Recomendaciones: {len(recomendaciones)}")
            for rec in recomendaciones:
                print(f"     - {rec.producto_nombre}: ${rec.producto_precio} (Score: {rec.score})")
            
            print("-" * 50)
        
        # Mostrar estadísticas generales
        total_pedidos = db.query(Pedido).count()
        total_items = db.query(ItemPedido).count()
        total_recomendaciones = db.query(Recomendacion).count()
        
        print(f"\n📊 Estadísticas generales:")
        print(f"   Total pedidos: {total_pedidos}")
        print(f"   Total items: {total_items}")
        print(f"   Total recomendaciones: {total_recomendaciones}")
        
    except Exception as e:
        print(f"❌ Error verificando datos: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    print("🚀 Verificando datos de carrito...")
    verificar_datos_carrito()
    print("✅ Verificación completada!") 