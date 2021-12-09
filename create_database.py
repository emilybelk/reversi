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

    load_dml_str = open("dml.sql").read()
    load_dml_data = load_dml_str.split(';')    

    for i in load_ddl_data:
        mycursor.execute(i)

    for i in load_dml_data:
        mycursor.execute(i)

    return mydb

db = init()