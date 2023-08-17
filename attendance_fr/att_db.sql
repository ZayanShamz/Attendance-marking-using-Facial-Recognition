/*
SQLyog Community v13.2.0 (64 bit)
MySQL - 5.1.32-community : Database - attendance
*********************************************************************
*/

/*!40101 SET NAMES utf8 */;

/*!40101 SET SQL_MODE=''*/;

/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;
CREATE DATABASE /*!32312 IF NOT EXISTS*/`attendance` /*!40100 DEFAULT CHARACTER SET latin1 */;

USE `attendance`;

/*Table structure for table `0_class` */

DROP TABLE IF EXISTS `0_class`;

CREATE TABLE `0_class` (
  `class_id` int(15) NOT NULL AUTO_INCREMENT,
  `class` varchar(50) DEFAULT NULL,
  `fac` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`class_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

/*Data for the table `0_class` */

/*Table structure for table `0_faculty` */

DROP TABLE IF EXISTS `0_faculty`;

CREATE TABLE `0_faculty` (
  `id` int(15) NOT NULL AUTO_INCREMENT,
  `login_id` int(15) DEFAULT NULL,
  `name` varchar(100) DEFAULT NULL,
  `dob` varchar(15) DEFAULT NULL,
  `gender` varchar(15) DEFAULT NULL,
  `email` varchar(88) DEFAULT NULL,
  `phone` varchar(15) DEFAULT NULL,
  `qualification` varchar(100) DEFAULT NULL,
  `department` varchar(50) DEFAULT NULL,
  `experience` varchar(15) DEFAULT NULL,
  `address` varchar(200) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=latin1;

/*Data for the table `0_faculty` */

/*Table structure for table `0_login` */

DROP TABLE IF EXISTS `0_login`;

CREATE TABLE `0_login` (
  `login_id` int(15) NOT NULL AUTO_INCREMENT,
  `username` varchar(100) DEFAULT NULL,
  `password` varchar(100) DEFAULT NULL,
  `usertype` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`login_id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=latin1;

/*Data for the table `0_login` */

insert  into `0_login`(`login_id`,`username`,`password`,`usertype`) values 
(1,'admin','admin','admin');

/*Table structure for table `0_students` */

DROP TABLE IF EXISTS `0_students`;

CREATE TABLE `0_students` (
  `id` int(15) NOT NULL AUTO_INCREMENT,
  `reg_no` varchar(50) DEFAULT NULL,
  `name` varchar(100) DEFAULT NULL,
  `dob` varchar(50) DEFAULT NULL,
  `gender` varchar(50) DEFAULT NULL,
  `email` varchar(100) DEFAULT NULL,
  `phone` varchar(15) DEFAULT NULL,
  `address` varchar(200) DEFAULT NULL,
  `class` varchar(100) DEFAULT NULL,
  `photo` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=latin1;

/*Data for the table `0_students` */

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;
