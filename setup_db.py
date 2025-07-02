"""
Script para configurar base de datos en Railway
Se ejecuta DENTRO de Railway después del deploy
"""
import os
from app.core.database import engine
from sqlalchemy import text

def setup_database():
    """Configurar base de datos en Railway"""
    print("🚀 CONFIGURANDO BASE DE DATOS EN RAILWAY")
    print("=" * 50)
    
    try:
        # Detectar entorno
        from app.core.config import settings
        print(f"🌐 Entorno Railway detectado")
        print(f"   Host: {settings.DATABASE_HOST}")
        print(f"   Base de datos: {settings.DATABASE_NAME}")
        
        # Crear tablas
        print("\n📋 1. Creando tablas...")
        from app.models.base import Base
        Base.metadata.create_all(bind=engine)
        print("   ✅ Tablas creadas")
        
        # Insertar datos básicos
        print("\n📦 2. Insertando datos básicos...")
        
        with engine.connect() as connection:
            # Mayorista ejemplo
            connection.execute(text("""
                INSERT IGNORE INTO mayoristas (id, nombre, email, telefono, whatsapp_phone_number, 
                                              recomendaciones_activas, tiempo_espera_horas, 
                                              max_productos_recomendados, reglas_recomendacion, activo)
                VALUES (4, 'Distribuidora Simón', 'simon@distribuidora.com', '+5491123456789', 
                        '5491123456789', true, 24, 3, 
                        '{"factores": ["historial", "popularidad", "margen"]}', true)
            """))
            
            # Productos ejemplo
            productos = [
                (1, 'COCA-350', 'Coca Cola 350ml', 150.0, 200.0, 100, 'Bebidas'),
                (2, 'PEPSI-350', 'Pepsi Cola 350ml', 140.0, 190.0, 80, 'Bebidas'),
                (3, 'AGUA-500', 'Agua Mineral 500ml', 80.0, 120.0, 150, 'Bebidas')
            ]
            
            for producto in productos:
                connection.execute(text("""
                    INSERT IGNORE INTO productos (id, codigo, nombre, precio_compra, precio_venta, 
                                                 stock, categoria, mayorista_id, activo)
                    VALUES (:id, :codigo, :nombre, :precio_compra, :precio_venta, 
                            :stock, :categoria, 4, true)
                """), {
                    'id': producto[0], 'codigo': producto[1], 'nombre': producto[2],
                    'precio_compra': producto[3], 'precio_venta': producto[4],
                    'stock': producto[5], 'categoria': producto[6]
                })
            
            # Pedidos ejemplo con UPSELL
            connection.execute(text("""
                INSERT IGNORE INTO pedidos (id, numero_pedido, fecha_pedido, tipo, total, 
                                           estado, mayorista_id)
                VALUES (1, 'ORD-20250702-SIM-141550', '2025-07-02', 'ORIGINAL', 2500.0, 
                        'COMPLETADO', 4)
            """))
            
            connection.execute(text("""
                INSERT IGNORE INTO pedidos (id, numero_pedido, fecha_pedido, tipo, total, 
                                           estado, codigo_referencia, pedido_original_id, mayorista_id)
                VALUES (2, 'ORD-20250702-SIM-141551', '2025-07-02', 'UPSELL', 850.0, 
                        'COMPLETADO', 'UP-001-ORD-20250702-SIM-141550', 1, 4)
            """))
            
            connection.commit()
        
        print("   ✅ Datos insertados")
        
        # Verificar
        print("\n🔍 3. Verificando...")
        with engine.connect() as connection:
            result = connection.execute(text("SELECT COUNT(*) FROM mayoristas"))
            print(f"   👥 Mayoristas: {result.fetchone()[0]}")
            
            result = connection.execute(text("SELECT COUNT(*) FROM productos"))
            print(f"   📦 Productos: {result.fetchone()[0]}")
            
            result = connection.execute(text("SELECT COUNT(*) FROM pedidos"))
            print(f"   🛒 Pedidos: {result.fetchone()[0]}")
        
        print(f"\n✅ BASE DE DATOS CONFIGURADA")
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    setup_database() 