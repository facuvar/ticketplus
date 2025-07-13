from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.core.config import settings

# Create engine with fallback to SQLite
try:
    # Intentar MySQL primero
    engine = create_engine(
        settings.DATABASE_URL,
        pool_pre_ping=True,
        pool_recycle=300,
        echo=settings.ENVIRONMENT == "development"
    )
    # Probar la conexión
    with engine.connect() as conn:
        # Obtener el nombre de la base de datos desde la URL
        db_name = settings.DATABASE_URL.split('/')[-1]
        print(f"✅ Conectado a MySQL: {db_name}")
except Exception as e:
    print(f"⚠️ No se pudo conectar a MySQL: {e}")
    print("🔄 Usando SQLite como fallback...")
    
    # Fallback a SQLite
    sqlite_url = "sqlite:///./ticketplus.db"
    engine = create_engine(
        sqlite_url,
        connect_args={"check_same_thread": False},  # Solo para SQLite
        echo=settings.ENVIRONMENT == "development"
    )

# Create SessionLocal class
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create Base class
Base = declarative_base()

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close() 