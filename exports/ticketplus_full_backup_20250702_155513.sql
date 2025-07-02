-- MariaDB dump 10.19  Distrib 10.4.32-MariaDB, for Win64 (AMD64)
--
-- Host: localhost    Database: ticketplus_dev
-- ------------------------------------------------------
-- Server version	10.4.32-MariaDB

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `alembic_version`
--

DROP TABLE IF EXISTS `alembic_version`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `alembic_version` (
  `version_num` varchar(32) NOT NULL,
  PRIMARY KEY (`version_num`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `alembic_version`
--

LOCK TABLES `alembic_version` WRITE;
/*!40000 ALTER TABLE `alembic_version` DISABLE KEYS */;
INSERT INTO `alembic_version` VALUES ('4432e085e1dc');
/*!40000 ALTER TABLE `alembic_version` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `clientes`
--

DROP TABLE IF EXISTS `clientes`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `clientes` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `gescom_cliente_id` varchar(50) NOT NULL,
  `nombre` varchar(255) NOT NULL,
  `email` varchar(255) DEFAULT NULL,
  `telefono` varchar(50) DEFAULT NULL,
  `direccion` text DEFAULT NULL,
  `mayorista_id` int(11) NOT NULL,
  `whatsapp_numero` varchar(50) DEFAULT NULL,
  `acepta_whatsapp` tinyint(1) DEFAULT NULL,
  `activo` tinyint(1) DEFAULT NULL,
  `fecha_ultimo_pedido` datetime DEFAULT NULL,
  `total_pedidos` int(11) DEFAULT NULL,
  `ticket_promedio` int(11) DEFAULT NULL,
  `fecha_creacion` datetime DEFAULT current_timestamp(),
  `fecha_actualizacion` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `mayorista_id` (`mayorista_id`),
  KEY `ix_clientes_gescom_cliente_id` (`gescom_cliente_id`),
  KEY `ix_clientes_id` (`id`),
  CONSTRAINT `clientes_ibfk_1` FOREIGN KEY (`mayorista_id`) REFERENCES `mayoristas` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=10 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `clientes`
--

LOCK TABLES `clientes` WRITE;
/*!40000 ALTER TABLE `clientes` DISABLE KEYS */;
INSERT INTO `clientes` VALUES (4,'CLI001','Almacén San Martín','almacen@sanmartin.com','+5491111111111','Av. San Martín 1234, Buenos Aires',4,'+5491111111111',1,1,'2025-06-29 13:46:41',15,1250,'2025-07-02 13:46:41',NULL),(5,'CLI002','Supermercado El Barrio','compras@elbarrio.com','+5492222222222','Calle Falsa 456, Córdoba',4,'+5492222222222',1,1,'2025-07-01 13:46:41',32,2101,'2025-07-02 13:46:41',NULL),(6,'CLI003','Kiosco Central','kiosco@central.com','+5493333333333','Plaza Central 789, Rosario',5,'+5493333333333',1,1,'2025-06-27 13:46:41',8,850,'2025-07-02 13:46:41',NULL),(9,'CLI-141550','Supermercado Los Alamos','gerente@losalamos.com','+5491156789012',NULL,4,'+5491156789012',1,1,'2025-07-02 14:15:50',1,8850,'2025-07-02 14:15:50',NULL);
/*!40000 ALTER TABLE `clientes` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `items_pedido`
--

DROP TABLE IF EXISTS `items_pedido`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `items_pedido` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `pedido_id` int(11) NOT NULL,
  `producto_id` int(11) NOT NULL,
  `cantidad` int(11) NOT NULL,
  `precio_unitario` decimal(10,2) NOT NULL,
  `descuento` decimal(10,2) DEFAULT NULL,
  `subtotal` decimal(10,2) NOT NULL,
  `producto_codigo` varchar(100) DEFAULT NULL,
  `producto_nombre` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `pedido_id` (`pedido_id`),
  KEY `producto_id` (`producto_id`),
  KEY `ix_items_pedido_id` (`id`),
  CONSTRAINT `items_pedido_ibfk_1` FOREIGN KEY (`pedido_id`) REFERENCES `pedidos` (`id`),
  CONSTRAINT `items_pedido_ibfk_2` FOREIGN KEY (`producto_id`) REFERENCES `productos` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `items_pedido`
--

LOCK TABLES `items_pedido` WRITE;
/*!40000 ALTER TABLE `items_pedido` DISABLE KEYS */;
INSERT INTO `items_pedido` VALUES (1,1,11,1,850.00,0.00,850.00,'ARR001','Arroz Gallo 1kg'),(2,1,12,1,450.00,0.00,450.00,'FID001','Fideos Matarazzo 500g'),(3,9,13,3,1250.00,0.00,3750.00,'ACE001','Aceite Girasol Natura 900ml'),(4,9,11,2,850.00,0.00,1700.00,'LEG001','Lentejas Secas 500g'),(5,9,11,4,1100.00,0.00,4400.00,'ARR001','Arroz Largo Fino 1kg');
/*!40000 ALTER TABLE `items_pedido` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `mayoristas`
--

DROP TABLE IF EXISTS `mayoristas`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `mayoristas` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `nombre` varchar(255) NOT NULL,
  `email` varchar(255) NOT NULL,
  `telefono` varchar(50) DEFAULT NULL,
  `gescom_db_host` varchar(255) DEFAULT NULL,
  `gescom_db_port` int(11) DEFAULT NULL,
  `gescom_db_name` varchar(255) DEFAULT NULL,
  `gescom_db_user` varchar(255) DEFAULT NULL,
  `gescom_db_password` varchar(255) DEFAULT NULL,
  `whatsapp_api_key` varchar(500) DEFAULT NULL,
  `whatsapp_phone_number` varchar(50) DEFAULT NULL,
  `logo_url` varchar(500) DEFAULT NULL,
  `color_primario` varchar(7) DEFAULT NULL,
  `color_secundario` varchar(7) DEFAULT NULL,
  `recomendaciones_activas` tinyint(1) DEFAULT NULL,
  `tiempo_espera_horas` int(11) DEFAULT NULL,
  `max_productos_recomendados` int(11) DEFAULT NULL,
  `reglas_recomendacion` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL CHECK (json_valid(`reglas_recomendacion`)),
  `activo` tinyint(1) DEFAULT NULL,
  `fecha_creacion` datetime DEFAULT current_timestamp(),
  `fecha_actualizacion` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `ix_mayoristas_email` (`email`),
  KEY `ix_mayoristas_id` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `mayoristas`
--

LOCK TABLES `mayoristas` WRITE;
/*!40000 ALTER TABLE `mayoristas` DISABLE KEYS */;
INSERT INTO `mayoristas` VALUES (4,'Distribuidora Norte','admin@distribuidoranorte.com','+5491234567890','localhost',3306,'gescom_norte','gescom_user','gescom_pass','sk-1234567890abcdef','+5491234567890','https://via.placeholder.com/150x50?text=Norte','#4CAF50','#45a049',1,24,5,'\"mas_vendidos,historico_cliente\"',1,'2025-07-02 13:46:41',NULL),(5,'Mayorista Sur','contacto@mayoristasur.com','+5497654321098','localhost',3306,'gescom_sur','gescom_user','gescom_pass','sk-abcdef1234567890','+5497654321098','https://via.placeholder.com/150x50?text=Sur','#2196F3','#1976D2',1,48,3,'\"categoria_similar,manual\"',1,'2025-07-02 13:46:41',NULL);
/*!40000 ALTER TABLE `mayoristas` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `pedidos`
--

DROP TABLE IF EXISTS `pedidos`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `pedidos` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `gescom_pedido_id` varchar(50) NOT NULL,
  `numero_pedido` varchar(100) NOT NULL,
  `mayorista_id` int(11) NOT NULL,
  `cliente_id` int(11) NOT NULL,
  `tipo` enum('ORIGINAL','UPSELL') DEFAULT NULL,
  `estado` enum('PENDIENTE','PROCESANDO','ENVIADO','ENTREGADO','CANCELADO') DEFAULT NULL,
  `subtotal` decimal(10,2) NOT NULL,
  `descuento` decimal(10,2) DEFAULT NULL,
  `impuestos` decimal(10,2) DEFAULT NULL,
  `total` decimal(10,2) NOT NULL,
  `observaciones` text DEFAULT NULL,
  `direccion_envio` text DEFAULT NULL,
  `recomendaciones_enviadas` tinyint(1) DEFAULT NULL,
  `fecha_envio_recomendaciones` datetime DEFAULT NULL,
  `token_carrito` varchar(255) DEFAULT NULL,
  `token_expiracion` datetime DEFAULT NULL,
  `click_whatsapp` tinyint(1) DEFAULT NULL,
  `fecha_click_whatsapp` datetime DEFAULT NULL,
  `conversion_upsell` tinyint(1) DEFAULT NULL,
  `monto_upsell` decimal(10,2) DEFAULT NULL,
  `fecha_pedido` datetime NOT NULL,
  `fecha_creacion` datetime DEFAULT current_timestamp(),
  `fecha_actualizacion` datetime DEFAULT NULL,
  `pedido_original_id` int(11) DEFAULT NULL,
  `codigo_referencia` varchar(200) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `ix_pedidos_token_carrito` (`token_carrito`),
  KEY `cliente_id` (`cliente_id`),
  KEY `mayorista_id` (`mayorista_id`),
  KEY `ix_pedidos_gescom_pedido_id` (`gescom_pedido_id`),
  KEY `ix_pedidos_id` (`id`),
  KEY `pedido_original_id` (`pedido_original_id`),
  CONSTRAINT `pedidos_ibfk_1` FOREIGN KEY (`cliente_id`) REFERENCES `clientes` (`id`),
  CONSTRAINT `pedidos_ibfk_2` FOREIGN KEY (`mayorista_id`) REFERENCES `mayoristas` (`id`),
  CONSTRAINT `pedidos_ibfk_3` FOREIGN KEY (`pedido_original_id`) REFERENCES `pedidos` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=13 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `pedidos`
--

LOCK TABLES `pedidos` WRITE;
/*!40000 ALTER TABLE `pedidos` DISABLE KEYS */;
INSERT INTO `pedidos` VALUES (1,'PED001','ORD-2025-001',4,4,'ORIGINAL','ENTREGADO',1300.00,0.00,236.70,1536.70,'Pedido de prueba','Av. San Martín 1234, Buenos Aires',1,'2025-07-02 11:46:41','PED001','2025-07-03 13:54:32',0,NULL,0,0.00,'2025-07-01 13:46:41','2025-07-02 13:46:41',NULL,NULL,NULL),(2,'UPSELL001','UP-2025-001',4,4,'UPSELL','ENTREGADO',2500.00,NULL,NULL,2500.00,NULL,NULL,NULL,NULL,'UP001','2025-07-03 14:08:33',NULL,NULL,NULL,NULL,'2025-07-02 14:08:33','2025-07-02 14:08:33',NULL,NULL,NULL),(3,'UPSELL001','UP-001',4,4,'UPSELL','ENTREGADO',2500.00,NULL,NULL,2500.00,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'2025-07-02 14:08:44','2025-07-02 14:08:44',NULL,NULL,NULL),(4,'UPSELL001','UP-001',4,4,'UPSELL','ENTREGADO',2500.00,NULL,NULL,2500.00,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'2025-07-02 14:09:21','2025-07-02 14:09:21',NULL,NULL,NULL),(5,'UPSELL002','UP-002',4,5,'UPSELL','ENTREGADO',1850.00,NULL,NULL,1850.00,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'2025-07-01 14:09:21','2025-07-02 14:09:21',NULL,NULL,NULL),(6,'UPSELL003','UP-003',4,6,'UPSELL','ENTREGADO',3200.00,NULL,NULL,3200.00,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'2025-06-30 14:09:21','2025-07-02 14:09:21',NULL,NULL,NULL),(7,'UPSELL004','UP-004',4,4,'UPSELL','ENTREGADO',950.00,NULL,NULL,950.00,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'2025-06-29 14:09:21','2025-07-02 14:09:21',NULL,NULL,NULL),(9,'SIM-141550','ORD-20250702-SIM-141550',4,9,'ORIGINAL','PROCESANDO',8850.00,0.00,0.00,8850.00,NULL,'Av. Los Alamos 456, Zona Norte',1,'2025-07-02 14:15:50','YB7G80YpU2__GGauJoKNMZML5c2ET6CdtJD9IShHQsI','2025-07-02 23:59:59',0,NULL,0,0.00,'2025-07-02 14:15:50','2025-07-02 14:15:50','2025-07-02 14:15:50',NULL,NULL),(10,'GESCOM_UPSELL_1_20250702_154556','UP-001-ORD-20250702-SIM-141550',4,9,'UPSELL','PENDIENTE',200.00,0.00,42.00,242.00,'Pedido UPSELL generado por recomendaciones de Ticket+ - Referencia: ORD-20250702-SIM-141550','Av. Los Alamos 456, Zona Norte',0,NULL,NULL,NULL,0,NULL,0,0.00,'2025-07-02 15:45:58','2025-07-02 15:45:58',NULL,9,'ORD-20250702-SIM-141550'),(11,'GESCOM_UPSELL_2_20250702_154558','UP-002-ORD-20250702-SIM-141550',4,9,'UPSELL','PENDIENTE',250.00,0.00,52.50,302.50,'Pedido UPSELL generado por recomendaciones de Ticket+ - Referencia: ORD-20250702-SIM-141550','Av. Los Alamos 456, Zona Norte',0,NULL,NULL,NULL,0,NULL,0,0.00,'2025-07-02 15:46:01','2025-07-02 15:46:01',NULL,9,'ORD-20250702-SIM-141550'),(12,'GESCOM_UPSELL_3_20250702_154601','UP-003-ORD-20250702-SIM-141550',4,9,'UPSELL','PENDIENTE',300.00,0.00,63.00,363.00,'Pedido UPSELL generado por recomendaciones de Ticket+ - Referencia: ORD-20250702-SIM-141550','Av. Los Alamos 456, Zona Norte',0,NULL,NULL,NULL,0,NULL,0,0.00,'2025-07-02 15:46:03','2025-07-02 15:46:03',NULL,9,'ORD-20250702-SIM-141550');
/*!40000 ALTER TABLE `pedidos` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `productos`
--

DROP TABLE IF EXISTS `productos`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `productos` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `gescom_producto_id` varchar(50) NOT NULL,
  `codigo` varchar(100) NOT NULL,
  `nombre` varchar(255) NOT NULL,
  `descripcion` text DEFAULT NULL,
  `mayorista_id` int(11) NOT NULL,
  `categoria` varchar(255) DEFAULT NULL,
  `marca` varchar(255) DEFAULT NULL,
  `precio` decimal(10,2) DEFAULT NULL,
  `stock` int(11) DEFAULT NULL,
  `imagen_url` varchar(500) DEFAULT NULL,
  `es_destacado` tinyint(1) DEFAULT NULL,
  `orden_recomendacion` int(11) DEFAULT NULL,
  `activo_recomendaciones` tinyint(1) DEFAULT NULL,
  `veces_vendido` int(11) DEFAULT NULL,
  `veces_recomendado` int(11) DEFAULT NULL,
  `conversion_recomendacion` decimal(5,2) DEFAULT NULL,
  `activo` tinyint(1) DEFAULT NULL,
  `fecha_creacion` datetime DEFAULT current_timestamp(),
  `fecha_actualizacion` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `mayorista_id` (`mayorista_id`),
  KEY `ix_productos_codigo` (`codigo`),
  KEY `ix_productos_gescom_producto_id` (`gescom_producto_id`),
  KEY `ix_productos_id` (`id`),
  CONSTRAINT `productos_ibfk_1` FOREIGN KEY (`mayorista_id`) REFERENCES `mayoristas` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=21 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `productos`
--

LOCK TABLES `productos` WRITE;
/*!40000 ALTER TABLE `productos` DISABLE KEYS */;
INSERT INTO `productos` VALUES (11,'PROD001','ARR001','Arroz Gallo 1kg',NULL,4,NULL,NULL,850.00,0,NULL,0,0,1,0,0,0.00,1,'2025-07-02 13:46:41',NULL),(12,'PROD002','FID001','Fideos Matarazzo 500g',NULL,4,NULL,NULL,450.00,0,NULL,0,0,1,0,0,0.00,1,'2025-07-02 13:46:41',NULL),(13,'PROD003','ACE001','Aceite Natura 900ml',NULL,4,NULL,NULL,1250.00,0,NULL,0,0,1,0,0,0.00,1,'2025-07-02 13:46:41',NULL),(14,'PROD004','LEC001','Leche La Serenísima 1L',NULL,4,NULL,NULL,650.00,0,NULL,0,0,1,0,0,0.00,1,'2025-07-02 13:46:41',NULL),(15,'PROD005','PAN001','Pan Lactal Bimbo',NULL,4,NULL,NULL,420.00,0,NULL,0,0,1,0,0,0.00,1,'2025-07-02 13:46:41',NULL),(16,'PROD006','YOG001','Yogur Ser Natural 900g',NULL,4,NULL,NULL,890.00,0,NULL,0,0,1,0,0,0.00,1,'2025-07-02 13:46:41',NULL),(17,'PROD007','QUE001','Queso Cremoso Casancrem 300g',NULL,4,NULL,NULL,1350.00,0,NULL,0,0,1,0,0,0.00,1,'2025-07-02 13:46:41',NULL),(18,'PROD008','AZU001','Azúcar Ledesma 1kg',NULL,4,NULL,NULL,780.00,0,NULL,0,0,1,0,0,0.00,1,'2025-07-02 13:46:41',NULL),(19,'PROD009','CAF001','Café La Virginia 500g',NULL,5,NULL,NULL,2200.00,0,NULL,0,0,1,0,0,0.00,1,'2025-07-02 13:46:41',NULL),(20,'PROD010','GAL001','Galletitas Oreo 118g',NULL,5,NULL,NULL,950.00,0,NULL,0,0,1,0,0,0.00,1,'2025-07-02 13:46:41',NULL);
/*!40000 ALTER TABLE `productos` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `recomendaciones`
--

DROP TABLE IF EXISTS `recomendaciones`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `recomendaciones` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `pedido_id` int(11) NOT NULL,
  `producto_id` int(11) NOT NULL,
  `mayorista_id` int(11) NOT NULL,
  `tipo` enum('MAS_VENDIDOS','HISTORICO_CLIENTE','CATEGORIA_SIMILAR','REGLA_PERSONALIZADA','MANUAL') NOT NULL,
  `estado` enum('GENERADA','ENVIADA','CLICKEADA','CONVERTIDA','IGNORADA') DEFAULT NULL,
  `orden` int(11) DEFAULT NULL,
  `score` decimal(5,2) DEFAULT NULL,
  `razon` text DEFAULT NULL,
  `producto_nombre` varchar(255) DEFAULT NULL,
  `producto_precio` decimal(10,2) DEFAULT NULL,
  `producto_imagen_url` varchar(500) DEFAULT NULL,
  `fue_clickeada` tinyint(1) DEFAULT NULL,
  `fecha_click` datetime DEFAULT NULL,
  `fue_agregada_carrito` tinyint(1) DEFAULT NULL,
  `fecha_agregada_carrito` datetime DEFAULT NULL,
  `cantidad_agregada` int(11) DEFAULT NULL,
  `monto_convertido` decimal(10,2) DEFAULT NULL,
  `fecha_generacion` datetime DEFAULT current_timestamp(),
  `fecha_envio` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `mayorista_id` (`mayorista_id`),
  KEY `pedido_id` (`pedido_id`),
  KEY `producto_id` (`producto_id`),
  KEY `ix_recomendaciones_id` (`id`),
  CONSTRAINT `recomendaciones_ibfk_1` FOREIGN KEY (`mayorista_id`) REFERENCES `mayoristas` (`id`),
  CONSTRAINT `recomendaciones_ibfk_2` FOREIGN KEY (`pedido_id`) REFERENCES `pedidos` (`id`),
  CONSTRAINT `recomendaciones_ibfk_3` FOREIGN KEY (`producto_id`) REFERENCES `productos` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=12 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `recomendaciones`
--

LOCK TABLES `recomendaciones` WRITE;
/*!40000 ALTER TABLE `recomendaciones` DISABLE KEYS */;
INSERT INTO `recomendaciones` VALUES (1,1,13,4,'MAS_VENDIDOS','ENVIADA',1,98.50,'Producto más vendido con arroz y fideos','Aceite Natura 900ml',1250.00,NULL,0,NULL,0,NULL,0,0.00,'2025-07-02 11:46:41','2025-07-02 11:46:41'),(2,1,14,4,'MAS_VENDIDOS','ENVIADA',2,95.00,'Excelente para acompañar tus comidas','Leche La Serenísima 1L',650.00,NULL,0,NULL,0,NULL,0,0.00,'2025-07-02 11:46:41','2025-07-02 11:46:41'),(3,1,15,4,'MAS_VENDIDOS','ENVIADA',3,90.00,'Perfecto para el desayuno','Pan Lactal Bimbo',420.00,NULL,0,NULL,0,NULL,0,0.00,'2025-07-02 11:46:41','2025-07-02 11:46:41'),(4,1,16,4,'MAS_VENDIDOS','ENVIADA',4,88.00,'Producto más vendido este mes','Yogur Ser Natural 900g',890.00,NULL,0,NULL,0,NULL,0,0.00,'2025-07-02 11:46:41','2025-07-02 11:46:41'),(5,1,17,4,'MAS_VENDIDOS','ENVIADA',5,85.00,'Ideal para sandwich y comidas','Queso Cremoso Casancrem 300g',1350.00,NULL,0,NULL,0,NULL,0,0.00,'2025-07-02 11:46:41','2025-07-02 11:46:41'),(6,9,11,4,'REGLA_PERSONALIZADA','GENERADA',1,28.00,'Basado en tu historial de compras','Arroz Gallo 1kg',850.00,NULL,0,NULL,0,NULL,0,0.00,'2025-07-02 14:15:50',NULL),(7,9,12,4,'REGLA_PERSONALIZADA','GENERADA',2,28.00,'Basado en tu historial de compras','Fideos Matarazzo 500g',450.00,NULL,0,NULL,0,NULL,0,0.00,'2025-07-02 14:15:50',NULL),(8,9,13,4,'REGLA_PERSONALIZADA','GENERADA',3,28.00,'Complementa perfecto con tu pedido','Aceite Natura 900ml',1250.00,NULL,0,NULL,0,NULL,0,0.00,'2025-07-02 14:15:50',NULL),(9,9,14,4,'REGLA_PERSONALIZADA','GENERADA',4,28.00,'Basado en tu historial de compras','Leche La Serenísima 1L',650.00,NULL,0,NULL,0,NULL,0,0.00,'2025-07-02 14:15:50',NULL),(10,9,15,4,'REGLA_PERSONALIZADA','GENERADA',5,28.00,'Complementa perfecto con tu pedido','Pan Lactal Bimbo',420.00,NULL,0,NULL,0,NULL,0,0.00,'2025-07-02 14:15:50',NULL),(11,9,16,4,'REGLA_PERSONALIZADA','GENERADA',6,28.00,'Basado en tu historial de compras','Yogur Ser Natural 900g',890.00,NULL,0,NULL,0,NULL,0,0.00,'2025-07-02 14:15:50',NULL);
/*!40000 ALTER TABLE `recomendaciones` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `usuarios`
--

DROP TABLE IF EXISTS `usuarios`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `usuarios` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `email` varchar(255) NOT NULL,
  `nombre` varchar(255) NOT NULL,
  `apellido` varchar(255) DEFAULT NULL,
  `hashed_password` varchar(255) NOT NULL,
  `mayorista_id` int(11) NOT NULL,
  `es_admin` tinyint(1) DEFAULT NULL,
  `activo` tinyint(1) DEFAULT NULL,
  `fecha_creacion` datetime DEFAULT current_timestamp(),
  `fecha_ultimo_acceso` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `ix_usuarios_email` (`email`),
  KEY `mayorista_id` (`mayorista_id`),
  KEY `ix_usuarios_id` (`id`),
  CONSTRAINT `usuarios_ibfk_1` FOREIGN KEY (`mayorista_id`) REFERENCES `mayoristas` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `usuarios`
--

LOCK TABLES `usuarios` WRITE;
/*!40000 ALTER TABLE `usuarios` DISABLE KEYS */;
INSERT INTO `usuarios` VALUES (3,'admin@distribuidoranorte.com','Admin Norte',NULL,'$2b$12$example_hash',4,1,1,'2025-07-02 13:46:41',NULL),(4,'admin@mayoristasur.com','Admin Sur',NULL,'$2b$12$example_hash',5,1,1,'2025-07-02 13:46:41',NULL);
/*!40000 ALTER TABLE `usuarios` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping routines for database 'ticketplus_dev'
--
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-07-02 15:55:14
