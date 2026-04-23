DROP DATABASE IF EXISTS albpb;
CREATE DATABASE albpb;
USE albpb;

CREATE TABLE productos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    categoria VARCHAR(50) NOT NULL,
    precio DECIMAL(10,2) NOT NULL,
    stock INT NOT NULL
);

CREATE TABLE carrito (
    id INT AUTO_INCREMENT PRIMARY KEY,
    id_producto INT NOT NULL,
    cantidad INT NOT NULL,
    FOREIGN KEY (id_producto) REFERENCES productos(id)
);

CREATE TABLE pedidos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    total DECIMAL(10,2) NOT NULL,
    estado VARCHAR(20) NOT NULL,
    fecha DATETIME NOT NULL
);

CREATE TABLE pedido_items (
    id INT AUTO_INCREMENT PRIMARY KEY,
    id_pedido INT NOT NULL,
    id_producto INT NOT NULL,
    cantidad INT NOT NULL,
    FOREIGN KEY (id_pedido) REFERENCES pedidos(id),
    FOREIGN KEY (id_producto) REFERENCES productos(id)
);

INSERT INTO productos (nombre, categoria, precio, stock) VALUES
('Aceite Vegetal 1L', 'Perecederos', 32.50, 100),
('Leche Entera 1L', 'Lácteos', 18.00, 80),
('Detergente 900g', 'Limpieza', 28.00, 50),
('Atún en Agua 140g', 'Enlatados', 15.50, 200),
('Refresco Cola 2L', 'Bebidas', 25.00, 60),
('Papel Higiénico 4pzas', 'Higiene', 22.00, 120),
('Galletas Marías 170g', 'Botanas', 12.00, 150),
('Arroz 1kg', 'Granos', 20.00, 90);
