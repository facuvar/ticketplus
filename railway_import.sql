-- Railway Import Script para Ticket+
-- Este archivo importará toda la estructura y datos de la base de datos

-- Crear base de datos si no existe
CREATE DATABASE IF NOT EXISTS railway;
USE railway;

-- Eliminar tablas si existen (para evitar conflictos)
DROP TABLE IF EXISTS recomendaciones;
DROP TABLE IF EXISTS items_pedido;
DROP TABLE IF EXISTS pedidos;
DROP TABLE IF EXISTS clientes;
DROP TABLE IF EXISTS productos;
DROP TABLE IF EXISTS mayoristas;
DROP TABLE IF EXISTS usuarios;
DROP TABLE IF EXISTS ventas_gescom;
DROP TABLE IF EXISTS combos_gescom;
DROP TABLE IF EXISTS clientes_gescom;

-- Crear tabla mayoristas
CREATE TABLE mayoristas (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(255) NOT NULL,
    email VARCHAR(255),
    telefono VARCHAR(50),
    direccion TEXT,
    activo BOOLEAN DEFAULT TRUE,
    fecha_creacion DATETIME DEFAULT CURRENT_TIMESTAMP,
    fecha_actualizacion DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    tiene_recomendaciones_activas BOOLEAN DEFAULT TRUE,
    tiempo_espera_horas INT DEFAULT 24,
    max_productos_recomendados INT DEFAULT 10
);

-- Crear tabla productos
CREATE TABLE productos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    codigo VARCHAR(100) UNIQUE NOT NULL,
    nombre VARCHAR(255) NOT NULL,
    descripcion TEXT,
    precio DECIMAL(10,2) NOT NULL,
    stock INT DEFAULT 0,
    mayorista_id INT,
    categoria VARCHAR(100),
    marca VARCHAR(100),
    imagen_url VARCHAR(500),
    activo BOOLEAN DEFAULT TRUE,
    fecha_creacion DATETIME DEFAULT CURRENT_TIMESTAMP,
    fecha_actualizacion DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (mayorista_id) REFERENCES mayoristas(id)
);

-- Crear tabla clientes
CREATE TABLE clientes (
    id INT AUTO_INCREMENT PRIMARY KEY,
    gescom_cliente_id INT,
    nombre VARCHAR(255) NOT NULL,
    email VARCHAR(255),
    telefono VARCHAR(50),
    direccion TEXT,
    mayorista_id INT,
    whatsapp_numero VARCHAR(50),
    acepta_whatsapp BOOLEAN DEFAULT FALSE,
    activo BOOLEAN DEFAULT TRUE,
    fecha_ultimo_pedido DATETIME,
    total_pedidos INT DEFAULT 0,
    ticket_promedio DECIMAL(10,2) DEFAULT 0,
    fecha_creacion DATETIME DEFAULT CURRENT_TIMESTAMP,
    fecha_actualizacion DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (mayorista_id) REFERENCES mayoristas(id)
);

-- Crear tabla usuarios
CREATE TABLE usuarios (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(100) UNIQUE NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    hashed_password VARCHAR(255) NOT NULL,
    activo BOOLEAN DEFAULT TRUE,
    fecha_creacion DATETIME DEFAULT CURRENT_TIMESTAMP,
    fecha_actualizacion DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- Crear tabla pedidos
CREATE TABLE pedidos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    numero_pedido VARCHAR(100) UNIQUE NOT NULL,
    cliente_id INT,
    mayorista_id INT,
    fecha_pedido DATETIME DEFAULT CURRENT_TIMESTAMP,
    estado VARCHAR(50) DEFAULT 'pendiente',
    total DECIMAL(10,2) DEFAULT 0,
    token_carrito VARCHAR(255) UNIQUE,
    fecha_expiracion_token DATETIME,
    fecha_creacion DATETIME DEFAULT CURRENT_TIMESTAMP,
    fecha_actualizacion DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (cliente_id) REFERENCES clientes(id),
    FOREIGN KEY (mayorista_id) REFERENCES mayoristas(id)
);

-- Crear tabla items_pedido
CREATE TABLE items_pedido (
    id INT AUTO_INCREMENT PRIMARY KEY,
    pedido_id INT NOT NULL,
    producto_id INT,
    cantidad INT NOT NULL DEFAULT 1,
    precio_unitario DECIMAL(10,2) NOT NULL,
    descuento DECIMAL(10,2) DEFAULT 0,
    subtotal DECIMAL(10,2) NOT NULL,
    producto_codigo VARCHAR(100),
    producto_nombre VARCHAR(255),
    FOREIGN KEY (pedido_id) REFERENCES pedidos(id),
    FOREIGN KEY (producto_id) REFERENCES productos(id)
);

-- Crear tabla recomendaciones
CREATE TABLE recomendaciones (
    id INT AUTO_INCREMENT PRIMARY KEY,
    pedido_id INT NOT NULL,
    producto_id INT,
    mayorista_id INT,
    tipo VARCHAR(50) DEFAULT 'upsell',
    estado VARCHAR(50) DEFAULT 'activa',
    orden INT DEFAULT 0,
    score DECIMAL(5,4) DEFAULT 0,
    razon TEXT,
    producto_nombre VARCHAR(255),
    producto_precio DECIMAL(10,2),
    producto_imagen_url VARCHAR(500),
    fue_clickeada BOOLEAN DEFAULT FALSE,
    fecha_click DATETIME,
    fue_agregada_carrito BOOLEAN DEFAULT FALSE,
    fecha_agregada_carrito DATETIME,
    cantidad_agregada INT DEFAULT 0,
    monto_convertido DECIMAL(10,2) DEFAULT 0,
    fecha_generacion DATETIME DEFAULT CURRENT_TIMESTAMP,
    fecha_envio DATETIME,
    FOREIGN KEY (pedido_id) REFERENCES pedidos(id),
    FOREIGN KEY (producto_id) REFERENCES productos(id),
    FOREIGN KEY (mayorista_id) REFERENCES mayoristas(id)
);

-- Crear tabla clientes_gescom
CREATE TABLE clientes_gescom (
    id INT AUTO_INCREMENT PRIMARY KEY,
    gescom_id INT UNIQUE NOT NULL,
    nombre VARCHAR(255) NOT NULL,
    email VARCHAR(255),
    telefono VARCHAR(50),
    direccion TEXT,
    activo BOOLEAN DEFAULT TRUE,
    fecha_creacion DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- Crear tabla combos_gescom
CREATE TABLE combos_gescom (
    id INT AUTO_INCREMENT PRIMARY KEY,
    gescom_id INT UNIQUE NOT NULL,
    nombre VARCHAR(255) NOT NULL,
    descripcion TEXT,
    precio DECIMAL(10,2),
    activo BOOLEAN DEFAULT TRUE,
    fecha_creacion DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- Crear tabla ventas_gescom
CREATE TABLE ventas_gescom (
    id INT AUTO_INCREMENT PRIMARY KEY,
    gescom_id INT UNIQUE NOT NULL,
    cliente_id INT,
    fecha_venta DATETIME,
    total DECIMAL(10,2),
    estado VARCHAR(50),
    fecha_creacion DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (cliente_id) REFERENCES clientes_gescom(id)
);

-- Insertar datos de ejemplo
INSERT INTO mayoristas (id, nombre, email, telefono, direccion, activo) VALUES
(1, 'Mayorista Demo', 'demo@mayorista.com', '123456789', 'Dirección Demo', 1),
(2, 'Distribuidora Central', 'central@dist.com', '987654321', 'Av. Central 123', 1),
(3, 'Proveedor Norte', 'norte@prov.com', '555123456', 'Calle Norte 456', 1),
(4, 'Comercial Sur', 'sur@comercial.com', '777888999', 'Ruta Sur 789', 1);

INSERT INTO productos (id, codigo, nombre, descripcion, precio, stock, mayorista_id, categoria, marca) VALUES
(1, 'PROD001', 'Fideos Matarazzo 500g', 'Fideos de trigo duro', 450.00, 100, 1, 'Pastas', 'Matarazzo'),
(2, 'PROD002', 'Yogur Ser Natural 900g', 'Yogur natural sin azúcar', 890.00, 50, 1, 'Lácteos', 'Ser'),
(3, 'PROD003', 'Pan Lactal Bimbo', 'Pan de molde integral', 420.00, 75, 1, 'Panificados', 'Bimbo'),
(4, 'PROD004', 'Leche La Serenísima 1L', 'Leche entera', 180.00, 200, 2, 'Lácteos', 'La Serenísima'),
(5, 'PROD005', 'Aceite de Oliva Extra Virgen', 'Aceite de oliva premium', 1200.00, 30, 2, 'Aceites', 'Premium'),
(6, 'PROD006', 'Arroz Integral 1kg', 'Arroz integral orgánico', 350.00, 80, 3, 'Cereales', 'Orgánico'),
(7, 'PROD007', 'Miel Pura 500g', 'Miel natural sin procesar', 450.00, 40, 3, 'Endulzantes', 'Natural'),
(8, 'PROD008', 'Té Verde Orgánico', 'Té verde en hebras', 280.00, 60, 4, 'Infusiones', 'Orgánico'),
(9, 'PROD009', 'Galletas de Avena', 'Galletas saludables', 320.00, 90, 4, 'Galletas', 'Saludable'),
(10, 'PROD010', 'Aceite de Coco Virgen', 'Aceite de coco extra virgen', 850.00, 25, 1, 'Aceites', 'Premium');

INSERT INTO clientes (id, gescom_cliente_id, nombre, email, telefono, direccion, mayorista_id, whatsapp_numero, acepta_whatsapp, activo) VALUES
(1, 1001, 'Juan Pérez', 'juan@email.com', '123456789', 'Av. Corrientes 123', 1, '123456789', 1, 1),
(2, 1002, 'María García', 'maria@email.com', '987654321', 'Calle Florida 456', 1, '987654321', 1, 1),
(3, 1003, 'Carlos López', 'carlos@email.com', '555123456', 'Ruta 9 789', 2, '555123456', 0, 1),
(4, 1004, 'Ana Rodríguez', 'ana@email.com', '777888999', 'Belgrano 321', 2, '777888999', 1, 1),
(5, 1005, 'Luis Martínez', 'luis@email.com', '111222333', 'San Martín 654', 3, '111222333', 0, 1);

INSERT INTO usuarios (id, username, email, hashed_password, activo) VALUES
(1, 'admin', 'admin@ticketplus.com', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewdBPj4J/8KqKqKq', 1),
(2, 'demo', 'demo@ticketplus.com', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewdBPj4J/8KqKqKq', 1);

INSERT INTO pedidos (id, numero_pedido, cliente_id, mayorista_id, fecha_pedido, estado, total, token_carrito, fecha_expiracion_token) VALUES
(1, 'ORD-2025-001', 1, 1, '2025-01-15 10:30:00', 'completado', 4830.00, 'PED001', '2025-12-31 23:59:59'),
(2, 'ORD-2025-002', 2, 1, '2025-01-16 14:20:00', 'pendiente', 2670.00, 'UP001', '2025-12-31 23:59:59'),
(3, 'ORD-2025-003', 3, 2, '2025-01-17 09:15:00', 'completado', 1580.00, 'W5SIe2I_uN6prtN3pSc6LxlvEPKINshh9H13XSbEJ_A', '2025-12-31 23:59:59'),
(4, 'ORD-2025-004', 4, 2, '2025-01-18 16:45:00', 'pendiente', 2050.00, 'demo-carrito-kxz0f1MofsEl3Seq73qIxw', '2025-12-31 23:59:59'),
(5, 'ORD-2025-005', 5, 3, '2025-01-19 11:30:00', 'completado', 3200.00, 'demo-carrito-HX1rQ-41_7DVzi0OWu8MAQ', '2025-12-31 23:59:59'),
(6, 'ORD-2025-006', 1, 1, '2025-01-20 13:20:00', 'pendiente', 1890.00, 'demo-carrito-wYIa_FTgjnOuKwXlGz_jaA', '2025-12-31 23:59:59'),
(7, 'ORD-2025-007', 2, 1, '2025-01-21 15:10:00', 'completado', 2670.00, 'demo-carrito-pmB5bBk3US4m9lTW5PSEHg', '2025-12-31 23:59:59'),
(8, 'ORD-2025-008', 3, 2, '2025-01-22 08:45:00', 'pendiente', 1580.00, 'demo-carrito--7YYOn_E_1kEG1xWaZ2vrA', '2025-12-31 23:59:59');

INSERT INTO items_pedido (pedido_id, producto_id, cantidad, precio_unitario, descuento, subtotal, producto_codigo, producto_nombre) VALUES
(1, 1, 2, 450.00, 0, 900.00, 'PROD001', 'Fideos Matarazzo 500g'),
(1, 2, 3, 890.00, 0, 2670.00, 'PROD002', 'Yogur Ser Natural 900g'),
(1, 3, 3, 420.00, 0, 1260.00, 'PROD003', 'Pan Lactal Bimbo'),
(2, 2, 3, 890.00, 0, 2670.00, 'PROD002', 'Yogur Ser Natural 900g'),
(3, 4, 2, 180.00, 0, 360.00, 'PROD004', 'Leche La Serenísima 1L'),
(3, 5, 1, 1200.00, 0, 1200.00, 'PROD005', 'Aceite de Oliva Extra Virgen'),
(3, 6, 1, 350.00, 0, 350.00, 'PROD006', 'Arroz Integral 1kg'),
(4, 7, 2, 450.00, 0, 900.00, 'PROD007', 'Miel Pura 500g'),
(4, 8, 2, 280.00, 0, 560.00, 'PROD008', 'Té Verde Orgánico'),
(4, 9, 2, 320.00, 0, 640.00, 'PROD009', 'Galletas de Avena'),
(5, 10, 2, 850.00, 0, 1700.00, 'PROD010', 'Aceite de Coco Virgen'),
(5, 1, 3, 450.00, 0, 1350.00, 'PROD001', 'Fideos Matarazzo 500g'),
(5, 2, 1, 890.00, 0, 890.00, 'PROD002', 'Yogur Ser Natural 900g'),
(6, 3, 3, 420.00, 0, 1260.00, 'PROD003', 'Pan Lactal Bimbo'),
(6, 4, 2, 180.00, 0, 360.00, 'PROD004', 'Leche La Serenísima 1L'),
(6, 5, 1, 1200.00, 0, 1200.00, 'PROD005', 'Aceite de Oliva Extra Virgen'),
(7, 2, 3, 890.00, 0, 2670.00, 'PROD002', 'Yogur Ser Natural 900g'),
(8, 4, 2, 180.00, 0, 360.00, 'PROD004', 'Leche La Serenísima 1L'),
(8, 5, 1, 1200.00, 0, 1200.00, 'PROD005', 'Aceite de Oliva Extra Virgen'),
(8, 6, 1, 350.00, 0, 350.00, 'PROD006', 'Arroz Integral 1kg');

INSERT INTO recomendaciones (pedido_id, producto_id, mayorista_id, tipo, estado, orden, score, razon, producto_nombre, producto_precio, producto_imagen_url) VALUES
-- Recomendaciones para PED001 (29 recomendaciones)
(1, 4, 1, 'upsell', 'activa', 1, 0.85, 'Complementa perfectamente con tus fideos', 'Leche La Serenísima 1L', 180.00, '/images/leche.jpg'),
(1, 5, 1, 'upsell', 'activa', 2, 0.82, 'Ideal para cocinar tus pastas', 'Aceite de Oliva Extra Virgen', 1200.00, '/images/aceite.jpg'),
(1, 6, 1, 'cross_sell', 'activa', 3, 0.78, 'Arroz integral para una dieta balanceada', 'Arroz Integral 1kg', 350.00, '/images/arroz.jpg'),
(1, 7, 1, 'cross_sell', 'activa', 4, 0.75, 'Endulzante natural para tu yogur', 'Miel Pura 500g', 450.00, '/images/miel.jpg'),
(1, 8, 1, 'cross_sell', 'activa', 5, 0.72, 'Té verde para acompañar tus comidas', 'Té Verde Orgánico', 280.00, '/images/te.jpg'),
(1, 9, 1, 'cross_sell', 'activa', 6, 0.70, 'Galletas saludables para el desayuno', 'Galletas de Avena', 320.00, '/images/galletas.jpg'),
(1, 10, 1, 'upsell', 'activa', 7, 0.68, 'Aceite de coco para cocinar', 'Aceite de Coco Virgen', 850.00, '/images/coco.jpg'),

-- Recomendaciones para demo-carrito-kxz0f1MofsEl3Seq73qIxw (3 recomendaciones)
(4, 1, 2, 'upsell', 'activa', 1, 0.85, 'Fideos para complementar tu pedido', 'Fideos Matarazzo 500g', 450.00, '/images/fideos.jpg'),
(4, 2, 2, 'cross_sell', 'activa', 2, 0.80, 'Yogur natural para el desayuno', 'Yogur Ser Natural 900g', 890.00, '/images/yogur.jpg'),
(4, 3, 2, 'cross_sell', 'activa', 3, 0.75, 'Pan integral para tus tostadas', 'Pan Lactal Bimbo', 420.00, '/images/pan.jpg'),

-- Recomendaciones para demo-carrito-HX1rQ-41_7DVzi0OWu8MAQ (3 recomendaciones)
(5, 4, 3, 'upsell', 'activa', 1, 0.88, 'Leche para tus recetas', 'Leche La Serenísima 1L', 180.00, '/images/leche.jpg'),
(5, 5, 3, 'cross_sell', 'activa', 2, 0.82, 'Aceite premium para cocinar', 'Aceite de Oliva Extra Virgen', 1200.00, '/images/aceite.jpg'),
(5, 6, 3, 'cross_sell', 'activa', 3, 0.78, 'Arroz integral saludable', 'Arroz Integral 1kg', 350.00, '/images/arroz.jpg'),

-- Recomendaciones para demo-carrito-wYIa_FTgjnOuKwXlGz_jaA (3 recomendaciones)
(6, 7, 1, 'upsell', 'activa', 1, 0.85, 'Miel natural para endulzar', 'Miel Pura 500g', 450.00, '/images/miel.jpg'),
(6, 8, 1, 'cross_sell', 'activa', 2, 0.80, 'Té verde antioxidante', 'Té Verde Orgánico', 280.00, '/images/te.jpg'),
(6, 9, 1, 'cross_sell', 'activa', 3, 0.75, 'Galletas de avena saludables', 'Galletas de Avena', 320.00, '/images/galletas.jpg'),

-- Recomendaciones para demo-carrito-pmB5bBk3US4m9lTW5PSEHg (3 recomendaciones)
(7, 10, 1, 'upsell', 'activa', 1, 0.88, 'Aceite de coco para cocinar', 'Aceite de Coco Virgen', 850.00, '/images/coco.jpg'),
(7, 1, 1, 'cross_sell', 'activa', 2, 0.82, 'Fideos para tus recetas', 'Fideos Matarazzo 500g', 450.00, '/images/fideos.jpg'),
(7, 2, 1, 'cross_sell', 'activa', 3, 0.78, 'Yogur natural sin azúcar', 'Yogur Ser Natural 900g', 890.00, '/images/yogur.jpg'),

-- Recomendaciones para demo-carrito--7YYOn_E_1kEG1xWaZ2vrA (3 recomendaciones)
(8, 3, 2, 'upsell', 'activa', 1, 0.85, 'Pan integral para el desayuno', 'Pan Lactal Bimbo', 420.00, '/images/pan.jpg'),
(8, 4, 2, 'cross_sell', 'activa', 2, 0.80, 'Leche para tus bebidas', 'Leche La Serenísima 1L', 180.00, '/images/leche.jpg'),
(8, 5, 2, 'cross_sell', 'activa', 3, 0.75, 'Aceite premium para cocinar', 'Aceite de Oliva Extra Virgen', 1200.00, '/images/aceite.jpg');

-- Insertar datos de Gescom
INSERT INTO clientes_gescom (gescom_id, nombre, email, telefono, direccion) VALUES
(1001, 'Juan Pérez', 'juan@email.com', '123456789', 'Av. Corrientes 123'),
(1002, 'María García', 'maria@email.com', '987654321', 'Calle Florida 456'),
(1003, 'Carlos López', 'carlos@email.com', '555123456', 'Ruta 9 789');

INSERT INTO combos_gescom (gescom_id, nombre, descripcion, precio) VALUES
(1, 'Combo Desayuno', 'Pan, leche y miel', 850.00),
(2, 'Combo Cocina', 'Aceite, fideos y arroz', 2000.00),
(3, 'Combo Saludable', 'Yogur, té y galletas', 1640.00);

INSERT INTO ventas_gescom (gescom_id, cliente_id, fecha_venta, total, estado) VALUES
(1, 1, '2025-01-15 10:30:00', 4830.00, 'completada'),
(2, 2, '2025-01-16 14:20:00', 2670.00, 'pendiente'),
(3, 3, '2025-01-17 09:15:00', 1580.00, 'completada');

-- Mensaje de confirmación
SELECT '✅ Base de datos Ticket+ importada exitosamente en Railway!' as mensaje; 