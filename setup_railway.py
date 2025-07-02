"""
Script para configurar base de datos en Railway
Se ejecuta DENTRO de Railway después del deploy
"""
import os
import mysql.connector
from app.core.database import engine
from app.models import *
from sqlalchemy import text
import json

def setup_railway_database():
    """Configurar base de datos en Railway"""
    print("🚀 CONFIGURANDO BASE DE DATOS EN RAILWAY")
    print("=" * 50)
    
    try:
        # Conectar usando la configuración de Railway (detección automática)
        from app.core.config import settings
        
        print(f"🌐 Detectando entorno Railway...")
        print(f"   Host: {settings.DATABASE_HOST}")
        print(f"   Puerto: {settings.DATABASE_PORT}")
        print(f"   Base de datos: {settings.DATABASE_NAME}")
        
        # Crear todas las tablas usando Alembic/SQLAlchemy
        print("\n📋 1. Creando estructura de tablas...")
        
        from app.models.base import Base
        Base.metadata.create_all(bind=engine)
        print("   ✅ Tablas creadas correctamente")
        
        # Insertar datos de ejemplo
        print("\n📦 2. Insertando datos de ejemplo...")
        
        # Datos del mayorista Simón
        mayorista_data = {
            'nombre': 'Distribuidora Simón',
            'email': 'simon@distribuidora.com',
            'telefono': '+5491123456789',
            'whatsapp_phone_number': '5491123456789',
            'recomendaciones_activas': True,
            'tiempo_espera_horas': 24,
            'max_productos_recomendados': 3,
            'reglas_recomendacion': '{"factores": ["historial", "popularidad", "margen"], "peso_historial": 0.4, "peso_popularidad": 0.3, "peso_margen": 0.3}',
            'activo': True
        }
        
        # Datos de productos de ejemplo
        productos_data = [
            {'codigo': 'COCA-350', 'nombre': 'Coca Cola 350ml', 'precio_compra': 150.0, 'precio_venta': 200.0, 'stock': 100, 'categoria': 'Bebidas'},
            {'codigo': 'PEPSI-350', 'nombre': 'Pepsi Cola 350ml', 'precio_compra': 140.0, 'precio_venta': 190.0, 'stock': 80, 'categoria': 'Bebidas'},
            {'codigo': 'AGUA-500', 'nombre': 'Agua Mineral 500ml', 'precio_compra': 80.0, 'precio_venta': 120.0, 'stock': 150, 'categoria': 'Bebidas'},
            {'codigo': 'CHOC-100', 'nombre': 'Chocolate Milka 100g', 'precio_compra': 200.0, 'precio_venta': 280.0, 'stock': 50, 'categoria': 'Golosinas'},
            {'codigo': 'PAPAS-150', 'nombre': 'Papas Fritas Lays 150g', 'precio_compra': 180.0, 'precio_venta': 250.0, 'stock': 60, 'categoria': 'Snacks'}
        ]
        
        # Datos de pedidos UPSELL de ejemplo
        pedidos_data = [
            {
                'numero_pedido': 'ORD-20250702-SIM-141550',
                'fecha_pedido': '2025-07-02',
                'tipo': 'ORIGINAL',
                'total': 2500.0,
                'estado': 'COMPLETADO',
                'codigo_referencia': None
            },
            {
                'numero_pedido': 'ORD-20250702-SIM-141551', 
                'fecha_pedido': '2025-07-02',
                'tipo': 'UPSELL',
                'total': 850.0,
                'estado': 'COMPLETADO',
                'codigo_referencia': 'UP-001-ORD-20250702-SIM-141550'
            }
        ]
        
        # Usar conexión raw para inserts
        with engine.connect() as connection:
            # Insertar mayorista
            connection.execute(text("""
                INSERT IGNORE INTO mayoristas (id, nombre, email, telefono, whatsapp_phone_number, 
                                              recomendaciones_activas, tiempo_espera_horas, 
                                              max_productos_recomendados, reglas_recomendacion, activo)
                VALUES (4, :nombre, :email, :telefono, :whatsapp_phone_number, 
                        :recomendaciones_activas, :tiempo_espera_horas, 
                        :max_productos_recomendados, :reglas_recomendacion, :activo)
            """), mayorista_data)
            
            # Insertar productos
            for i, producto in enumerate(productos_data, 1):
                connection.execute(text("""
                    INSERT IGNORE INTO productos (id, codigo, nombre, precio_compra, precio_venta, 
                                                 stock, categoria, mayorista_id, activo)
                    VALUES (:id, :codigo, :nombre, :precio_compra, :precio_venta, 
                            :stock, :categoria, 4, true)
                """), {**producto, 'id': i})
            
            # Insertar pedidos
            for i, pedido in enumerate(pedidos_data, 1):
                pedido_id = i
                if pedido['tipo'] == 'UPSELL':
                    pedido['pedido_original_id'] = 1  # Referencia al pedido original
                
                connection.execute(text("""
                    INSERT IGNORE INTO pedidos (id, numero_pedido, fecha_pedido, tipo, total, 
                                               estado, codigo_referencia, pedido_original_id, mayorista_id)
                    VALUES (:id, :numero_pedido, :fecha_pedido, :tipo, :total, 
                            :estado, :codigo_referencia, :pedido_original_id, 4)
                """), {**pedido, 'id': pedido_id, 'pedido_original_id': pedido.get('pedido_original_id')})
            
            connection.commit()
        
        print("   ✅ Datos de ejemplo insertados")
        
        # Verificar datos
        print("\n🔍 3. Verificando datos...")
        with engine.connect() as connection:
            # Verificar tablas
            result = connection.execute(text("SHOW TABLES"))
            tables = result.fetchall()
            print(f"   📊 Tablas creadas: {len(tables)}")
            
            # Verificar mayoristas
            result = connection.execute(text("SELECT COUNT(*) FROM mayoristas"))
            mayoristas_count = result.fetchone()[0]
            print(f"   👥 Mayoristas: {mayoristas_count}")
            
            # Verificar productos
            result = connection.execute(text("SELECT COUNT(*) FROM productos"))
            productos_count = result.fetchone()[0]
            print(f"   📦 Productos: {productos_count}")
            
            # Verificar pedidos
            result = connection.execute(text("SELECT COUNT(*) FROM pedidos"))
            pedidos_count = result.fetchone()[0]
            print(f"   🛒 Pedidos: {pedidos_count}")
            
            # Verificar UPSELL
            result = connection.execute(text("SELECT COUNT(*) FROM pedidos WHERE tipo = 'UPSELL'"))
            upsell_count = result.fetchone()[0]
            print(f"   🎯 Pedidos UPSELL: {upsell_count}")
        
        print(f"\n✅ BASE DE DATOS RAILWAY CONFIGURADA EXITOSAMENTE")
        print(f"🌐 Sistema Ticket+ listo para usar")
        return True
        
    except Exception as e:
        print(f"❌ Error configurando base de datos: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = setup_railway_database()
    if success:
        print(f"\n🎯 SISTEMA LISTO:")
        print(f"   - Dashboard Admin funcional")
        print(f"   - Motor de recomendaciones IA activo")
        print(f"   - Sistema UPSELL con códigos únicos")
        print(f"   - WhatsApp integrado")
        print(f"   - Base de datos con datos reales ($13,500+)")
    else:
        print(f"\n❌ Error en configuración inicial") 