#!/usr/bin/env python3
"""
Script para probar el endpoint del carrito directamente
"""
import requests
import json
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.models.pedido import Pedido
from app.core.config import settings
from datetime import datetime

def probar_endpoint_carrito():
    """Probar el endpoint del carrito con un token válido"""
    
    # Conectar a la base de datos para obtener un token válido
    engine = create_engine(settings.DATABASE_URL)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    db = SessionLocal()
    
    try:
        # Buscar un pedido con token válido
        ahora = datetime.now()
        pedido = db.query(Pedido).filter(
            Pedido.token_carrito.isnot(None),
            Pedido.token_carrito != '',
            Pedido.token_expiracion > ahora
        ).first()
        
        if not pedido:
            print("❌ No se encontró ningún pedido con token válido")
            return
        
        token = pedido.token_carrito
        print(f"🔍 Probando con token: {token}")
        print(f"📦 Pedido: {pedido.numero_pedido}")
        
        # Probar el endpoint
        url = f"http://localhost:8000/api/v1/carrito/{token}/data"
        print(f"🌐 URL: {url}")
        
        try:
            response = requests.get(url, timeout=10)
            print(f"📊 Status Code: {response.status_code}")
            
            if response.status_code == 200:
                data = response.json()
                print("✅ Respuesta exitosa:")
                print(json.dumps(data, indent=2, ensure_ascii=False))
            else:
                print(f"❌ Error: {response.status_code}")
                print(f"📄 Respuesta: {response.text}")
                
        except requests.exceptions.RequestException as e:
            print(f"❌ Error de conexión: {e}")
        
    except Exception as e:
        print(f"❌ Error: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    print("🚀 Probando endpoint del carrito...")
    probar_endpoint_carrito()
    print("✅ Prueba completada!") 