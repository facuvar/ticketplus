import os
from pydantic_settings import BaseSettings
from typing import Optional


def is_railway() -> bool:
    """Detecta si la aplicación está ejecutándose en Railway"""
    return os.getenv("RAILWAY_ENVIRONMENT") is not None or os.getenv("RAILWAY_PROJECT_ID") is not None


def get_database_url() -> str:
    """Obtiene la URL de la base de datos según el entorno"""
    if is_railway():
        railway_db_url = os.getenv("DATABASE_URL")
        print(f"DEBUG: Valor original de DATABASE_URL: {railway_db_url}")
        if railway_db_url:
            # Forzar SIEMPRE el prefijo pymysql
            if railway_db_url.startswith("mysql://"):
                print("DEBUG: Reemplazando prefijo mysql:// por mysql+pymysql://")
                railway_db_url = railway_db_url.replace("mysql://", "mysql+pymysql://", 1)
            elif not railway_db_url.startswith("mysql+pymysql://"):
                print("DEBUG: Agregando prefijo mysql+pymysql://")
                railway_db_url = "mysql+pymysql://" + railway_db_url
            print(f"DEBUG: Valor final de DATABASE_URL: {railway_db_url}")
            return railway_db_url
        
        # Construir URL desde variables individuales de Railway
        db_host = os.getenv("MYSQLHOST", "localhost")
        db_port = os.getenv("MYSQLPORT", "3306")
        db_user = os.getenv("MYSQLUSER", "root")
        db_password = os.getenv("MYSQLPASSWORD", "")
        db_name = os.getenv("MYSQLDATABASE", "ticketplus_prod")
        
        if db_password:
            return f"mysql+pymysql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"
        else:
            return f"mysql+pymysql://{db_user}@{db_host}:{db_port}/{db_name}"
    else:
        # Desarrollo local
        return os.getenv("DATABASE_URL", "mysql+pymysql://root@localhost:3306/ticketplus_dev")


class Settings(BaseSettings):
    # Environment detection
    IS_RAILWAY: bool = is_railway()
    ENVIRONMENT: str = "production" if is_railway() else "development"
    
    # Database - Detección automática
    DATABASE_URL: str = get_database_url()
    
    # Security
    SECRET_KEY: str = os.getenv("SECRET_KEY", "your-secret-key-change-in-production")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # WhatsApp API
    WHATSAPP_API_URL: str = "https://api.botsapper.com/v1"
    WHATSAPP_API_KEY: str = os.getenv("WHATSAPP_API_KEY", "")
    WHATSAPP_PHONE_NUMBER: str = os.getenv("WHATSAPP_PHONE_NUMBER", "")
    
    # Redis
    REDIS_URL: str = os.getenv("REDIS_URL", "redis://localhost:6379" if not is_railway() else "redis://redis:6379")
    
    # Frontend URLs
    FRONTEND_URL: str = os.getenv("FRONTEND_URL", "http://localhost:3000")
    ADMIN_URL: str = os.getenv("ADMIN_URL", "http://localhost:3001")
    
    # Server configuration
    HOST: str = "0.0.0.0" if is_railway() else "127.0.0.1"
    PORT: int = int(os.getenv("PORT", "8000"))
    
    # Token expiration for cart links (48 hours in seconds)
    CART_TOKEN_EXPIRE_SECONDS: int = 48 * 60 * 60  # 48 horas
    
    # Debugging
    DEBUG: bool = not is_railway()
    
    class Config:
        env_file = ".env"
        case_sensitive = True
        extra = 'ignore'


settings = Settings()

# Log de configuración al iniciar
if __name__ == "__main__":
    print(f"🚀 Ticket+ - Configuración cargada:")
    print(f"   Entorno: {'🌐 Railway (Producción)' if settings.IS_RAILWAY else '💻 Local (Desarrollo)'}")
    print(f"   Base de datos: {settings.DATABASE_URL}")
    print(f"   Host: {settings.HOST}:{settings.PORT}")
    print(f"   Debug: {settings.DEBUG}") 