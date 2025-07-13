
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
