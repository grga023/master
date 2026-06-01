-- ============================================================
-- DDL za Reverse Engineer u Oracle SQL Developer Data Modeler
-- Seminarski rad: Data Warehouse IT kompanije
-- Student: Ognjen Grgur, MIT 37/24
--
-- UPUTSTVO:
-- 1. U Oracle Data Modeler: File -> Import -> DDL File
-- 2. Odaberi ovaj fajl
-- 3. RDBMS: Microsoft SQL Server
-- 4. Klikni Import
-- 5. Dobićeš PDM (Relational model)
-- 6. Za CDM: Engineer -> Engineer to Logical Model
-- ============================================================

CREATE TABLE Odeljenje (
    idOdeljenja INT NOT NULL PRIMARY KEY,
    nazivOdeljenja NVARCHAR(100) NOT NULL
);

CREATE TABLE Zaposleni (
    idZaposlenog INT NOT NULL PRIMARY KEY,
    ime NVARCHAR(50) NOT NULL,
    prezime NVARCHAR(50) NOT NULL,
    pozicija NVARCHAR(100),
    idOdeljenja INT NOT NULL,
    datumZaposlenja DATE,
    satnica DECIMAL(10,2),
    CONSTRAINT FK_Zaposleni_Odeljenje FOREIGN KEY (idOdeljenja) REFERENCES Odeljenje(idOdeljenja)
);

CREATE TABLE Klijent (
    idKlijenta INT NOT NULL PRIMARY KEY,
    nazivKompanije NVARCHAR(200) NOT NULL,
    kontaktOsoba NVARCHAR(100),
    grad NVARCHAR(100),
    drzava NVARCHAR(100)
);

CREATE TABLE Projekat (
    idProjekta INT NOT NULL PRIMARY KEY,
    nazivProjekta NVARCHAR(200) NOT NULL,
    opis NVARCHAR(4000),
    datumPocetka DATE,
    datumZavrsetka DATE,
    budzet DECIMAL(12,2),
    status NVARCHAR(50),
    idKlijenta INT NOT NULL,
    CONSTRAINT FK_Projekat_Klijent FOREIGN KEY (idKlijenta) REFERENCES Klijent(idKlijenta)
);

CREATE TABLE Tehnologija (
    idTehnologije INT NOT NULL PRIMARY KEY,
    nazivTehnologije NVARCHAR(100) NOT NULL,
    kategorija NVARCHAR(50)
);

CREATE TABLE ProjekatTehnologija (
    idProjekta INT NOT NULL,
    idTehnologije INT NOT NULL,
    CONSTRAINT PK_ProjekatTehnologija PRIMARY KEY (idProjekta, idTehnologije),
    CONSTRAINT FK_PT_Projekat FOREIGN KEY (idProjekta) REFERENCES Projekat(idProjekta),
    CONSTRAINT FK_PT_Tehnologija FOREIGN KEY (idTehnologije) REFERENCES Tehnologija(idTehnologije)
);

CREATE TABLE EvidencijaSati (
    idEvidencije INT NOT NULL PRIMARY KEY,
    idZaposlenog INT NOT NULL,
    idProjekta INT NOT NULL,
    datum DATE NOT NULL,
    brojSati DECIMAL(5,2) NOT NULL,
    opis NVARCHAR(500),
    CONSTRAINT FK_Evidencija_Zaposleni FOREIGN KEY (idZaposlenog) REFERENCES Zaposleni(idZaposlenog),
    CONSTRAINT FK_Evidencija_Projekat FOREIGN KEY (idProjekta) REFERENCES Projekat(idProjekta)
);

CREATE TABLE Faktura (
    idFakture INT NOT NULL PRIMARY KEY,
    idProjekta INT NOT NULL,
    mesec INT,
    godina INT,
    ukupnoSati DECIMAL(10,2),
    iznos DECIMAL(12,2),
    status NVARCHAR(50),
    CONSTRAINT FK_Faktura_Projekat FOREIGN KEY (idProjekta) REFERENCES Projekat(idProjekta)
);
