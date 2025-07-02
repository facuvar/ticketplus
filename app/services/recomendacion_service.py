from sqlalchemy.orm import Session
from sqlalchemy import func, and_, desc
from app.models.pedido import Pedido
from app.models.item_pedido import ItemPedido
from app.models.producto import Producto
from app.models.recomendacion import Recomendacion, TipoRecomendacion, EstadoRecomendacion
from app.models.cliente import Cliente
from typing import List, Dict, Tuple
import random
from datetime import datetime, timedelta
import secrets


class RecomendacionService:
    def __init__(self, db: Session):
        self.db = db
    
    def obtener_pedido(self, pedido_id: int):
        """Obtener pedido por ID"""
        return self.db.query(Pedido).filter(Pedido.id == pedido_id).first()
    
    async def obtener_o_generar_recomendaciones(self, pedido_id: int):
        """Obtener recomendaciones existentes o generar nuevas"""
        # Verificar si ya existen recomendaciones
        recomendaciones_existentes = self.db.query(Recomendacion).filter(
            Recomendacion.pedido_id == pedido_id
        ).all()
        
        if recomendaciones_existentes:
            return recomendaciones_existentes
        
        # Si no existen, generar nuevas
        return await self.generar_recomendaciones(pedido_id)
    
    async def generar_recomendaciones(self, pedido_id: int, forzar_regeneracion: bool = False):
        """🧠 MOTOR DE RECOMENDACIONES: Generar recomendaciones inteligentes para un pedido"""
        
        # 1. Obtener el pedido original
        pedido = self.obtener_pedido(pedido_id)
        if not pedido:
            return []
        
        # 2. Obtener productos del pedido original
        items_pedido = self.db.query(ItemPedido).filter(
            ItemPedido.pedido_id == pedido_id
        ).all()
        
        # 3. Obtener información del cliente
        cliente = self.db.query(Cliente).filter(Cliente.id == pedido.cliente_id).first()
        
        # 4. Motor de recomendaciones multi-algoritmo
        candidatos = await self._generar_candidatos_recomendacion(pedido, items_pedido, cliente)
        
        # 5. Filtrar y rankear productos
        productos_finales = self._rankear_y_filtrar_productos(candidatos, max_productos=6)
        
        # 6. Crear recomendaciones en la base de datos
        recomendaciones = []
        for i, (producto, score, tipo) in enumerate(productos_finales):
            recomendacion = Recomendacion(
                pedido_id=pedido_id,
                producto_id=producto.id,
                mayorista_id=pedido.mayorista_id,
                tipo=tipo,
                estado=EstadoRecomendacion.GENERADA,
                orden=i + 1,
                score=round(score, 2),
                razon=self._generar_razon_recomendacion(tipo, producto),
                producto_nombre=producto.nombre,
                producto_precio=producto.precio,
                producto_imagen_url=producto.imagen_url,
                fecha_generacion=datetime.now()
            )
            self.db.add(recomendacion)
            recomendaciones.append(recomendacion)
        
        self.db.commit()
        return recomendaciones
    
    async def _generar_candidatos_recomendacion(self, pedido: Pedido, items_pedido: List[ItemPedido], cliente: Cliente) -> List[Tuple[Producto, float, TipoRecomendacion]]:
        """Generar pool de productos candidatos con diferentes algoritmos"""
        candidatos = []
        
        # A) PRODUCTOS COMPLEMENTARIOS (40% peso)
        complementarios = await self._obtener_productos_complementarios(items_pedido)
        for producto in complementarios:
            score = self._calcular_score_complementario(producto, items_pedido)
            candidatos.append((producto, score * 0.4, TipoRecomendacion.REGLA_PERSONALIZADA))
        
        # B) HISTORIAL DEL CLIENTE (30% peso)
        if cliente:
            favoritos = await self._obtener_productos_favoritos_cliente(cliente.id)
            for producto in favoritos:
                score = self._calcular_score_historial(producto, cliente)
                candidatos.append((producto, score * 0.3, TipoRecomendacion.REGLA_PERSONALIZADA))
        
        # C) MÁS VENDIDOS GENERALES (20% peso)
        mas_vendidos = await self._obtener_productos_mas_vendidos(pedido.mayorista_id)
        for producto in mas_vendidos:
            score = self._calcular_score_popularidad(producto)
            candidatos.append((producto, score * 0.2, TipoRecomendacion.MAS_VENDIDOS))
        
        # D) PRODUCTOS DE ALTO MARGEN (10% peso)
        alto_margen = await self._obtener_productos_alto_margen(pedido.mayorista_id)
        for producto in alto_margen:
            score = self._calcular_score_margen(producto)
            candidatos.append((producto, score * 0.1, TipoRecomendacion.REGLA_PERSONALIZADA))
        
        return candidatos
    
    async def _obtener_productos_complementarios(self, items_pedido: List[ItemPedido]) -> List[Producto]:
        """Obtener productos que suelen comprarse junto con los del pedido original"""
        productos_originales = [item.producto_codigo for item in items_pedido if item.producto_codigo]
        
        # Buscar productos que NO están en el pedido original
        query = self.db.query(Producto).filter(
            ~Producto.codigo.in_(productos_originales) if productos_originales else True
        )
        
        # Filtros de complementariedad (ejemplo: categorías relacionadas)
        # En un sistema real, esto sería más sofisticado
        productos = query.limit(10).all()
        return productos
    
    async def _obtener_productos_favoritos_cliente(self, cliente_id: int) -> List[Producto]:
        """Obtener productos que el cliente ha comprado frecuentemente"""
        # Buscar productos más comprados por este cliente
        subquery = self.db.query(
            ItemPedido.producto_codigo,
            func.count(ItemPedido.id).label('frecuencia')
        ).join(Pedido).filter(
            Pedido.cliente_id == cliente_id
        ).group_by(ItemPedido.producto_codigo).subquery()
        
        productos = self.db.query(Producto).join(
            subquery, Producto.codigo == subquery.c.producto_codigo
        ).order_by(desc(subquery.c.frecuencia)).limit(5).all()
        
        return productos
    
    async def _obtener_productos_mas_vendidos(self, mayorista_id: int) -> List[Producto]:
        """Obtener productos más vendidos del mayorista"""
        # En un sistema real, esto se basaría en datos de ventas
        productos = self.db.query(Producto).filter(
            Producto.activo == True
        ).order_by(desc(Producto.fecha_creacion)).limit(8).all()
        
        return productos
    
    async def _obtener_productos_alto_margen(self, mayorista_id: int) -> List[Producto]:
        """Obtener productos con alto margen para el mayorista"""
        # En un sistema real, esto se basaría en datos de margen/rentabilidad
        productos = self.db.query(Producto).filter(
            and_(
                Producto.activo == True,
                Producto.precio > 1000  # Productos de precio medio-alto
            )
        ).limit(5).all()
        
        return productos
    
    def _calcular_score_complementario(self, producto: Producto, items_pedido: List[ItemPedido]) -> float:
        """Calcular score de complementariedad"""
        # Lógica simplificada - en sistema real sería más compleja
        base_score = 70.0
        
        # Bonus por categorías complementarias
        categorias_originales = set()
        for item in items_pedido:
            if 'aceite' in item.producto_nombre.lower():
                categorias_originales.add('cocina')
            elif 'leche' in item.producto_nombre.lower():
                categorias_originales.add('lacteos')
        
        if 'cocina' in categorias_originales and 'pan' in producto.nombre.lower():
            base_score += 20
        elif 'lacteos' in categorias_originales and 'queso' in producto.nombre.lower():
            base_score += 25
        
        return min(base_score, 100.0)
    
    def _calcular_score_historial(self, producto: Producto, cliente: Cliente) -> float:
        """Calcular score basado en historial del cliente"""
        # Lógica simplificada
        return 60.0 + random.uniform(0, 30)  # Entre 60-90
    
    def _calcular_score_popularidad(self, producto: Producto) -> float:
        """Calcular score basado en popularidad general"""
        return 50.0 + random.uniform(0, 40)  # Entre 50-90
    
    def _calcular_score_margen(self, producto: Producto) -> float:
        """Calcular score basado en margen del producto"""
        # A mayor precio, mayor score (simplificado)
        if producto.precio > 2000:
            return 80.0
        elif producto.precio > 1000:
            return 60.0
        else:
            return 40.0
    
    def _rankear_y_filtrar_productos(self, candidatos: List[Tuple[Producto, float, TipoRecomendacion]], max_productos: int = 6) -> List[Tuple[Producto, float, TipoRecomendacion]]:
        """Rankear candidatos y seleccionar los mejores"""
        # Eliminar duplicados (por ID de producto)
        productos_unicos = {}
        for producto, score, tipo in candidatos:
            if producto.id not in productos_unicos or productos_unicos[producto.id][1] < score:
                productos_unicos[producto.id] = (producto, score, tipo)
        
        # Convertir a lista y ordenar por score
        candidatos_filtrados = list(productos_unicos.values())
        candidatos_filtrados.sort(key=lambda x: x[1], reverse=True)
        
        # Tomar los mejores
        return candidatos_filtrados[:max_productos]
    
    def _generar_razon_recomendacion(self, tipo: TipoRecomendacion, producto: Producto) -> str:
        """Generar razón humana para la recomendación"""
        if tipo == TipoRecomendacion.MAS_VENDIDOS:
            return f"Producto muy popular entre nuestros clientes"
        elif tipo == TipoRecomendacion.REGLA_PERSONALIZADA:
            if 'aceite' in producto.nombre.lower() or 'pan' in producto.nombre.lower():
                return "Complementa perfecto con tu pedido"
            else:
                return "Basado en tu historial de compras"
        else:
            return "Recomendado especialmente para vos"
    
    async def registrar_click(self, recomendacion_id: int):
        """Registrar click en recomendación"""
        recomendacion = self.db.query(Recomendacion).filter(
            Recomendacion.id == recomendacion_id
        ).first()
        
        if recomendacion:
            recomendacion.fue_clickeada = True
            recomendacion.fecha_click = datetime.now()
            self.db.commit()
            return True
        return False
    
    async def obtener_estadisticas_mayorista(self, mayorista_id: int, dias: int):
        """Obtener estadísticas de recomendaciones"""
        fecha_inicio = datetime.now() - timedelta(days=dias)
        
        total_recomendaciones = self.db.query(func.count(Recomendacion.id)).filter(
            and_(
                Recomendacion.mayorista_id == mayorista_id,
                Recomendacion.fecha_generacion >= fecha_inicio
            )
        ).scalar() or 0
        
        recomendaciones_clickeadas = self.db.query(func.count(Recomendacion.id)).filter(
            and_(
                Recomendacion.mayorista_id == mayorista_id,
                Recomendacion.fue_clickeada == True,
                Recomendacion.fecha_generacion >= fecha_inicio
            )
        ).scalar() or 0
        
        conversion_rate = (recomendaciones_clickeadas / total_recomendaciones * 100) if total_recomendaciones > 0 else 0
        
        return {
            "total_recomendaciones": total_recomendaciones,
            "recomendaciones_clickeadas": recomendaciones_clickeadas,
            "conversion_rate": round(conversion_rate, 2),
            "dias_analizados": dias
        } 