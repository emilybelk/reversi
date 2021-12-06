import mysql.connector
import argparse
import os
from datetime import datetime

# function to register a user 
def register_user(username, password):
    mydb = mysql.connector.connect(
        host="localhost",
        user="root"
    )  
    mycursor = mydb.cursor()
    mycursor.execute("USE reversi")
    sel = ("SELECT username FROM user WHERE username = %s")
    seldata = (username,)
    data = (username, password)
    ins = ("INSERT INTO user (username, password) VALUES (%s, %s)")
    try: 
        mycursor.execute(sel, seldata)
        if mycursor.fetchall(): # checking if something found with this username
            print('Username already exists')
            return False
        else:
            try:
                mycursor.execute(ins, data)
                mydb.commit()
                return True
            except mysql.connector.Error as err:
                print("Error: {}".format(err))
                return False         
    except mysql.connector.Error as err:
        print("Error: {}".format(err))
        return False

# function to help a user login 
def login_user(username, password):
    mydb = mysql.connector.connect(
        host="localhost",
        user="root"
    )  
    mycursor = mydb.cursor()
    mycursor.execute("USE reversi")
    exe = ("SELECT userID from user WHERE username =%s AND password=%s")
    data = (username, password)
    try: 
        mycursor.execute(exe, data)  
        if mycursor.fetchall():      
            return True
        else:
            print("Account not found")
            return False
    except mysql.connector.Error as err:
        print("Error: {}".format(err))
        return False
        

# def updateUserInformation():    

# result = mycursor.fetchall() -> fetching data from table