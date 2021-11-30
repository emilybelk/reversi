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

def registerUser(mydb, username, password):
# credit to https://dev.mysql.com/doc/connector-python/en/connector-python-api-mysqlcursor-execute.html
    mycursor = mydb.cursor()
    mycursor.execute("USE reversi")
    insert_stmt = ("INSERT INTO user (username, password) VALUES (%s, %s)")
    data = (username.get(), password.get())
    try: 
        mycursor.execute(insert_stmt, data)
        # print("Updated table")
        # print("{:<15}{:<15}".format("username", "password"))
    #     mycursor.execute("SELECT * FROM user")
    #     for x in mycursor:
    #         print("{:<15}{:<15}".format(x[0],x[1]))
    # except mysql.connector.Error as err:
    #     print("Error: {}".format(err))


def cleanup(mydb):
    mycursor = mydb.cursor()
    mycursor.execute("DROP DATABASE reversi")

    mydb.close()
    exit()

db = init()
cleanup(db)
