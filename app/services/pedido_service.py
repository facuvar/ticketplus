from sqlalchemy.orm import Session
from sqlalchemy import func
from app.schemas.pedido import PedidoNuevo
from app.models.pedido import Pedido, TipoPedido
from datetime import datetime


class PedidoService:
    def __init__(self, db: Session):
        self.db = db
    
    async def crear_pedido_desde_gescom(self, pedido_data: PedidoNuevo):
        """Crear pedido desde datos de Gescom"""
        # TODO: Implementar lógica real
        return {"id": 1, "token_carrito": "dummy-token"}
    
    async def procesar_pedido_para_recomendaciones(self, pedido_id: int):
        """Procesar pedido para generar recomendaciones"""
        # TODO: Implementar lógica real
        pass
    
    def obtener_pedidos_mayorista(self, mayorista_id: int, skip: int, limit: int):
        """Obtener pedidos de un mayorista"""
        # TODO: Implementar lógica real
        return []
    
    def obtener_pedido_por_id(self, pedido_id: int):
        """Obtener pedido por ID"""
        # TODO: Implementar lógica real
        return None
    
    def generar_codigo_upsell(self, pedido_original: Pedido) -> str:
        """
        Genera un código único para pedidos UPSELL
        Formato: UP-001-ORD-20250702-SIM-141550
        """
        # Contar cuántos UPSELL ya existen para este pedido original
        count_upsell = self.db.query(func.count(Pedido.id)).filter(
            Pedido.pedido_original_id == pedido_original.id,
            Pedido.tipo == TipoPedido.UPSELL
        ).scalar() or 0
        
        # Siguiente número de UPSELL
        siguiente_numero = count_upsell + 1
        
        # Formatear: UP-001-ORD-20250702-SIM-141550
        codigo_upsell = f"UP-{siguiente_numero:03d}-{pedido_original.numero_pedido}"
        
        return codigo_upsell
    
    def crear_pedido_upsell(self, pedido_original_id: int, datos_upsell: dict) -> Pedido:
        """
        Crea un nuevo pedido UPSELL referenciando al pedido original
        """
        # Obtener pedido original
        pedido_original = self.db.query(Pedido).filter(Pedido.id == pedido_original_id).first()
        if not pedido_original:
            raise ValueError(f"Pedido original {pedido_original_id} no encontrado")
        
        # Generar código UPSELL
        codigo_upsell = self.generar_codigo_upsell(pedido_original)
        
        # Crear nuevo pedido UPSELL
        pedido_upsell = Pedido(
            gescom_pedido_id=datos_upsell.get('gescom_pedido_id'),
            numero_pedido=codigo_upsell,
            mayorista_id=pedido_original.mayorista_id,
            cliente_id=pedido_original.cliente_id,
            tipo=TipoPedido.UPSELL,
            pedido_original_id=pedido_original.id,
            codigo_referencia=pedido_original.numero_pedido,
            subtotal=datos_upsell.get('subtotal', 0),
            descuento=datos_upsell.get('descuento', 0),
            impuestos=datos_upsell.get('impuestos', 0),
            total=datos_upsell.get('total', 0),
            observaciones=f"Pedido UPSELL generado por recomendaciones de Ticket+ - Referencia: {pedido_original.numero_pedido}",
            direccion_envio=pedido_original.direccion_envio,
            fecha_pedido=datetime.now()
        )
        
        self.db.add(pedido_upsell)
        self.db.commit()
        self.db.refresh(pedido_upsell)
        
        return pedido_upsell
    
    def obtener_pedidos_con_referencias(self, mayorista_id: int, incluir_upsell: bool = True):
        """
        Obtiene pedidos con información de referencias
        """
        query = self.db.query(Pedido).filter(Pedido.mayorista_id == mayorista_id)
        
        if not incluir_upsell:
            query = query.filter(Pedido.tipo == TipoPedido.ORIGINAL)
        
        pedidos = query.order_by(Pedido.fecha_pedido.desc()).all()
        
        resultado = []
        for pedido in pedidos:
            pedido_info = {
                'id': pedido.id,
                'numero_pedido': pedido.numero_pedido,
                'tipo': pedido.tipo.value,
                'total': float(pedido.total),
                'fecha_pedido': pedido.fecha_pedido,
                'estado': pedido.estado.value,
                'pedido_original_id': pedido.pedido_original_id,
                'codigo_referencia': pedido.codigo_referencia,
            }
            
            # Si es ORIGINAL, agregar lista de UPSELL
            if pedido.tipo == TipoPedido.ORIGINAL:
                upsells = [p for p in pedido.pedidos_upsell] if hasattr(pedido, 'pedidos_upsell') else []
                pedido_info['upsells'] = [
                    {
                        'id': u.id,
                        'numero_pedido': u.numero_pedido,
                        'total': float(u.total),
                        'fecha_pedido': u.fecha_pedido
                    } for u in upsells
                ]
                pedido_info['total_upsells'] = sum(float(u.total) for u in upsells)
                pedido_info['count_upsells'] = len(upsells)
            
            resultado.append(pedido_info)
        
        return resultado 