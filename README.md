# 🎯 Ticket+ - Sistema de Recomendaciones IA para Mayoristas

Sistema inteligente de recomendaciones que genera ingresos adicionales automáticamente mediante análisis de pedidos y sugerencias personalizadas vía WhatsApp.

## 🚀 Características Principales

### 📊 Dashboard Administrativo
- **Dashboard responsive** optimizado para móvil y desktop
- **Métricas en tiempo real** de ingresos por Ticket+
- **Gráficos interactivos** de pedidos e ingresos por días
- **Análisis de productos** más recomendados
- **Sistema de códigos UPSELL** con referencia a pedidos originales

### 🤖 Motor de Recomendaciones IA
- **Algoritmos multi-factor** basado en historial de compras
- **Análisis de patrones** de consumo por cliente
- **Generación automática** de carritos personalizados
- **Tokens únicos** con expiración configurable

### 📱 Integración WhatsApp
- **Envío automático** de recomendaciones
- **Links únicos** de carrito por cliente
- **Tracking de conversiones** y clicks
- **API WhatsApp** completamente integrada

### 🎯 Sistema de UPSELL Inteligente
- **Códigos únicos** tipo `UP-001-ORD-20250702-SIM-141550`
- **Trazabilidad completa** de pedidos originales vs UPSELL
- **Estadísticas de conversión** y ROI
- **Logística optimizada** para entregas coordinadas

## 🏗️ Arquitectura Técnica

### Backend
- **FastAPI** con Python 3.12
- **MySQL** como base de datos principal
- **SQLAlchemy** ORM con Alembic para migraciones
- **Pydantic** para validación de datos
- **API RESTful** completamente documentada

### Frontend
- **HTML5 + JavaScript vanilla** optimizado
- **Chart.js** para gráficos interactivos
- **Diseño responsive** con CSS Grid/Flexbox
- **PWA-ready** para instalación móvil

### Infraestructura
- **Railway** para deploy en producción
- **Detección automática** de entorno (local vs producción)
- **Variables de entorno** para configuración
- **MySQL** tanto local (XAMPP) como Railway

## 📦 Instalación y Configuración

### Requisitos Previos
- Python 3.12+
- MySQL (XAMPP recomendado para desarrollo)
- Git

### Instalación Local

1. **Clonar el repositorio**
```bash
git clone https://github.com/facuvar/ticketplus.git
cd ticketplus
```

2. **Instalar dependencias**
```bash
pip install -r requirements.txt
```

3. **Configurar base de datos MySQL**
```bash
# Iniciar XAMPP MySQL
# Crear base de datos: ticketplus_dev
```

4. **Ejecutar migraciones**
```bash
alembic upgrade head
```

5. **Poblar datos de prueba**
```bash
python populate_mysql.py
```

6. **Iniciar servidor**
```bash
python main.py
```

### Acceso a la Aplicación
- **Dashboard**: http://localhost:8000/api/v1/admin/dashboard
- **API Docs**: http://localhost:8000/docs
- **Carrito de prueba**: http://localhost:8000/carrito.html

## 🌐 Deploy en Railway

### Configuración Automática
El sistema detecta automáticamente si está ejecutándose en Railway mediante variables de entorno:

```python
def is_railway() -> bool:
    return os.getenv("RAILWAY_ENVIRONMENT") is not None
```

### Variables de Entorno para Railway
```bash
# Automáticas de Railway MySQL
MYSQLHOST=your-railway-mysql-host
MYSQLPORT=3306
MYSQLUSER=root
MYSQLPASSWORD=your-password
MYSQLDATABASE=railway

# Opcionales
SECRET_KEY=your-production-secret
WHATSAPP_API_KEY=your-whatsapp-key
WHATSAPP_PHONE_NUMBER=your-number
```

### Script de Migración de Datos
```bash
# Exportar datos locales
python export_db_to_railway.py

# Los archivos se generan en ./exports/
# Subir a Railway y ejecutar el script de importación
```

## 📊 Casos de Uso y Métricas

### Ejemplo de Ingresos Generados
- **Pedidos ORIGINAL**: Pedidos normales del cliente
- **Pedidos UPSELL**: Ingresos adicionales por Ticket+ ($13,500+ demostrados)
- **Conversión promedio**: 15-25% de recomendaciones enviadas
- **ROI típico**: 300-500% sobre inversión en el sistema

### Códigos de Ejemplo
```
ORIGINAL: ORD-20250702-SIM-141550
UPSELL:   UP-001-ORD-20250702-SIM-141550
          UP-002-ORD-20250702-SIM-141550
```

## 🔧 API Endpoints Principales

### Dashboard Admin
- `GET /api/v1/admin/dashboard/{mayorista_id}` - Métricas principales
- `GET /api/v1/admin/pedidos/{mayorista_id}` - Gestión de pedidos
- `GET /api/v1/admin/recomendaciones/{mayorista_id}` - Análisis recomendaciones

### Sistema de Carritos
- `POST /api/v1/carrito/generar` - Generar carrito personalizado
- `GET /api/v1/carrito/{token}` - Obtener carrito por token
- `POST /api/v1/carrito/{token}/confirmar` - Confirmar pedido UPSELL

### WhatsApp Integration
- `POST /api/v1/whatsapp/enviar-recomendaciones` - Envío automático
- `GET /api/v1/whatsapp/status/{mayorista_id}` - Estado de envíos

## 🎯 Funcionalidades Avanzadas

### Motor de Recomendaciones
```python
# Factores de análisis:
- Historial de compras del cliente
- Productos frecuentes por categoría  
- Estacionalidad y tendencias
- Margen de ganancia por producto
- Stock disponible
```

### Sistema de Códigos UPSELL
```python
# Formato: UP-XXX-ORD-FECHA-CLIENTE-TIMESTAMP
def generar_codigo_upsell(pedido_original):
    count = count_upsells_existentes(pedido_original.id)
    return f"UP-{count+1:03d}-{pedido_original.numero_pedido}"
```

## 📱 Responsive Design

### Mobile-First
- **Menú hamburguesa** para navegación móvil
- **Gráficos adaptivos** que se escalan automáticamente
- **Touch-friendly** interface para tablets
- **PWA capabilities** para instalación

### Desktop
- **Sidebar fijo** para navegación rápida
- **Dashboard de 2 columnas** optimizado
- **Gráficos de alta resolución**
- **Keyboard shortcuts** para power users

## 🔐 Seguridad y Configuración

### Tokens de Carrito
- **Expiración automática** (48 horas configurable)
- **UUID únicos** para cada carrito
- **Validación de mayorista** en cada request

### Base de Datos
- **Conexiones seguras** con certificados SSL en producción
- **Migraciones versionadas** con Alembic
- **Backup automático** incluido en scripts

## 🚧 Roadmap Futuro

### Próximas Funcionalidades
- [ ] **Analytics avanzados** con ML predictions
- [ ] **A/B testing** de recomendaciones
- [ ] **Integración con ERPs** populares
- [ ] **API de terceros** para conectar con otros sistemas
- [ ] **Dashboard white-label** personalizable

### Optimizaciones Técnicas
- [ ] **Redis caching** para consultas frecuentes
- [ ] **Websockets** para updates en tiempo real
- [ ] **Background jobs** con Celery
- [ ] **Docker containerization**

## 👥 Contribución

Este proyecto está desarrollado para mayoristas que buscan aumentar sus ingresos mediante recomendaciones inteligentes automatizadas.

## 📄 Licencia

Proyecto propietario - Todos los derechos reservados.

---

**Desarrollado con ❤️ para maximizar ingresos de mayoristas mediante IA** 