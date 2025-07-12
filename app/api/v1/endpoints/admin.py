from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session
from pydantic import BaseModel
from app.core.database import get_db
import os
from sqlalchemy import func, and_, desc, case, cast, String
from datetime import datetime, timedelta

# Importar todos los modelos necesarios
from app.models.pedido import Pedido, EstadoPedido, TipoPedido
from app.models.item_pedido import ItemPedido
from app.models.recomendacion import Recomendacion
from app.models.mayorista import Mayorista
from app.models.cliente import Cliente
from app.models.producto import Producto

router = APIRouter()


class LoginRequest(BaseModel):
    email: str
    password: str


class LoginResponse(BaseModel):
    access_token: str
    token_type: str
    user_id: int
    mayorista_id: int


@router.get("/dashboard", response_class=HTMLResponse)
async def mostrar_dashboard():
    """
    Mostrar página HTML del dashboard admin
    """
    html_path = os.path.join("frontend", "dashboard.html")
    
    try:
        with open(html_path, "r", encoding="utf-8") as file:
            html_content = file.read()
        return HTMLResponse(content=html_content)
    except FileNotFoundError:
        return HTMLResponse(content="""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Dashboard - Ticket+</title>
            <style>body { font-family: Arial, sans-serif; background: #121212; color: white; padding: 20px; }</style>
        </head>
        <body>
            <h1>📊 Dashboard Ticket+</h1>
            <p>Dashboard en desarrollo...</p>
        </body>
        </html>
        """)


@router.post("/login", response_model=LoginResponse)
async def login(
    request: LoginRequest,
    db: Session = Depends(get_db)
):
    """
    Login para usuarios del admin panel.
    """
    try:
        # TODO: Implementar autenticación real
        # Por ahora devolvemos un token dummy para testing
        
        return LoginResponse(
            access_token="dummy-token-for-testing",
            token_type="bearer",
            user_id=1,
            mayorista_id=1
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error en login: {str(e)}")


@router.get("/me")
async def obtener_usuario_actual():
    """
    Obtener información del usuario autenticado.
    """
    try:
        # TODO: Implementar obtención de usuario desde token
        return {
            "id": 1,
            "email": "admin@example.com",
            "nombre": "Admin",
            "mayorista_id": 1,
            "es_admin": True
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener usuario: {str(e)}")


@router.get("/dashboard/{mayorista_id}")
async def obtener_dashboard(
    mayorista_id: int,
    db: Session = Depends(get_db)
):
    """
    Obtener datos del dashboard para un mayorista con datos reales de MySQL.
    """
    try:
        # Verificar que el mayorista existe
        mayorista = db.query(Mayorista).filter(Mayorista.id == mayorista_id).first()
        if not mayorista:
            raise HTTPException(status_code=404, detail="Mayorista no encontrado")
        
        # Fecha de hoy para filtros
        hoy = datetime.now().date()
        hace_30_dias = hoy - timedelta(days=30)
        
        # 1. Pedidos de hoy
        pedidos_hoy = db.query(func.count(Pedido.id)).filter(
            and_(
                Pedido.mayorista_id == mayorista_id,
                func.date(Pedido.fecha_pedido) == hoy
            )
        ).scalar() or 0
        
        # 2. Total de recomendaciones enviadas (últimos 30 días)
        recomendaciones_enviadas = db.query(func.count(Recomendacion.id)).filter(
            and_(
                Recomendacion.mayorista_id == mayorista_id,
                Recomendacion.fecha_generacion >= hace_30_dias
            )
        ).scalar() or 0
        
        # 3. Conversión de recomendaciones (% clickeadas)
        recomendaciones_clickeadas = db.query(func.count(Recomendacion.id)).filter(
            and_(
                Recomendacion.mayorista_id == mayorista_id,
                Recomendacion.fue_clickeada == True,
                Recomendacion.fecha_generacion >= hace_30_dias
            )
        ).scalar() or 0
        
        conversion_rate = (recomendaciones_clickeadas / recomendaciones_enviadas * 100) if recomendaciones_enviadas > 0 else 0
        
        # 4. Ticket promedio (últimos 30 días)
        ticket_promedio = db.query(func.avg(Pedido.total)).filter(
            and_(
                Pedido.mayorista_id == mayorista_id,
                Pedido.fecha_pedido >= hace_30_dias
            )
        ).scalar() or 0
        
        # 5. NUEVA MÉTRICA: Ingresos generados por Ticket+ (pedidos upsell)
        ingresos_ticket_plus = db.query(func.sum(Pedido.total)).filter(
            and_(
                Pedido.mayorista_id == mayorista_id,
                Pedido.tipo == TipoPedido.UPSELL,
                Pedido.fecha_pedido >= hace_30_dias
            )
        ).scalar() or 0
        
        # 6. Productos más recomendados
        productos_recomendados = db.query(
            Recomendacion.producto_nombre,
            func.count(Recomendacion.id).label('veces')
        ).filter(
            and_(
                Recomendacion.mayorista_id == mayorista_id,
                Recomendacion.fecha_generacion >= hace_30_dias
            )
        ).group_by(Recomendacion.producto_nombre).order_by(
            func.count(Recomendacion.id).desc()
        ).limit(5).all()
        
        productos_mas_recomendados = [
            {"nombre": prod.producto_nombre, "veces": prod.veces}
            for prod in productos_recomendados
        ]
        
        # 7. Gráficos: Pedidos e ingresos por día (últimos 7 días)
        graficos_data = []
        for i in range(7):
            fecha = hoy - timedelta(days=i)
            fecha_str = fecha.strftime('%Y-%m-%d')
            
            # Pedidos del día (usando LIKE para compatibilidad SQLite)
            pedidos_dia = db.query(func.count(Pedido.id)).filter(
                and_(
                    Pedido.mayorista_id == mayorista_id,
                    cast(Pedido.fecha_pedido, String).like(f'{fecha_str}%')
                )
            ).scalar() or 0
            
            # Ingresos del día por UPSELL
            ingresos_dia = db.query(func.sum(Pedido.total)).filter(
                and_(
                    Pedido.mayorista_id == mayorista_id,
                    Pedido.tipo == TipoPedido.UPSELL,
                    cast(Pedido.fecha_pedido, String).like(f'{fecha_str}%')
                )
            ).scalar() or 0
            
            graficos_data.append({
                "fecha": fecha.strftime("%d/%m"),
                "pedidos": pedidos_dia,
                "ingresos_ticket_plus": float(ingresos_dia)
            })
        
        # Invertir para que esté en orden cronológico
        graficos_data.reverse()
        
        return {
            "pedidos_hoy": pedidos_hoy,
            "recomendaciones_enviadas": recomendaciones_enviadas,
            "conversion_rate": round(conversion_rate, 1),
            "ticket_promedio": float(ticket_promedio),
            "ingresos_ticket_plus": float(ingresos_ticket_plus),  # NUEVA MÉTRICA
            "productos_mas_recomendados": productos_mas_recomendados,
            "graficos": {
                "pedidos_por_dia": [g["pedidos"] for g in graficos_data],
                "ingresos_por_dia": [g["ingresos_ticket_plus"] for g in graficos_data],
                "fechas": [g["fecha"] for g in graficos_data]
            },
            "mayorista": {
                "nombre": mayorista.nombre,
                "email": mayorista.email
            }
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener dashboard: {str(e)}")


@router.get("/pedidos/{mayorista_id}")
async def obtener_pedidos(
    mayorista_id: int,
    skip: int = 0,
    limit: int = 50,
    estado: str = None,
    db: Session = Depends(get_db)
):
    """📦 PEDIDOS: Obtener lista de pedidos del mayorista"""
    try:
        # Query más simple y directo
        query = db.query(Pedido).filter(Pedido.mayorista_id == mayorista_id)
        
        if estado:
            query = query.filter(Pedido.estado == estado)
        
        # Obtener pedidos sin complex order by por ahora
        pedidos = query.limit(limit).offset(skip).all()
        
        pedidos_data = []
        for pedido in pedidos:
            # Datos básicos del pedido sin joins complejos
            cliente_info = {"id": pedido.cliente_id, "nombre": "Cliente"}
            
            # Intentar obtener nombre del cliente de forma segura
            try:
                cliente = db.query(Cliente).filter(Cliente.id == pedido.cliente_id).first()
                if cliente and cliente.nombre:
                    cliente_info["nombre"] = cliente.nombre
            except:
                pass
            
            # Items count de forma más simple
            items_count = 0
            try:
                items_count = db.query(ItemPedido).filter(ItemPedido.pedido_id == pedido.id).count()
            except:
                pass
            
            pedidos_data.append({
                "id": pedido.id,
                "numero_pedido": pedido.numero_pedido or f"PED-{pedido.id}",
                "cliente": cliente_info,
                "tipo": pedido.tipo.value if pedido.tipo else "original",
                "estado": pedido.estado.value if pedido.estado else "pendiente",
                "total": float(pedido.total) if pedido.total else 0.0,
                "items_count": items_count,
                "fecha_pedido": pedido.fecha_pedido.strftime("%Y-%m-%d") if pedido.fecha_pedido else "Sin fecha",
                "recomendaciones_enviadas": pedido.recomendaciones_enviadas or False,
                "token_carrito": pedido.token_carrito or f"token-{pedido.id}",
                "referencia": {"icono": "📦" if not pedido.tipo or pedido.tipo.value == "original" else "🎯"}
            })
        
        # Estadísticas más simples
        total_pedidos = 0
        pendientes = 0
        
        try:
            total_pedidos = db.query(Pedido).filter(Pedido.mayorista_id == mayorista_id).count()
            
            # Solo contar pendientes de forma básica
            if hasattr(Pedido, 'estado'):
                pendientes = db.query(Pedido).filter(
                    Pedido.mayorista_id == mayorista_id,
                    Pedido.estado == "PENDIENTE"
                ).count()
        except Exception as e:
            print(f"Error en estadísticas: {e}")
            pass

        return {
            "pedidos": pedidos_data,
            "total": total_pedidos,
            "pagina": skip // limit + 1 if limit > 0 else 1,
            "limite": limit,
            "estadisticas": {
                "pendientes": pendientes,
                "procesando": 0,  # Simplificado por ahora
                "entregados": total_pedidos - pendientes if total_pedidos > pendientes else 0
            }
        }
        
    except Exception as e:
        print(f"Error completo en pedidos: {str(e)}")
        # En caso de error, devolver estructura básica
        return {
            "pedidos": [],
            "total": 0,
            "pagina": 1,
            "limite": limit,
            "estadisticas": {
                "pendientes": 0,
                "procesando": 0,
                "entregados": 0
            },
            "error_debug": str(e)
        }


@router.get("/recomendaciones/{mayorista_id}")
async def obtener_recomendaciones(
    mayorista_id: int,
    skip: int = 0,
    limit: int = 50,
    db: Session = Depends(get_db)
):
    """🎯 RECOMENDACIONES: Obtener recomendaciones generadas"""
    try:
        recomendaciones = db.query(Recomendacion).filter(
            Recomendacion.mayorista_id == mayorista_id
        ).order_by(desc(Recomendacion.fecha_generacion)).offset(skip).limit(limit).all()
        
        recomendaciones_data = []
        for rec in recomendaciones:
            # Obtener pedido relacionado de forma segura
            pedido = None
            cliente_nombre = "Desconocido"
            pedido_numero = "N/A"
            
            try:
                pedido = db.query(Pedido).filter(Pedido.id == rec.pedido_id).first()
                if pedido:
                    pedido_numero = pedido.numero_pedido
                    cliente = db.query(Cliente).filter(Cliente.id == pedido.cliente_id).first()
                    if cliente:
                        cliente_nombre = cliente.nombre
            except:
                pass  # Si hay error, usar valores por defecto
            
            recomendaciones_data.append({
                "id": rec.id,
                "producto_nombre": rec.producto_nombre or "Producto sin nombre",
                "precio": float(rec.producto_precio) if rec.producto_precio else 0.0,
                "tipo": rec.tipo.value if rec.tipo else "desconocido",
                "estado": rec.estado.value if rec.estado else "generada",
                "score": float(rec.score) if rec.score else 0.0,
                "razon": rec.razon or "Sin razón especificada",
                "fue_clickeada": rec.fue_clickeada or False,
                "fecha_generacion": rec.fecha_generacion.isoformat() if rec.fecha_generacion else None,
                "fecha_click": rec.fecha_click.isoformat() if rec.fecha_click else None,
                "pedido": {
                    "numero": pedido_numero,
                    "cliente": cliente_nombre
                }
            })
        
        # Estadísticas simplificadas
        total_recomendaciones = db.query(func.count(Recomendacion.id)).filter(
            Recomendacion.mayorista_id == mayorista_id
        ).scalar() or 0
        
        clickeadas = db.query(func.count(Recomendacion.id)).filter(
            and_(
                Recomendacion.mayorista_id == mayorista_id,
                Recomendacion.fue_clickeada == True
            )
        ).scalar() or 0
        
        conversion_rate = round((clickeadas / total_recomendaciones * 100) if total_recomendaciones > 0 else 0, 2)
        
        return {
            "recomendaciones": recomendaciones_data,
            "total": total_recomendaciones,
            "clickeadas": clickeadas,
            "conversion_rate": conversion_rate
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error obteniendo recomendaciones: {str(e)}")


@router.get("/whatsapp/{mayorista_id}")
async def obtener_estadisticas_whatsapp(
    mayorista_id: int,
    db: Session = Depends(get_db)
):
    """📱 WHATSAPP: Estadísticas de mensajes enviados"""
    try:
        # Pedidos con recomendaciones enviadas
        mensajes_enviados = db.query(func.count(Pedido.id)).filter(
            and_(
                Pedido.mayorista_id == mayorista_id,
                Pedido.recomendaciones_enviadas == True
            )
        ).scalar() or 0
        
        # Pedidos con click en WhatsApp
        clicks_whatsapp = db.query(func.count(Pedido.id)).filter(
            and_(
                Pedido.mayorista_id == mayorista_id,
                Pedido.click_whatsapp == True
            )
        ).scalar() or 0
        
        # Últimos mensajes enviados
        ultimos_mensajes = db.query(Pedido).filter(
            and_(
                Pedido.mayorista_id == mayorista_id,
                Pedido.recomendaciones_enviadas == True
            )
        ).order_by(desc(Pedido.fecha_envio_recomendaciones)).limit(10).all()
        
        mensajes_data = []
        for pedido in ultimos_mensajes:
            cliente = db.query(Cliente).filter(Cliente.id == pedido.cliente_id).first()
            mensajes_data.append({
                "pedido_numero": pedido.numero_pedido,
                "cliente": cliente.nombre if cliente else "Desconocido",
                "telefono": cliente.whatsapp_numero if cliente else None,
                "fecha_envio": pedido.fecha_envio_recomendaciones.isoformat() if pedido.fecha_envio_recomendaciones else None,
                "click_realizado": pedido.click_whatsapp,
                "fecha_click": pedido.fecha_click_whatsapp.isoformat() if pedido.fecha_click_whatsapp else None
            })
        
        return {
            "mensajes_enviados": mensajes_enviados,
            "clicks_whatsapp": clicks_whatsapp,
            "tasa_apertura": round((clicks_whatsapp / mensajes_enviados * 100) if mensajes_enviados > 0 else 0, 2),
            "ultimos_mensajes": mensajes_data
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error obteniendo estadísticas WhatsApp: {str(e)}")


@router.get("/clientes/{mayorista_id}")
async def obtener_clientes(
    mayorista_id: int,
    skip: int = 0,
    limit: int = 50,
    db: Session = Depends(get_db)
):
    """👥 CLIENTES: Lista de clientes del mayorista"""
    try:
        clientes = db.query(Cliente).filter(
            Cliente.mayorista_id == mayorista_id
        ).order_by(desc(Cliente.fecha_ultimo_pedido)).offset(skip).limit(limit).all()
        
        clientes_data = []
        for cliente in clientes:
            # Contar pedidos del cliente de forma segura
            total_pedidos = 0
            ultimo_pedido_info = {"numero": None, "total": 0}
            
            try:
                total_pedidos = db.query(func.count(Pedido.id)).filter(
                    Pedido.cliente_id == cliente.id
                ).scalar() or 0
                
                # Último pedido
                ultimo_pedido = db.query(Pedido).filter(
                    Pedido.cliente_id == cliente.id
                ).order_by(desc(Pedido.fecha_pedido)).first()
                
                if ultimo_pedido:
                    ultimo_pedido_info = {
                        "numero": ultimo_pedido.numero_pedido,
                        "total": float(ultimo_pedido.total) if ultimo_pedido.total else 0
                    }
            except:
                pass
            
            clientes_data.append({
                "id": cliente.id,
                "nombre": cliente.nombre or "Sin nombre",
                "email": cliente.email or "",
                "telefono": cliente.telefono or "",
                "whatsapp_numero": cliente.whatsapp_numero or "",
                "acepta_whatsapp": cliente.acepta_whatsapp or False,
                "total_pedidos": total_pedidos,
                "ticket_promedio": float(cliente.ticket_promedio) if cliente.ticket_promedio else 0,
                "fecha_ultimo_pedido": cliente.fecha_ultimo_pedido.isoformat() if cliente.fecha_ultimo_pedido else None,
                "ultimo_pedido": ultimo_pedido_info,
                "activo": cliente.activo or False
            })
        
        # Estadísticas simplificadas
        total_clientes = db.query(func.count(Cliente.id)).filter(
            Cliente.mayorista_id == mayorista_id
        ).scalar() or 0
        
        clientes_activos = 0
        try:
            clientes_activos = db.query(func.count(Cliente.id)).filter(
                and_(Cliente.mayorista_id == mayorista_id, Cliente.activo == True)
            ).scalar() or 0
        except:
            pass
        
        return {
            "clientes": clientes_data,
            "total": total_clientes,
            "activos": clientes_activos,
            "pagina": skip // limit + 1,
            "limite": limit
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error obteniendo clientes: {str(e)}")


@router.get("/analytics/{mayorista_id}")
async def obtener_analytics(
    mayorista_id: int,
    dias: int = 30,
    db: Session = Depends(get_db)
):
    """📈 ANALYTICS: Análisis avanzado de datos"""
    try:
        fecha_inicio = datetime.now() - timedelta(days=dias)
        
        # Análisis de conversión por día (simplificado para SQLite)
        conversion_por_dia = []
        for i in range(min(dias, 7)):  # Limitamos a 7 días para mejor rendimiento
            fecha = fecha_inicio + timedelta(days=i)
            fecha_str = fecha.strftime('%Y-%m-%d')
            
            # Usar LIKE para comparar fechas (compatible con SQLite)
            recomendaciones_dia = db.query(func.count(Recomendacion.id)).filter(
                and_(
                    Recomendacion.mayorista_id == mayorista_id,
                    cast(Recomendacion.fecha_generacion, String).like(f'{fecha_str}%')
                )
            ).scalar() or 0
            
            clicks_dia = db.query(func.count(Recomendacion.id)).filter(
                and_(
                    Recomendacion.mayorista_id == mayorista_id,
                    Recomendacion.fue_clickeada == True,
                    cast(Recomendacion.fecha_generacion, String).like(f'{fecha_str}%')
                )
            ).scalar() or 0
            
            conversion_por_dia.append({
                "fecha": fecha.strftime("%d/%m"),
                "recomendaciones": recomendaciones_dia,
                "clicks": clicks_dia,
                "conversion": round((clicks_dia / recomendaciones_dia * 100) if recomendaciones_dia > 0 else 0, 2)
            })
        
        # Top productos recomendados
        top_productos = db.query(
            Recomendacion.producto_nombre,
            func.count(Recomendacion.id).label('total'),
            func.sum(case((Recomendacion.fue_clickeada == True, 1), else_=0)).label('clicks')
        ).filter(
            Recomendacion.mayorista_id == mayorista_id
        ).group_by(Recomendacion.producto_nombre).order_by(desc('total')).limit(10).all()
        
        productos_data = []
        for producto in top_productos:
            conversion = round((producto.clicks / producto.total * 100) if producto.total > 0 else 0, 2)
            productos_data.append({
                "nombre": producto.producto_nombre,
                "recomendaciones": producto.total,
                "clicks": producto.clicks,
                "conversion": conversion
            })
        
        # Recomendaciones por hora simplificado (usar conteos básicos)
        total_recomendaciones = db.query(func.count(Recomendacion.id)).filter(
            Recomendacion.mayorista_id == mayorista_id
        ).scalar() or 0
        
        total_clicks = db.query(func.count(Recomendacion.id)).filter(
            and_(
                Recomendacion.mayorista_id == mayorista_id,
                Recomendacion.fue_clickeada == True
            )
        ).scalar() or 0
        
        return {
            "periodo_dias": min(dias, 7),
            "fecha_inicio": fecha_inicio.isoformat(),
            "fecha_fin": datetime.now().isoformat(),
            "conversion_por_dia": conversion_por_dia,
            "top_productos": productos_data,
            "recomendaciones_por_hora": {}, # Simplificado para compatibilidad
            "resumen": {
                "total_recomendaciones": total_recomendaciones,
                "total_clicks": total_clicks,
                "conversion_promedio": round((total_clicks / total_recomendaciones * 100) if total_recomendaciones > 0 else 0, 2)
            }
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error obteniendo analytics: {str(e)}")


@router.get("/configuracion/{mayorista_id}")
async def obtener_configuracion(
    mayorista_id: int,
    db: Session = Depends(get_db)
):
    """⚙️ CONFIGURACIÓN: Configuración del mayorista"""
    try:
        mayorista = db.query(Mayorista).filter(Mayorista.id == mayorista_id).first()
        
        if not mayorista:
            raise HTTPException(status_code=404, detail="Mayorista no encontrado")
        
        return {
            "mayorista": {
                "id": mayorista.id,
                "nombre": mayorista.nombre,
                "email": mayorista.email,
                "telefono": mayorista.telefono,
                "logo_url": mayorista.logo_url,
                "color_primario": mayorista.color_primario,
                "color_secundario": mayorista.color_secundario,
                "recomendaciones_activas": mayorista.recomendaciones_activas,
                "tiempo_espera_horas": mayorista.tiempo_espera_horas,
                "max_productos_recomendados": mayorista.max_productos_recomendados,
                "activo": mayorista.activo
            },
            "gescom": {
                "host": mayorista.gescom_db_host,
                "puerto": mayorista.gescom_db_port,
                "base_datos": mayorista.gescom_db_name,
                "usuario": mayorista.gescom_db_user,
                "password": "***" if mayorista.gescom_db_password else None
            },
            "whatsapp": {
                "api_key": "***" if mayorista.whatsapp_api_key else None,
                "phone_number": mayorista.whatsapp_phone_number
            }
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error obteniendo configuración: {str(e)}")


@router.put("/configuracion/{mayorista_id}")
async def actualizar_configuracion(
    mayorista_id: int,
    configuracion: dict,
    db: Session = Depends(get_db)
):
    """⚙️ CONFIGURACIÓN: Actualizar configuración del mayorista"""
    try:
        mayorista = db.query(Mayorista).filter(Mayorista.id == mayorista_id).first()
        
        if not mayorista:
            raise HTTPException(status_code=404, detail="Mayorista no encontrado")
        
        # Actualizar campos permitidos
        campos_permitidos = [
            'nombre', 'email', 'telefono', 'color_primario', 'color_secundario',
            'recomendaciones_activas', 'tiempo_espera_horas', 'max_productos_recomendados'
        ]
        
        for campo in campos_permitidos:
            if campo in configuracion:
                setattr(mayorista, campo, configuracion[campo])
        
        mayorista.fecha_actualizacion = datetime.now()
        db.commit()
        
        return {"message": "Configuración actualizada exitosamente"}
        
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error actualizando configuración: {str(e)}")


@router.post("/pedidos/{mayorista_id}/crear-upsell")
async def crear_pedido_upsell(
    mayorista_id: int,
    pedido_original_id: int,
    datos_upsell: dict,
    db: Session = Depends(get_db)
):
    """🎯 CREAR UPSELL: Crear un pedido UPSELL desde un pedido original"""
    try:
        from app.services.pedido_service import PedidoService
        
        pedido_service = PedidoService(db)
        nuevo_upsell = pedido_service.crear_pedido_upsell(pedido_original_id, datos_upsell)
        
        return {
            "success": True,
            "pedido_upsell": {
                "id": nuevo_upsell.id,
                "numero_pedido": nuevo_upsell.numero_pedido,
                "codigo_referencia": nuevo_upsell.codigo_referencia,
                "total": float(nuevo_upsell.total),
                "fecha_pedido": nuevo_upsell.fecha_pedido.isoformat()
            },
            "mensaje": f"Pedido UPSELL {nuevo_upsell.numero_pedido} creado exitosamente"
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error creando pedido UPSELL: {str(e)}")


@router.get("/pedidos/{mayorista_id}/referencias")
async def obtener_pedidos_con_referencias(
    mayorista_id: int,
    db: Session = Depends(get_db)
):
    """📋 REFERENCIAS: Obtener pedidos con información completa de referencias UPSELL"""
    try:
        from app.services.pedido_service import PedidoService
        
        pedido_service = PedidoService(db)
        pedidos_con_referencias = pedido_service.obtener_pedidos_con_referencias(mayorista_id)
        
        return {
            "pedidos": pedidos_con_referencias,
            "total": len(pedidos_con_referencias)
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error obteniendo referencias: {str(e)}") 