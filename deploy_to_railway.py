#!/usr/bin/env python3
"""
Script para desplegar la base de datos a Railway
"""
import os
import subprocess
import sys
from datetime import datetime

def check_railway_cli():
    """Verificar si Railway CLI está instalado"""
    try:
        result = subprocess.run(['railway', '--version'], capture_output=True, text=True)
        if result.returncode == 0:
            print("✅ Railway CLI está instalado")
            return True
        else:
            print("❌ Railway CLI no está instalado o no funciona")
            return False
    except FileNotFoundError:
        print("❌ Railway CLI no está instalado")
        return False

def login_to_railway():
    """Iniciar sesión en Railway"""
    print("🔐 Iniciando sesión en Railway...")
    result = subprocess.run(['railway', 'login'], capture_output=True, text=True)
    if result.returncode == 0:
        print("✅ Sesión iniciada en Railway")
        return True
    else:
        print(f"❌ Error al iniciar sesión: {result.stderr}")
        return False

def link_project():
    """Vincular el proyecto actual con Railway"""
    print("🔗 Vinculando proyecto con Railway...")
    result = subprocess.run(['railway', 'link'], capture_output=True, text=True)
    if result.returncode == 0:
        print("✅ Proyecto vinculado")
        return True
    else:
        print(f"❌ Error al vincular proyecto: {result.stderr}")
        return False

def get_mysql_service():
    """Obtener el servicio MySQL de Railway"""
    print("🔍 Buscando servicio MySQL en Railway...")
    result = subprocess.run(['railway', 'service', 'list'], capture_output=True, text=True)
    if result.returncode == 0:
        print("✅ Servicios encontrados:")
        print(result.stdout)
        return True
    else:
        print(f"❌ Error al listar servicios: {result.stderr}")
        return False

def export_database():
    """Exportar la base de datos local"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"ticketplus_export_{timestamp}.sql"
    
    print(f"📤 Exportando base de datos local a {filename}...")
    
    # Comando para exportar MySQL
    cmd = [
        'mysqldump',
        '--host=localhost',
        '--user=root',
        '--password=',
        '--single-transaction',
        '--routines',
        '--triggers',
        'ticketplus_dev'
    ]
    
    try:
        with open(filename, 'w') as f:
            result = subprocess.run(cmd, stdout=f, stderr=subprocess.PIPE, text=True)
        
        if result.returncode == 0:
            print(f"✅ Base de datos exportada a {filename}")
            return filename
        else:
            print(f"❌ Error al exportar: {result.stderr}")
            return None
    except Exception as e:
        print(f"❌ Error al exportar: {e}")
        return None

def import_to_railway(filename):
    """Importar la base de datos a Railway"""
    print(f"📥 Importando {filename} a Railway...")
    
    # Primero, obtener las variables de entorno de Railway
    result = subprocess.run(['railway', 'variables'], capture_output=True, text=True)
    if result.returncode != 0:
        print("❌ Error al obtener variables de Railway")
        return False
    
    # Leer el archivo SQL y enviarlo a Railway
    try:
        with open(filename, 'r') as f:
            sql_content = f.read()
        
        # Crear un comando para importar usando railway run
        cmd = ['railway', 'run', '--', 'mysql', '-h', '$MYSQLHOST', '-P', '$MYSQLPORT', '-u', '$MYSQLUSER', '-p$MYSQLPASSWORD', '$MYSQLDATABASE']
        
        # Usar subprocess con input para enviar el SQL
        process = subprocess.Popen(cmd, stdin=subprocess.PIPE, text=True)
        process.communicate(input=sql_content)
        
        if process.returncode == 0:
            print("✅ Base de datos importada a Railway")
            return True
        else:
            print("❌ Error al importar a Railway")
            return False
            
    except Exception as e:
        print(f"❌ Error al importar: {e}")
        return False

def deploy_app():
    """Desplegar la aplicación a Railway"""
    print("🚀 Desplegando aplicación a Railway...")
    result = subprocess.run(['railway', 'up'], capture_output=True, text=True)
    if result.returncode == 0:
        print("✅ Aplicación desplegada")
        return True
    else:
        print(f"❌ Error al desplegar: {result.stderr}")
        return False

def main():
    """Función principal"""
    print("🚀 Desplegando Ticket+ a Railway")
    print("=" * 50)
    
    # 1. Verificar Railway CLI
    if not check_railway_cli():
        print("\n📋 Para instalar Railway CLI:")
        print("npm install -g @railway/cli")
        return
    
    # 2. Iniciar sesión
    if not login_to_railway():
        return
    
    # 3. Vincular proyecto
    if not link_project():
        return
    
    # 4. Verificar servicios
    if not get_mysql_service():
        return
    
    # 5. Exportar base de datos local
    export_file = export_database()
    if not export_file:
        return
    
    # 6. Importar a Railway
    if not import_to_railway(export_file):
        return
    
    # 7. Desplegar aplicación
    if not deploy_app():
        return
    
    print("\n🎉 ¡Despliegue completado!")
    print("📱 Tu aplicación estará disponible en Railway")
    print("🔗 Verifica el estado en: https://railway.app")

if __name__ == "__main__":
    main() 