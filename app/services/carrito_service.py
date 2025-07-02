from sqlalchemy.orm import Session
from datetime import datetime
from app.models.pedido import Pedido
from app.models.recomendacion import Recomendacion
from app.models.mayorista import Mayorista
from app.models.producto import Producto
from typing import Optional, Dict, Any, List


class CarritoService:
    
    def obtener_carrito_por_token(self, db: Session, token: str) -> Optional[Dict[str, Any]]:
        """
        Obtener carrito por token con datos reales de la BD
        """
        # Buscar pedido por token
        pedido = db.query(Pedido).filter(
            Pedido.token_carrito == token,
            Pedido.token_expiracion > datetime.now()
        ).first()
        
        if not pedido:
            return None
        
        # Obtener mayorista para branding
        mayorista = db.query(Mayorista).filter(Mayorista.id == pedido.mayorista_id).first()
        
        # Obtener cliente del pedido
        from app.models.cliente import Cliente
        cliente = db.query(Cliente).filter(Cliente.id == pedido.cliente_id).first()
        
        # Obtener items del pedido
        from app.models.item_pedido import ItemPedido
        items_pedido = db.query(ItemPedido).filter(ItemPedido.pedido_id == pedido.id).all()
        
        # Obtener recomendaciones del pedido
        recomendaciones = db.query(Recomendacion).filter(
            Recomendacion.pedido_id == pedido.id
        ).order_by(Recomendacion.orden).all()
        
        # Formatear recomendaciones
        productos_recomendados = []
        for rec in recomendaciones:
            productos_recomendados.append({
                "id": rec.producto_id,
                "nombre": rec.producto_nombre,
                "precio": float(rec.producto_precio),
                "imagen_url": rec.producto_imagen_url or "https://via.placeholder.com/200",
                "razon": rec.razon,
                "score": float(rec.score)
            })
        
        return {
            "pedido_id": pedido.id,
            "numero_pedido": pedido.numero_pedido,
            "cliente": {
                "nombre": cliente.nombre if cliente else "Cliente",
                "email": cliente.email if cliente else "cliente@email.com"
            },
            "mayorista": {
                "nombre": mayorista.nombre,
                "logo_url": mayorista.logo_url or "https://via.placeholder.com/150x50?text=Logo",
                "color_primario": mayorista.color_primario or "#007bff",
                "color_secundario": mayorista.color_secundario or "#6c757d"
            },
            "productos_originales": [
                {
                    "nombre": item.producto_nombre,
                    "cantidad": item.cantidad,
                    "precio": float(item.precio_unitario),
                    "subtotal": float(item.subtotal)
                }
                for item in items_pedido
            ],
            "productos_recomendados": productos_recomendados,
            "total_original": float(pedido.total),
            "token_expiracion": pedido.token_expiracion.isoformat(),
            "tiempo_restante_horas": int((pedido.token_expiracion - datetime.now()).total_seconds() / 3600)
        }
    
    def obtener_branding_mayorista(self, db: Session, mayorista_id: int) -> Optional[Dict[str, Any]]:
        """
        Obtener información de branding del mayorista
        """
        mayorista = db.query(Mayorista).filter(Mayorista.id == mayorista_id).first()
        
        if not mayorista:
            return None
        
        return {
            "nombre": mayorista.nombre,
            "logo_url": mayorista.logo_url or "https://via.placeholder.com/150x50?text=Logo",
            "color_primario": mayorista.color_primario or "#007bff",
            "color_secundario": mayorista.color_secundario or "#6c757d",
            "telefono": mayorista.telefono,
            "email": mayorista.email
        }
    
    def agregar_producto_carrito(self, db: Session, token: str, producto_id: int, cantidad: int = 1) -> bool:
        """
        Agregar producto al carrito (simular click en recomendación)
        """
        # Buscar pedido por token
        pedido = db.query(Pedido).filter(
            Pedido.token_carrito == token,
            Pedido.token_expiracion > datetime.now()
        ).first()
        
        if not pedido:
            return False
        
        # Buscar la recomendación y marcarla como clickeada
        recomendacion = db.query(Recomendacion).filter(
            Recomendacion.pedido_id == pedido.id,
            Recomendacion.producto_id == producto_id
        ).first()
        
        if recomendacion:
            recomendacion.fue_clickeada = True
            recomendacion.fecha_click = datetime.now()
            # Aquí podrías agregar el producto al pedido como upsell
            db.commit()
            return True
        
        return False
    
    async def agregar_producto(self, token: str, recomendacion_id: int, cantidad: int):
        """Agregar producto al carrito"""
        # TODO: Implementar lógica real
        return {"total": 0}
    
    async def confirmar_pedido(self, token: str, productos: List, observaciones: str):
        """Confirmar pedido complementario"""
        # TODO: Implementar lógica real
        return None
    
    async def registrar_click_recomendacion(self, token: str, recomendacion_id: int):
        """Registrar click en recomendación"""
        # TODO: Implementar lógica real
        pass 