import mysql.connector
import pandas as pd

cnx = mysql.connector.MySQLConnection(
    ser='root',password='',host='localhost',
    database='warehousesystem',port='3306'
)
cursor = cnx.cursor()
