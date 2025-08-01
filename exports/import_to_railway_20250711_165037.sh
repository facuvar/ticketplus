#!/bin/bash
# Script de importación para Railway - Ticket+ 
# Generado: 2025-07-11 16:50:38

echo "🚀 IMPORTANDO DATOS A RAILWAY MYSQL"
echo "=================================="

# Variables (ajustar con credenciales de Railway)
export MYSQL_HOST="$MYSQLHOST"
export MYSQL_PORT="$MYSQLPORT"
export MYSQL_USER="$MYSQLUSER"
export MYSQL_PASSWORD="$MYSQLPASSWORD"
export MYSQL_DATABASE="$MYSQLDATABASE"

echo "📋 1. Importando estructura..."
mysql -h $MYSQL_HOST -P $MYSQL_PORT -u $MYSQL_USER -p$MYSQL_PASSWORD $MYSQL_DATABASE < ticketplus_structure_20250711_165037.sql

echo "📦 2. Importando datos..."
mysql -h $MYSQL_HOST -P $MYSQL_PORT -u $MYSQL_USER -p$MYSQL_PASSWORD $MYSQL_DATABASE < ticketplus_data_20250711_165037.sql

echo "✅ Importación completada!"
echo "🌐 Base de datos lista en Railway"
