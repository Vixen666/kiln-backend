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
-- Table structure for table `Oven`
--

DROP TABLE IF EXISTS `Oven`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Oven` (
  `oven_id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(450) DEFAULT NULL,
  `max_temp_positive` float DEFAULT NULL,
  `max_temp_negative` float DEFAULT NULL,
  `location` varchar(450) DEFAULT NULL,
  `power` int(11) DEFAULT NULL,
  `thermometer_type` varchar(20) DEFAULT NULL,
  `thermometer_pin` int(11) DEFAULT NULL,
  `burner_pin` int(11) DEFAULT NULL,
  `thermocouple_type` enum('MAX3155','MAX3166','DHT11','DHT22','DS1820') DEFAULT NULL,
  `gpio_sensor_cs` int(2) DEFAULT NULL,
  `gpio_sensor_clock` int(2) DEFAULT NULL,
  `gpio_sensor_data` int(2) DEFAULT NULL,
  `gpio_sensor_di` int(2) DEFAULT NULL,
  `gpio_cool` int(2) DEFAULT NULL,
  `gpio_hatchet` int(2) DEFAULT NULL,
  `gpio_heat` int(11) DEFAULT NULL,
  `gpio_failsafe` int(2) DEFAULT NULL,
  `sensor_time_wait` int(4) DEFAULT 2,
  `pid_kp` int(11) DEFAULT 25,
  `pid_ki` int(11) DEFAULT 10,
  `pid_kd` int(11) DEFAULT 200,
  `temp_scale` char(1) DEFAULT 'c',
  `emergency_shutoff_temp` int(11) DEFAULT 1500,
  `kiln_must_catch_up` tinyint(4) DEFAULT 1,
  `pid_control_window` int(11) DEFAULT 5,
  `thermocouple_offset` int(11) DEFAULT 0,
  `temperature_average_samples` int(11) DEFAULT 40,
  `ac_freq_50hz` tinyint(4) DEFAULT 0,
  `automatic_restarts` tinyint(4) DEFAULT 1,
  `automatic_restart_window` int(11) DEFAULT 15,
  `simulate` tinyint(4) DEFAULT NULL,
  `sim_t_env` float DEFAULT NULL,
  `sim_c_heat` float DEFAULT NULL,
  `sim_c_oven` float DEFAULT NULL,
  `sim_p_heat` float DEFAULT NULL,
  `sim_R_o_nocool` float DEFAULT NULL,
  `sim_R_o_cool` float DEFAULT NULL,
  `sim_R_ho_noair` float DEFAULT NULL,
  `sim_R_ho_air` float DEFAULT NULL,
  `kwh_rate` float DEFAULT NULL,
  `currency_type` varchar(45) DEFAULT NULL,
  `kw_elements` float DEFAULT NULL,
  `hatchet_mode` enum('HIGH_OPEN','HIGH_CLOSED') DEFAULT 'HIGH_OPEN',
  PRIMARY KEY (`oven_id`)
) ENGINE=InnoDB AUTO_INCREMENT=18 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Oven`
--

LOCK TABLES `Oven` WRITE;
/*!40000 ALTER TABLE `Oven` DISABLE KEYS */;
INSERT INTO `Oven` VALUES (1,'Rohde TE-MCC+12345',80,52,'Attefall',5000,'K',15,18,'DS1820',NULL,NULL,NULL,NULL,NULL,NULL,24,NULL,2,25,14,202,'c',1500,1,5,0,10,0,0,15,0,25,500,5000,5450,0.5,0.05,0.1,0.05,1,'$',10,NULL),(16,'Rohde Ecotop123',12,2,'asdf',200,'S',3,2,'DS1820',23,2,3,4,0,24,25,8,2,26,5,17,'c',10000,1,10,0,10,1,1,10,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'HIGH_OPEN'),(17,'Testar',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL);
/*!40000 ALTER TABLE `Oven` ENABLE KEYS */;
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
