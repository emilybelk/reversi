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
	gameID INT PRIMARY KEY,
	userID INT,
	CONSTRAINT FOREIGN KEY (userID) REFERENCES user(userid),
	p1Score INT,
	p2Score INT,
	nextTurn TINYINT(1)
);

CREATE TABLE ranking (
	elo INT,	
	userID INT PRIMARY KEY,
	wins INT,
	losses INT,
	draws INT,
	CONSTRAINT FOREIGN KEY (userID) REFERENCES user(userID)
);