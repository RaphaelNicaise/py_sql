import mysql.connector
import random
import pandas as pd
import tkinter as tk
from tkinter import messagebox

cnx = mysql.connector.MySQLConnection(
    user='root', password='', host='localhost',
    database='warehousesystem', port='3306')
cursor = cnx.cursor()

def choose_random_quantity():
    return random.randint(1, 50)

def choose_random_product():
    return random.randint(1, quantity_of_products())

def quantity_of_products():
    cursor.execute("SELECT MAX(id_product) FROM products")
    result = cursor.fetchone()[0]
    return result

def calculate_price():
    try:
        id_product = int(entry_product_id.get())
        if id_product <= max_product_id:
            cursor.execute(f"SELECT product_name FROM products WHERE id_product = {id_product}")
            product_name = cursor.fetchone()[0]

            quantity = int(entry_quantity.get())
            cursor.execute(f"SELECT price*{quantity} FROM products WHERE id_product = {id_product}")
            total_price = cursor.fetchone()[0]

            result_label.config(text=f"{quantity} of {product_name} -> {total_price}$")
        else:
            messagebox.showinfo("Error", f"There's no product with id {id_product}")
    except ValueError:
        messagebox.showinfo("Error", "Invalid input. Please enter valid numeric values.")

def insert_random_products():
    max_inserts = int(entry_max_inserts.get())
    i = 0
    results_text.set('')

    while i < max_inserts:
        rand_product = choose_random_product()
        rand_quantity = choose_random_quantity()
        cursor.callproc("add_stock_without_text", (rand_product, rand_quantity))
        cursor.execute(f"SELECT product_name FROM products WHERE id_product = {rand_product}")
        product_name = cursor.fetchone()[0]

        results_text.set(results_text.get() + f"Product: {rand_product}- {product_name} Added: {rand_quantity}\n")
        i += 1

    cnx.commit()

# Create Tkinter window
window = tk.Tk()
window.title("WarehouseSystem")

# Labels
label_product_id = tk.Label(window, text="Enter Product ID:")
label_quantity = tk.Label(window, text="Enter Quantity:")
label_max_inserts = tk.Label(window, text="Enter Max Inserts:")

# Entry widgets
entry_product_id = tk.Entry(window)
entry_quantity = tk.Entry(window)
entry_max_inserts = tk.Entry(window)

# Result label
result_label = tk.Label(window, text="")
results_text = tk.StringVar()
results_label = tk.Label(window, textvariable=results_text)

# Buttons
calculate_button = tk.Button(window, text="Calculate Price", command=calculate_price)
insert_button = tk.Button(window, text="Insert Random Products", command=insert_random_products)
quit_button = tk.Button(window, text="Quit", command=window.quit)

# Grid layout
label_product_id.grid(row=0, column=0)
entry_product_id.grid(row=0, column=1)
label_quantity.grid(row=1, column=0)
entry_quantity.grid(row=1, column=1)
calculate_button.grid(row=2, column=0, columnspan=2, pady=10)
result_label.grid(row=3, column=0, columnspan=2, pady=10)
label_max_inserts.grid(row=4, column=0)
entry_max_inserts.grid(row=4, column=1)
insert_button.grid(row=5, column=0, columnspan=2, pady=10)
results_label.grid(row=6, column=0, columnspan=2, pady=10)
quit_button.grid(row=7, column=0, columnspan=2, pady=10)

# Set initial max_product_id
max_product_id = quantity_of_products()

# Run the Tkinter event loop
window.mainloop()

# Close the database connection
cnx.close()