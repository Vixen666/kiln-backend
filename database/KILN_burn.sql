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
-- Table structure for table `burn`
--

DROP TABLE IF EXISTS `burn`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `burn` (
  `burn_id` int(11) NOT NULL,
  `start_date` datetime DEFAULT NULL,
  `end_date` datetime DEFAULT NULL,
  `description` varchar(400) DEFAULT NULL,
  `oven_id` int(11) NOT NULL,
  `template_id` int(11) NOT NULL,
  `status` varchar(400) NOT NULL DEFAULT 'Preparing',
  PRIMARY KEY (`burn_id`,`oven_id`,`template_id`),
  KEY `fk_burn_Oven1_idx` (`oven_id`),
  KEY `fk_burn_template1_idx` (`template_id`),
  CONSTRAINT `fk_burn_template1` FOREIGN KEY (`template_id`) REFERENCES `template` (`template_id`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `burn`
--

LOCK TABLES `burn` WRITE;
/*!40000 ALTER TABLE `burn` DISABLE KEYS */;
INSERT INTO `burn` VALUES (1,'2024-06-17 12:52:06',NULL,'Test',1,1,'Preparing'),(2,'2025-02-09 22:18:00',NULL,'test123',1,1,'Preparing'),(3,'2025-02-17 22:54:18',NULL,'',16,1,'Preparing'),(4,'2025-02-25 23:24:40',NULL,'Test',16,1,'Preparing'),(5,'2025-02-25 23:24:55',NULL,'Test2',16,19,'Preparing'),(6,'2025-02-26 00:17:05',NULL,'321',1,1,'Preparing'),(7,'2025-02-26 00:22:17',NULL,'321',1,19,'Preparing'),(8,'2025-02-26 19:05:38',NULL,'',16,1,'Preparing'),(9,'2025-02-26 21:07:39',NULL,'',16,1,'Preparing');
/*!40000 ALTER TABLE `burn` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-03-02 19:34:37
