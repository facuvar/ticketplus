# 🚀 Guía de Deploy - Ticket+ en Railway

Esta guía te ayudará a desplegar el sistema Ticket+ en Railway con configuración automática de entorno.

## 📋 Prerequisitos

1. **Cuenta en Railway**: [railway.app](https://railway.app)
2. **CLI de Railway** (opcional): `npm install -g @railway/cli`
3. **Archivos de exportación**: Ejecutar `python export_db_to_railway.py` localmente

## 🌐 Paso 1: Crear Proyecto en Railway

### Desde Railway Dashboard:
1. **Ir a railway.app** y hacer login
2. **New Project** → **Deploy from GitHub repo**
3. **Conectar** tu repositorio `facuvar/ticketplus`
4. **Deploy Now**

## 🗄️ Paso 2: Configurar MySQL en Railway

1. **En el dashboard de Railway**, ir a tu proyecto
2. **Add Service** → **Database** → **MySQL**
3. **Railway generará automáticamente** las siguientes variables:
   - `MYSQLHOST`
   - `MYSQLPORT` 
   - `MYSQLUSER`
   - `MYSQLPASSWORD`
   - `MYSQLDATABASE`

## ⚙️ Paso 3: Variables de Entorno (Opcionales)

Agregar en Railway Dashboard → **Variables**:

```bash
# Opcional - para personalizar
SECRET_KEY=tu-clave-secreta-produccion-muy-segura
WHATSAPP_API_KEY=tu-api-key-whatsapp
WHATSAPP_PHONE_NUMBER=tu-numero-whatsapp
```

## 📦 Paso 4: Importar Datos

### Usando Railway CLI:
```bash
# Conectar a tu proyecto
railway connect

# Subir archivos de export (desde carpeta exports/)
# Ejecutar en el shell de Railway:
mysql -h $MYSQLHOST -P $MYSQLPORT -u $MYSQLUSER -p$MYSQLPASSWORD $MYSQLDATABASE < ticketplus_structure_TIMESTAMP.sql
mysql -h $MYSQLHOST -P $MYSQLPORT -u $MYSQLUSER -p$MYSQLPASSWORD $MYSQLDATABASE < ticketplus_data_TIMESTAMP.sql
```

## 🎯 Paso 5: Verificar Deploy

### Accesos después del deploy:
- 🌐 **Web App**: https://tu-app.railway.app
- 📊 **Dashboard**: https://tu-app.railway.app/api/v1/admin/dashboard/4
- 📖 **API Docs**: https://tu-app.railway.app/docs
- 🛒 **Carrito**: https://tu-app.railway.app/carrito.html

## 🔧 Configuración Automática Incluida

El sistema detecta automáticamente Railway y configura:

### ✅ Detección de entorno
```python
def is_railway() -> bool:
    return os.getenv("RAILWAY_ENVIRONMENT") is not None
```

### ✅ Base de Datos
- Conexión automática a MySQL de Railway
- URL construida desde variables de entorno
- Pool de conexiones optimizado para producción

### ✅ Servidor
- Host: `0.0.0.0` (todas las interfaces)
- Puerto: Variable `$PORT` de Railway
- Reload: Deshabilitado en producción
- Logs: Nivel INFO para Railway

## 📊 Funcionalidades Disponibles Post-Deploy

- ✅ **Dashboard responsive** (móvil + desktop)
- ✅ **Motor de recomendaciones IA**
- ✅ **Sistema códigos UPSELL** (UP-001-ORD-20250702-SIM-141550)
- ✅ **Integración WhatsApp**
- ✅ **API FastAPI** documentada
- ✅ **Métricas en tiempo real**
- ✅ **Gráficos interactivos**
- ✅ **Trazabilidad pedidos ORIGINAL vs UPSELL**

---

¡El sistema está optimizado para deploy automático en Railway! 🚀 