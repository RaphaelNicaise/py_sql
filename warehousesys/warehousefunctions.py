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
                  2 - Info of all products
                  3 - Select a Product ID & Calculate Price
                  4 - Insert N randon products 
                  5 - Show all prices
                  6 - Change price of a product 
                  7 - Create a product
                  8 - Show stock movements
                  C - Clear Console
                  Q - Quit
                  
                """)
def quantity_of_products():
    cnx = connect_to_db() # agregada la conexion ya que no devolvia datos actualizados
    cursor = cnx.cursor()
    cursor.execute("select max(id_product) from products")
    result = cursor.fetchone()[0]
    return result

def write_products_csv():
    
    result = select_all_products()
    df = pd.DataFrame(result, columns=['id_product', 'product_name', 'description', 'price', 'quantity', 'category', 'Supplier'])
    df.to_csv('products.csv', index=False)
    print("File created successfully")
    
def clear_console(): ## clear console
    print("\n" * 100)
 
   
def choose_random_quantity(min,max):
    random_quantity = random.randint(min,max)
    return random_quantity

def choose_random_product():
    random_id_product = random.randint(1,quantity_of_products())
    return random_id_product

def select_a_product(id_product):
    cnx = connect_to_db() # agregada la conexion ya que no devolvia datos actualizados
    cursor = cnx.cursor()
    cursor.execute(f"SELECT PR.id_product,PR.product_name,PR.description ,PR.price,INV.quantity,CT.category,SP.name as Supplier FROM products PR JOIN categories CT ON	CT.id_category = PR.id_category JOIN inventory INV ON INV.id_product = PR.id_product JOIN suppliers SP ON SP.id_supplier = PR.id_supplier where PR.id_product = {id_product} group by id_product")
    result = cursor.fetchone()
    return result
  
def select_all_products():
    cnx = connect_to_db()
    cursor = cnx.cursor()
    cursor.execute("SELECT PR.id_product,PR.product_name,PR.description ,PR.price,INV.quantity,CT.category,SP.name as Supplier FROM products PR JOIN categories CT ON	CT.id_category = PR.id_category JOIN inventory INV ON INV.id_product = PR.id_product JOIN suppliers SP ON SP.id_supplier = PR.id_supplier group by id_product")
    result = cursor.fetchall()
    return result

def calculate_price(id_product,quantity):
    cursor.execute(f"Select price*{quantity} from products where id_product = {id_product} ")
    result = cursor.fetchone()
    return result

def change_price(id_product,new_price):
    cursor.callproc("change_price",(id_product,new_price))
    cnx.commit()

def create_product(product_name,description,price,id_supplier,id_category):
    cursor.callproc("create_product",(product_name,description,price,id_supplier,id_category))
    cnx.commit()

def get_categories():
    cursor.execute("select * from categories order by id_category asc")
    result = cursor.fetchall()
    return result

def get_suppliers():
    cursor.execute("select id_supplier,name from suppliers order by id_supplier asc")
    result = cursor.fetchall()
    return result

def stock_movements(id_product):
    cursor.execute(f"select * from stock_movements where id_product = {id_product}")
    result = cursor.fetchall()
    return result

def get_name_of_product(id_product):
    cursor.execute(f"select product_name from products where id_product = {id_product}")
    result = cursor.fetchone()
    return result 

def goodbye():
    cursor.close()
    cnx.close()
    print(r"""
░░░░░░░░░░░░░┌┬─┬┬┐┌┬──┐░▄▄▄░▄▄▄░░░░░░░░
░░░░░░░░░░░░░│││││└┘│──┤░█░▀█▀░█░░░░░░░░
░░░░░░░░░░░░░│││││┌┐├──│░▀█░░░█▀░░░░░░░░
░░░░░░░░░░░░░└─┴─┴┘└┴──┘░░░█▄█░░░░░░░░░░
          """)

print("Fucntions loaded successfully")