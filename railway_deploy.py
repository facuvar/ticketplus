#!/usr/bin/env python3
"""
Script para desplegar la base de datos en Railway usando variables de entorno y mysql-connector-python
"""
import os
import sys
import mysql.connector
from urllib.parse import urlparse

def import_to_railway():
    """Importar base de datos a Railway usando variables de entorno"""
    
    # Variables de Railway (se configurarán en Railway)
    DATABASE_URL = os.getenv('DATABASE_URL', 'mysql://root:BIHRcTOjhslPTJvrDWqaaqSEYzizZmXE@hopper.proxy.rlwy.net:41023/railway')
    
    print("🚀 Importando base de datos a Railway...")
    print(f"📊 URL de la base de datos: {DATABASE_URL}")
    
    try:
        # Parsear la URL de la base de datos
        parsed = urlparse(DATABASE_URL)
        
        # Conectar a Railway
        connection = mysql.connector.connect(
            host=parsed.hostname,
            port=parsed.port,
            user=parsed.username,
            password=parsed.password,
            database=parsed.path.lstrip('/'),
            charset='utf8mb4',
            autocommit=True
        )
        
        print("✅ Conectado a Railway MySQL")
        
        # Leer el archivo SQL
        with open('railway_import.sql', 'r', encoding='utf-8') as f:
            sql_content = f.read()
        
        # Ejecutar el SQL sentencia por sentencia
        cursor = connection.cursor()
        print("📝 Ejecutando sentencias SQL una por una...")
        statements = sql_content.split(';')
        for i, statement in enumerate(statements):
            stmt = statement.strip()
            if stmt and not stmt.startswith('--'):
                try:
                    cursor.execute(stmt)
                except Exception as e:
                    print(f"⚠️  Error en sentencia {i+1}: {e}")
                    continue
        cursor.close()
        
        print("✅ Base de datos importada exitosamente en Railway!")
        
        # Verificar que las tablas se crearon
        cursor = connection.cursor()
        cursor.execute("SHOW TABLES")
        tables = [row[0] for row in cursor.fetchall()]
        print(f"📋 Tablas creadas: {', '.join(tables)}")
        
        # Verificar datos
        cursor.execute("SELECT COUNT(*) FROM pedidos")
        pedidos_count = cursor.fetchone()[0]
        print(f"📦 Pedidos importados: {pedidos_count}")
        
        cursor.execute("SELECT COUNT(*) FROM recomendaciones")
        recomendaciones_count = cursor.fetchone()[0]
        print(f"🎯 Recomendaciones importadas: {recomendaciones_count}")
        cursor.close()
        connection.close()
        
    except Exception as e:
        print(f"❌ Error al importar: {e}")
        sys.exit(1)

if __name__ == "__main__":
    import_to_railway() 