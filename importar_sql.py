#!/usr/bin/env python3
"""
Script para importar un archivo SQL completo a la base de datos de Railway.
Debe ejecutarse en Railway o en un entorno donde DATABASE_URL apunte a la base de datos destino.
"""
import os
import sys
import mysql.connector
from urllib.parse import urlparse

def main():
    DATABASE_URL = os.getenv('DATABASE_URL')
    if not DATABASE_URL:
        print('❌ No se encontró la variable de entorno DATABASE_URL')
        sys.exit(1)

    print(f'📊 Usando base de datos: {DATABASE_URL}')

    # Parsear la URL
    parsed = urlparse(DATABASE_URL)
    connection = mysql.connector.connect(
        host=parsed.hostname,
        port=parsed.port,
        user=parsed.username,
        password=parsed.password,
        database=parsed.path.lstrip('/'),
        charset='utf8mb4',
        autocommit=True
    )

    # Leer el archivo SQL
    sql_file = 'railway_import.sql'
    if not os.path.exists(sql_file):
        print(f'❌ No se encontró el archivo {sql_file}')
        sys.exit(1)

    with open(sql_file, 'r', encoding='utf-8') as f:
        sql_content = f.read()

    print('📝 Ejecutando importación...')
    cursor = connection.cursor()
    statements = sql_content.split(';')
    for i, statement in enumerate(statements):
        stmt = statement.strip()
        if stmt and not stmt.startswith('--'):
            try:
                cursor.execute(stmt)
            except Exception as e:
                print(f'⚠️  Error en sentencia {i+1}: {e}')
                continue
    cursor.close()
    connection.close()
    print('✅ Importación finalizada.')

if __name__ == '__main__':
    main() 