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
        from app.core.database import engine
        from sqlalchemy import text
        
        print("🚀 CONFIGURANDO BASE DE DATOS EN RAILWAY")
        
        # Crear tablas
        from app.core.database import Base
        Base.metadata.create_all(bind=engine)
        
        # Insertar datos básicos usando sintaxis compatible
        with engine.connect() as connection:
            # Verificar si el mayorista ya existe
            result = connection.execute(text("SELECT COUNT(*) FROM mayoristas WHERE id = 4"))
            if result.fetchone()[0] == 0:
                # Mayorista ejemplo
                connection.execute(text("""
                    INSERT INTO mayoristas (id, nombre, email, telefono, whatsapp_phone_number, 
                                          recomendaciones_activas, tiempo_espera_horas, 
                                          max_productos_recomendados, reglas_recomendacion, activo)
                    VALUES (4, 'Distribuidora Simón', 'simon@distribuidora.com', '+5491123456789', 
                            '5491123456789', true, 24, 3, 
                            '{"factores": ["historial", "popularidad", "margen"]}', true)
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
                result = connection.execute(text("SELECT COUNT(*) FROM productos WHERE id = :id"), {'id': producto[0]})
                if result.fetchone()[0] == 0:
                    connection.execute(text("""
                        INSERT INTO productos (id, gescom_producto_id, codigo, nombre, precio, 
                                             stock, categoria, mayorista_id, activo)
                        VALUES (:id, :gescom_producto_id, :codigo, :nombre, :precio, 
                                :stock, :categoria, 4, true)
                    """), {
                        'id': producto[0], 'gescom_producto_id': producto[1], 'codigo': producto[2], 
                        'nombre': producto[3], 'precio': producto[4], 'stock': producto[5], 
                        'categoria': producto[6]
                    })
            
            # Pedidos ejemplo con UPSELL
            result = connection.execute(text("SELECT COUNT(*) FROM pedidos WHERE id = 1"))
            if result.fetchone()[0] == 0:
                connection.execute(text("""
                    INSERT INTO pedidos (id, gescom_pedido_id, numero_pedido, fecha_pedido, tipo, total, 
                                       estado, mayorista_id)
                    VALUES (1, 'SIM-141550', 'ORD-20250702-SIM-141550', '2025-07-02', 'ORIGINAL', 590.0, 
                            'COMPLETADO', 4)
                """))
            
            result = connection.execute(text("SELECT COUNT(*) FROM pedidos WHERE id = 2"))
            if result.fetchone()[0] == 0:
                connection.execute(text("""
                    INSERT INTO pedidos (id, gescom_pedido_id, numero_pedido, fecha_pedido, tipo, total, 
                                       estado, codigo_referencia, pedido_original_id, mayorista_id)
                    VALUES (2, 'SIM-141551', 'ORD-20250702-SIM-141551', '2025-07-02', 'UPSELL', 360.0, 
                            'COMPLETADO', 'UP-001-ORD-20250702-SIM-141550', 1, 4)
                """))
            
            # Items de pedidos
            items_pedidos = [
                (1, 1, 1, 2, 200.0, 400.0, 'COCA-350', 'Coca Cola 350ml'),  # Pedido 1, Producto 1 (Coca), cantidad 2
                (2, 1, 2, 1, 190.0, 190.0, 'PEPSI-350', 'Pepsi Cola 350ml'),  # Pedido 1, Producto 2 (Pepsi), cantidad 1  
                (3, 2, 3, 3, 120.0, 360.0, 'AGUA-500', 'Agua Mineral 500ml'),  # Pedido 2 (UPSELL), Producto 3 (Agua), cantidad 3
            ]
            
            for item in items_pedidos:
                result = connection.execute(text("SELECT COUNT(*) FROM items_pedido WHERE id = :id"), {'id': item[0]})
                if result.fetchone()[0] == 0:
                    connection.execute(text("""
                        INSERT INTO items_pedido (id, pedido_id, producto_id, cantidad, precio_unitario, 
                                                 subtotal, producto_codigo, producto_nombre)
                        VALUES (:id, :pedido_id, :producto_id, :cantidad, :precio_unitario, 
                                :subtotal, :producto_codigo, :producto_nombre)
                    """), {
                        'id': item[0], 'pedido_id': item[1], 'producto_id': item[2],
                        'cantidad': item[3], 'precio_unitario': item[4], 'subtotal': item[5],
                        'producto_codigo': item[6], 'producto_nombre': item[7]
                    })
            
            # Recomendaciones de ejemplo
            result = connection.execute(text("SELECT COUNT(*) FROM recomendaciones WHERE id = 1"))
            if result.fetchone()[0] == 0:
                connection.execute(text("""
                    INSERT INTO recomendaciones (id, mayorista_id, cliente_id, producto_nombre, 
                                               motivo, confianza, fecha_generacion, fue_clickeada)
                    VALUES (1, 4, 'CLI-001', 'Coca Cola 350ml', 
                            'Producto popular en tu categoría', 85.5, '2025-07-02', true)
                """))
            
            connection.commit()
        
        # Verificar datos
        with engine.connect() as connection:
            result = connection.execute(text("SELECT COUNT(*) FROM mayoristas"))
            mayoristas = result.fetchone()[0]
            
            result = connection.execute(text("SELECT COUNT(*) FROM productos"))
            productos = result.fetchone()[0]
            
            result = connection.execute(text("SELECT COUNT(*) FROM pedidos"))
            pedidos = result.fetchone()[0]
            
            result = connection.execute(text("SELECT COUNT(*) FROM items_pedido"))
            items = result.fetchone()[0]
        
        return {
            "success": True,
            "message": "✅ Base de datos configurada exitosamente",
            "data": {
                "mayoristas": mayoristas,
                "productos": productos,
                "pedidos": pedidos,
                "items_pedido": items,
                "dashboard_url": "/api/v1/admin/dashboard/4",
                "carrito_url": "/carrito.html"
            }
        }
        
    except Exception as e:
        return {
            "success": False,
            "message": f"❌ Error configurando base de datos: {str(e)}",
            "data": None
        } 