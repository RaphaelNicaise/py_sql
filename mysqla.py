import mysql.connector

conexion = mysql.connector.connect(user="root",password="",host="127.0.0.1",
                                   database="warehousesystem",port="3306",)

cursor = conexion.cursor()

cursor.execute("select count(*) from inventory")
quantity = cursor.fetchone()[0]
productQuantities = {}
for i in (range(1,quantity+1)):
   
    cursor.execute(f"SELECT * FROM inventory i join products p on p.id_product = i.id_product where i.id_product = {i} ")
    result = cursor.fetchone()
    quantity = result[2]
    product_name = result[6]
    productQuantities[product_name] = quantity
    
total_sum = sum(productQuantities.values())
for product,quantity in productQuantities.items():
    print(f"{product}: {quantity} $")
print(f"Suma total de productos es: {total_sum}$")
print(f"El precio promedio de los productos es {round(total_sum/quantity+1)}")
cursor.close()
conexion.close()
