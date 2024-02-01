USE lahman_2014;

DROP TABLE IF EXISTS `fielding_sub`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `fielding_sub` (
  `playerID` varchar(9) NOT NULL,
  `yearID` int(11) NOT NULL,
  `stint` int(11) NOT NULL,
  `teamID` varchar(3) DEFAULT NULL,
  `lgID` varchar(2) DEFAULT NULL,
  `WP` int(11) DEFAULT NULL,
  `ZR` int(11) DEFAULT NULL,
  PRIMARY KEY (`playerID`,`yearID`,`stint`),
  KEY `fielding_sub_teamID` (`teamID`),
  CONSTRAINT `fielding_sub_ibfk_1` FOREIGN KEY (`teamID`) REFERENCES `teams` (`teamID`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `fielding_sub_ibfk_2` FOREIGN KEY (`playerID`) REFERENCES `players` (`playerID`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3 COLLATE=utf8mb3_general_ci;

INSERT INTO fielding_sub (playerID, yearID, stint)
SELECT DISTINCT playerID, yearID, stint FROM fielding;

UPDATE fielding_sub
JOIN fielding ON fielding.playerID = fielding_sub.playerID AND
fielding.yearID = fielding_sub.yearID AND fielding.stint = fielding_sub.stint
SET fielding_sub.teamID = fielding.teamID, fielding_sub.lgID = fielding.lgID,
fielding_sub.wp = fielding.wp, fielding_sub.zr = fielding.zr;

ALTER TABLE fielding
DROP COLUMN WP,
DROP COLUMN ZR;

SELECT * FROM fielding;