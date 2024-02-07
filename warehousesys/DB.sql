
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

CREATE DEFINER=`root`@`localhost` PROCEDURE `change_price`(IN id_product_ INT,IN new_price DECIMAL(10,2))
BEGIN
	IF new_price >= 0 THEN
		UPDATE products set price = new_price where id_product = id_product_;
	ELSE
		SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'You cant set that price.';
	END IF;
END

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

CREATE TRIGGER ins_outs_stock 
AFTER UPDATE ON inventory
FOR EACH ROW
BEGIN
    DECLARE quantity_change INT;

    SET quantity_change = NEW.quantity - OLD.quantity;
	IF OLD.quantity != NEW.quantity THEN
		IF quantity_change > 0 THEN
			INSERT INTO stock_movements (id_product,old_quantity, quantity,type,new_quantity)
			VALUES (OLD.id_product,OLD.quantity, quantity_change,'ins',NEW.quantity);
			
		ELSEIF quantity_change < 0 THEN
			INSERT INTO stock_movements (id_product,old_quantity, quantity,type,new_quantity)
			VALUES (OLD.id_product,OLD.quantity, -quantity_change,'outs',NEW.quantity);
		END IF;
	END IF;
    
END //

DELIMITER //

CREATE TRIGGER insert_product_into_inventory
AFTER INSERT ON products
FOR EACH ROW
BEGIN
    INSERT INTO inventory (id_product, quantity)
    VALUES (NEW.id_product, 0);
END //

DELIMITER //

CREATE TRIGGER update_price_of_product
AFTER UPDATE ON products
FOR EACH ROW
BEGIN
	IF OLD.price <> NEW.price THEN
		INSERT INTO price_changes (id_product,old_price,new_price)
		VALUES (new.id_product,OLD.price,NEW.price);
	END IF;
END //

DELIMITER //
CREATE TRIGGER alert_amount0_product
AFTER UPDATE ON inventory
FOR EACH ROW
BEGIN
	IF NEW.Quantity = 0 AND OLD.Quantity > 0 THEN
		INSERT INTO alert_amount_0 (id_product,alert) 
        VALUES (NEW.id_product, 'Add Stock!');
	END IF;
END //

DELIMITER //
CREATE TRIGGER delete_alert_when_stocked
AFTER UPDATE ON inventory
FOR EACH ROW
BEGIN
	IF OLD.Quantity = 0 AND NEW.Quantity > 0 THEN
		DELETE FROM alert_amount_0 WHERE id_product = NEW.id_product;
	END IF;
END //

INSERT INTO categories (category) VALUES ('Bakery'),
	('Sodas'),
    ('Pharmacy'),
    ('Meat'),
    ('Seafood'),
    ('Canned'),
    ('Fruits & Vegetables'),
    ('Dairy'),
    ('Alcohol');
    
insert into suppliers (name, phone_number, email, direction, information) values ('Bernhard-Brown', '+420 591 646 2580', 'sredholls0@usgs.gov', '8297 Grim Street', 'integer aliquet massa id lobortis convallis tortor risus dapibus augue');
insert into suppliers (name, phone_number, email, direction, information) values ('Blanda, Gottlieb and Ritchie', '+62 456 485 0136', 'rbricket1@netlog.com', '4436 Old Gate Way', 'consequat in consequat ut nulla sed accumsan felis ut at dolor quis odio consequat varius');
insert into suppliers (name, phone_number, email, direction, information) values ('Stark-Schuster', '+47 677 936 2596', 'csimmans2@tinypic.com', '1 Messerschmidt Pass', 'semper sapien a libero nam dui proin leo odio porttitor id consequat in');
insert into suppliers (name, phone_number, email, direction, information) values ('Schmitt, Raynor and Lueilwitz', '+351 950 415 0105', 'atudgay3@craigslist.org', '6332 Buell Park', 'et ultrices posuere cubilia curae nulla dapibus dolor vel est donec odio justo sollicitudin');
insert into suppliers (name, phone_number, email, direction, information) values ('Reichert Inc', '+1 319 488 7005', 'dstalley4@tiny.cc', '97 Darwin Street', 'volutpat eleifend donec ut dolor morbi vel lectus in quam fringilla rhoncus mauris enim leo rhoncus sed vestibulum sit amet');
insert into suppliers (name, phone_number, email, direction, information) values ('Mayert-Bechtelar', '+46 465 885 3118', 'aschieferstein5@dailymail.co.uk', '98687 School Street', 'lectus vestibulum quam sapien varius ut blandit non interdum in ante vestibulum ante ipsum primis in faucibus orci luctus');
insert into suppliers (name, phone_number, email, direction, information) values ('Kassulke-Yost', '+1 763 580 5922', 'utolliday6@youtube.com', '2455 Trailsway Trail', 'gravida sem praesent id massa id nisl venenatis lacinia aenean sit');
insert into suppliers (name, phone_number, email, direction, information) values ('Kuphal, Cronin and Schoen', '+63 674 598 0257', 'lcaccavale7@china.com.cn', '2074 Gina Circle', 'dolor quis odio consequat varius integer ac leo pellentesque ultrices mattis odio donec vitae nisi nam ultrices');
insert into suppliers (name, phone_number, email, direction, information) values ('McGlynn LLC', '+7 992 734 1512', 'sbolte8@instagram.com', '0287 Stone Corner Plaza', 'amet eros suspendisse accumsan tortor quis turpis sed ante vivamus tortor duis mattis egestas metus aenean fermentum donec ut');
insert into suppliers (name, phone_number, email, direction, information) values ('Price, Russel and Bashirian', '+965 460 342 0331', 'sfeaver9@berkeley.edu', '7018 Carberry Crossing', 'lacinia eget tincidunt eget tempus vel pede morbi porttitor lorem id ligula suspendisse ornare consequat lectus in est risus');
insert into suppliers (name, phone_number, email, direction, information) values ('Waters-Gislason', '+269 257 799 5535', 'cfaulknera@tinypic.com', '74 Anniversary Crossing', 'curabitur at ipsum ac tellus semper interdum mauris ullamcorper purus sit amet nulla quisque arcu');
insert into suppliers (name, phone_number, email, direction, information) values ('Hoppe, Block and Nolan', '+7 281 435 0701', 'adionisettib@yahoo.com', '41 Mandrake Plaza', 'curabitur gravida nisi at nibh in hac habitasse platea dictumst aliquam');
insert into suppliers (name, phone_number, email, direction, information) values ('Heathcote-Hills', '+1 330 884 1555', 'thamletc@free.fr', '53500 6th Place', 'nunc nisl duis bibendum felis sed interdum venenatis turpis enim blandit mi in');
insert into suppliers (name, phone_number, email, direction, information) values ('Shields-Bayer', '+86 356 683 4576', 'elowersd@networkadvertising.org', '01 Pleasure Pass', 'id ligula suspendisse ornare consequat lectus in est risus auctor sed tristique in tempus sit amet sem fusce consequat nulla');
insert into suppliers (name, phone_number, email, direction, information) values ('O''Connell LLC', '+976 199 660 1374', 'dshippeye@archive.org', '4 Everett Street', 'vel augue vestibulum ante ipsum primis in faucibus orci');
insert into suppliers (name, phone_number, email, direction, information) values ('Sawayn, Hilll and Connelly', '+53 765 152 5853', 'kbroomhallf@etsy.com', '4771 Commercial Road', 'phasellus in felis donec semper sapien a libero nam dui proin leo');
insert into suppliers (name, phone_number, email, direction, information) values ('Russel, Kessler and Wilkinson', '+86 410 615 0405', 'vscopesg@bizjournals.com', '6790 Nancy Alley', 'augue vel accumsan tellus nisi eu orci mauris lacinia sapien quis libero nullam sit');
insert into suppliers (name, phone_number, email, direction, information) values ('Murphy-Funk', '+86 960 140 7904', 'rbazireh@amazon.de', '726 Lakewood Lane', 'morbi non quam nec dui luctus rutrum nulla tellus');
insert into suppliers (name, phone_number, email, direction, information) values ('Konopelski and Sons', '+420 229 946 3118', 'sduesteri@zdnet.com', '0 Prairie Rose Place', 'lectus aliquam sit amet diam in magna bibendum imperdiet nullam orci pede venenatis non sodales');
insert into suppliers (name, phone_number, email, direction, information) values ('Goodwin-Balistreri', '+20 429 742 1649', 'cmincinij@biglobe.ne.jp', '17600 Debra Avenue', 'integer a nibh in quis justo maecenas rhoncus aliquam lacus');

INSERT INTO products (product_name, description, price, id_supplier, id_category)
VALUES
  ('Chocolate Chip Cookies', 'Delicious homemade cookies', 3.99, 5000, 1),
  ('Whole Wheat Bread', 'Healthy whole wheat bread', 2.49, 5001, 1),
  ('Soda Pop', 'Refreshing soda in various flavors', 1.50, 5002, 2),
  ('Pain Reliever', 'Fast-acting pain reliever', 8.99, 5003, 3),
  ('Chicken Breast', 'Fresh boneless chicken breast', 7.99, 5004, 4),
  ('Salmon Fillet', 'Wild-caught salmon fillet', 12.99, 5005, 5),
  ('Canned Tomato Soup', 'Classic tomato soup in a can', 1.99, 5006, 6),
  ('Apples', 'Crisp and juicy apples', 0.99, 5007, 7),
  ('Milk', 'Fresh cows milk', 2.29, 5008, 8),
  ('Vodka', 'Premium vodka', 19.99, 5009, 9),
  ('Brownies', 'Fudge brownies', 4.49, 5010, 1),
  ('Multigrain Cereal', 'Healthy breakfast cereal', 3.79, 5011, 1),
  ('Cola', 'Classic cola beverage', 1.50, 5012, 2),
  ('Allergy Medication', 'Relief from allergies', 9.99, 5013, 3),
  ('Ribeye Steak', 'Prime ribeye steak', 14.99, 5014, 4),
  ('Shrimp', 'Fresh shrimp', 11.99, 5015, 5),
  ('Canned Green Beans', 'Crisp green beans in a can', 1.49, 5016, 6),
  ('Oranges', 'Sweet and juicy oranges', 0.79, 5017, 7),
  ('Yogurt', 'Creamy yogurt', 2.99, 5018, 8),
  ('Whiskey', 'Premium whiskey', 24.99, 5019, 9),
  ('Bagels', 'Freshly baked bagels', 3.49, 5000, 1),
  ('White Bread', 'Soft and fluffy white bread', 2.29, 5001, 1),
  ('Lemonade', 'Refreshing lemonade', 2.00, 5002, 2),
  ('Aspirin', 'Headache relief', 5.99, 5003, 3),
  ('Pork Chops', 'Tender pork chops', 9.99, 5004, 4),
  ('Tuna Steak', 'Premium tuna steak', 10.99, 5005, 5),
  ('Canned Corn', 'Sweet corn in a can', 1.29, 5006, 6),
  ('Bananas', 'Ripe and yellow bananas', 0.69, 5007, 7),
  ('Cheese', 'Assorted cheese selection', 4.99, 5008, 8),
  ('Rum', 'Fine rum', 22.99, 5009, 9),
  ('Aviator Sunglasses', 'Classic aviator sunglasses with UV protection', 49.99, 5000, 8),
  ('Beach Umbrella', 'Large beach umbrella for shade', 24.99, 5001, 7),
  ('Sour Gummy Worms', 'Tangy and sweet gummy candies', 2.99, 5002, 1),
  ('Digital Thermometer', 'Accurate digital thermometer', 12.99, 5003, 3),
  ('Ribbed Tank Top', 'Comfortable ribbed tank top for summer', 9.99, 5004, 4),
  ('Fish Oil Capsules', 'Omega-3 fish oil capsules', 15.99, 5005, 3),
  ('Canned Pineapple', 'Sliced pineapple in a can', 1.79, 5006, 6),
  ('Strawberries', 'Fresh and juicy strawberries', 2.49, 5007, 7),
  ('Greek Yogurt', 'Creamy Greek yogurt', 3.49, 5008, 8),
  ('Craft Beer Assortment', 'Variety pack of craft beers', 18.99, 5009, 9),
  ('Sunglasses Case', 'Protective case for your sunglasses', 4.99, 5010, 8),
  ('Beach Towel', 'Colorful beach towel for lounging', 8.49, 5011, 7),
  ('Chocolate Bars', 'Assorted gourmet chocolate bars', 4.99, 5012, 1),
  ('First Aid Kit', 'Comprehensive first aid kit for emergencies', 19.99, 5013, 3),
  ('Ground Beef', 'Fresh ground beef for cooking', 6.99, 5014, 4),
  ('Lobster Tails', 'Delicious lobster tails', 23.99, 5015, 5),
  ('Canned Peas', 'Tender green peas in a can', 1.29, 5016, 6),
  ('Grapes', 'Sweet and seedless grapes', 3.99, 5017, 7),
  ('Almond Milk', 'Plant-based almond milk', 2.99, 5018, 8),
  ('Tequila', 'Premium tequila for cocktails', 29.99, 5019, 9),
  ('Wayfarer Sunglasses', 'Iconic wayfarer-style sunglasses', 39.99, 5000, 8),
  ('Beach Chair', 'Portable beach chair for relaxation', 19.99, 5001, 7),
  ('Sour Patch Kids', 'Tart and chewy candy favorites', 2.49, 5002, 1),
  ('Blood Pressure Monitor', 'Digital blood pressure monitor', 24.99, 5003, 3),
  ('Pork Ribs', 'Tasty pork ribs for grilling', 11.99, 5004, 4),
  ('Sardines', 'Canned sardines in olive oil', 1.99, 5005, 5),
  ('Canned Carrots', 'Sliced carrots in a can', 1.29, 5006, 6),
  ('Blueberries', 'Fresh and antioxidant-rich blueberries', 3.49, 5007, 7),
  ('Coconut Milk', 'Creamy coconut milk for cooking', 2.79, 5008, 8),
  ('Gin', 'Premium gin for cocktails', 21.99, 5009, 9);