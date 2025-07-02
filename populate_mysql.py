"""
Script para poblar la base de datos MySQL con datos de prueba
"""
from app.core.database import SessionLocal, engine
from app.models import *  # Importar todos los modelos
from app.models.pedido import TipoPedido, EstadoPedido
from app.models.recomendacion import TipoRecomendacion, EstadoRecomendacion
from datetime import datetime, timedelta
import secrets

def create_sample_data():
    """Crear datos de prueba en MySQL"""
    db = SessionLocal()
    
    try:
        print("🏗️ Creando datos de prueba en MySQL...")
        
        # 1. Crear Mayoristas
        mayorista1 = Mayorista(
            nombre="Distribuidora Norte",
            email="admin@distribuidoranorte.com",
            telefono="+5491234567890",
            gescom_db_host="localhost",
            gescom_db_port=3306,
            gescom_db_name="gescom_norte",
            gescom_db_user="gescom_user",
            gescom_db_password="gescom_pass",
            whatsapp_api_key="sk-1234567890abcdef",
            whatsapp_phone_number="+5491234567890",
            logo_url="https://via.placeholder.com/150x50?text=Norte",
            color_primario="#4CAF50",
            color_secundario="#45a049",
            recomendaciones_activas=True,
            tiempo_espera_horas=24,
            max_productos_recomendados=5,
            reglas_recomendacion="mas_vendidos,historico_cliente",
            activo=True
        )
        
        mayorista2 = Mayorista(
            nombre="Mayorista Sur",
            email="contacto@mayoristasur.com",
            telefono="+5497654321098",
            gescom_db_host="localhost",
            gescom_db_port=3306,
            gescom_db_name="gescom_sur",
            gescom_db_user="gescom_user",
            gescom_db_password="gescom_pass",
            whatsapp_api_key="sk-abcdef1234567890",
            whatsapp_phone_number="+5497654321098",
            logo_url="https://via.placeholder.com/150x50?text=Sur",
            color_primario="#2196F3",
            color_secundario="#1976D2",
            recomendaciones_activas=True,
            tiempo_espera_horas=48,
            max_productos_recomendados=3,
            reglas_recomendacion="categoria_similar,manual",
            activo=True
        )
        
        db.add_all([mayorista1, mayorista2])
        db.commit()
        
        # 2. Crear Usuarios
        usuario1 = Usuario(
            email="admin@distribuidoranorte.com",
            nombre="Admin Norte",
            mayorista_id=mayorista1.id,
            hashed_password="$2b$12$example_hash",  # En producción usar hash real
            activo=True,
            es_admin=True
        )
        
        usuario2 = Usuario(
            email="admin@mayoristasur.com",
            nombre="Admin Sur", 
            mayorista_id=mayorista2.id,
            hashed_password="$2b$12$example_hash",
            activo=True,
            es_admin=True
        )
        
        db.add_all([usuario1, usuario2])
        db.commit()
        
        # 3. Crear Clientes
        cliente1 = Cliente(
            gescom_cliente_id="CLI001",
            nombre="Almacén San Martín",
            email="almacen@sanmartin.com",
            telefono="+5491111111111",
            direccion="Av. San Martín 1234, Buenos Aires",
            mayorista_id=mayorista1.id,
            whatsapp_numero="+5491111111111",
            acepta_whatsapp=True,
            activo=True,
            fecha_ultimo_pedido=datetime.now() - timedelta(days=3),
            total_pedidos=15,
            ticket_promedio=1250.50
        )
        
        cliente2 = Cliente(
            gescom_cliente_id="CLI002",
            nombre="Supermercado El Barrio",
            email="compras@elbarrio.com",
            telefono="+5492222222222",
            direccion="Calle Falsa 456, Córdoba",
            mayorista_id=mayorista1.id,
            whatsapp_numero="+5492222222222",
            acepta_whatsapp=True,
            activo=True,
            fecha_ultimo_pedido=datetime.now() - timedelta(days=1),
            total_pedidos=32,
            ticket_promedio=2100.75
        )
        
        cliente3 = Cliente(
            gescom_cliente_id="CLI003",
            nombre="Kiosco Central",
            email="kiosco@central.com",
            telefono="+5493333333333",
            direccion="Plaza Central 789, Rosario",
            mayorista_id=mayorista2.id,
            whatsapp_numero="+5493333333333",
            acepta_whatsapp=True,
            activo=True,
            fecha_ultimo_pedido=datetime.now() - timedelta(days=5),
            total_pedidos=8,
            ticket_promedio=850.25
        )
        
        db.add_all([cliente1, cliente2, cliente3])
        db.commit()
        
        # 4. Crear Productos
        productos = [
            # Productos de Mayorista Norte
            Producto(
                gescom_producto_id="PROD001",
                codigo="ARR001",
                nombre="Arroz Gallo 1kg",
                precio=850.00,
                mayorista_id=mayorista1.id,
                activo=True
            ),
            Producto(
                gescom_producto_id="PROD002", 
                codigo="FID001",
                nombre="Fideos Matarazzo 500g",
                precio=450.00,
                mayorista_id=mayorista1.id,
                activo=True
            ),
            Producto(
                gescom_producto_id="PROD003",
                codigo="ACE001",
                nombre="Aceite Natura 900ml", 
                precio=1250.00,
                mayorista_id=mayorista1.id,
                activo=True
            ),
            Producto(
                gescom_producto_id="PROD004",
                codigo="LEC001",
                nombre="Leche La Serenísima 1L",
                precio=650.00,
                mayorista_id=mayorista1.id,
                activo=True
            ),
            Producto(
                gescom_producto_id="PROD005",
                codigo="PAN001",
                nombre="Pan Lactal Bimbo",
                precio=420.00,
                mayorista_id=mayorista1.id,
                activo=True
            ),
            Producto(
                gescom_producto_id="PROD006",
                codigo="YOG001",
                nombre="Yogur Ser Natural 900g",
                precio=890.00,
                mayorista_id=mayorista1.id,
                activo=True
            ),
            Producto(
                gescom_producto_id="PROD007",
                codigo="QUE001",
                nombre="Queso Cremoso Casancrem 300g",
                precio=1350.00,
                mayorista_id=mayorista1.id,
                activo=True
            ),
            Producto(
                gescom_producto_id="PROD008",
                codigo="AZU001",
                nombre="Azúcar Ledesma 1kg",
                precio=780.00,
                mayorista_id=mayorista1.id,
                activo=True
            ),
            # Productos de Mayorista Sur
            Producto(
                gescom_producto_id="PROD009",
                codigo="CAF001",
                nombre="Café La Virginia 500g",
                precio=2200.00,
                mayorista_id=mayorista2.id,
                activo=True
            ),
            Producto(
                gescom_producto_id="PROD010",
                codigo="GAL001",
                nombre="Galletitas Oreo 118g",
                precio=950.00,
                mayorista_id=mayorista2.id,
                activo=True
            )
        ]
        
        db.add_all(productos)
        db.commit()
        
        # 5. Crear Pedido con Token de Carrito
        token_carrito = secrets.token_urlsafe(32)
        
        pedido1 = Pedido(
            gescom_pedido_id="PED001",
            numero_pedido="ORD-2025-001",
            mayorista_id=mayorista1.id,
            cliente_id=cliente1.id,
            tipo=TipoPedido.ORIGINAL,
            estado=EstadoPedido.ENTREGADO,
            subtotal=1300.00,
            descuento=0.00,
            impuestos=236.70,
            total=1536.70,
            observaciones="Pedido de prueba",
            direccion_envio="Av. San Martín 1234, Buenos Aires",
            recomendaciones_enviadas=True,
            fecha_envio_recomendaciones=datetime.now() - timedelta(hours=2),
            token_carrito=token_carrito,
            token_expiracion=datetime.now() + timedelta(hours=46),  # 46h restantes
            click_whatsapp=False,
            conversion_upsell=False,
            monto_upsell=0.00,
            fecha_pedido=datetime.now() - timedelta(days=1)
        )
        
        db.add(pedido1)
        db.commit()
        
        # 6. Crear Items del Pedido
        items = [
            ItemPedido(
                pedido_id=pedido1.id,
                producto_id=productos[0].id,  # Arroz
                cantidad=1,
                precio_unitario=850.00,
                descuento=0.00,
                subtotal=850.00,
                producto_codigo="ARR001",
                producto_nombre="Arroz Gallo 1kg"
            ),
            ItemPedido(
                pedido_id=pedido1.id,
                producto_id=productos[1].id,  # Fideos
                cantidad=1,
                precio_unitario=450.00,
                descuento=0.00,
                subtotal=450.00,
                producto_codigo="FID001",
                producto_nombre="Fideos Matarazzo 500g"
            )
        ]
        
        db.add_all(items)
        db.commit()
        
        # 7. Crear Recomendaciones
        recomendaciones = [
            Recomendacion(
                pedido_id=pedido1.id,
                producto_id=productos[2].id,  # Aceite
                mayorista_id=mayorista1.id,
                tipo=TipoRecomendacion.MAS_VENDIDOS,
                estado=EstadoRecomendacion.ENVIADA,
                orden=1,
                score=98.5,
                razon="Producto más vendido con arroz y fideos",
                producto_nombre="Aceite Natura 900ml",
                producto_precio=1250.00,
                producto_imagen_url=None,
                fecha_generacion=datetime.now() - timedelta(hours=2),
                fecha_envio=datetime.now() - timedelta(hours=2)
            ),
            Recomendacion(
                pedido_id=pedido1.id,
                producto_id=productos[3].id,  # Leche
                mayorista_id=mayorista1.id,
                tipo=TipoRecomendacion.MAS_VENDIDOS,
                estado=EstadoRecomendacion.ENVIADA,
                orden=2,
                score=95.0,
                razon="Excelente para acompañar tus comidas",
                producto_nombre="Leche La Serenísima 1L",
                producto_precio=650.00,
                producto_imagen_url=None,
                fecha_generacion=datetime.now() - timedelta(hours=2),
                fecha_envio=datetime.now() - timedelta(hours=2)
            ),
            Recomendacion(
                pedido_id=pedido1.id,
                producto_id=productos[4].id,  # Pan
                mayorista_id=mayorista1.id,
                tipo=TipoRecomendacion.MAS_VENDIDOS,
                estado=EstadoRecomendacion.ENVIADA,
                orden=3,
                score=90.0,
                razon="Perfecto para el desayuno",
                producto_nombre="Pan Lactal Bimbo",
                producto_precio=420.00,
                producto_imagen_url=None,
                fecha_generacion=datetime.now() - timedelta(hours=2),
                fecha_envio=datetime.now() - timedelta(hours=2)
            ),
            Recomendacion(
                pedido_id=pedido1.id,
                producto_id=productos[5].id,  # Yogur
                mayorista_id=mayorista1.id,
                tipo=TipoRecomendacion.MAS_VENDIDOS,
                estado=EstadoRecomendacion.ENVIADA,
                orden=4,
                score=88.0,
                razon="Producto más vendido este mes",
                producto_nombre="Yogur Ser Natural 900g",
                producto_precio=890.00,
                producto_imagen_url=None,
                fecha_generacion=datetime.now() - timedelta(hours=2),
                fecha_envio=datetime.now() - timedelta(hours=2)
            ),
            Recomendacion(
                pedido_id=pedido1.id,
                producto_id=productos[6].id,  # Queso
                mayorista_id=mayorista1.id,
                tipo=TipoRecomendacion.MAS_VENDIDOS,
                estado=EstadoRecomendacion.ENVIADA,
                orden=5,
                score=85.0,
                razon="Ideal para sandwich y comidas",
                producto_nombre="Queso Cremoso Casancrem 300g",
                producto_precio=1350.00,
                producto_imagen_url=None,
                fecha_generacion=datetime.now() - timedelta(hours=2),
                fecha_envio=datetime.now() - timedelta(hours=2)
            )
        ]
        
        db.add_all(recomendaciones)
        db.commit()
        
        print("✅ Datos de prueba creados exitosamente!")
        print(f"🔗 Token de carrito activo: {token_carrito}")
        print(f"🏪 Mayoristas: {len([mayorista1, mayorista2])}")
        print(f"👥 Usuarios: {len([usuario1, usuario2])}")
        print(f"🛒 Clientes: {len([cliente1, cliente2, cliente3])}")
        print(f"📦 Productos: {len(productos)}")
        print(f"📋 Pedidos: 1")
        print(f"🎯 Recomendaciones: {len(recomendaciones)}")
        
        return token_carrito
        
    except Exception as e:
        print(f"❌ Error creando datos: {e}")
        db.rollback()
        raise
    finally:
        db.close()

if __name__ == "__main__":
    print("🚀 Iniciando población de MySQL...")
    token = create_sample_data()
    print(f"\n🎉 ¡Listo! Usa este token para probar el carrito:")
    print(f"http://localhost:8000/api/v1/carrito/{token}") 