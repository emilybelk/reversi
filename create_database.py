import mysql.connector
import argparse
import os
from datetime import datetime


# Loads data into the database
# returns connection to the database
def init():
    mydb = mysql.connector.connect(
        host="localhost",
        user="root"
    )  
    mydb.autocommit = True
    mycursor = mydb.cursor()

    load_ddl_str = open("ddl.sql").read()
    load_ddl_data = load_ddl_str.split(';')

    for i in load_ddl_data:
        mycursor.execute(i)

    return mydb

db = init()
