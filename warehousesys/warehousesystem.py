import warehousefunctions as wf
import pandas as pd

cnx = wf.connect_to_db()
cursor = cnx.cursor()


while (True):
    try:
        
        wf.menu()
        
        option = input("Choose an Option -> ")
        if option.isdigit():
            option = int(option)
        if option == 1: 
            try: 
                id_product = input("Select an Id_product: ")
                product = wf.select_a_product(id_product)
                if  int(id_product) <= wf.quantity_of_products(): 
                    print(f"Product ID: {product[0]}")
                    print(f"Product Name: {product[1]}")
                    print(f"Description: {product[2]}")
                    print(f"Price: {product[3]} Total Price: {wf.calculate_price(id_product,product[4])[0]}$")
                    print(f"Quantity: {product[4]}")
                    print(f"Category: {product[5]}")
                    print(f"Supplier: {product[6]}")
                    
                else:
                    print(f"There's no product with id {id_product}")
            except ValueError:
                print("Invalid Character")
                
        elif option == 2:
            try:
                productos = wf.select_all_products()
                
                print(pd.DataFrame(productos, columns=['id_product', 'product_name', 'description', 'price', 'quantity', 'category', 'Supplier']))
                response = input("Do you want to save this data in a csv file? (Y/N) -> ")
                if response.lower() == 'y':
                    wf.write_products_csv()
            except ValueError:
                print("Invalid Character")
        elif option == 3:
            try:
                id_product = input("Select an Id_product: ")
                if id_product.lower() == 'quit':
                    print("Returning to menu")
                    break
                id_product = int(id_product)
                
                if  id_product <= wf.quantity_of_products() :       
                    
                    productname = wf.select_a_product(id_product)[1]
                    q = input(f"How many of {productname}? -> ")
                    price = wf.calculate_price(id_product,q)[0]
                    print(f"{q} of {productname} -> {price}$ ")   
                else:
                    print(f"There's no product with id {id_product}")
            except ValueError:
                print("Invalid Character")
                 
        elif option == 4:
            
            amount_products_to_insert = int(input("How Many random inserts do you want? -> "))
            i = 0
            print('')
            while (i < amount_products_to_insert):
                
                rand_product = wf.choose_random_product()
                product = wf.select_a_product(rand_product)
                
                
                productname =  product[1]
                quantity = product[4] # Cantidades actuales del producto
                
                if quantity > 50:
                    rand_quantity = wf.choose_random_quantity(-49,50)
                elif quantity <= 50:
                    rand_quantity = wf.choose_random_quantity(0,50)
                    while rand_quantity == 0:
                        rand_quantity = wf.choose_random_quantity(0,50)
                        
                    
                cursor.callproc("add_stock_2",(rand_product,rand_quantity))
                if rand_quantity > 0:
                        print(f"Product: {rand_product}- {product[1]} Added: {rand_quantity}")
                elif rand_quantity < 0:
                    print(f"Product: {rand_product}- {product[1]} removed: {rand_quantity}")    
                        
                i += 1    
            print('')
            cnx.commit()
            
        elif option == 5:
            print(f"{wf.quantity_of_products()} products")
            for i in range(1,wf.quantity_of_products()+1):
                product = wf.select_a_product(i)
                print(f"{i}-{product[1]} -> {wf.calculate_price(i,1)[0]}$ each one. Total: {wf.calculate_price(i,product[4])[0]}$")
        
        
        elif option == 6: 
            try:
                id_product = int(input("Select an Id_product to change price: "))
                product = wf.select_a_product(id_product)
                print(F"Current price: {product[3]}$")
                new_price = float(input(f"New price for {product[1]} -> "))
                while new_price < 0:
                    new_price = float(input("Price can't be negative -> "))
                wf.change_price(id_product,new_price)
                if new_price > product[3]:
                    print(f"Price of {product[1]} increased from {product[3]}to {new_price}$")
                elif new_price < product[3]:
                    print(f"Price of {product[1]} decreased from {product[3]}to {new_price}$")
                else:
                    print(f"Price of {product[1]} its the same")
            except ValueError:
                print("Invalid Character")
        elif option == 7:
            
            product_name = input("New Product Name: ")
            description = input("Description: ")
            price = float(input("Price: "))
     
            categories = wf.get_categories()
            print("Available categories:")
            for category in categories:
                print(f"id: {category[0]} - {category[1]}")
            id_category = int(input("choose a Category: "))
        
            suppliers = wf.get_suppliers()
            print("Available suppliers:")
            for supplier in suppliers:
                print(f"id: {supplier[0]} - {supplier[1]}")
            id_supplier = int(input("choose a Supplier: "))
            wf.create_product(product_name,description,price,id_supplier,id_category)
            print(f"{product_name} with id: {wf.quantity_of_products()} added to the system")
            
        elif option.lower() == 'c':
            wf.clear_console()
        elif option.lower() == 'q':
            wf.goodbye()
            break
    except ValueError:
        print("Invalid character, choose an option")

 
    