import math
import mysql.connector
import argparse
import os
from datetime import datetime

def probability (rating1, rating2):
	return 1.0 * 1.0 / (1 + 1.0 * math.pow(10, 1.0 * (rating1 - rating2) / 400))

# function to calculate and update elos 
def elo_rating (player1_elo, player2_elo, K, winner):
   
  
    # probability of player 2 winning
    p2 = probability(player1_elo, player2_elo)
  
    # probability of player 1 winning
    p1 = probability(player2_elo, player1_elo)
  
    # when winner == 1, player 1 wins. 
    if (winner == 1) :
        player1_elo = player1_elo + k * (1 - p1)
        player2_elo = player2_elo + k * (0 - p2)
      
  
    # when winner == 0, player 2 wins. 
    else :
        player1_elo = player1_elo + k * (0 - p1)
        player2_elo = player2_elo + k * (1 - p2)
      
  
player1_elo = 1200 # must pull current elo ratings of players
player2_elo = 1000 # must pull current elo ratings of players
k = 34 # a constant that determines how far the ratings can skew. We've chosen 34.
winner = 1	# must pull winner from game

#elo_rating(player1_elo, player2_elo, K, winner)

def elo_display():
    mydb = mysql.connector.connect(
        host="localhost",
        user="root"
    )  
    
    mycursor = mydb.cursor()
    mycursor.execute("USE reversi")
    operation = ("SELECT username , elo FROM ranking INNER JOIN user ON user.userID = ranking.userID ORDER BY elo DESC LIMIT 10")
    try: 
        mycursor.execute(operation)
        results = mycursor.fetchall()
        for result in results:
            print(result)
            #print(f"{result[0]} ({result[1]})")
            #results.append(result)
        return results
    except mysql.connector.Error as err:
        print("Error: {}".format(err))
        return False
