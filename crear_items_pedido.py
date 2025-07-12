#!/usr/bin/env python3
"""
Script para crear items de pedido para pedidos existentes
"""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.models.pedido import Pedido
from app.models.item_pedido import ItemPedido
from app.models.producto import Producto
from app.core.config import settings
from datetime import datetime

def crear_items_pedido():
    """Crear items de pedido para pedidos que no los tienen"""
    
    # Conectar a la base de datos
    engine = create_engine(settings.DATABASE_URL)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    db = SessionLocal()
    
    try:
        # Buscar pedidos sin items
        pedidos_sin_items = db.query(Pedido).filter(
            ~Pedido.id.in_(
                db.query(ItemPedido.pedido_id).distinct()
            )
        ).all()  # Quitar el limit(5) para afectar a todos
        
        print(f"🔍 Encontrados {len(pedidos_sin_items)} pedidos sin items")
        
        # Obtener productos disponibles
        productos = db.query(Producto).limit(10).all()
        
        if not productos:
            print("❌ No hay productos disponibles en la base de datos")
            return
        
        for pedido in pedidos_sin_items:
            print(f"📦 Añadiendo items al pedido: {pedido.numero_pedido}")
            
            # Crear 2-3 items por pedido
            import random
            num_items = random.randint(2, 3)
            productos_seleccionados = random.sample(productos, num_items)
            
            for i, producto in enumerate(productos_seleccionados):
                cantidad = random.randint(1, 3)
                precio_unitario = float(producto.precio) if producto.precio else 1000.0
                subtotal = cantidad * precio_unitario
                
                item = ItemPedido(
                    pedido_id=pedido.id,
                    producto_id=producto.id,
                    cantidad=cantidad,
                    precio_unitario=precio_unitario,
                    subtotal=subtotal,
                    producto_codigo=producto.codigo,
                    producto_nombre=producto.nombre
                )
                db.add(item)
                print(f"   ✅ {producto.nombre}: {cantidad} x ${precio_unitario}")
            
            print()
        
        # Commit cambios
        db.commit()
        print(f"🎉 Items creados exitosamente para {len(pedidos_sin_items)} pedidos")
        
        # Verificar que los items se crearon
        for pedido in pedidos_sin_items:
            items = db.query(ItemPedido).filter(ItemPedido.pedido_id == pedido.id).all()
            print(f"   Pedido {pedido.numero_pedido}: {len(items)} items")
        
    except Exception as e:
        print(f"❌ Error creando items: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    print("🚀 Creando items de pedido...")
    crear_items_pedido()
    print("✅ Proceso completado!") 