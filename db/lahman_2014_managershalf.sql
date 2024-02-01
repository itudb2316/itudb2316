-- MySQL dump 10.13  Distrib 8.0.34, for Win64 (x86_64)
--
-- Host: relational.fit.cvut.cz    Database: lahman_2014
-- ------------------------------------------------------
-- Server version	5.5.5-10.6.12-MariaDB-log

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `managershalf`
--

DROP TABLE IF EXISTS `managershalf`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `managershalf` (
  `managerID` varchar(10) NOT NULL,
  `yearID` int(11) NOT NULL,
  `teamID` varchar(3) NOT NULL,
  `lgID` varchar(2) DEFAULT NULL,
  `inseason` int(11) DEFAULT NULL,
  `half` int(11) NOT NULL,
  `G` int(11) DEFAULT NULL,
  `W` int(11) DEFAULT NULL,
  `L` int(11) DEFAULT NULL,
  `rank` int(11) DEFAULT NULL,
  PRIMARY KEY (`yearID`,`teamID`,`managerID`,`half`),
  KEY `managershalf_teamID` (`teamID`),
  KEY `managershalf_managerID` (`managerID`),
  CONSTRAINT `managershalf_ibfk_1` FOREIGN KEY (`teamID`) REFERENCES `teams` (`teamID`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `managershalf_ibfk_2` FOREIGN KEY (`managerID`) REFERENCES `managers` (`managerID`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3 COLLATE=utf8mb3_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `managershalf`
--

LOCK TABLES `managershalf` WRITE;
/*!40000 ALTER TABLE `managershalf` DISABLE KEYS */;
INSERT INTO `managershalf` VALUES ('hanlone01m',1892,'BLN','NL',3,1,56,17,39,12),('hanlone01m',1892,'BLN','NL',3,2,77,26,46,10),('vanhage01m',1892,'BLN','NL',1,1,11,1,10,12),('waltzjo99m',1892,'BLN','NL',2,1,8,2,6,12),('wardjo01m',1892,'BRO','NL',1,1,78,51,26,2),('wardjo01m',1892,'BRO','NL',1,2,80,44,33,3),('seleefr99m',1892,'BSN','NL',1,1,75,52,22,1),('seleefr99m',1892,'BSN','NL',1,2,77,50,26,2),('ansonca01m',1892,'CHN','NL',1,1,71,31,39,8),('ansonca01m',1892,'CHN','NL',1,2,76,39,37,7),('comisch01m',1892,'CIN','NL',1,1,77,44,31,4),('comisch01m',1892,'CIN','NL',1,2,78,38,37,8),('tebeapa01m',1892,'CL4','NL',1,1,74,40,33,5),('tebeapa01m',1892,'CL4','NL',1,2,79,53,23,1),('chapmja01m',1892,'LS3','NL',1,1,54,21,33,11),('pfefffr01m',1892,'LS3','NL',2,1,23,9,14,11),('pfefffr01m',1892,'LS3','NL',2,2,77,33,42,9),('powerpa99m',1892,'NY1','NL',1,1,74,31,43,10),('powerpa99m',1892,'NY1','NL',1,2,79,40,37,6),('wrighha01m',1892,'PHI','NL',1,1,77,46,30,3),('wrighha01m',1892,'PHI','NL',1,2,78,41,36,5),('buckeal99m',1892,'PIT','NL',1,1,29,15,14,6),('buckeal99m',1892,'PIT','NL',3,2,66,38,27,4),('burnsto01m',1892,'PIT','NL',2,1,47,22,25,6),('burnsto01m',1892,'PIT','NL',2,2,13,5,7,4),('carutbo01m',1892,'SLN','NL',5,2,50,16,32,11),('crookja01m',1892,'SLN','NL',3,1,47,24,22,9),('crookja01m',1892,'SLN','NL',3,2,15,3,11,11),('glassja01m',1892,'SLN','NL',1,1,4,1,3,9),('gorege01m',1892,'SLN','NL',4,2,16,6,9,11),('striccu01m',1892,'SLN','NL',2,1,23,6,17,9),('coxbo01m',1981,'ATL','NL',1,1,55,25,29,4),('coxbo01m',1981,'ATL','NL',1,2,52,25,27,5),('weaveea99m',1981,'BAL','AL',1,1,54,31,23,2),('weaveea99m',1981,'BAL','AL',1,2,51,28,23,4),('houkra01m',1981,'BOS','AL',1,1,56,30,26,5),('houkra01m',1981,'BOS','AL',1,2,52,29,23,2),('fregoji01m',1981,'CAL','AL',1,1,47,22,25,4),('mauchge01m',1981,'CAL','AL',2,1,13,9,4,4),('mauchge01m',1981,'CAL','AL',2,2,50,20,30,7),('larusto01m',1981,'CHA','AL',1,1,53,31,22,3),('larusto01m',1981,'CHA','AL',1,2,53,23,30,6),('amalfjo01m',1981,'CHN','NL',1,1,54,15,37,6),('amalfjo01m',1981,'CHN','NL',1,2,52,23,28,5),('mcnamjo99m',1981,'CIN','NL',1,1,56,35,21,2),('mcnamjo99m',1981,'CIN','NL',1,2,52,31,21,2),('garcida99m',1981,'CLE','AL',1,1,50,26,24,6),('garcida99m',1981,'CLE','AL',1,2,53,26,27,5),('andersp01m',1981,'DET','AL',1,1,57,31,26,4),('andersp01m',1981,'DET','AL',1,2,52,29,23,2),('virdobi01m',1981,'HOU','NL',1,1,57,28,29,3),('virdobi01m',1981,'HOU','NL',1,2,53,33,20,1),('freyji99m',1981,'KCA','AL',1,1,50,20,30,5),('freyji99m',1981,'KCA','AL',1,2,20,10,10,1),('howsedi01m',1981,'KCA','AL',2,2,33,20,13,1),('lasorto01m',1981,'LAN','NL',1,1,57,36,21,1),('lasorto01m',1981,'LAN','NL',1,2,53,27,26,4),('gardnbi02m',1981,'MIN','AL',2,1,20,6,14,7),('gardnbi02m',1981,'MIN','AL',2,2,53,24,29,4),('goryljo01m',1981,'MIN','AL',1,1,37,11,25,7),('rodgebu01m',1981,'ML4','AL',1,1,56,31,25,3),('rodgebu01m',1981,'ML4','AL',1,2,53,31,22,1),('fanniji01m',1981,'MON','NL',2,2,27,16,11,1),('willidi02m',1981,'MON','NL',1,1,55,30,25,3),('willidi02m',1981,'MON','NL',1,2,26,14,12,1),('lemonbo01m',1981,'NYA','AL',2,2,25,11,14,6),('michage01m',1981,'NYA','AL',1,1,56,34,22,1),('michage01m',1981,'NYA','AL',1,2,26,14,12,6),('torrejo01m',1981,'NYN','NL',1,1,52,17,34,5),('torrejo01m',1981,'NYN','NL',1,2,53,24,28,4),('martibi02m',1981,'OAK','AL',1,1,60,37,23,1),('martibi02m',1981,'OAK','AL',1,2,49,27,22,2),('greenda02m',1981,'PHI','NL',1,1,55,34,21,1),('greenda02m',1981,'PHI','NL',1,2,52,25,27,3),('tannech01m',1981,'PIT','NL',1,1,49,25,23,4),('tannech01m',1981,'PIT','NL',1,2,54,21,33,6),('howarfr01m',1981,'SDN','NL',1,1,56,23,33,6),('howarfr01m',1981,'SDN','NL',1,2,54,18,36,6),('lachere01m',1981,'SEA','AL',2,1,33,15,18,6),('lachere01m',1981,'SEA','AL',2,2,52,23,29,5),('willsma01m',1981,'SEA','AL',1,1,25,6,18,6),('robinfr02m',1981,'SFN','NL',1,1,59,27,32,5),('robinfr02m',1981,'SFN','NL',1,2,52,29,23,3),('herzowh01m',1981,'SLN','NL',1,1,51,30,20,2),('herzowh01m',1981,'SLN','NL',1,2,52,29,23,2),('zimmedo01m',1981,'TEX','AL',1,1,55,33,22,2),('zimmedo01m',1981,'TEX','AL',1,2,50,24,26,3),('mattibo01m',1981,'TOR','AL',1,1,58,16,42,7),('mattibo01m',1981,'TOR','AL',1,2,48,21,27,7);
/*!40000 ALTER TABLE `managershalf` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2023-10-20 19:00:13
