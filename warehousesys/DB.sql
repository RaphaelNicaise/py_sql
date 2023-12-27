
DROP SCHEMA IF EXISTS WarehouseSystem;

    CREATE SCHEMA WarehouseSystem;
    USE WarehouseSystem;

    CREATE TABLE suppliers (
        id_supplier INT AUTO_INCREMENT NOT NULL ,
        name varchar(255) NOT NULL,
        phone_number varchar(255) NOT NULL,
        email varchar(255) NOT NULL,
        direction varchar(255) NOT NULL,
        information varchar(255),
        PRIMARY KEY (id_supplier)
    );

    ALTER TABLE suppliers AUTO_INCREMENT = 5000;

    CREATE TABLE categories (
        id_category INT AUTO_INCREMENT NOT NULL,
        category varchar(255) NOT NULL UNIQUE,
        PRIMARY KEY (id_category)
    );

    CREATE TABLE products (
        id_product INT AUTO_INCREMENT NOT NULL,
        product_name varchar(255) NOT NULL,
        description varchar(255),
        price DECIMAL(10,2),
        id_supplier INT NOT NULL,
        id_category INT DEFAULT NULL,
        PRIMARY KEY (id_product),
        FOREIGN KEY (id_supplier) REFERENCES suppliers (id_supplier),
        FOREIGN KEY (id_category) REFERENCES categories (id_category)
        
    );

    CREATE TABLE inventory (
        id_inventory INT AUTO_INCREMENT NOT NULL,
        id_product INT NOT NULL UNIQUE,
        quantity INT DEFAULT 0 CHECK (quantity >= 0),
        last_movement TIMESTAMP DEFAULT NOW(),
        sector ENUM('A', 'B', 'C', 'D', 'E', 'F') NULL,
        PRIMARY KEY (id_inventory),
        FOREIGN KEY (id_product)
            REFERENCES products (id_product)
    );

    CREATE TABLE stock_movements (
        id_movement INT AUTO_INCREMENT NOT NULL,
        id_product INT NOT NULL,
        old_quantity INT NOT NULL,
        quantity INT NOT NULL,
        type ENUM('ins','outs'),
        new_quantity INT NOT NULL,
        movement_date TIMESTAMP DEFAULT NOW(),
        
        PRIMARY KEY (id_movement),
        FOREIGN KEY (id_product) REFERENCES products (id_product)
    );
    
    CREATE TABLE price_changes (
        id_movement INT auto_increment NOT NULL,
        id_product INT NOT NULL,
        old_price decimal (10,2) NOT NULL,
        new_price decimal (10,2) NOT NULL,
        movement_date TIMESTAMP DEFAULT NOW(), 
        
        PRIMARY KEY (id_movement),
        FOREIGN KEY (id_product) REFERENCES products (id_product)
    );
    
    CREATE TABLE alert_amount_0 (
        id_product INT NOT NULL,
        moment TIMESTAMP DEFAULT NOW(),
        Alert enum ('Add Stock!'),
        FOREIGN KEY (id_product) REFERENCES products (id_product)
        );

CREATE DEFINER=`root`@`localhost` PROCEDURE `add_stock_2`(IN p_id_product INT, IN p_in_quantity INT)
BEGIN
    DECLARE product_count INT;
    
    START TRANSACTION;
    SELECT COUNT(*) INTO product_count FROM products WHERE id_product = p_id_product;
	
    IF product_count > 0 THEN
        IF p_in_quantity > 0 THEN
            
            UPDATE inventory SET quantity = quantity + p_in_quantity, last_movement = NOW() WHERE id_product = p_id_product;
            
        ELSEIF p_in_quantity < 0 THEN 
            
            UPDATE inventory SET quantity = quantity + p_in_quantity, last_movement = NOW() WHERE id_product = p_id_product;
           
        END IF;
    END IF;
    COMMIT;
END