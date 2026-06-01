-- ============================================================
-- SEMINARSKI RAD: Data Warehouse IT kompanije
-- Student: Ognjen Grgur, MIT 37/24
-- ============================================================
-- KORAK 1: Kreiranje baze podataka
-- ============================================================

CREATE DATABASE ITKompanijaDW;
GO
USE ITKompanijaDW;
GO

-- ============================================================
-- KORAK 2: Kreiranje tabela (transakciona baza)
-- ============================================================

CREATE TABLE Odeljenje (
    idOdeljenja INT PRIMARY KEY IDENTITY(1,1),
    nazivOdeljenja NVARCHAR(100) NOT NULL
);

CREATE TABLE Zaposleni (
    idZaposlenog INT PRIMARY KEY IDENTITY(1,1),
    ime NVARCHAR(50) NOT NULL,
    prezime NVARCHAR(50) NOT NULL,
    pozicija NVARCHAR(100),
    idOdeljenja INT FOREIGN KEY REFERENCES Odeljenje(idOdeljenja),
    datumZaposlenja DATE,
    satnica DECIMAL(10,2)
);

CREATE TABLE Klijent (
    idKlijenta INT PRIMARY KEY IDENTITY(1,1),
    nazivKompanije NVARCHAR(200) NOT NULL,
    kontaktOsoba NVARCHAR(100),
    grad NVARCHAR(100),
    drzava NVARCHAR(100)
);

CREATE TABLE Projekat (
    idProjekta INT PRIMARY KEY IDENTITY(1,1),
    nazivProjekta NVARCHAR(200) NOT NULL,
    opis NVARCHAR(MAX),
    datumPocetka DATE,
    datumZavrsetka DATE,
    budzet DECIMAL(12,2),
    status NVARCHAR(50),
    idKlijenta INT FOREIGN KEY REFERENCES Klijent(idKlijenta)
);

CREATE TABLE Tehnologija (
    idTehnologije INT PRIMARY KEY IDENTITY(1,1),
    nazivTehnologije NVARCHAR(100) NOT NULL,
    kategorija NVARCHAR(50)
);

CREATE TABLE ProjekatTehnologija (
    idProjekta INT FOREIGN KEY REFERENCES Projekat(idProjekta),
    idTehnologije INT FOREIGN KEY REFERENCES Tehnologija(idTehnologije),
    PRIMARY KEY (idProjekta, idTehnologije)
);

CREATE TABLE EvidencijaSati (
    idEvidencije INT PRIMARY KEY IDENTITY(1,1),
    idZaposlenog INT FOREIGN KEY REFERENCES Zaposleni(idZaposlenog),
    idProjekta INT FOREIGN KEY REFERENCES Projekat(idProjekta),
    datum DATE NOT NULL,
    brojSati DECIMAL(5,2) NOT NULL,
    opis NVARCHAR(500)
);

CREATE TABLE Faktura (
    idFakture INT PRIMARY KEY IDENTITY(1,1),
    idProjekta INT FOREIGN KEY REFERENCES Projekat(idProjekta),
    mesec INT,
    godina INT,
    ukupnoSati DECIMAL(10,2),
    iznos DECIMAL(12,2),
    status NVARCHAR(50)
);

-- ============================================================
-- KORAK 3: Unos test podataka
-- ============================================================

-- Odeljenja
INSERT INTO Odeljenje (nazivOdeljenja) VALUES 
('Development'), ('QA'), ('Design'), ('Management'), ('Administration');

-- Zaposleni
INSERT INTO Zaposleni (ime, prezime, pozicija, idOdeljenja, datumZaposlenja, satnica) VALUES
('Marko', 'Petrovic', 'Senior Developer', 1, '2020-03-15', 30.00),
('Ana', 'Stojanovic', 'Developer', 1, '2021-06-01', 25.00),
('Ivan', 'Markovic', 'QA Engineer', 2, '2021-09-10', 22.00),
('Jelena', 'Nikolic', 'UI/UX Designer', 3, '2022-01-15', 26.00),
('Stefan', 'Jovanovic', 'Project Manager', 4, '2019-05-20', 35.00),
('Milica', 'Djordjevic', 'Junior Developer', 1, '2023-02-01', 18.00),
('Nikola', 'Todorovic', 'Senior Developer', 1, '2020-08-10', 32.00),
('Maja', 'Ilic', 'QA Lead', 2, '2020-04-01', 28.00),
('Petar', 'Pavlovic', 'DevOps Engineer', 1, '2021-11-15', 30.00),
('Tamara', 'Milosevic', 'Administrator', 5, '2022-06-01', 20.00);

-- Klijenti
INSERT INTO Klijent (nazivKompanije, kontaktOsoba, grad, drzava) VALUES
('TechCorp Solutions', 'John Smith', 'Berlin', 'Nemacka'),
('DataSys GmbH', 'Hans Mueller', 'Minhen', 'Nemacka'),
('WebPro Ltd', 'James Wilson', 'London', 'Velika Britanija'),
('CloudNet d.o.o', 'Dragan Antic', 'Beograd', 'Srbija'),
('AppDev Inc', 'Michael Brown', 'Njujork', 'SAD');

-- Projekti
INSERT INTO Projekat (nazivProjekta, opis, datumPocetka, datumZavrsetka, budzet, status, idKlijenta) VALUES
('E-Commerce platforma', 'Razvoj web prodavnice sa placananjem', '2024-01-15', '2024-08-30', 85000.00, 'Zavrsen', 1),
('CRM sistem', 'Customer relationship management aplikacija', '2024-03-01', '2024-12-31', 120000.00, 'Zavrsen', 2),
('Mobile Banking App', 'Mobilna aplikacija za bankarstvo', '2024-06-01', '2025-06-30', 150000.00, 'Aktivan', 3),
('Cloud Migration', 'Migracija infrastrukture u cloud', '2025-01-10', '2025-09-30', 95000.00, 'Aktivan', 4),
('Analytics Dashboard', 'BI dashboard za izvestavanje', '2025-02-01', '2025-07-31', 60000.00, 'Aktivan', 5);

-- Tehnologije
INSERT INTO Tehnologija (nazivTehnologije, kategorija) VALUES
('Java', 'Backend'),
('Spring Boot', 'Backend'),
('React', 'Frontend'),
('Angular', 'Frontend'),
('Python', 'Backend'),
('.NET/C#', 'Backend'),
('Flutter', 'Mobile'),
('PostgreSQL', 'Database'),
('MongoDB', 'Database'),
('AWS', 'Cloud'),
('Docker', 'DevOps'),
('Node.js', 'Backend');

-- Projekat-Tehnologija veze
INSERT INTO ProjekatTehnologija (idProjekta, idTehnologije) VALUES
(1, 1), (1, 2), (1, 3), (1, 8),        -- E-Commerce: Java, Spring, React, PostgreSQL
(2, 6), (2, 4), (2, 8),                 -- CRM: .NET, Angular, PostgreSQL
(3, 7), (3, 5), (3, 9),                 -- Mobile Banking: Flutter, Python, MongoDB
(4, 10), (4, 11), (4, 8),               -- Cloud Migration: AWS, Docker, PostgreSQL
(5, 5), (5, 3), (5, 8);                 -- Analytics: Python, React, PostgreSQL

-- Evidencija sati (simulacija za 2024-2025)
INSERT INTO EvidencijaSati (idZaposlenog, idProjekta, datum, brojSati, opis) VALUES
-- Projekat 1 (E-Commerce) - 2024
(1, 1, '2024-01-20', 8, 'Backend API development'),
(1, 1, '2024-02-15', 7, 'Payment integration'),
(1, 1, '2024-03-10', 8, 'Order management module'),
(2, 1, '2024-01-22', 6, 'Frontend components'),
(2, 1, '2024-02-18', 8, 'Shopping cart implementation'),
(4, 1, '2024-02-01', 5, 'UI/UX design'),
(4, 1, '2024-03-05', 6, 'Product page design'),
(3, 1, '2024-04-01', 7, 'Integration testing'),
(3, 1, '2024-05-10', 8, 'Performance testing'),
(5, 1, '2024-01-15', 4, 'Project planning'),
-- Projekat 2 (CRM) - 2024
(7, 2, '2024-03-15', 8, '.NET backend development'),
(7, 2, '2024-04-20', 8, 'Customer module'),
(7, 2, '2024-05-15', 7, 'Reporting module'),
(2, 2, '2024-04-01', 6, 'Angular frontend'),
(2, 2, '2024-05-20', 8, 'Dashboard components'),
(8, 2, '2024-06-01', 7, 'QA testing'),
(8, 2, '2024-07-10', 8, 'Regression testing'),
(5, 2, '2024-03-10', 5, 'Sprint planning'),
-- Projekat 3 (Mobile Banking) - 2024/2025
(6, 3, '2024-06-15', 7, 'Flutter UI development'),
(6, 3, '2024-07-20', 8, 'Authentication screens'),
(6, 3, '2024-08-15', 6, 'Transaction history'),
(1, 3, '2024-07-01', 8, 'Python backend API'),
(1, 3, '2024-08-10', 8, 'Security implementation'),
(3, 3, '2024-09-01', 7, 'Mobile testing'),
(3, 3, '2024-10-15', 8, 'Security testing'),
(5, 3, '2024-06-10', 4, 'Project kickoff'),
-- Projekat 4 (Cloud Migration) - 2025
(9, 4, '2025-01-20', 8, 'AWS infrastructure setup'),
(9, 4, '2025-02-15', 8, 'Docker containerization'),
(9, 4, '2025-03-10', 7, 'CI/CD pipeline'),
(7, 4, '2025-02-01', 6, 'Application refactoring'),
(7, 4, '2025-03-15', 8, 'Database migration'),
(8, 4, '2025-03-20', 7, 'Migration testing'),
(5, 4, '2025-01-15', 5, 'Migration planning'),
-- Projekat 5 (Analytics Dashboard) - 2025
(1, 5, '2025-02-10', 8, 'Data pipeline development'),
(1, 5, '2025-03-15', 7, 'ETL processes'),
(2, 5, '2025-02-20', 8, 'React dashboard components'),
(2, 5, '2025-03-25', 6, 'Chart visualizations'),
(4, 5, '2025-02-15', 5, 'Dashboard UI design'),
(5, 5, '2025-02-05', 4, 'Requirements gathering');

-- Fakture
INSERT INTO Faktura (idProjekta, mesec, godina, ukupnoSati, iznos, status) VALUES
(1, 1, 2024, 180, 4800.00, 'Placena'),
(1, 2, 2024, 210, 5600.00, 'Placena'),
(1, 3, 2024, 195, 5200.00, 'Placena'),
(1, 4, 2024, 160, 4300.00, 'Placena'),
(1, 5, 2024, 140, 3750.00, 'Placena'),
(2, 3, 2024, 150, 4500.00, 'Placena'),
(2, 4, 2024, 200, 6000.00, 'Placena'),
(2, 5, 2024, 220, 6600.00, 'Placena'),
(2, 6, 2024, 180, 5400.00, 'Placena'),
(2, 7, 2024, 160, 4800.00, 'Placena'),
(3, 6, 2024, 170, 5100.00, 'Placena'),
(3, 7, 2024, 210, 6300.00, 'Placena'),
(3, 8, 2024, 190, 5700.00, 'Placena'),
(3, 9, 2024, 150, 4500.00, 'Placena'),
(3, 10, 2024, 165, 4950.00, 'Placena'),
(4, 1, 2025, 180, 5400.00, 'Placena'),
(4, 2, 2025, 200, 6000.00, 'Placena'),
(4, 3, 2025, 220, 6600.00, 'Placena'),
(5, 2, 2025, 160, 4800.00, 'Placena'),
(5, 3, 2025, 180, 5400.00, 'Na cekanju');

-- ============================================================
-- KORAK 4: Kreiranje VIEW-a za Data Warehouse analizu
-- ============================================================

-- VIEW 1: Analiza troska rada (ovo ce biti fact tabela u OLAP kocki)
CREATE VIEW [Analiza_troska_rada]
AS
SELECT 
    e.idEvidencije,
    e.idZaposlenog,
    z.ime + ' ' + z.prezime AS imeZaposlenog,
    z.pozicija,
    o.nazivOdeljenja,
    e.idProjekta,
    p.nazivProjekta,
    p.status AS statusProjekta,
    k.nazivKompanije AS klijent,
    k.grad,
    k.drzava,
    e.datum,
    e.brojSati,
    z.satnica,
    e.brojSati * z.satnica AS TrosakRada,
    YEAR(e.datum) AS Godina,
    MONTH(e.datum) AS Mesec,
    DATEPART(QUARTER, e.datum) AS Kvartal
FROM EvidencijaSati e
INNER JOIN Zaposleni z ON e.idZaposlenog = z.idZaposlenog
INNER JOIN Odeljenje o ON z.idOdeljenja = o.idOdeljenja
INNER JOIN Projekat p ON e.idProjekta = p.idProjekta
INNER JOIN Klijent k ON p.idKlijenta = k.idKlijenta;
GO

-- VIEW 2: Analiza prihoda po projektima
CREATE VIEW [Analiza_prihoda]
AS
SELECT 
    f.idFakture,
    f.idProjekta,
    p.nazivProjekta,
    p.budzet,
    p.status AS statusProjekta,
    k.nazivKompanije AS klijent,
    k.grad,
    k.drzava,
    f.mesec,
    f.godina,
    f.ukupnoSati,
    f.iznos,
    f.status AS statusFakture,
    CASE 
        WHEN f.mesec BETWEEN 1 AND 3 THEN 1
        WHEN f.mesec BETWEEN 4 AND 6 THEN 2
        WHEN f.mesec BETWEEN 7 AND 9 THEN 3
        ELSE 4
    END AS Kvartal
FROM Faktura f
INNER JOIN Projekat p ON f.idProjekta = p.idProjekta
INNER JOIN Klijent k ON p.idKlijenta = k.idKlijenta;
GO

-- VIEW 3: Tehnologije po projektima (za analizu)
CREATE VIEW [Analiza_tehnologija]
AS
SELECT 
    p.idProjekta,
    p.nazivProjekta,
    t.nazivTehnologije,
    t.kategorija,
    k.nazivKompanije AS klijent
FROM ProjekatTehnologija pt
INNER JOIN Projekat p ON pt.idProjekta = p.idProjekta
INNER JOIN Tehnologija t ON pt.idTehnologije = t.idTehnologije
INNER JOIN Klijent k ON p.idKlijenta = k.idKlijenta;
GO

-- ============================================================
-- KORAK 5: Korisni upiti za proveru podataka
-- ============================================================

-- Ukupno sati po projektima
SELECT p.nazivProjekta, SUM(e.brojSati) AS UkupnoSati, 
       SUM(e.brojSati * z.satnica) AS UkupanTrosak
FROM EvidencijaSati e
JOIN Zaposleni z ON e.idZaposlenog = z.idZaposlenog
JOIN Projekat p ON e.idProjekta = p.idProjekta
GROUP BY p.nazivProjekta
ORDER BY UkupanTrosak DESC;

-- Produktivnost po zaposlenima
SELECT z.ime + ' ' + z.prezime AS Zaposleni, o.nazivOdeljenja,
       SUM(e.brojSati) AS UkupnoSati
FROM EvidencijaSati e
JOIN Zaposleni z ON e.idZaposlenog = z.idZaposlenog
JOIN Odeljenje o ON z.idOdeljenja = o.idOdeljenja
GROUP BY z.ime, z.prezime, o.nazivOdeljenja
ORDER BY UkupnoSati DESC;

-- Prihod po klijentima
SELECT k.nazivKompanije, SUM(f.iznos) AS UkupanPrihod
FROM Faktura f
JOIN Projekat p ON f.idProjekta = p.idProjekta
JOIN Klijent k ON p.idKlijenta = k.idKlijenta
GROUP BY k.nazivKompanije
ORDER BY UkupanPrihod DESC;

-- Prihod po kvartalima
SELECT f.godina, 
       CASE 
           WHEN f.mesec BETWEEN 1 AND 3 THEN 'Q1'
           WHEN f.mesec BETWEEN 4 AND 6 THEN 'Q2'
           WHEN f.mesec BETWEEN 7 AND 9 THEN 'Q3'
           ELSE 'Q4'
       END AS Kvartal,
       SUM(f.iznos) AS UkupanPrihod
FROM Faktura f
GROUP BY f.godina, 
         CASE 
           WHEN f.mesec BETWEEN 1 AND 3 THEN 'Q1'
           WHEN f.mesec BETWEEN 4 AND 6 THEN 'Q2'
           WHEN f.mesec BETWEEN 7 AND 9 THEN 'Q3'
           ELSE 'Q4'
         END
ORDER BY f.godina, Kvartal;
