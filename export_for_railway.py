#!/usr/bin/env python3
"""
Script para exportar la base de datos para Railway
"""
import os
import subprocess
from datetime import datetime

def export_database():
    """Exportar la base de datos local para Railway"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"ticketplus_railway_{timestamp}.sql"
    
    print(f"📤 Exportando base de datos para Railway...")
    print(f"📁 Archivo: {filename}")
    
    # Ruta de mysqldump en XAMPP
    mysqldump_path = r"C:\xampp\mysql\bin\mysqldump.exe"
    
    # Comando para exportar MySQL (sin --create-database)
    cmd = [
        mysqldump_path,
        '--host=localhost',
        '--user=root',
        '--password=',
        '--single-transaction',
        '--routines',
        '--triggers',
        '--add-drop-database',
        'ticketplus_dev'
    ]
    
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            result = subprocess.run(cmd, stdout=f, stderr=subprocess.PIPE, text=True)
        
        if result.returncode == 0:
            print(f"✅ Base de datos exportada exitosamente")
            print(f"📁 Archivo creado: {filename}")
            print(f"📏 Tamaño: {os.path.getsize(filename) / 1024:.1f} KB")
            
            # Mostrar instrucciones para Railway
            print("\n📋 Instrucciones para Railway:")
            print("1. Ve a https://railway.app")
            print("2. Crea un nuevo proyecto")
            print("3. Agrega un servicio MySQL")
            print("4. En la pestaña 'Variables', copia las credenciales")
            print("5. En la pestaña 'Connect', usa el comando:")
            print(f"   mysql -h $MYSQLHOST -P $MYSQLPORT -u $MYSQLUSER -p$MYSQLPASSWORD $MYSQLDATABASE < {filename}")
            
            return filename
        else:
            print(f"❌ Error al exportar: {result.stderr}")
            return None
    except Exception as e:
        print(f"❌ Error al exportar: {e}")
        return None

def create_railway_instructions():
    """Crear instrucciones detalladas para Railway"""
    instructions = """
🚀 GUÍA PARA DESPLEGAR EN RAILWAY
================================

1. 📋 PREPARACIÓN
   - Ve a https://railway.app
   - Inicia sesión con tu cuenta GitHub
   - Crea un nuevo proyecto

2. 🗄️ BASE DE DATOS MYSQL
   - En tu proyecto Railway, haz clic en "New Service"
   - Selecciona "Database" → "MySQL"
   - Espera a que se cree el servicio

3. 📊 IMPORTAR DATOS
   - Ve a la pestaña "Variables" del servicio MySQL
   - Copia las credenciales (MYSQLHOST, MYSQLPORT, etc.)
   - Ve a la pestaña "Connect"
   - Usa el comando de importación con el archivo SQL generado

4. 🚀 DESPLEGAR APLICACIÓN
   - En tu proyecto Railway, haz clic en "New Service"
   - Selecciona "GitHub Repo"
   - Conecta tu repositorio: https://github.com/facuvar/ticketplus
   - Railway detectará automáticamente que es Python

5. ⚙️ CONFIGURAR VARIABLES
   - En el servicio de la aplicación, ve a "Variables"
   - Agrega las variables de entorno necesarias:
     * DATABASE_URL (Railway la genera automáticamente)
     * SECRET_KEY (genera una clave secreta)
     * WHATSAPP_API_KEY (si usas WhatsApp)
     * WHATSAPP_PHONE_NUMBER (si usas WhatsApp)

6. 🔗 CONECTAR SERVICIOS
   - En el servicio de la aplicación, ve a "Settings"
   - En "Connect" selecciona el servicio MySQL
   - Railway conectará automáticamente los servicios

7. 🚀 DESPLEGAR
   - Railway desplegará automáticamente
   - Ve a la pestaña "Deployments" para ver el progreso
   - Una vez completado, obtendrás una URL pública

8. ✅ VERIFICAR
   - Visita la URL de tu aplicación
   - Prueba los endpoints: /api/v1/carrito/PED001
   - Verifica que la base de datos esté conectada

📞 SOPORTE
- Si tienes problemas, revisa los logs en Railway
- Verifica que las variables de entorno estén correctas
- Asegúrate de que la base de datos esté importada correctamente
"""
    
    with open("RAILWAY_DEPLOY_GUIDE.md", "w", encoding="utf-8") as f:
        f.write(instructions)
    
    print("📖 Guía de despliegue creada: RAILWAY_DEPLOY_GUIDE.md")

if __name__ == "__main__":
    print("🚀 Preparando Ticket+ para Railway")
    print("=" * 50)
    
    # Exportar base de datos
    export_file = export_database()
    
    if export_file:
        # Crear guía de instrucciones
        create_railway_instructions()
        
        print("\n🎉 ¡Preparación completada!")
        print("📁 Archivos creados:")
        print(f"   - {export_file} (Base de datos)")
        print("   - RAILWAY_DEPLOY_GUIDE.md (Instrucciones)")
        print("\n📋 Siguiente paso: Sigue la guía para desplegar en Railway")
    else:
        print("❌ Error en la preparación") 