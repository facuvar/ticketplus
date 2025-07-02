from sqlalchemy.orm import Session


class GescomService:
    def __init__(self, db: Session):
        self.db = db
    
    async def sincronizar_pedidos_mayorista(self, mayorista_id: int):
        """Sincronizar pedidos desde Gescom"""
        # TODO: Implementar conexión real a Gescom
        pass 