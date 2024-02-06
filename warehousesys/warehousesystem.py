import mysql.connector
import random
import pandas as pd

def connect_to_db():
    try:
        return mysql.connector.MySQLConnection(
            user='root',password='',host='localhost',
            database='warehousesystem',port='3306')
                                               
    except mysql.connector.Error as err:
        print(f"{err}")
        return None
cnx = connect_to_db()
cursor = cnx.cursor()

def choose_random_quantity(min,max):
    random_quantity = random.randint(min,max)
    return random_quantity

def choose_random_product():
    random_id_product = random.randint(1,quantity_of_products())
    return random_id_product

def quantity_of_products():
    cursor.execute("select max(id_product) from products")
    result = cursor.fetchone()[0]
    return result

def select_a_product(id_product):
    cursor.execute(f"SELECT PR.id_product,PR.product_name,PR.description ,PR.price,INV.quantity,CT.category,count(*) ,	SP.name as Supplier ,TIMESTAMPDIFF(HOUR, INV.last_movement, NOW()) FROM products PR JOIN categories CT ON	CT.id_category = PR.id_category JOIN inventory INV ON INV.id_product = PR.id_product JOIN suppliers SP ON SP.id_supplier = PR.id_supplier JOIN stock_movements SM ON SM.id_product = PR.id_product where PR.id_product = {id_product} group by id_product")
    result = cursor.fetchone()
    return result

def calculate_price(id_product,quantity):
    cursor.execute(f"Select price*{quantity} from products where id_product = {id_product} ")
    result = cursor.fetchone()
    return result

  
    
max_product_id = quantity_of_products()
    
while (True):
    try:
        
        print("| WarehouseSystem |")
        print("1 - Info of a product \n2 - Select a Product ID & Calculate Price \n3 - Insert N randon products \n4 - Quit")
        choice = int(input("Choose an Option -> "))
        if choice == 1: 
            try: 
                id_product = input("Select an Id_product: ")
                product = select_a_product(id_product)
                if  int(id_product) <= max_product_id: 
                    print(f"Product ID: {product[0]}")
                    print(f"Product Name: {product[1]}")
                    print(f"Description: {product[2]}")
                    print(f"Price: {product[3]}")
                    print(f"Quantity: {product[4]}")
                    print(f"Category: {product[5]}")
                    print(f"Supplier: {product[7]}")
                    print(f"Last Movement: {product[8]} hours ago")
                else:
                    print(f"There's no product with id {id_product}")
            except ValueError:
                print("Invalid Character")
                
        
        if choice == 2:
            try:
                id_product = input("Select an Id_product: ")
                if id_product.lower() == 'quit':
                    print("Returning to menu")
                    break
                id_product = int(id_product)
                
                if  id_product <= max_product_id :       
                    
                    productname = select_a_product(id_product)[1]
                    q = input(f"How many of {productname}? -> ")
                    price = calculate_price(id_product,q)[0]
                    print(f"{q} of {productname} -> {price}$ ")   
                else:
                    print(f"There's no product with id {id_product}")
            except ValueError:
                print("Invalid Character")
                
                 
        elif choice == 3:
            
            amount_products_to_insert = int(input("How Many random inserts do you want? -> "))
            i = 0
            print('')
            while (i < amount_products_to_insert):
                rand_product = choose_random_product()
                cursor.execute(f"SELECT product_name,quantity FROM warehousesystem.products pr join inventory inv on inv.id_product = pr.id_product where inv.id_product = {rand_product} ")
                productname_,q = cursor.fetchone()
                
                if q > 50:
                    rand_quantity = choose_random_quantity(-49,50)
                elif q <= 50:
                    rand_quantity = choose_random_quantity(0,50)
                    while rand_quantity == 0:
                        rand_quantity = choose_random_quantity(0,50)
                    
                
                cursor.callproc("add_stock_2",(rand_product,rand_quantity))
                if rand_quantity > 0:
                        print(f"Product: {rand_product}- {productname_} Added: {rand_quantity}")
                elif rand_quantity < 0:
                    print(f"Product: {rand_product}- {productname_} removed: {rand_quantity}")    
                    
                i += 1    
            print('')
            cnx.commit()
            
        elif choice == 4:
            print("Leaving program")
            break
    except ValueError:
        print("Wrong character")
cnx.close()
 
    