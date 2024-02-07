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

def menu():
    print(r"""
              
                █░█░█ ▄▀█ █▀█ █▀▀ █░█ █▀█ █░█ █▀ █▀▀ █▀ █▄█ █▀
                ▀▄▀▄▀ █▀█ █▀▄ ██▄ █▀█ █▄█ █▄█ ▄█ ██▄ ▄█ ░█░ ▄█
                
                  1 - Info of a product 
                  2 - Select a Product ID & Calculate Price
                  3 - Insert N randon products 
                  4 - Show all prices
                  5 - Change price of a product 
                  6 - Quit
                  
                """)
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

def change_price(id_product,new_price):
    
    cursor.callproc("change_price",(id_product,new_price))
    cnx.commit()


max_product_id = quantity_of_products()