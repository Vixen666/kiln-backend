CREATE DATABASE  IF NOT EXISTS `KILN` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci */;
USE `KILN`;
-- MySQL dump 10.13  Distrib 8.0.36, for Win64 (x86_64)
--
-- Host: 192.168.0.21    Database: KILN
-- ------------------------------------------------------
-- Server version	5.5.5-10.5.26-MariaDB-0+deb11u2

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
-- Table structure for table `burn_curve`
--

DROP TABLE IF EXISTS `burn_curve`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `burn_curve` (
  `sequence` int(11) NOT NULL,
  `time` int(11) DEFAULT NULL,
  `temperature` int(11) DEFAULT NULL,
  `burn_id` int(11) NOT NULL,
  PRIMARY KEY (`sequence`,`burn_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `burn_curve`
--

LOCK TABLES `burn_curve` WRITE;
/*!40000 ALTER TABLE `burn_curve` DISABLE KEYS */;
INSERT INTO `burn_curve` VALUES (0,0,20,1),(0,0,20,2),(0,0,20,3),(0,0,20,4),(0,0,10,6),(0,0,10,8),(0,0,25,9),(1,7,60,1),(1,7,60,2),(1,7,60,3),(1,7,60,4),(1,1,10,5),(1,20,25,6),(1,1,10,7),(1,20,25,8),(1,2,27,9),(2,3,60,1),(2,3,60,2),(2,3,60,3),(2,3,60,4),(2,5,9,5),(2,7,60,6),(2,5,9,7),(2,7,60,8),(2,7,60,9),(3,5,70,1),(3,5,70,2),(3,5,70,3),(3,5,70,4),(3,3,60,6),(3,3,60,8),(3,3,60,9),(4,10,65,1),(4,10,65,2),(4,10,65,3),(4,10,65,4),(4,5,70,6),(4,5,70,8),(4,5,70,9),(5,5,90,1),(5,5,90,2),(5,5,90,3),(5,5,90,4),(5,10,65,6),(5,10,65,8),(5,10,65,9),(6,60,50,1),(6,5,90,6),(6,5,90,8),(6,5,90,9),(7,10,50,1),(7,60,50,2),(7,60,50,3),(7,60,50,4),(8,10,50,2),(8,10,50,3),(8,10,50,4),(8,60,50,6),(8,60,50,8),(8,60,50,9),(9,10,50,6),(9,10,50,8),(9,10,50,9);
/*!40000 ALTER TABLE `burn_curve` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-03-02 19:34:34
