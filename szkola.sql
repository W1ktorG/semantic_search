-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Maj 12, 2025 at 11:44 AM
-- Wersja serwera: 10.4.32-MariaDB
-- Wersja PHP: 8.2.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `szkola`
--

-- --------------------------------------------------------

--
-- Struktura tabeli dla tabeli `absolwenci`
--

CREATE TABLE `absolwenci` (
  `id` int(11) NOT NULL,
  `szkola_id` int(11) DEFAULT NULL,
  `laczna_liczba` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `absolwenci`
--

INSERT INTO `absolwenci` (`id`, `szkola_id`, `laczna_liczba`) VALUES
(1, 1, 8000);

-- --------------------------------------------------------

--
-- Struktura tabeli dla tabeli `obecna_sytuacja`
--

CREATE TABLE `obecna_sytuacja` (
  `id` int(11) NOT NULL,
  `szkola_id` int(11) DEFAULT NULL,
  `liczba_uczniow` int(11) DEFAULT NULL,
  `kadra` text DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `obecna_sytuacja`
--

INSERT INTO `obecna_sytuacja` (`id`, `szkola_id`, `liczba_uczniow`, `kadra`) VALUES
(1, 1, 700, 'wysoko wykwalifikowana kadra nauczycielska');

-- --------------------------------------------------------

--
-- Struktura tabeli dla tabeli `osiagniecia`
--

CREATE TABLE `osiagniecia` (
  `id` int(11) NOT NULL,
  `absolwent_id` int(11) DEFAULT NULL,
  `opis` text DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `osiagniecia`
--

INSERT INTO `osiagniecia` (`id`, `absolwent_id`, `opis`) VALUES
(1, 1, 'tytuły naukowe (politechnika, humanistyka, sztuka, wojskowość, oświata)'),
(2, 1, 'ważne funkcje w administracji państwowej i oświatowej'),
(3, 1, 'dobrzy fachowcy, menadżerowie, właściciele firm');

-- --------------------------------------------------------

--
-- Struktura tabeli dla tabeli `profile`
--

CREATE TABLE `profile` (
  `id` int(11) NOT NULL,
  `szkola_id` int(11) DEFAULT NULL,
  `nazwa` varchar(255) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `profile`
--

INSERT INTO `profile` (`id`, `szkola_id`, `nazwa`) VALUES
(1, 1, 'profil ogólny'),
(2, 1, 'profil turystyczno-przyrodniczy');

-- --------------------------------------------------------

--
-- Struktura tabeli dla tabeli `szkola`
--

CREATE TABLE `szkola` (
  `id` int(11) NOT NULL,
  `nazwa` varchar(255) DEFAULT NULL,
  `rok_zalozenia` int(11) DEFAULT NULL,
  `opis` text DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `szkola`
--

INSERT INTO `szkola` (`id`, `nazwa`, `rok_zalozenia`, `opis`) VALUES
(1, 'Zespół Szkół Nr 2 im. Przyjaźni Polsko-Norweskiej w Ostrzeszowie', 1972, 'Placówka kształcąca nieustannie od 1972 roku. Modernizowana i dostosowywana do wymogów lokalnego rynku pracy. Opuszczona przez ponad 8000 absolwentów, wielu z nich pełni ważne funkcje w administracji i oświacie.');

-- --------------------------------------------------------

--
-- Struktura tabeli dla tabeli `szkoly`
--

CREATE TABLE `szkoly` (
  `id` int(11) NOT NULL,
  `szkola_id` int(11) DEFAULT NULL,
  `typ` varchar(100) DEFAULT NULL,
  `cykl` varchar(50) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `szkoly`
--

INSERT INTO `szkoly` (`id`, `szkola_id`, `typ`, `cykl`) VALUES
(1, 1, 'Liceum Ogólnokształcące', '4-letni'),
(2, 1, 'Technikum', '5-letni'),
(3, 1, 'Branżowa Szkoła I Stopnia', '3-letni'),
(4, 1, 'Branżowa Szkoła II Stopnia', '2-letni');

-- --------------------------------------------------------

--
-- Struktura tabeli dla tabeli `zawody`
--

CREATE TABLE `zawody` (
  `id` int(11) NOT NULL,
  `szkola_id` int(11) DEFAULT NULL,
  `nazwa` varchar(255) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `zawody`
--

INSERT INTO `zawody` (`id`, `szkola_id`, `nazwa`) VALUES
(1, 2, 'technik architektury krajobrazu'),
(2, 2, 'technik elektryk (z elementami OZE)'),
(3, 2, 'technik informatyk'),
(4, 2, 'technik logistyk'),
(5, 2, 'technik mechatronik (z elementami OZE)'),
(6, 2, 'technik pojazdów samochodowych'),
(7, 2, 'technik programista'),
(8, 2, 'technik rolnik'),
(9, 2, 'technik żywienia i usług gastronomicznych'),
(10, 3, 'elektryk'),
(11, 3, 'magazynier – logistyk'),
(12, 3, 'mechanik pojazdów samochodowych'),
(13, 3, 'operator obrabiarek skrawających'),
(14, 3, 'klasa wielozawodowa'),
(15, 4, 'technik pojazdów samochodowych');

--
-- Indeksy dla zrzutów tabel
--

--
-- Indeksy dla tabeli `absolwenci`
--
ALTER TABLE `absolwenci`
  ADD PRIMARY KEY (`id`),
  ADD KEY `szkola_id` (`szkola_id`);

--
-- Indeksy dla tabeli `obecna_sytuacja`
--
ALTER TABLE `obecna_sytuacja`
  ADD PRIMARY KEY (`id`),
  ADD KEY `szkola_id` (`szkola_id`);

--
-- Indeksy dla tabeli `osiagniecia`
--
ALTER TABLE `osiagniecia`
  ADD PRIMARY KEY (`id`),
  ADD KEY `absolwent_id` (`absolwent_id`);

--
-- Indeksy dla tabeli `profile`
--
ALTER TABLE `profile`
  ADD PRIMARY KEY (`id`),
  ADD KEY `szkola_id` (`szkola_id`);

--
-- Indeksy dla tabeli `szkola`
--
ALTER TABLE `szkola`
  ADD PRIMARY KEY (`id`);

--
-- Indeksy dla tabeli `szkoly`
--
ALTER TABLE `szkoly`
  ADD PRIMARY KEY (`id`),
  ADD KEY `szkola_id` (`szkola_id`);

--
-- Indeksy dla tabeli `zawody`
--
ALTER TABLE `zawody`
  ADD PRIMARY KEY (`id`),
  ADD KEY `szkola_id` (`szkola_id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `absolwenci`
--
ALTER TABLE `absolwenci`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT for table `obecna_sytuacja`
--
ALTER TABLE `obecna_sytuacja`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT for table `osiagniecia`
--
ALTER TABLE `osiagniecia`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT for table `profile`
--
ALTER TABLE `profile`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT for table `szkola`
--
ALTER TABLE `szkola`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT for table `szkoly`
--
ALTER TABLE `szkoly`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- AUTO_INCREMENT for table `zawody`
--
ALTER TABLE `zawody`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=16;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `absolwenci`
--
ALTER TABLE `absolwenci`
  ADD CONSTRAINT `absolwenci_ibfk_1` FOREIGN KEY (`szkola_id`) REFERENCES `szkola` (`id`);

--
-- Constraints for table `obecna_sytuacja`
--
ALTER TABLE `obecna_sytuacja`
  ADD CONSTRAINT `obecna_sytuacja_ibfk_1` FOREIGN KEY (`szkola_id`) REFERENCES `szkola` (`id`);

--
-- Constraints for table `osiagniecia`
--
ALTER TABLE `osiagniecia`
  ADD CONSTRAINT `osiagniecia_ibfk_1` FOREIGN KEY (`absolwent_id`) REFERENCES `absolwenci` (`id`);

--
-- Constraints for table `profile`
--
ALTER TABLE `profile`
  ADD CONSTRAINT `profile_ibfk_1` FOREIGN KEY (`szkola_id`) REFERENCES `szkoly` (`id`);

--
-- Constraints for table `szkoly`
--
ALTER TABLE `szkoly`
  ADD CONSTRAINT `szkoly_ibfk_1` FOREIGN KEY (`szkola_id`) REFERENCES `szkola` (`id`);

--
-- Constraints for table `zawody`
--
ALTER TABLE `zawody`
  ADD CONSTRAINT `zawody_ibfk_1` FOREIGN KEY (`szkola_id`) REFERENCES `szkoly` (`id`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
