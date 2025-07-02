from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.schemas.pedido import PedidoNuevo, PedidoResponse, PedidoListResponse
from app.services.pedido_service import PedidoService
from app.services.gescom_service import GescomService
from app.services.recomendacion_service import RecomendacionService
from app.models.pedido import Pedido, TipoPedido, EstadoPedido
from app.models.item_pedido import ItemPedido
from app.models.cliente import Cliente
from app.models.mayorista import Mayorista
from app.models.recomendacion import Recomendacion
from pydantic import BaseModel
from typing import List
from datetime import datetime
import secrets

router = APIRouter()


class ProductoPedido(BaseModel):
    codigo: str
    nombre: str
    cantidad: int
    precio: float


class ClientePedido(BaseModel):
    gescom_id: str
    nombre: str
    email: str
    telefono: str


class PedidoNuevo(BaseModel):
    gescom_pedido_id: str
    mayorista_id: int
    cliente: ClientePedido
    productos: List[ProductoPedido]
    total: float
    direccion_envio: str


@router.post("/webhook/gescom/nuevo-pedido")
async def recibir_pedido_gescom(
    pedido_data: PedidoNuevo,
    db: Session = Depends(get_db)
):
    """
    🚀 WEBHOOK: Recibir pedido desde Gescom y generar carrito dinámico
    
    Simula el proceso completo:
    1. Recibir pedido desde sistema del mayorista
    2. Crear/actualizar cliente
    3. Crear pedido en BD
    4. Generar recomendaciones automáticamente
    5. Crear token único para carrito
    6. Simular envío de WhatsApp
    """
    
    try:
        print(f"🔔 NUEVO PEDIDO RECIBIDO: {pedido_data.gescom_pedido_id}")
        
        # 1. Verificar que el mayorista existe
        mayorista = db.query(Mayorista).filter(Mayorista.id == pedido_data.mayorista_id).first()
        if not mayorista:
            raise HTTPException(status_code=404, detail="Mayorista no encontrado")
        
        # 2. Crear o actualizar cliente
        cliente = db.query(Cliente).filter(
            Cliente.gescom_cliente_id == pedido_data.cliente.gescom_id
        ).first()
        
        if not cliente:
            print(f"👤 Creando nuevo cliente: {pedido_data.cliente.nombre}")
            cliente = Cliente(
                gescom_cliente_id=pedido_data.cliente.gescom_id,
                nombre=pedido_data.cliente.nombre,
                email=pedido_data.cliente.email,
                telefono=pedido_data.cliente.telefono,
                mayorista_id=pedido_data.mayorista_id,
                whatsapp_numero=pedido_data.cliente.telefono,
                acepta_whatsapp=True,
                activo=True,
                total_pedidos=1,
                ticket_promedio=pedido_data.total,
                fecha_ultimo_pedido=datetime.now()
            )
            db.add(cliente)
            db.flush()  # Para obtener el ID
        else:
            # Actualizar datos del cliente
            cliente.nombre = pedido_data.cliente.nombre
            cliente.email = pedido_data.cliente.email
            cliente.telefono = pedido_data.cliente.telefono
            cliente.total_pedidos += 1
            cliente.fecha_ultimo_pedido = datetime.now()
        
        # 3. Crear pedido
        token_carrito = secrets.token_urlsafe(32)
        
        pedido = Pedido(
            gescom_pedido_id=pedido_data.gescom_pedido_id,
            numero_pedido=f"ORD-{datetime.now().strftime('%Y%m%d')}-{pedido_data.gescom_pedido_id}",
            mayorista_id=pedido_data.mayorista_id,
            cliente_id=cliente.id,
            tipo=TipoPedido.ORIGINAL,
            estado=EstadoPedido.PROCESANDO,
            subtotal=pedido_data.total,
            total=pedido_data.total,
            direccion_envio=pedido_data.direccion_envio,
            recomendaciones_enviadas=False,
            token_carrito=token_carrito,
            token_expiracion=datetime.now().replace(hour=23, minute=59, second=59),  # Expira al final del día
            fecha_pedido=datetime.now()
        )
        db.add(pedido)
        db.flush()  # Para obtener el ID
        
        print(f"📦 Pedido creado: ID {pedido.id}, Token: {token_carrito[:10]}...")
        
        # 4. Crear items del pedido
        from app.models.producto import Producto
        
        for producto_data in pedido_data.productos:
            # Buscar producto existente por código o usar el primero disponible
            producto_existente = db.query(Producto).filter(
                Producto.codigo == producto_data.codigo
            ).first()
            
            if not producto_existente:
                # Si no existe, usar el primer producto disponible como placeholder
                producto_existente = db.query(Producto).first()
            
            item = ItemPedido(
                pedido_id=pedido.id,
                producto_id=producto_existente.id,
                cantidad=producto_data.cantidad,
                precio_unitario=producto_data.precio,
                subtotal=producto_data.cantidad * producto_data.precio,
                producto_codigo=producto_data.codigo,
                producto_nombre=producto_data.nombre
            )
            db.add(item)
        
        print(f"📝 {len(pedido_data.productos)} productos agregados al pedido")
        
        # 5. 🧠 GENERAR RECOMENDACIONES AUTOMÁTICAMENTE
        print("🧠 Iniciando motor de recomendaciones...")
        recomendacion_service = RecomendacionService(db)
        recomendaciones = await recomendacion_service.generar_recomendaciones(pedido.id)
        
        print(f"🎯 {len(recomendaciones)} recomendaciones generadas")
        
        # 6. Marcar recomendaciones como enviadas
        pedido.recomendaciones_enviadas = True
        pedido.fecha_envio_recomendaciones = datetime.now()
        
        # 7. Commit final
        db.commit()
        
        # 8. 📱 SIMULAR ENVÍO DE WHATSAPP
        whatsapp_message = generar_mensaje_whatsapp(
            cliente.nombre,
            pedido.numero_pedido,
            token_carrito,
            mayorista.nombre
        )
        
        print("📱 WHATSAPP ENVIADO:")
        print(whatsapp_message)
        
        # 9. Respuesta del webhook
        return {
            "status": "success",
            "message": "Pedido procesado y recomendaciones generadas",
            "pedido_id": pedido.id,
            "token_carrito": token_carrito,
            "carrito_url": f"http://localhost:8000/api/v1/carrito/{token_carrito}",
            "recomendaciones_generadas": len(recomendaciones),
            "whatsapp_enviado": True,
            "cliente": {
                "nombre": cliente.nombre,
                "es_nuevo": cliente.total_pedidos == 1
            }
        }
        
    except Exception as e:
        db.rollback()
        print(f"❌ Error procesando pedido: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error procesando pedido: {str(e)}")


@router.post("/simular-pedido-dinamico")
async def simular_pedido_dinamico(db: Session = Depends(get_db)):
    """
    🎬 DEMO: Simular un pedido completo con generación dinámica de carrito
    
    Este endpoint simula todo el flujo desde que un cliente hace un pedido
    hasta que recibe el WhatsApp con recomendaciones personalizadas.
    """
    
    # Datos de ejemplo de un pedido real
    pedido_ejemplo = PedidoNuevo(
        gescom_pedido_id=f"SIM-{datetime.now().strftime('%H%M%S')}",
        mayorista_id=4,  # Distribuidora Norte
        cliente=ClientePedido(
            gescom_id=f"CLI-{datetime.now().strftime('%H%M%S')}",
            nombre="Supermercado Los Alamos",
            email="gerente@losalamos.com",
            telefono="+5491156789012"
        ),
        productos=[
            ProductoPedido(
                codigo="ACE001",
                nombre="Aceite Girasol Natura 900ml",
                cantidad=3,
                precio=1250.00
            ),
            ProductoPedido(
                codigo="LEG001", 
                nombre="Lentejas Secas 500g",
                cantidad=2,
                precio=850.00
            ),
            ProductoPedido(
                codigo="ARR001",
                nombre="Arroz Largo Fino 1kg", 
                cantidad=4,
                precio=1100.00
            )
        ],
        total=8850.00,  # 3*1250 + 2*850 + 4*1100
        direccion_envio="Av. Los Alamos 456, Zona Norte"
    )
    
    return await recibir_pedido_gescom(pedido_ejemplo, db)


def generar_mensaje_whatsapp(nombre_cliente: str, numero_pedido: str, token_carrito: str, nombre_mayorista: str) -> str:
    """Generar mensaje de WhatsApp personalizado"""
    
    mensaje = f"""🛒 ¡Hola {nombre_cliente}!

Tu pedido {numero_pedido} está confirmado y en proceso.

🎯 ¿Te interesa agregar algo más?
Tenemos productos especiales seleccionados para vos:

🔗 Ver recomendaciones personalizadas:
http://localhost:8000/api/v1/carrito/{token_carrito}

✅ Entrega estimada: Mañana 9-12hs
📱 Consultas: Responde este mensaje

---
{nombre_mayorista}
Powered by Ticket+"""
    
    return mensaje


@router.get("/test-recomendaciones/{pedido_id}")
async def test_generar_recomendaciones(
    pedido_id: int,
    forzar: bool = False,
    db: Session = Depends(get_db)
):
    """🧪 TEST: Generar recomendaciones para un pedido existente"""
    
    recomendacion_service = RecomendacionService(db)
    
    if forzar:
        # Eliminar recomendaciones existentes
        db.query(Recomendacion).filter(Recomendacion.pedido_id == pedido_id).delete()
        db.commit()
    
    recomendaciones = await recomendacion_service.generar_recomendaciones(pedido_id, forzar)
    
    return {
        "pedido_id": pedido_id,
        "recomendaciones_generadas": len(recomendaciones),
        "recomendaciones": [
            {
                "id": r.id,
                "producto_nombre": r.producto_nombre,
                "precio": float(r.producto_precio),
                "score": r.score,
                "tipo": r.tipo.value,
                "razon": r.razon
            }
            for r in recomendaciones
        ]
    }


@router.post("/nuevo", response_model=dict)
async def crear_pedido_nuevo(
    pedido_data: PedidoNuevo,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):
    """
    Endpoint para recibir pedidos nuevos desde Gescom.
    Crea el pedido y programa el envío de recomendaciones.
    """
    try:
        pedido_service = PedidoService(db)
        
        # Crear el pedido
        pedido = await pedido_service.crear_pedido_desde_gescom(pedido_data)
        
        # Programar la generación de recomendaciones en background
        background_tasks.add_task(
            pedido_service.procesar_pedido_para_recomendaciones,
            pedido.id
        )
        
        return {
            "success": True,
            "message": "Pedido creado exitosamente",
            "pedido_id": pedido.id,
            "token_carrito": pedido.token_carrito
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al crear pedido: {str(e)}")


@router.get("/", response_model=List[PedidoListResponse])
async def listar_pedidos(
    mayorista_id: int,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """Listar pedidos de un mayorista"""
    try:
        pedido_service = PedidoService(db)
        pedidos = pedido_service.obtener_pedidos_mayorista(mayorista_id, skip, limit)
        return pedidos
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener pedidos: {str(e)}")


@router.get("/{pedido_id}", response_model=PedidoResponse)
async def obtener_pedido(
    pedido_id: int,
    db: Session = Depends(get_db)
):
    """Obtener detalles de un pedido específico"""
    try:
        pedido_service = PedidoService(db)
        pedido = pedido_service.obtener_pedido_por_id(pedido_id)
        
        if not pedido:
            raise HTTPException(status_code=404, detail="Pedido no encontrado")
            
        return pedido
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener pedido: {str(e)}")


@router.post("/sincronizar-gescom")
async def sincronizar_con_gescom(
    mayorista_id: int,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):
    """
    Sincronizar pedidos desde la base de datos de Gescom de un mayorista específico.
    Este endpoint será llamado periódicamente para detectar nuevos pedidos.
    """
    try:
        gescom_service = GescomService(db)
        
        # Ejecutar sincronización en background
        background_tasks.add_task(
            gescom_service.sincronizar_pedidos_mayorista,
            mayorista_id
        )
        
        return {
            "success": True,
            "message": f"Sincronización iniciada para mayorista {mayorista_id}"
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al iniciar sincronización: {str(e)}") 