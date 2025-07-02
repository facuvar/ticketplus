from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.schemas.recomendacion import RecomendacionesRequest, RecomendacionesResponse
from app.services.recomendacion_service import RecomendacionService

router = APIRouter()


@router.get("/{pedido_id}", response_model=RecomendacionesResponse)
async def obtener_recomendaciones(
    pedido_id: int,
    db: Session = Depends(get_db)
):
    """
    Obtener recomendaciones para un pedido específico.
    Si no existen, las genera automáticamente.
    """
    try:
        recomendacion_service = RecomendacionService(db)
        
        # Verificar si el pedido existe
        pedido = recomendacion_service.obtener_pedido(pedido_id)
        if not pedido:
            raise HTTPException(status_code=404, detail="Pedido no encontrado")
        
        # Obtener o generar recomendaciones
        recomendaciones = await recomendacion_service.obtener_o_generar_recomendaciones(pedido_id)
        
        return RecomendacionesResponse(
            pedido_id=pedido_id,
            total_recomendaciones=len(recomendaciones),
            recomendaciones=recomendaciones,
            token_carrito=pedido.token_carrito,
            url_carrito=f"/carrito/{pedido.token_carrito}" if pedido.token_carrito else None
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener recomendaciones: {str(e)}")


@router.post("/generar", response_model=RecomendacionesResponse)
async def generar_recomendaciones(
    request: RecomendacionesRequest,
    db: Session = Depends(get_db)
):
    """
    Generar nuevas recomendaciones para un pedido.
    Permite forzar la regeneración si ya existen.
    """
    try:
        recomendacion_service = RecomendacionService(db)
        
        # Verificar si el pedido existe
        pedido = recomendacion_service.obtener_pedido(request.pedido_id)
        if not pedido:
            raise HTTPException(status_code=404, detail="Pedido no encontrado")
        
        # Generar recomendaciones
        recomendaciones = await recomendacion_service.generar_recomendaciones(
            request.pedido_id,
            forzar_regeneracion=request.forzar_regeneracion
        )
        
        return RecomendacionesResponse(
            pedido_id=request.pedido_id,
            total_recomendaciones=len(recomendaciones),
            recomendaciones=recomendaciones,
            token_carrito=pedido.token_carrito,
            url_carrito=f"/carrito/{pedido.token_carrito}" if pedido.token_carrito else None
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al generar recomendaciones: {str(e)}")


@router.post("/{recomendacion_id}/click")
async def registrar_click_recomendacion(
    recomendacion_id: int,
    db: Session = Depends(get_db)
):
    """
    Registrar que una recomendación fue clickeada.
    """
    try:
        recomendacion_service = RecomendacionService(db)
        
        success = await recomendacion_service.registrar_click(recomendacion_id)
        
        if not success:
            raise HTTPException(status_code=404, detail="Recomendación no encontrada")
        
        return {"success": True, "message": "Click registrado exitosamente"}
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al registrar click: {str(e)}")


@router.get("/stats/{mayorista_id}")
async def obtener_estadisticas_recomendaciones(
    mayorista_id: int,
    dias: int = 30,
    db: Session = Depends(get_db)
):
    """
    Obtener estadísticas de recomendaciones para un mayorista.
    """
    try:
        recomendacion_service = RecomendacionService(db)
        
        stats = await recomendacion_service.obtener_estadisticas_mayorista(mayorista_id, dias)
        
        return stats
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener estadísticas: {str(e)}") 