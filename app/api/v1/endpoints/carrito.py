from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.services.carrito_service import CarritoService
from app.schemas.recomendacion import RecomendacionParaCarrito
from pydantic import BaseModel
from typing import List
from decimal import Decimal
import os

router = APIRouter()
carrito_service = CarritoService()


class CarritoResponse(BaseModel):
    token: str
    pedido_original: dict
    cliente: dict
    mayorista: dict
    recomendaciones: List[RecomendacionParaCarrito]
    token_valido: bool
    expiracion: str


class AgregarProductoRequest(BaseModel):
    recomendacion_id: int
    cantidad: int


class ConfirmarPedidoRequest(BaseModel):
    productos: List[AgregarProductoRequest]
    observaciones: str = ""


@router.get("/{token}", response_class=HTMLResponse)
async def mostrar_carrito_web(token: str):
    """
    Mostrar página HTML del carrito (microcarrito público)
    """
    # Leer el archivo HTML
    html_path = os.path.join("frontend", "carrito.html")
    
    try:
        with open(html_path, "r", encoding="utf-8") as file:
            html_content = file.read()
        return HTMLResponse(content=html_content)
    except FileNotFoundError:
        # HTML inline simple si no existe el archivo
        return HTMLResponse(content=f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Carrito - Ticket+</title>
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <style>
                body {{ font-family: Arial, sans-serif; margin: 20px; background: #f5f5f5; }}
                .container {{ max-width: 400px; margin: 0 auto; background: white; padding: 20px; border-radius: 10px; }}
                .loading {{ text-align: center; padding: 40px; }}
            </style>
        </head>
        <body>
            <div class="container">
                <h1>🛒 Tu Carrito</h1>
                <div class="loading">Cargando...</div>
            </div>
            <script>
                fetch('/api/v1/carrito/{token}')
                    .then(r => r.json())
                    .then(data => {{
                        document.querySelector('.loading').innerHTML = 
                            '<pre>' + JSON.stringify(data, null, 2) + '</pre>';
                    }});
            </script>
        </body>
        </html>
        """)


@router.get("/{token}/data")
async def obtener_carrito_data(token: str, db: Session = Depends(get_db)):
    """
    Obtener datos del carrito en formato JSON
    """
    carrito = carrito_service.obtener_carrito_por_token(db, token)
    
    if not carrito:
        raise HTTPException(
            status_code=404, 
            detail="Token de carrito inválido o expirado"
        )
    
    return {
        "message": "Carrito obtenido exitosamente",
        "carrito": carrito
    }


@router.post("/{token}/agregar/{producto_id}")
async def agregar_producto_carrito(
    token: str, 
    producto_id: int, 
    cantidad: int = 1,
    db: Session = Depends(get_db)
):
    """
    Agregar producto al carrito (click en recomendación)
    """
    exito = carrito_service.agregar_producto_carrito(db, token, producto_id, cantidad)
    
    if not exito:
        raise HTTPException(
            status_code=400,
            detail="No se pudo agregar el producto al carrito"
        )
    
    return {
        "message": "Producto agregado exitosamente",
        "producto_id": producto_id,
        "cantidad": cantidad
    }


@router.post("/{token}/confirmar")
async def confirmar_pedido_carrito(
    token: str,
    request: ConfirmarPedidoRequest,
    db: Session = Depends(get_db)
):
    """
    Confirmar el pedido complementario con los productos seleccionados.
    """
    try:
        carrito_service = CarritoService(db)
        
        pedido_upsell = await carrito_service.confirmar_pedido(
            token,
            request.productos,
            request.observaciones
        )
        
        if not pedido_upsell:
            raise HTTPException(status_code=400, detail="No se pudo confirmar el pedido")
        
        return {
            "success": True,
            "message": "Pedido confirmado exitosamente",
            "pedido_id": pedido_upsell.id,
            "numero_pedido": pedido_upsell.numero_pedido,
            "total": float(pedido_upsell.total)
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al confirmar pedido: {str(e)}")


@router.get("/{token}/tracking")
async def obtener_tracking_click(
    token: str,
    recomendacion_id: int,
    db: Session = Depends(get_db)
):
    """
    Endpoint para trackear clicks en recomendaciones.
    Se llama cuando el usuario hace click en una recomendación.
    """
    try:
        carrito_service = CarritoService(db)
        
        await carrito_service.registrar_click_recomendacion(token, recomendacion_id)
        
        return {"success": True, "message": "Click registrado"}
        
    except Exception as e:
        # No devolver error para no romper la experiencia del usuario
        print(f"Error al registrar click: {str(e)}")
        return {"success": False}


@router.get("/public/branding/{mayorista_id}")
async def obtener_branding_publico(mayorista_id: int, db: Session = Depends(get_db)):
    """
    Obtener branding del mayorista para el carrito público
    """
    branding = carrito_service.obtener_branding_mayorista(db, mayorista_id)
    
    if not branding:
        raise HTTPException(
            status_code=404,
            detail="Mayorista no encontrado"
        )
    
    return {
        "message": "Branding obtenido exitosamente",
        "branding": branding
    } 