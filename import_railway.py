"""
Script para importar datos directamente a Railway MySQL
Usa las credenciales de Railway para importar estructura y datos
"""
import mysql.connector
import os
from pathlib import Path
import glob

# Credenciales de Railway
RAILWAY_CONFIG = {
    'host': 'mysql.railway.internal',
    'port': 3306,
    'user': 'root',
    'password': 'BIHRcTOjhslPTJvrDWqaaqSEYzizZmXE',
    'database': 'railway'
}

def connect_to_railway():
    """Conectar a Railway MySQL"""
    try:
        connection = mysql.connector.connect(**RAILWAY_CONFIG)
        print(f"✅ Conectado a Railway MySQL: {RAILWAY_CONFIG['host']}")
        return connection
    except Exception as e:
        print(f"❌ Error conectando a Railway: {e}")
        return None

def execute_sql_file(connection, file_path):
    """Ejecutar un archivo SQL en Railway"""
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            sql_content = file.read()
        
        # Dividir por statements (separados por ;)
        statements = [stmt.strip() for stmt in sql_content.split(';') if stmt.strip()]
        
        cursor = connection.cursor()
        for statement in statements:
            if statement:
                cursor.execute(statement)
        
        connection.commit()
        cursor.close()
        print(f"✅ Ejecutado: {file_path.name}")
        return True
    except Exception as e:
        print(f"❌ Error ejecutando {file_path.name}: {e}")
        return False

def import_to_railway():
    """Importar datos a Railway MySQL"""
    print("🚀 IMPORTANDO DATOS A RAILWAY MYSQL")
    print("=" * 50)
    
    # Buscar archivos de exportación más recientes
    export_dir = Path("exports")
    if not export_dir.exists():
        print("❌ Directorio exports/ no encontrado")
        return False
    
    # Buscar archivos de estructura y datos
    structure_files = list(export_dir.glob("ticketplus_structure_*.sql"))
    data_files = list(export_dir.glob("ticketplus_data_*.sql"))
    
    if not structure_files or not data_files:
        print("❌ Archivos de exportación no encontrados")
        return False
    
    # Usar los archivos más recientes
    structure_file = max(structure_files, key=lambda x: x.stat().st_mtime)
    data_file = max(data_files, key=lambda x: x.stat().st_mtime)
    
    print(f"📋 Estructura: {structure_file.name}")
    print(f"📦 Datos: {data_file.name}")
    
    # Conectar a Railway
    connection = connect_to_railway()
    if not connection:
        return False
    
    try:
        # 1. Importar estructura
        print("\n📋 1. Importando estructura de tablas...")
        if execute_sql_file(connection, structure_file):
            print("   ✅ Estructura importada correctamente")
        else:
            print("   ❌ Error importando estructura")
            return False
        
        # 2. Importar datos
        print("\n📦 2. Importando datos...")
        if execute_sql_file(connection, data_file):
            print("   ✅ Datos importados correctamente")
        else:
            print("   ❌ Error importando datos")
            return False
        
        # 3. Verificar importación
        print("\n🔍 3. Verificando importación...")
        cursor = connection.cursor()
        
        # Verificar tablas
        cursor.execute("SHOW TABLES")
        tables = cursor.fetchall()
        print(f"   📊 Tablas encontradas: {len(tables)}")
        for table in tables:
            print(f"      - {table[0]}")
        
        # Verificar datos en tabla pedidos
        cursor.execute("SELECT COUNT(*) FROM pedidos")
        pedidos_count = cursor.fetchone()[0]
        print(f"   📦 Pedidos importados: {pedidos_count}")
        
        # Verificar mayoristas
        cursor.execute("SELECT COUNT(*) FROM mayoristas")
        mayoristas_count = cursor.fetchone()[0]
        print(f"   👥 Mayoristas importados: {mayoristas_count}")
        
        cursor.close()
        
        print(f"\n✅ IMPORTACIÓN COMPLETADA EXITOSAMENTE")
        print(f"🌐 Base de datos Railway lista para usar")
        
        return True
        
    except Exception as e:
        print(f"❌ Error durante importación: {e}")
        return False
    finally:
        connection.close()

if __name__ == "__main__":
    success = import_to_railway()
    if success:
        print(f"\n🎯 PRÓXIMO PASO:")
        print(f"   Deploy tu aplicación en Railway")
        print(f"   El sistema detectará automáticamente el entorno Railway")
        print(f"   URLs de acceso:")
        print(f"   - Dashboard: https://tu-app.railway.app/api/v1/admin/dashboard/4")
        print(f"   - API Docs: https://tu-app.railway.app/docs")
    else:
        print(f"\n❌ Importación falló. Revisar errores arriba.") 