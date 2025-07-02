from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.services.whatsapp_service import WhatsAppService
from pydantic import BaseModel
from typing import Optional

router = APIRouter()


class EnviarWhatsAppRequest(BaseModel):
    pedido_id: int
    mensaje_personalizado: Optional[str] = None


class TestWhatsAppRequest(BaseModel):
    mayorista_id: int
    numero_telefono: str
    mensaje: str


@router.post("/enviar")
async def enviar_mensaje_recomendaciones(
    request: EnviarWhatsAppRequest,
    db: Session = Depends(get_db)
):
    """
    Enviar mensaje de WhatsApp con recomendaciones para un pedido específico.
    """
    try:
        whatsapp_service = WhatsAppService(db)
        
        resultado = await whatsapp_service.enviar_recomendaciones_pedido(
            request.pedido_id,
            mensaje_personalizado=request.mensaje_personalizado
        )
        
        return {
            "success": True,
            "message": "Mensaje enviado exitosamente",
            "whatsapp_id": resultado.get("whatsapp_id"),
            "url_carrito": resultado.get("url_carrito")
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al enviar WhatsApp: {str(e)}")


@router.post("/test")
async def enviar_whatsapp_test(
    request: TestWhatsAppRequest,
    db: Session = Depends(get_db)
):
    """
    Enviar mensaje de prueba de WhatsApp.
    Solo para testing y configuración.
    """
    try:
        whatsapp_service = WhatsAppService(db)
        
        resultado = await whatsapp_service.enviar_mensaje_test(
            request.mayorista_id,
            request.numero_telefono,
            request.mensaje
        )
        
        return {
            "success": True,
            "message": "Mensaje de prueba enviado",
            "whatsapp_id": resultado.get("whatsapp_id")
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al enviar WhatsApp de prueba: {str(e)}")


@router.get("/webhooks/status")
async def webhook_estado_mensaje(
    whatsapp_id: str,
    estado: str,
    db: Session = Depends(get_db)
):
    """
    Webhook para recibir actualizaciones del estado de mensajes de WhatsApp.
    """
    try:
        whatsapp_service = WhatsAppService(db)
        
        await whatsapp_service.actualizar_estado_mensaje(whatsapp_id, estado)
        
        return {"success": True, "message": "Estado actualizado"}
        
    except Exception as e:
        # En webhooks, mejor no devolver error 500 para evitar reintentos innecesarios
        print(f"Error en webhook WhatsApp: {str(e)}")
        return {"success": False, "error": str(e)}


@router.get("/stats/{mayorista_id}")
async def obtener_estadisticas_whatsapp(
    mayorista_id: int,
    dias: int = 30,
    db: Session = Depends(get_db)
):
    """
    Obtener estadísticas de envíos de WhatsApp para un mayorista.
    """
    try:
        whatsapp_service = WhatsAppService(db)
        
        stats = await whatsapp_service.obtener_estadisticas_mayorista(mayorista_id, dias)
        
        return stats
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener estadísticas: {str(e)}")


@router.post("/procesar-pendientes")
async def procesar_mensajes_pendientes(
    mayorista_id: Optional[int] = None,
    db: Session = Depends(get_db)
):
    """
    Procesar mensajes de WhatsApp pendientes de envío.
    Si no se especifica mayorista_id, procesa todos.
    """
    try:
        whatsapp_service = WhatsAppService(db)
        
        procesados = await whatsapp_service.procesar_mensajes_pendientes(mayorista_id)
        
        return {
            "success": True,
            "message": f"Se procesaron {procesados} mensajes pendientes"
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al procesar mensajes pendientes: {str(e)}") 