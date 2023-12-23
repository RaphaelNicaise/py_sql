import mysql.connector
import pandas as pd

cnx = mysql.connector.MySQLConnection(
    user='root',password='',host='localhost',
    database='warehousesystem',port='3306'
)
cursor = cnx.cursor()
print("MySQL Connected")
