"""
Script para exportar datos de MySQL local y preparar para Railway
Genera archivos SQL para migrar datos a producción
"""
import os
import subprocess
import json
from datetime import datetime
from pathlib import Path

def export_mysql_data():
    """Exporta datos de MySQL local usando mysqldump"""
    print("🗄️  EXPORTANDO DATOS MYSQL LOCAL")
    print("=" * 50)
    
    # Configuración de la base de datos local
    db_host = "localhost"
    db_port = "3306"
    db_user = "root"
    db_name = "ticketplus_dev"
    
    # Crear directorio de exports
    export_dir = Path("exports")
    export_dir.mkdir(exist_ok=True)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # 1. Exportar estructura de la base de datos
    print("\n📋 1. Exportando estructura de la base de datos...")
    structure_file = export_dir / f"ticketplus_structure_{timestamp}.sql"
    
    structure_cmd = [
        "C:\\xampp\\mysql\\bin\\mysqldump.exe",
        f"--host={db_host}",
        f"--port={db_port}",
        f"--user={db_user}",
        "--no-data",  # Solo estructura, no datos
        "--routines",
        "--triggers",
        db_name
    ]
    
    try:
        with open(structure_file, 'w', encoding='utf-8') as f:
            result = subprocess.run(structure_cmd, stdout=f, stderr=subprocess.PIPE, text=True)
        
        if result.returncode == 0:
            print(f"   ✅ Estructura exportada: {structure_file}")
        else:
            print(f"   ❌ Error exportando estructura: {result.stderr}")
            return False
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return False
    
    # 2. Exportar datos (solo las tablas importantes)
    print("\n📦 2. Exportando datos de tablas...")
    data_file = export_dir / f"ticketplus_data_{timestamp}.sql"
    
    # Tablas a exportar (nombres corregidos según SHOW TABLES)
    tables_to_export = [
        "mayoristas",
        "clientes", 
        "usuarios",
        "productos",
        "pedidos",
        "items_pedido",  # Corregido: items_pedido no item_pedido
        "recomendaciones"
    ]
    
    data_cmd = [
        "C:\\xampp\\mysql\\bin\\mysqldump.exe",
        f"--host={db_host}",
        f"--port={db_port}",
        f"--user={db_user}",
        "--no-create-info",  # Solo datos, no estructura
        "--complete-insert",
        "--single-transaction",
        db_name
    ] + tables_to_export
    
    try:
        with open(data_file, 'w', encoding='utf-8') as f:
            result = subprocess.run(data_cmd, stdout=f, stderr=subprocess.PIPE, text=True)
        
        if result.returncode == 0:
            print(f"   ✅ Datos exportados: {data_file}")
        else:
            print(f"   ❌ Error exportando datos: {result.stderr}")
            return False
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return False
    
    # 3. Exportar backup completo
    print("\n💾 3. Exportando backup completo...")
    backup_file = export_dir / f"ticketplus_full_backup_{timestamp}.sql"
    
    backup_cmd = [
        "C:\\xampp\\mysql\\bin\\mysqldump.exe",
        f"--host={db_host}",
        f"--port={db_port}",
        f"--user={db_user}",
        "--single-transaction",
        "--routines",
        "--triggers",
        db_name
    ]
    
    try:
        with open(backup_file, 'w', encoding='utf-8') as f:
            result = subprocess.run(backup_cmd, stdout=f, stderr=subprocess.PIPE, text=True)
        
        if result.returncode == 0:
            print(f"   ✅ Backup completo: {backup_file}")
        else:
            print(f"   ❌ Error en backup: {result.stderr}")
            return False
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return False
    
    # 4. Generar script de importación para Railway
    print("\n🚀 4. Generando script de importación para Railway...")
    import_script = export_dir / f"import_to_railway_{timestamp}.sh"
    
    import_content = f"""#!/bin/bash
# Script de importación para Railway - Ticket+ 
# Generado: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

echo "🚀 IMPORTANDO DATOS A RAILWAY MYSQL"
echo "=================================="

# Variables (ajustar con credenciales de Railway)
export MYSQL_HOST="$MYSQLHOST"
export MYSQL_PORT="$MYSQLPORT"
export MYSQL_USER="$MYSQLUSER"
export MYSQL_PASSWORD="$MYSQLPASSWORD"
export MYSQL_DATABASE="$MYSQLDATABASE"

echo "📋 1. Importando estructura..."
mysql -h $MYSQL_HOST -P $MYSQL_PORT -u $MYSQL_USER -p$MYSQL_PASSWORD $MYSQL_DATABASE < ticketplus_structure_{timestamp}.sql

echo "📦 2. Importando datos..."
mysql -h $MYSQL_HOST -P $MYSQL_PORT -u $MYSQL_USER -p$MYSQL_PASSWORD $MYSQL_DATABASE < ticketplus_data_{timestamp}.sql

echo "✅ Importación completada!"
echo "🌐 Base de datos lista en Railway"
"""
    
    with open(import_script, 'w', encoding='utf-8') as f:
        f.write(import_content)
    
    print(f"   ✅ Script de importación: {import_script}")
    
    # 5. Generar resumen
    print("\n📊 5. Generando resumen de exportación...")
    summary = {
        "timestamp": timestamp,
        "database": db_name,
        "files": {
            "structure": str(structure_file),
            "data": str(data_file), 
            "backup": str(backup_file),
            "import_script": str(import_script)
        },
        "tables_exported": tables_to_export,
        "export_date": datetime.now().isoformat()
    }
    
    summary_file = export_dir / f"export_summary_{timestamp}.json"
    with open(summary_file, 'w', encoding='utf-8') as f:
        json.dump(summary, f, indent=2, ensure_ascii=False)
    
    print(f"   ✅ Resumen: {summary_file}")
    
    # Mostrar estadísticas de archivos
    print(f"\n📈 ESTADÍSTICAS DE EXPORTACIÓN:")
    for desc, file_path in [
        ("Estructura", structure_file),
        ("Datos", data_file),
        ("Backup completo", backup_file)
    ]:
        if file_path.exists():
            size_mb = file_path.stat().st_size / (1024 * 1024)
            print(f"   {desc}: {size_mb:.2f} MB")
    
    print(f"\n✅ EXPORTACIÓN COMPLETADA")
    print(f"   📁 Archivos guardados en: {export_dir.absolute()}")
    print(f"   🚀 Para importar en Railway:")
    print(f"      1. Subir archivos a tu servidor Railway")
    print(f"      2. Ejecutar: bash {import_script.name}")
    
    return True

if __name__ == "__main__":
    export_mysql_data() 