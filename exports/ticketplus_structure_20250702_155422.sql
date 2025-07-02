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

-- Dump completed on 2025-07-02 15:54:23
