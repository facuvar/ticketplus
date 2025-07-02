"""
Ticket+ - Sistema de Recomendaciones IA para Mayoristas
Entry point principal con detección automática de entorno
"""
import uvicorn
from app.main import app
from app.core.config import settings

if __name__ == "__main__":
    print("🚀 Iniciando Ticket+ API...")
    print(f"   Entorno: {'🌐 Railway (Producción)' if settings.IS_RAILWAY else '💻 Local (Desarrollo)'}")
    print(f"   Base de datos: {settings.DATABASE_URL.split('@')[1] if '@' in settings.DATABASE_URL else 'localhost'}")
    print(f"   Servidor: {settings.HOST}:{settings.PORT}")
    print(f"   Debug: {settings.DEBUG}")
    
    # Configuración específica por entorno
    uvicorn_config = {
        "app": "app.main:app",
        "host": settings.HOST,
        "port": settings.PORT,
        "reload": settings.DEBUG,  # Solo reload en desarrollo
        "log_level": "info" if settings.IS_RAILWAY else "debug"
    }
    
    if settings.IS_RAILWAY:
        print("🌐 Configuración Railway:")
        print("   - Host: 0.0.0.0 (todas las interfaces)")
        print("   - Reload: Deshabilitado")
        print("   - Log level: INFO")
    else:
        print("💻 Configuración Local:")
        print("   - Host: 127.0.0.1 (localhost)")
        print("   - Reload: Habilitado")
        print("   - Log level: DEBUG")
    
    uvicorn.run(**uvicorn_config) 