import mysql.connector
import random
import pandas as pd

cnx = mysql.connector.MySQLConnection(user='root',password='',host='localhost',
                                      database='warehousesystem',port='3306')
cursor = cnx.cursor()

cursor.execute("select distinct count(*) from products")
q_products = cursor.fetchone()[0]


def choose_random_quantity():
    random_quantity = random.randint(1,50)
    return random_quantity

def choose_random_product():
    random_id_product = random.randint(1,q_products)
    return random_id_product

def p(text):
    print(text) 

while (True):
    try:
        print("| WarehouseSystem |")
        print("1 - Select a Product ID & Calculate Price \n2 - Insert N randon products \n3 - Quit")
        choice = int(input("Choose an Option -> "))
        if choice == 1:
            id_product = input("Select an Id_product: ")
            if id_product.lower() == 'quit':
                p("Returning to menu")
                break
            id_product = int(id_product)
            cursor.execute(f"select product_name from products where id_product = {id_product}")
            productname = cursor.fetchone()[0]
            q = input(f"How many of {productname}? -> ")
            cursor.execute(f"Select price*{q} from products where id_product = {id_product} ")
            product = cursor.fetchone()
            price = product[0]
            p(f"{q} of {productname} -> {price}$ ")   
        elif choice == 2:
            max = int(input("How Many random inserts do you want? -> "))
            i = 0
            while (i < max):
                rand_product = choose_random_product()
                rand_quantity = choose_random_quantity()
                cursor.callproc("add_stock_without_text",(rand_product,rand_quantity))
                cursor.execute(f"select product_name from products where id_product = {rand_product} ")
                productname_ = cursor.fetchone()[0]
                p('')  
                if rand_product >= 10:
                    p(f"Product: {rand_product}- {productname_} Added: {rand_quantity}")
                elif rand_product < 10:
                    p(f"Product:  {rand_product}- {productname_} Added: {rand_quantity}")
                p('')
                i += 1
            cnx.commit()
        elif choice == 3:
            p("Leaving program")
            break
    except ValueError:
        print("Wrong character")
cnx.close()
 
    