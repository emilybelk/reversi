USE reversi; 

INSERT INTO user (userID, onlineStatus, inGameStatus, username, password)
VALUES  (1, 0, 0, "edwardsmith123", "$2a$04$kMD/yOVyrXoohIve83k31uXL4VIi6p8B/oZlG7tbWqXGBq2C.4HAS"),
		(2, 0, 0, "janebrown125", "$2a$04$KAq0BK4/x3hbDpVbdb3j/OTDcpRmTFHJd.5OlbzGzc3.mg43NRe.q"),
		(3, 0, 0, "randomaccount", "$2a$04$hux67tSR9lhaxrmlYln6uOGzddqZYUiCaqETqxHGzsYWiRSwyHsk2"),
		(4, 0, 0, "also_random_woo", "$2a$04$hp5tcPt4DANWASFka7QEl.e9nJZrpTMREbITfgyRwJ/OafQ3wlrxC"),
		(5, 0, 0, "emilywangxd", "$2a$04$E3IyxvqPI4QmrJnfOdmaTeZwywQTwhM1C/i26IYhXDlv4gqKbrhxy"),
		(6, 0, 0, "patriciablack135", "$2a$04$fD5h.DGFOYUbsZd0jUqx2.4ny7.yrc1w./zBwk9lfbCzHx1veCSf6"),
		(7, 0, 0, "software_engineering_is_fun", "$2a$04$543GwVNX2984qDGu5.2e9usaBht7Q496g7L0ouz40NSXazPLsnsCG"),
		(8, 0, 0, "paytonvu222", "$2a$04$xQiAyTs4hSnBjk5TQFrOguBNyJlER9ggRbv/mb0pP1yCBACrSO4ba"),
		(9, 0, 0, "ducky_45", "$2a$04$abrtNLsst9SrCmGHrR46GOw2mAiM8ONnh27wrXdb.EQ6QUovnwWp6"),
		(10, 0, 0, "zak_yok", "$2a$04$4lRJl5RFqyGH5LXukE6NCOQXFcezyEXpM0vdk9nKZS.AQDj13gPkm");

INSERT INTO ranking (userID, wins, losses, draws, elo)
VALUES	(1, 0, 0, 0, 1000),
		(2, 1, 0, 0, 1400),
		(3, 0, 0, 0, 1000),
		(4, 0, 0, 0, 1000),
		(5, 0, 0, 0, 1000),
		(6, 0, 0, 0, 1000),
		(7, 0, 0, 0, 1000),
		(8, 2, 0, 0, 1400),
		(9, 0, 0, 0, 1000),
		(10, 0, 0, 0, 1000);														

INSERT INTO game (gameID, userID, p1Score, p2Score, nextTurn)
VALUES	(1, 1, 22, 10, 0),
		(2, 2, 12, 20, 0);