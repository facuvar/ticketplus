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
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Dumping data for table `mayoristas`
--

LOCK TABLES `mayoristas` WRITE;
/*!40000 ALTER TABLE `mayoristas` DISABLE KEYS */;
INSERT INTO `mayoristas` (`id`, `nombre`, `email`, `telefono`, `gescom_db_host`, `gescom_db_port`, `gescom_db_name`, `gescom_db_user`, `gescom_db_password`, `whatsapp_api_key`, `whatsapp_phone_number`, `logo_url`, `color_primario`, `color_secundario`, `recomendaciones_activas`, `tiempo_espera_horas`, `max_productos_recomendados`, `reglas_recomendacion`, `activo`, `fecha_creacion`, `fecha_actualizacion`) VALUES (4,'Distribuidora Norte','admin@distribuidoranorte.com','+5491234567890','localhost',3306,'gescom_norte','gescom_user','gescom_pass','sk-1234567890abcdef','+5491234567890','https://via.placeholder.com/150x50?text=Norte','#4CAF50','#45a049',1,24,5,'\"mas_vendidos,historico_cliente\"',1,'2025-07-02 13:46:41',NULL),(5,'Mayorista Sur','contacto@mayoristasur.com','+5497654321098','localhost',3306,'gescom_sur','gescom_user','gescom_pass','sk-abcdef1234567890','+5497654321098','https://via.placeholder.com/150x50?text=Sur','#2196F3','#1976D2',1,48,3,'\"categoria_similar,manual\"',1,'2025-07-02 13:46:41',NULL);
/*!40000 ALTER TABLE `mayoristas` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping data for table `clientes`
--

LOCK TABLES `clientes` WRITE;
/*!40000 ALTER TABLE `clientes` DISABLE KEYS */;
INSERT INTO `clientes` (`id`, `gescom_cliente_id`, `nombre`, `email`, `telefono`, `direccion`, `mayorista_id`, `whatsapp_numero`, `acepta_whatsapp`, `activo`, `fecha_ultimo_pedido`, `total_pedidos`, `ticket_promedio`, `fecha_creacion`, `fecha_actualizacion`) VALUES (4,'CLI001','Almacén San Martín','almacen@sanmartin.com','+5491111111111','Av. San Martín 1234, Buenos Aires',4,'+5491111111111',1,1,'2025-06-29 13:46:41',15,1250,'2025-07-02 13:46:41',NULL),(5,'CLI002','Supermercado El Barrio','compras@elbarrio.com','+5492222222222','Calle Falsa 456, Córdoba',4,'+5492222222222',1,1,'2025-07-01 13:46:41',32,2101,'2025-07-02 13:46:41',NULL),(6,'CLI003','Kiosco Central','kiosco@central.com','+5493333333333','Plaza Central 789, Rosario',5,'+5493333333333',1,1,'2025-06-27 13:46:41',8,850,'2025-07-02 13:46:41',NULL),(9,'CLI-141550','Supermercado Los Alamos','gerente@losalamos.com','+5491156789012',NULL,4,'+5491156789012',1,1,'2025-07-02 14:15:50',1,8850,'2025-07-02 14:15:50',NULL);
/*!40000 ALTER TABLE `clientes` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping data for table `usuarios`
--

LOCK TABLES `usuarios` WRITE;
/*!40000 ALTER TABLE `usuarios` DISABLE KEYS */;
INSERT INTO `usuarios` (`id`, `email`, `nombre`, `apellido`, `hashed_password`, `mayorista_id`, `es_admin`, `activo`, `fecha_creacion`, `fecha_ultimo_acceso`) VALUES (3,'admin@distribuidoranorte.com','Admin Norte',NULL,'$2b$12$example_hash',4,1,1,'2025-07-02 13:46:41',NULL),(4,'admin@mayoristasur.com','Admin Sur',NULL,'$2b$12$example_hash',5,1,1,'2025-07-02 13:46:41',NULL);
/*!40000 ALTER TABLE `usuarios` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping data for table `productos`
--

LOCK TABLES `productos` WRITE;
/*!40000 ALTER TABLE `productos` DISABLE KEYS */;
INSERT INTO `productos` (`id`, `gescom_producto_id`, `codigo`, `nombre`, `descripcion`, `mayorista_id`, `categoria`, `marca`, `precio`, `stock`, `imagen_url`, `es_destacado`, `orden_recomendacion`, `activo_recomendaciones`, `veces_vendido`, `veces_recomendado`, `conversion_recomendacion`, `activo`, `fecha_creacion`, `fecha_actualizacion`) VALUES (11,'PROD001','ARR001','Arroz Gallo 1kg',NULL,4,NULL,NULL,850.00,0,NULL,0,0,1,0,0,0.00,1,'2025-07-02 13:46:41',NULL),(12,'PROD002','FID001','Fideos Matarazzo 500g',NULL,4,NULL,NULL,450.00,0,NULL,0,0,1,0,0,0.00,1,'2025-07-02 13:46:41',NULL),(13,'PROD003','ACE001','Aceite Natura 900ml',NULL,4,NULL,NULL,1250.00,0,NULL,0,0,1,0,0,0.00,1,'2025-07-02 13:46:41',NULL),(14,'PROD004','LEC001','Leche La Serenísima 1L',NULL,4,NULL,NULL,650.00,0,NULL,0,0,1,0,0,0.00,1,'2025-07-02 13:46:41',NULL),(15,'PROD005','PAN001','Pan Lactal Bimbo',NULL,4,NULL,NULL,420.00,0,NULL,0,0,1,0,0,0.00,1,'2025-07-02 13:46:41',NULL),(16,'PROD006','YOG001','Yogur Ser Natural 900g',NULL,4,NULL,NULL,890.00,0,NULL,0,0,1,0,0,0.00,1,'2025-07-02 13:46:41',NULL),(17,'PROD007','QUE001','Queso Cremoso Casancrem 300g',NULL,4,NULL,NULL,1350.00,0,NULL,0,0,1,0,0,0.00,1,'2025-07-02 13:46:41',NULL),(18,'PROD008','AZU001','Azúcar Ledesma 1kg',NULL,4,NULL,NULL,780.00,0,NULL,0,0,1,0,0,0.00,1,'2025-07-02 13:46:41',NULL),(19,'PROD009','CAF001','Café La Virginia 500g',NULL,5,NULL,NULL,2200.00,0,NULL,0,0,1,0,0,0.00,1,'2025-07-02 13:46:41',NULL),(20,'PROD010','GAL001','Galletitas Oreo 118g',NULL,5,NULL,NULL,950.00,0,NULL,0,0,1,0,0,0.00,1,'2025-07-02 13:46:41',NULL);
/*!40000 ALTER TABLE `productos` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping data for table `pedidos`
--

LOCK TABLES `pedidos` WRITE;
/*!40000 ALTER TABLE `pedidos` DISABLE KEYS */;
INSERT INTO `pedidos` (`id`, `gescom_pedido_id`, `numero_pedido`, `mayorista_id`, `cliente_id`, `tipo`, `estado`, `subtotal`, `descuento`, `impuestos`, `total`, `observaciones`, `direccion_envio`, `recomendaciones_enviadas`, `fecha_envio_recomendaciones`, `token_carrito`, `token_expiracion`, `click_whatsapp`, `fecha_click_whatsapp`, `conversion_upsell`, `monto_upsell`, `fecha_pedido`, `fecha_creacion`, `fecha_actualizacion`, `pedido_original_id`, `codigo_referencia`) VALUES (1,'PED001','ORD-2025-001',4,4,'ORIGINAL','ENTREGADO',1300.00,0.00,236.70,1536.70,'Pedido de prueba','Av. San Martín 1234, Buenos Aires',1,'2025-07-02 11:46:41','PED001','2025-07-03 13:54:32',0,NULL,0,0.00,'2025-07-01 13:46:41','2025-07-02 13:46:41',NULL,NULL,NULL),(2,'UPSELL001','UP-2025-001',4,4,'UPSELL','ENTREGADO',2500.00,NULL,NULL,2500.00,NULL,NULL,NULL,NULL,'UP001','2025-07-03 14:08:33',NULL,NULL,NULL,NULL,'2025-07-02 14:08:33','2025-07-02 14:08:33',NULL,NULL,NULL),(3,'UPSELL001','UP-001',4,4,'UPSELL','ENTREGADO',2500.00,NULL,NULL,2500.00,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'2025-07-02 14:08:44','2025-07-02 14:08:44',NULL,NULL,NULL),(4,'UPSELL001','UP-001',4,4,'UPSELL','ENTREGADO',2500.00,NULL,NULL,2500.00,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'2025-07-02 14:09:21','2025-07-02 14:09:21',NULL,NULL,NULL),(5,'UPSELL002','UP-002',4,5,'UPSELL','ENTREGADO',1850.00,NULL,NULL,1850.00,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'2025-07-01 14:09:21','2025-07-02 14:09:21',NULL,NULL,NULL),(6,'UPSELL003','UP-003',4,6,'UPSELL','ENTREGADO',3200.00,NULL,NULL,3200.00,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'2025-06-30 14:09:21','2025-07-02 14:09:21',NULL,NULL,NULL),(7,'UPSELL004','UP-004',4,4,'UPSELL','ENTREGADO',950.00,NULL,NULL,950.00,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'2025-06-29 14:09:21','2025-07-02 14:09:21',NULL,NULL,NULL),(9,'SIM-141550','ORD-20250702-SIM-141550',4,9,'ORIGINAL','PROCESANDO',8850.00,0.00,0.00,8850.00,NULL,'Av. Los Alamos 456, Zona Norte',1,'2025-07-02 14:15:50','YB7G80YpU2__GGauJoKNMZML5c2ET6CdtJD9IShHQsI','2025-07-02 23:59:59',0,NULL,0,0.00,'2025-07-02 14:15:50','2025-07-02 14:15:50','2025-07-02 14:15:50',NULL,NULL),(10,'GESCOM_UPSELL_1_20250702_154556','UP-001-ORD-20250702-SIM-141550',4,9,'UPSELL','PENDIENTE',200.00,0.00,42.00,242.00,'Pedido UPSELL generado por recomendaciones de Ticket+ - Referencia: ORD-20250702-SIM-141550','Av. Los Alamos 456, Zona Norte',0,NULL,NULL,NULL,0,NULL,0,0.00,'2025-07-02 15:45:58','2025-07-02 15:45:58',NULL,9,'ORD-20250702-SIM-141550'),(11,'GESCOM_UPSELL_2_20250702_154558','UP-002-ORD-20250702-SIM-141550',4,9,'UPSELL','PENDIENTE',250.00,0.00,52.50,302.50,'Pedido UPSELL generado por recomendaciones de Ticket+ - Referencia: ORD-20250702-SIM-141550','Av. Los Alamos 456, Zona Norte',0,NULL,NULL,NULL,0,NULL,0,0.00,'2025-07-02 15:46:01','2025-07-02 15:46:01',NULL,9,'ORD-20250702-SIM-141550'),(12,'GESCOM_UPSELL_3_20250702_154601','UP-003-ORD-20250702-SIM-141550',4,9,'UPSELL','PENDIENTE',300.00,0.00,63.00,363.00,'Pedido UPSELL generado por recomendaciones de Ticket+ - Referencia: ORD-20250702-SIM-141550','Av. Los Alamos 456, Zona Norte',0,NULL,NULL,NULL,0,NULL,0,0.00,'2025-07-02 15:46:03','2025-07-02 15:46:03',NULL,9,'ORD-20250702-SIM-141550');
/*!40000 ALTER TABLE `pedidos` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping data for table `items_pedido`
--

LOCK TABLES `items_pedido` WRITE;
/*!40000 ALTER TABLE `items_pedido` DISABLE KEYS */;
INSERT INTO `items_pedido` (`id`, `pedido_id`, `producto_id`, `cantidad`, `precio_unitario`, `descuento`, `subtotal`, `producto_codigo`, `producto_nombre`) VALUES (1,1,11,1,850.00,0.00,850.00,'ARR001','Arroz Gallo 1kg'),(2,1,12,1,450.00,0.00,450.00,'FID001','Fideos Matarazzo 500g'),(3,9,13,3,1250.00,0.00,3750.00,'ACE001','Aceite Girasol Natura 900ml'),(4,9,11,2,850.00,0.00,1700.00,'LEG001','Lentejas Secas 500g'),(5,9,11,4,1100.00,0.00,4400.00,'ARR001','Arroz Largo Fino 1kg');
/*!40000 ALTER TABLE `items_pedido` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping data for table `recomendaciones`
--

LOCK TABLES `recomendaciones` WRITE;
/*!40000 ALTER TABLE `recomendaciones` DISABLE KEYS */;
INSERT INTO `recomendaciones` (`id`, `pedido_id`, `producto_id`, `mayorista_id`, `tipo`, `estado`, `orden`, `score`, `razon`, `producto_nombre`, `producto_precio`, `producto_imagen_url`, `fue_clickeada`, `fecha_click`, `fue_agregada_carrito`, `fecha_agregada_carrito`, `cantidad_agregada`, `monto_convertido`, `fecha_generacion`, `fecha_envio`) VALUES (1,1,13,4,'MAS_VENDIDOS','ENVIADA',1,98.50,'Producto más vendido con arroz y fideos','Aceite Natura 900ml',1250.00,NULL,0,NULL,0,NULL,0,0.00,'2025-07-02 11:46:41','2025-07-02 11:46:41'),(2,1,14,4,'MAS_VENDIDOS','ENVIADA',2,95.00,'Excelente para acompañar tus comidas','Leche La Serenísima 1L',650.00,NULL,0,NULL,0,NULL,0,0.00,'2025-07-02 11:46:41','2025-07-02 11:46:41'),(3,1,15,4,'MAS_VENDIDOS','ENVIADA',3,90.00,'Perfecto para el desayuno','Pan Lactal Bimbo',420.00,NULL,0,NULL,0,NULL,0,0.00,'2025-07-02 11:46:41','2025-07-02 11:46:41'),(4,1,16,4,'MAS_VENDIDOS','ENVIADA',4,88.00,'Producto más vendido este mes','Yogur Ser Natural 900g',890.00,NULL,0,NULL,0,NULL,0,0.00,'2025-07-02 11:46:41','2025-07-02 11:46:41'),(5,1,17,4,'MAS_VENDIDOS','ENVIADA',5,85.00,'Ideal para sandwich y comidas','Queso Cremoso Casancrem 300g',1350.00,NULL,0,NULL,0,NULL,0,0.00,'2025-07-02 11:46:41','2025-07-02 11:46:41'),(6,9,11,4,'REGLA_PERSONALIZADA','GENERADA',1,28.00,'Basado en tu historial de compras','Arroz Gallo 1kg',850.00,NULL,0,NULL,0,NULL,0,0.00,'2025-07-02 14:15:50',NULL),(7,9,12,4,'REGLA_PERSONALIZADA','GENERADA',2,28.00,'Basado en tu historial de compras','Fideos Matarazzo 500g',450.00,NULL,0,NULL,0,NULL,0,0.00,'2025-07-02 14:15:50',NULL),(8,9,13,4,'REGLA_PERSONALIZADA','GENERADA',3,28.00,'Complementa perfecto con tu pedido','Aceite Natura 900ml',1250.00,NULL,0,NULL,0,NULL,0,0.00,'2025-07-02 14:15:50',NULL),(9,9,14,4,'REGLA_PERSONALIZADA','GENERADA',4,28.00,'Basado en tu historial de compras','Leche La Serenísima 1L',650.00,NULL,0,NULL,0,NULL,0,0.00,'2025-07-02 14:15:50',NULL),(10,9,15,4,'REGLA_PERSONALIZADA','GENERADA',5,28.00,'Complementa perfecto con tu pedido','Pan Lactal Bimbo',420.00,NULL,0,NULL,0,NULL,0,0.00,'2025-07-02 14:15:50',NULL),(11,9,16,4,'REGLA_PERSONALIZADA','GENERADA',6,28.00,'Basado en tu historial de compras','Yogur Ser Natural 900g',890.00,NULL,0,NULL,0,NULL,0,0.00,'2025-07-02 14:15:50',NULL);
/*!40000 ALTER TABLE `recomendaciones` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-07-02 15:55:14
