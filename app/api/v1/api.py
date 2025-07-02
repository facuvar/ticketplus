from fastapi import APIRouter
from app.api.v1.endpoints import pedidos, recomendaciones, whatsapp, admin, carrito

api_router = APIRouter()

# Include all endpoint routers
api_router.include_router(pedidos.router, prefix="/pedidos", tags=["Pedidos"])
api_router.include_router(recomendaciones.router, prefix="/recomendaciones", tags=["Recomendaciones"])
api_router.include_router(whatsapp.router, prefix="/whatsapp", tags=["WhatsApp"])
api_router.include_router(admin.router, prefix="/admin", tags=["Admin"])
api_router.include_router(carrito.router, prefix="/carrito", tags=["Carrito"]) 