CREATE DATABASE reversi; 

USE reversi; 

CREATE TABLE user (
  userID INT PRIMARY KEY AUTO_INCREMENT,
  onlineStatus INT,
  inGameStatus INT,
  username VARCHAR(50),
  password VARCHAR(320)
);

CREATE TABLE game (
	#each square can be empty, white, or black
	#use size and board state to see which goes where -> need to convert to x by y array

	gameID INT,
	userID INT,
	CONSTRAINT FOREIGN KEY (userID) references user(userid),
	p1Score INT,
	p2Score INT,
	boardState BLOB, 
	rules VARCHAR(50),
	nextTurn TINYINT(1),
	boardSize INT
	PRIMARY KEY (userID, gameID)
);

CREATE TABLE ranking (
	userID INT,
	wins INT,
	losses INT,
	draws INT,
	elo INT,
	CONSTRAINT FOREIGN KEY (userID) references user(userID)
	PRIMARY KEY (userID, elo)
)