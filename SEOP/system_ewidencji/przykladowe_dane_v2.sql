-- --------------------------------------------------------
-- Host:                         127.0.0.1
-- Wersja serwera:               8.1.0 - MySQL Community Server - GPL
-- Serwer OS:                    Win64
-- HeidiSQL Wersja:              12.6.0.6765
-- --------------------------------------------------------

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET NAMES utf8 */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

-- Zrzut struktury tabela system_ewidencji.achievement
CREATE TABLE IF NOT EXISTS `achievement` (
  `aid` int NOT NULL AUTO_INCREMENT,
  `cid` int DEFAULT NULL,
  `title` varchar(100) DEFAULT NULL,
  `description` varchar(400) DEFAULT NULL,
  `start_date` date DEFAULT NULL,
  `end_date` date DEFAULT NULL,
  `hid` int DEFAULT NULL,
  `rating` float DEFAULT NULL,
  `uid` int DEFAULT NULL,
  `status` varchar(100) DEFAULT NULL,
  `to_fix_comment` varchar(200) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  PRIMARY KEY (`aid`),
  KEY `cid` (`cid`),
  KEY `hid` (`hid`),
  KEY `uid` (`uid`),
  CONSTRAINT `achievement_ibfk_1` FOREIGN KEY (`cid`) REFERENCES `category` (`cid`),
  CONSTRAINT `achievement_ibfk_2` FOREIGN KEY (`hid`) REFERENCES `hashtags` (`hid`),
  CONSTRAINT `achievement_ibfk_3` FOREIGN KEY (`uid`) REFERENCES `user` (`uid`)
) ENGINE=InnoDB AUTO_INCREMENT=28 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Zrzucanie danych dla tabeli system_ewidencji.achievement: ~19 rows (około)
INSERT INTO `achievement` (`aid`, `cid`, `title`, `description`, `start_date`, `end_date`, `hid`, `rating`, `uid`, `status`, `to_fix_comment`) VALUES
	(9, 28, 'Teoria ewolucji', 'O powstaniu gatunków', '2024-01-08', '2024-01-14', 2, 8.3, 5, 'APPROVED', NULL),
	(10, 28, 'Teoria ewolucji mózgu', 'Hmmmm', '2024-01-18', '2024-01-28', 2, 7.4, 5, 'APPROVED', NULL),
	(11, 32, 'Inna kategoria', 'Hmmmm', '2024-01-19', '2024-01-27', 6, NULL, 5, 'TO_BE_FIXED', 'Do poprawki to i to'),
	(12, 32, 'Tabliczka mnożenia', 'Tabliczka mnożenia', '2024-01-06', '2024-01-13', 1, 2, 12, 'APPROVED', NULL),
	(13, 31, 'Pierwsze lekcje kompozycji.', '1822', '2024-01-10', '2024-01-27', 3, 8, 3, 'APPROVED', NULL),
	(14, 31, 'Zakończenie nauki w Liceum Warszawskim.', '2024', '2024-01-09', '2024-01-18', 3, NULL, 3, 'REJECTED', NULL),
	(15, 31, 'Fortepian do poprawk', 'Do poprawki', '2024-01-11', '2024-02-01', 3, NULL, 3, 'TO_BE_FIXED', 'Do poprawki to i to'),
	(16, 31, 'Mistrzowskie kompozycje', 'Sonata', '2024-01-11', '2024-01-20', 3, 8.5, 3, 'APPROVED', NULL),
	(17, 31, 'Poznałem nuty', 'Do re mi', '2024-01-12', '2024-01-19', 3, 2, 4, 'APPROVED', NULL),
	(18, 31, 'Gra na skrzypcach', 'Fail', '2024-01-25', '2024-01-31', 3, NULL, 4, 'REJECTED', NULL),
	(19, 31, 'Witek Muzyk Ulicy', 'Do poprawki', '2024-01-06', '2024-01-19', 3, NULL, 4, 'TO_BE_FIXED', 'Do poprawki to i to'),
	(20, 28, 'Szczepionki', 'wiem wszystko o szczepionkach', '2024-01-20', '2024-01-20', 2, 3.8, 13, 'APPROVED', NULL),
	(21, 28, '5G', 'a co to?', '2024-01-12', '2024-01-19', 2, 2.6, 13, 'APPROVED', NULL),
	(22, 28, 'Ewolucja', 'do poprawy', '2024-01-13', '2024-01-19', 2, NULL, 13, 'TO_BE_FIXED', 'Do poprawki to i to'),
	(23, 28, 'Koniec COVIDa', 'Fail', '2024-01-04', '2024-01-18', 2, NULL, 13, 'REJECTED', NULL),
	(24, 27, 'Kamień jest super', 'ale jak to?', '2024-01-11', '2024-01-25', 2, NULL, 20, 'REJECTED', NULL),
	(25, 29, 'dobre osiągnięcie', 'to jest bardzo dobre osiągnięcie', '2024-01-09', '2024-01-18', 2, 6.5, 20, 'APPROVED', NULL),
	(26, 29, 'osiągniecie test 2', 'test daty', '2024-01-25', '2024-01-28', 1, NULL, 9, 'TO_BE_FIXED', 'To też sobie popraw'),
	(27, 29, 'słabe osiągnięcie', 'geolog7', '2024-01-18', '2024-01-18', 4, NULL, 20, 'NEW', NULL);

-- Zrzut struktury tabela system_ewidencji.category
CREATE TABLE IF NOT EXISTS `category` (
  `cid` int NOT NULL AUTO_INCREMENT,
  `category_name` varchar(100) NOT NULL,
  PRIMARY KEY (`cid`),
  UNIQUE KEY `category_name` (`category_name`)
) ENGINE=InnoDB AUTO_INCREMENT=33 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Zrzucanie danych dla tabeli system_ewidencji.category: ~6 rows (około)
INSERT INTO `category` (`cid`, `category_name`) VALUES
	(29, 'Badanie minerałow'),
	(27, 'Koordynacja zadań'),
	(32, 'Nauczanie algebry'),
	(28, 'Nauczanie o ewolucji'),
	(31, 'Tworzenie muzyki'),
	(30, 'Zarządzanie uczelnią');

-- Zrzut struktury tabela system_ewidencji.hashtags
CREATE TABLE IF NOT EXISTS `hashtags` (
  `hid` int NOT NULL AUTO_INCREMENT,
  `hashtag_name` varchar(100) NOT NULL,
  PRIMARY KEY (`hid`),
  UNIQUE KEY `hashtag_name` (`hashtag_name`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Zrzucanie danych dla tabeli system_ewidencji.hashtags: ~6 rows (około)
INSERT INTO `hashtags` (`hid`, `hashtag_name`) VALUES
	(2, 'Biolog'),
	(6, 'Dziekan'),
	(4, 'Geolog'),
	(1, 'Matematyk'),
	(3, 'Muzyk'),
	(5, 'Organizator');

-- Zrzut struktury tabela system_ewidencji.task
CREATE TABLE IF NOT EXISTS `task` (
  `tid` int NOT NULL AUTO_INCREMENT,
  `title` varchar(100) DEFAULT NULL,
  `description` varchar(400) DEFAULT NULL,
  `cid` int DEFAULT NULL,
  `uid` int DEFAULT NULL,
  PRIMARY KEY (`tid`),
  KEY `cid` (`cid`),
  KEY `uid` (`uid`),
  CONSTRAINT `task_ibfk_1` FOREIGN KEY (`cid`) REFERENCES `category` (`cid`),
  CONSTRAINT `task_ibfk_2` FOREIGN KEY (`uid`) REFERENCES `user` (`uid`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Zrzucanie danych dla tabeli system_ewidencji.task: ~0 rows (około)
INSERT INTO `task` (`tid`, `title`, `description`, `cid`, `uid`) VALUES
	(4, 'zadanie matematyczne', 'w tym zadaniu należy obliczyć deltę', 32, 3);

-- Zrzut struktury tabela system_ewidencji.user
CREATE TABLE IF NOT EXISTS `user` (
  `uid` int NOT NULL AUTO_INCREMENT,
  `login` varchar(100) DEFAULT NULL,
  `password` varchar(300) DEFAULT NULL,
  `role` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`uid`),
  UNIQUE KEY `login` (`login`)
) ENGINE=InnoDB AUTO_INCREMENT=21 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Zrzucanie danych dla tabeli system_ewidencji.user: ~19 rows (około)
INSERT INTO `user` (`uid`, `login`, `password`, `role`) VALUES
	(2, 'admin', 'pbkdf2:sha256:600000$QcxOET4pKLUPRjZJ$b8a79c72dab435c4cef8668888106d700ebde9c9f14ebbbf7f695d59f636073f', 'admin'),
	(3, 'szopen', 'pbkdf2:sha256:600000$NCWzdXVGwAq4wemh$795039dcc9a8822e74d4f2160382ea67813e3c4c31b54f59864c5f29927e9eb2', 'user'),
	(4, 'slabymuzyk', 'pbkdf2:sha256:600000$XTbYMmICIPRqsHWe$4d600783b6bf86c7bc4aa7e056cc7d064890d155898ba62a5850e7c9caa9b134', 'user'),
	(5, 'darwin', 'pbkdf2:sha256:600000$IGMOuHQFDuEG62xt$9de292ea10230ac9fa506867934e53beea00f755dce18fc69d8ee1823e63e7a6', 'user'),
	(6, 'geolog_dobry', 'pbkdf2:sha256:600000$o8MVRdfxnTvEyy0x$b024e768af88d8755947a8e9f5bdf68f09661deda15ddb40064cd8bce213ad11', 'user'),
	(7, 'geolog_sredni', 'pbkdf2:sha256:600000$suz9Ikrxc8Nm0g3I$d743b75a5136897561ac5e416b225619bbf0bc164775139ac785438a1eb23059', 'user'),
	(8, 'geolog_slaby', 'pbkdf2:sha256:600000$0O8ynmFw1Zfyl6Bg$b5c37dc33fa20260d6b99af76cdab9c84883e6b007cbc9db9e0aaee7fcca6b96', 'user'),
	(9, 'koordynator_dobry', 'pbkdf2:sha256:600000$CKh8PyEbQ4TIXUXe$4d941bdc3e4f029b884f2f1ad416aae5ce18a9729bc9a60036e25bff22243f7b', 'user'),
	(10, 'koordynator_slaby', 'pbkdf2:sha256:600000$PKmtsvCiGjhK5buO$fe3aa87ea22a37251128dfb4056ec36600613d551bcf3914341d12e8b2953611', 'user'),
	(11, 'matematyk_wyzszy', 'pbkdf2:sha256:600000$C6haqhIt2ASEDvT0$7943937b557b9567d879f6d030debedd66280e2a72cf53c3aa4ed111a0887386', 'user'),
	(12, 'matematyk_nizszy', 'pbkdf2:sha256:600000$GqipVWdtnXct39wG$228a4f217b0443e958faaf33ead3e361570178987991d340f489a09f3febfb44', 'user'),
	(13, 'antyewolucjonista', 'pbkdf2:sha256:600000$NbTrq49cRVhIZDA8$b9b1b4c0ff6e631bc0d2533512d8864764831567b8450ab486672ffdd1ecd226', 'user'),
	(14, 'dziekan_mit', 'pbkdf2:sha256:600000$egFRUBzYOZAStUpW$2c126034b9e26c8e421e41d6b322f2ab3b4410abe25a10ce4cae2c5a2bdc2fa8', 'user'),
	(15, 'dziekan_pbs', 'pbkdf2:sha256:600000$m6OX0u4Pe7EmgSvc$edca4954a04071ce8bbffd90961d316d3c31fb79ef71d72e5cb651eccf5aa6bc', 'user'),
	(16, 'dziekan_ukw', 'pbkdf2:sha256:600000$UjSzi3zPUS5ePDu4$ca20799319d97d481bef4369ed09d49a71fbc552d15b7b9a714c82720cba86b5', 'user'),
	(17, 'osoba1', 'pbkdf2:sha256:600000$YW7H7PcQLZCnzy1G$df378f83787db21db9df894092065d762ca08091fb04d266ec0bbecb5da4ba07', 'user'),
	(18, 'osoba2', 'pbkdf2:sha256:600000$7ll9ikib4Gmab7Jj$cda9f14d8499e5b84ecab343e10314dbefcb4b871715c1b84f83f9aa967e387d', 'user'),
	(19, 'osoba3', 'pbkdf2:sha256:600000$P263dpw3ep7PkSQr$36aa7e9e7d3cc36bbceb000737cb305343415147d5cd92ff97592ab82035a78b', 'user'),
	(20, 'ww', 'pbkdf2:sha256:600000$Z3ACtekzBjDT3PEk$7268385bb915b1a5f6cdd513695a11d3a5f8b30e968f7eec12708ffa24a88a65', 'user');

/*!40103 SET TIME_ZONE=IFNULL(@OLD_TIME_ZONE, 'system') */;
/*!40101 SET SQL_MODE=IFNULL(@OLD_SQL_MODE, '') */;
/*!40014 SET FOREIGN_KEY_CHECKS=IFNULL(@OLD_FOREIGN_KEY_CHECKS, 1) */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40111 SET SQL_NOTES=IFNULL(@OLD_SQL_NOTES, 1) */;
