"""
Script para importar datos a Railway MySQL usando host público
Para uso desde máquina local hacia Railway
"""
import mysql.connector
import os
from pathlib import Path
import glob

# Credenciales de Railway - Host público
# Nota: Necesitas obtener el host público desde Railway Dashboard
RAILWAY_CONFIG = {
    'host': 'autorack.proxy.rlwy.net',  # Host público típico de Railway
    'port': 3306,  # Puerto público de Railway MySQL
    'user': 'root',
    'password': 'BIHRcTOjhslPTJvrDWqaaqSEYzizZmXE',
    'database': 'railway'
}

def test_connection():
    """Probar diferentes configuraciones de conexión"""
    print("🔍 PROBANDO CONEXIONES A RAILWAY")
    print("=" * 40)
    
    # Configuraciones posibles
    configs = [
        {
            'name': 'Host público Railway',
            'config': {
                'host': 'autorack.proxy.rlwy.net',
                'port': 3306,
                'user': 'root',
                'password': 'BIHRcTOjhslPTJvrDWqaaqSEYzizZmXE',
                'database': 'railway'
            }
        },
        {
            'name': 'Host público alternativo',
            'config': {
                'host': 'mysql.railway.app',
                'port': 3306,
                'user': 'root',
                'password': 'BIHRcTOjhslPTJvrDWqaaqSEYzizZmXE',
                'database': 'railway'
            }
        }
    ]
    
    for config_info in configs:
        print(f"\n📡 Probando: {config_info['name']}")
        try:
            connection = mysql.connector.connect(**config_info['config'])
            print(f"   ✅ Conexión exitosa!")
            print(f"   🌐 Host: {config_info['config']['host']}")
            
            # Probar una consulta simple
            cursor = connection.cursor()
            cursor.execute("SELECT VERSION()")
            version = cursor.fetchone()
            print(f"   📊 MySQL Version: {version[0]}")
            
            cursor.close()
            connection.close()
            return config_info['config']
            
        except Exception as e:
            print(f"   ❌ Error: {e}")
    
    return None

def connect_to_railway(config=None):
    """Conectar a Railway MySQL"""
    if not config:
        config = RAILWAY_CONFIG
        
    try:
        connection = mysql.connector.connect(**config)
        print(f"✅ Conectado a Railway MySQL: {config['host']}")
        return connection
    except Exception as e:
        print(f"❌ Error conectando a Railway: {e}")
        return None

def execute_sql_file(connection, file_path):
    """Ejecutar un archivo SQL en Railway"""
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            sql_content = file.read()
        
        # Limpiar contenido SQL
        sql_content = sql_content.replace('USE `ticketplus_dev`;', '')  # Remover USE statement
        sql_content = sql_content.replace('CREATE DATABASE', '-- CREATE DATABASE')  # Comentar CREATE DATABASE
        
        # Dividir por statements (separados por ;)
        statements = [stmt.strip() for stmt in sql_content.split(';') if stmt.strip() and not stmt.strip().startswith('--')]
        
        cursor = connection.cursor()
        success_count = 0
        
        for statement in statements:
            if statement and not statement.startswith('/*'):
                try:
                    cursor.execute(statement)
                    success_count += 1
                except Exception as e:
                    print(f"   ⚠️  Error en statement: {str(e)[:100]}...")
        
        connection.commit()
        cursor.close()
        print(f"✅ Ejecutado: {file_path.name} ({success_count} statements)")
        return True
    except Exception as e:
        print(f"❌ Error ejecutando {file_path.name}: {e}")
        return False

def import_to_railway():
    """Importar datos a Railway MySQL"""
    print("🚀 IMPORTANDO DATOS A RAILWAY MYSQL")
    print("=" * 50)
    
    # Primero probar conexiones
    working_config = test_connection()
    if not working_config:
        print("\n❌ No se pudo conectar a Railway MySQL")
        print("📋 Instrucciones:")
        print("   1. Ve a Railway Dashboard")
        print("   2. Ve a tu proyecto MySQL")
        print("   3. En 'Variables' copia el host público")
        print("   4. Actualiza el script con el host correcto")
        return False
    
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
    
    print(f"\n📋 Estructura: {structure_file.name}")
    print(f"📦 Datos: {data_file.name}")
    
    # Conectar a Railway
    connection = connect_to_railway(working_config)
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
        try:
            cursor.execute("SELECT COUNT(*) FROM pedidos")
            pedidos_count = cursor.fetchone()[0]
            print(f"   📦 Pedidos importados: {pedidos_count}")
        except:
            print(f"   📦 Tabla pedidos: No encontrada o vacía")
        
        # Verificar mayoristas
        try:
            cursor.execute("SELECT COUNT(*) FROM mayoristas")
            mayoristas_count = cursor.fetchone()[0]
            print(f"   👥 Mayoristas importados: {mayoristas_count}")
        except:
            print(f"   👥 Tabla mayoristas: No encontrada o vacía")
        
        cursor.close()
        
        print(f"\n✅ IMPORTACIÓN COMPLETADA")
        print(f"🌐 Base de datos Railway configurada")
        
        return True
        
    except Exception as e:
        print(f"❌ Error durante importación: {e}")
        return False
    finally:
        connection.close()

if __name__ == "__main__":
    success = import_to_railway()
    if success:
        print(f"\n🎯 PRÓXIMOS PASOS:")
        print(f"   1. Deploy tu aplicación en Railway")
        print(f"   2. El sistema detectará automáticamente el entorno Railway")
        print(f"   3. Acceder a:")
        print(f"      - Dashboard: https://tu-app.railway.app/api/v1/admin/dashboard/4")
        print(f"      - API Docs: https://tu-app.railway.app/docs")
        print(f"      - Carrito: https://tu-app.railway.app/carrito.html")
    else:
        print(f"\n❌ Necesitas el host público de Railway MySQL")
        print(f"   Ve a Railway Dashboard → MySQL Service → Connect")
        print(f"   Copia el host público y actualiza el script") 