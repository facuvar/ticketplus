from fastapi import APIRouter
from app.api.v1.endpoints import pedidos, recomendaciones, whatsapp, admin, carrito

# Importar todos los modelos para que SQLAlchemy los registre
from app.models.mayorista import Mayorista
from app.models.usuario import Usuario
from app.models.cliente import Cliente
from app.models.producto import Producto
from app.models.pedido import Pedido
from app.models.item_pedido import ItemPedido
from app.models.recomendacion import Recomendacion

api_router = APIRouter()

# Include all endpoint routers
api_router.include_router(pedidos.router, prefix="/pedidos", tags=["Pedidos"])
api_router.include_router(recomendaciones.router, prefix="/recomendaciones", tags=["Recomendaciones"])
api_router.include_router(whatsapp.router, prefix="/whatsapp", tags=["WhatsApp"])
api_router.include_router(admin.router, prefix="/admin", tags=["Admin"])
api_router.include_router(carrito.router, prefix="/carrito", tags=["Carrito"])

# Endpoint temporal para configurar Railway DB
@api_router.get("/setup-database")
async def setup_railway_database():
    """
    Endpoint temporal para configurar la base de datos en Railway
    Una vez configurada, este endpoint puede ser removido
    """
    try:
        from app.core.database import engine, SessionLocal
        from sqlalchemy import text, inspect
        
        print("🚀 CONFIGURANDO BASE DE DATOS EN RAILWAY")
        
        # Verificar qué tablas existen actualmente
        inspector = inspect(engine)
        tablas_existentes = inspector.get_table_names()
        print(f"📋 Tablas existentes antes: {tablas_existentes}")
        
        # Crear tablas
        from app.core.database import Base
        print("🔨 Creando tablas...")
        Base.metadata.create_all(bind=engine)
        
        # Verificar qué tablas se crearon
        inspector = inspect(engine)
        tablas_despues = inspector.get_table_names()
        print(f"📋 Tablas después de create_all: {tablas_despues}")
        
        # Usar SessionLocal en lugar de engine.connect()
        db = SessionLocal()
        
        try:
            # Verificar si el mayorista ya existe
            result = db.execute(text("SELECT COUNT(*) FROM mayoristas WHERE id = 4"))
            count = result.fetchone()[0]
            print(f"👤 Mayoristas con ID 4: {count}")
            
            if count == 0:
                print("➕ Creando mayorista...")
                # Mayorista ejemplo
                db.execute(text("""
                    INSERT INTO mayoristas (id, nombre, email, telefono, whatsapp_phone_number, 
                                          recomendaciones_activas, tiempo_espera_horas, 
                                          max_productos_recomendados, reglas_recomendacion, activo)
                    VALUES (4, 'Distribuidora Simón', 'simon@distribuidora.com', '+5491123456789', 
                            '5491123456789', true, 24, 3, 
                            '{"factores": ["historial", "popularidad", "margen"]}', true)
                """))
            
            # Cliente ejemplo
            result = db.execute(text("SELECT COUNT(*) FROM clientes WHERE id = 1"))
            count = result.fetchone()[0]
            print(f"👥 Clientes con ID 1: {count}")
            
            if count == 0:
                print("➕ Creando cliente...")
                db.execute(text("""
                    INSERT INTO clientes (id, gescom_cliente_id, nombre, email, telefono, 
                                        mayorista_id, whatsapp_numero, acepta_whatsapp, activo)
                    VALUES (1, 'CLI-001', 'Cliente Ejemplo', 'cliente@ejemplo.com', '+5491234567890',
                            4, '5491234567890', true, true)
                """))
            
            # Productos ejemplo
            productos = [
                (1, 'COCA-350', 'COCA-350', 'Coca Cola 350ml', 200.0, 100, 'Bebidas'),
                (2, 'PEPSI-350', 'PEPSI-350', 'Pepsi Cola 350ml', 190.0, 80, 'Bebidas'),
                (3, 'AGUA-500', 'AGUA-500', 'Agua Mineral 500ml', 120.0, 150, 'Bebidas'),
                (4, 'CHOC-100', 'CHOC-100', 'Chocolate Milka 100g', 280.0, 50, 'Golosinas'),
                (5, 'PAPAS-150', 'PAPAS-150', 'Papas Fritas Lays 150g', 250.0, 60, 'Snacks')
            ]
            
            for producto in productos:
                # Verificar si el producto ya existe
                result = db.execute(text("SELECT COUNT(*) FROM productos WHERE id = :id"), {'id': producto[0]})
                if result.fetchone()[0] == 0:
                    print(f"➕ Creando producto: {producto[3]}")
                    db.execute(text("""
                        INSERT INTO productos (id, codigo, gescom_producto_id, nombre, precio, 
                                             stock, categoria, mayorista_id, activo)
                        VALUES (:id, :codigo, :gescom_producto_id, :nombre, :precio, 
                                :stock, :categoria, 4, true)
                    """), {
                        'id': producto[0], 'codigo': producto[1], 'gescom_producto_id': producto[2],
                        'nombre': producto[3], 'precio': producto[4], 'stock': producto[5], 'categoria': producto[6]
                    })
            
            # Pedidos ejemplo con UPSELL
            result = db.execute(text("SELECT COUNT(*) FROM pedidos WHERE id = 1"))
            if result.fetchone()[0] == 0:
                print("➕ Creando pedido ORIGINAL...")
                db.execute(text("""
                    INSERT INTO pedidos (id, gescom_pedido_id, numero_pedido, fecha_pedido, tipo, 
                                       subtotal, total, estado, cliente_id, mayorista_id)
                    VALUES (1, 'SIM-141550', 'ORD-20250702-SIM-141550', '2025-07-02 14:15:50', 'ORIGINAL', 
                            590.0, 590.0, 'COMPLETADO', 1, 4)
                """))
            
            result = db.execute(text("SELECT COUNT(*) FROM pedidos WHERE id = 2"))
            if result.fetchone()[0] == 0:
                print("➕ Creando pedido UPSELL...")
                db.execute(text("""
                    INSERT INTO pedidos (id, gescom_pedido_id, numero_pedido, fecha_pedido, tipo, 
                                       subtotal, total, estado, codigo_referencia, pedido_original_id, 
                                       cliente_id, mayorista_id)
                    VALUES (2, 'SIM-141551', 'ORD-20250702-SIM-141551', '2025-07-02 15:30:00', 'UPSELL', 
                            360.0, 360.0, 'COMPLETADO', 'UP-001-ORD-20250702-SIM-141550', 1, 1, 4)
                """))
            
            # Items de pedidos
            items_pedidos = [
                (1, 1, 1, 2, 200.0, 400.0, 'COCA-350', 'Coca Cola 350ml'),
                (2, 1, 2, 1, 190.0, 190.0, 'PEPSI-350', 'Pepsi Cola 350ml'),
                (3, 2, 3, 3, 120.0, 360.0, 'AGUA-500', 'Agua Mineral 500ml'),
            ]
            
            for item in items_pedidos:
                result = db.execute(text("SELECT COUNT(*) FROM items_pedido WHERE id = :id"), {'id': item[0]})
                if result.fetchone()[0] == 0:
                    print(f"➕ Creando item pedido: {item[7]}")
                    db.execute(text("""
                        INSERT INTO items_pedido (id, pedido_id, producto_id, cantidad, precio_unitario, 
                                                subtotal, producto_codigo, producto_nombre)
                        VALUES (:id, :pedido_id, :producto_id, :cantidad, :precio_unitario, :subtotal,
                                :producto_codigo, :producto_nombre)
                    """), {
                        'id': item[0], 'pedido_id': item[1], 'producto_id': item[2], 'cantidad': item[3],
                        'precio_unitario': item[4], 'subtotal': item[5], 'producto_codigo': item[6], 
                        'producto_nombre': item[7]
                    })
            
            # Recomendaciones ejemplo
            recomendaciones = [
                (1, 1, 1, 4, 'MAS_VENDIDOS', 85.5, 'Producto popular en tu categoría', 'Coca Cola 350ml', 200.0),
                (2, 1, 2, 4, 'CATEGORIA_SIMILAR', 75.0, 'Bebida complementaria', 'Pepsi Cola 350ml', 190.0),
                (3, 2, 3, 4, 'HISTORICO_CLIENTE', 90.0, 'Te gusta esta categoría', 'Agua Mineral 500ml', 120.0),
            ]
            
            for rec in recomendaciones:
                result = db.execute(text("SELECT COUNT(*) FROM recomendaciones WHERE id = :id"), {'id': rec[0]})
                if result.fetchone()[0] == 0:
                    print(f"➕ Creando recomendación: {rec[7]}")
                    db.execute(text("""
                        INSERT INTO recomendaciones (id, pedido_id, producto_id, mayorista_id, tipo, 
                                                   score, razon, producto_nombre, producto_precio, 
                                                   fue_clickeada, fecha_generacion)
                        VALUES (:id, :pedido_id, :producto_id, :mayorista_id, :tipo, 
                                :score, :razon, :producto_nombre, :producto_precio,
                                true, '2025-07-02 16:00:00')
                    """), {
                        'id': rec[0], 'pedido_id': rec[1], 'producto_id': rec[2], 'mayorista_id': rec[3],
                        'tipo': rec[4], 'score': rec[5], 'razon': rec[6], 'producto_nombre': rec[7], 
                        'producto_precio': rec[8]
                    })
            
            db.commit()
            
            # Verificar qué se creó
            mayoristas = db.execute(text("SELECT COUNT(*) FROM mayoristas")).fetchone()[0]
            productos = db.execute(text("SELECT COUNT(*) FROM productos")).fetchone()[0]
            pedidos = db.execute(text("SELECT COUNT(*) FROM pedidos")).fetchone()[0]
            items = db.execute(text("SELECT COUNT(*) FROM items_pedido")).fetchone()[0]
            recomendaciones = db.execute(text("SELECT COUNT(*) FROM recomendaciones")).fetchone()[0]
            
            print("✅ BASE DE DATOS CONFIGURADA EXITOSAMENTE")
            print(f"📊 Registros: Mayoristas={mayoristas}, Productos={productos}, Pedidos={pedidos}, Items={items}, Recomendaciones={recomendaciones}")
            
            return {
                "success": True,
                "message": "✅ Base de datos configurada exitosamente",
                "data": {
                    "tablas_antes": tablas_existentes,
                    "tablas_despues": tablas_despues,
                    "mayoristas": mayoristas,
                    "productos": productos,
                    "pedidos": pedidos,
                    "items_pedido": items,
                    "recomendaciones": recomendaciones,
                    "dashboard_url": "/api/v1/admin/dashboard/4",
                    "carrito_url": "/carrito.html"
                }
            }
            
        finally:
            db.close()
        
    except Exception as e:
        import traceback
        error_details = traceback.format_exc()
        print(f"❌ ERROR: {str(e)}")
        print(f"🔍 DETALLES: {error_details}")
        return {
            "success": False,
            "message": f"❌ Error configurando base de datos: {str(e)}",
            "data": {
                "error_details": error_details
            }
        }

# Endpoint temporal de diagnóstico para debug
@api_router.get("/debug-dashboard/{mayorista_id}")
async def debug_dashboard_endpoints(mayorista_id: int):
    """
    Endpoint temporal para probar todas las secciones del dashboard
    """
    from app.core.database import get_db
    from fastapi import Depends
    from sqlalchemy.orm import Session
    import traceback
    
    def get_db_sync():
        from app.core.database import SessionLocal
        db = SessionLocal()
        try:
            return db
        finally:
            pass
    
    db = get_db_sync()
    resultados = {}
    
    # Test pedidos
    try:
        from app.api.v1.endpoints.admin import obtener_pedidos
        # No podemos llamar directamente la función async, simulamos
        from app.models.pedido import Pedido
        count_pedidos = db.query(Pedido).filter(Pedido.mayorista_id == mayorista_id).count()
        resultados["pedidos"] = {"status": "OK", "count": count_pedidos}
    except Exception as e:
        resultados["pedidos"] = {"status": "ERROR", "error": str(e)}
    
    # Test clientes  
    try:
        from app.models.cliente import Cliente
        count_clientes = db.query(Cliente).filter(Cliente.mayorista_id == mayorista_id).count()
        resultados["clientes"] = {"status": "OK", "count": count_clientes}
    except Exception as e:
        resultados["clientes"] = {"status": "ERROR", "error": str(e)}
    
    # Test recomendaciones
    try:
        from app.models.recomendacion import Recomendacion
        count_recs = db.query(Recomendacion).filter(Recomendacion.mayorista_id == mayorista_id).count()
        resultados["recomendaciones"] = {"status": "OK", "count": count_recs}
    except Exception as e:
        resultados["recomendaciones"] = {"status": "ERROR", "error": str(e)}
    
    # Test analytics (aquí puede estar el problema)
    try:
        from sqlalchemy import func
        from datetime import datetime, timedelta
        fecha_inicio = datetime.now() - timedelta(days=7)
        
        # Probar func.hour() que puede fallar en SQLite
        test_hour = db.query(func.hour(Recomendacion.fecha_generacion)).first()
        resultados["analytics_hour"] = {"status": "OK", "test": "func.hour() funciona"}
    except Exception as e:
        resultados["analytics_hour"] = {"status": "ERROR", "error": str(e)}
    
    db.close()
    
    return {
        "mayorista_id": mayorista_id,
        "tests": resultados,
        "mensaje": "🔍 Diagnóstico completo de endpoints del dashboard"
    } 