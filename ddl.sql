CREATE DATABASE reversi; 

USE reversi; 

CREATE TABLE user (
  userID INT PRIMARY KEY AUTO_INCREMENT,
  elo INT,
  username VARCHAR(50),
  password VARCHAR(320)
);

CREATE TABLE game (
	#each square can be empty, white, or black
	#use size and board state to see which goes where -> need to convert to x by y array

	player1ID INT,
	player2ID INT, 
	gameID INT,
	p1Score INT,
	p2Score INT,
	boardState BLOB, 
	rules VARCHAR(50),
	nextTurn TINYINT(1),
	boardSize INT
)