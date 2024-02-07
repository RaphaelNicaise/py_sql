import warehousefunctions as wf

cnx = wf.connect_to_db()
cursor = cnx.cursor()
    

    
while (True):
    try:
        
        print(r"""
              
                █░█░█ ▄▀█ █▀█ █▀▀ █░█ █▀█ █░█ █▀ █▀▀ █▀ █▄█ █▀
                ▀▄▀▄▀ █▀█ █▀▄ ██▄ █▀█ █▄█ █▄█ ▄█ ██▄ ▄█ ░█░ ▄█
                
                  1 - Info of a product 
                  2 - Select a Product ID & Calculate Price
                  3 - Insert N randon products 
                  4 - Show all prices 
                  5 - Quit
                  
                """)
        choice = int(input("Choose an Option -> "))
        if choice == 1: 
            try: 
                id_product = input("Select an Id_product: ")
                product = wf.select_a_product(id_product)
                if  int(id_product) <= wf.max_product_id: 
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
                
                if  id_product <= wf.max_product_id :       
                    
                    productname = wf.select_a_product(id_product)[1]
                    q = input(f"How many of {productname}? -> ")
                    price = wf.calculate_price(id_product,q)[0]
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
                rand_product = wf.choose_random_product()
                cursor.execute(f"SELECT product_name,quantity FROM warehousesystem.products pr join inventory inv on inv.id_product = pr.id_product where inv.id_product = {rand_product} ")
                productname_,q = cursor.fetchone()
                
                if q > 50:
                    rand_quantity = wf.choose_random_quantity(-49,50)
                elif q <= 50:
                    rand_quantity = wf.choose_random_quantity(0,50)
                    while rand_quantity == 0:
                        rand_quantity = wf.choose_random_quantity(0,50)
                    
                
                cursor.callproc("add_stock_2",(rand_product,rand_quantity))
                if rand_quantity > 0:
                        print(f"Product: {rand_product}- {productname_} Added: {rand_quantity}")
                elif rand_quantity < 0:
                    print(f"Product: {rand_product}- {productname_} removed: {rand_quantity}")    
                    
                i += 1    
            print('')
            cnx.commit()
            
        elif choice == 4:
            print(f"{wf.max_product_id} products")
            for i in range(1,wf.max_product_id+1):
                product = wf.select_a_product(i)
                print(f"{i}-{product[1]} -> {wf.calculate_price(i,1)[0]}$ each one. Total: {wf.calculate_price(i,product[4])[0]}$")
                  
        elif choice == 5:
            print("Leaving program")
            break
    except ValueError:
        print("Wrong character")
cnx.close()
 
    