-- ============================================================
-- PowerDesigner PDM - Physical Data Model
-- Ovaj SQL fajl mozes importovati u PowerDesigner:
--   File -> Reverse Engineer -> Database...
--   Izaberi DBMS: Microsoft SQL Server 2008
--   Izaberi "Using script files" i ucitaj ovaj fajl
-- ============================================================
-- Nakon importa dobices fizicki model sa svim tabelama i vezama
-- Zatim: Database -> Generate Database za kreiranje baze
-- ============================================================

CREATE TABLE Odeljenje (
    idOdeljenja  INT          NOT NULL IDENTITY(1,1),
    nazivOdeljenja NVARCHAR(100) NOT NULL,
    CONSTRAINT PK_Odeljenje PRIMARY KEY (idOdeljenja)
);

CREATE TABLE Zaposleni (
    idZaposlenog   INT           NOT NULL IDENTITY(1,1),
    ime            NVARCHAR(50)  NOT NULL,
    prezime        NVARCHAR(50)  NOT NULL,
    pozicija       NVARCHAR(100) NULL,
    idOdeljenja    INT           NULL,
    datumZaposlenja DATE         NULL,
    satnica        DECIMAL(10,2) NULL,
    CONSTRAINT PK_Zaposleni PRIMARY KEY (idZaposlenog),
    CONSTRAINT FK_Zaposleni_Odeljenje FOREIGN KEY (idOdeljenja) 
        REFERENCES Odeljenje(idOdeljenja)
);

CREATE TABLE Klijent (
    idKlijenta     INT           NOT NULL IDENTITY(1,1),
    nazivKompanije NVARCHAR(200) NOT NULL,
    kontaktOsoba   NVARCHAR(100) NULL,
    grad           NVARCHAR(100) NULL,
    drzava         NVARCHAR(100) NULL,
    CONSTRAINT PK_Klijent PRIMARY KEY (idKlijenta)
);

CREATE TABLE Projekat (
    idProjekta     INT           NOT NULL IDENTITY(1,1),
    nazivProjekta  NVARCHAR(200) NOT NULL,
    opis           NVARCHAR(MAX) NULL,
    datumPocetka   DATE          NULL,
    datumZavrsetka DATE          NULL,
    budzet         DECIMAL(12,2) NULL,
    status         NVARCHAR(50)  NULL,
    idKlijenta     INT           NULL,
    CONSTRAINT PK_Projekat PRIMARY KEY (idProjekta),
    CONSTRAINT FK_Projekat_Klijent FOREIGN KEY (idKlijenta) 
        REFERENCES Klijent(idKlijenta)
);

CREATE TABLE Tehnologija (
    idTehnologije     INT           NOT NULL IDENTITY(1,1),
    nazivTehnologije  NVARCHAR(100) NOT NULL,
    kategorija        NVARCHAR(50)  NULL,
    CONSTRAINT PK_Tehnologija PRIMARY KEY (idTehnologije)
);

CREATE TABLE ProjekatTehnologija (
    idProjekta    INT NOT NULL,
    idTehnologije INT NOT NULL,
    CONSTRAINT PK_ProjekatTehnologija PRIMARY KEY (idProjekta, idTehnologije),
    CONSTRAINT FK_PT_Projekat FOREIGN KEY (idProjekta) 
        REFERENCES Projekat(idProjekta),
    CONSTRAINT FK_PT_Tehnologija FOREIGN KEY (idTehnologije) 
        REFERENCES Tehnologija(idTehnologije)
);

CREATE TABLE EvidencijaSati (
    idEvidencije  INT          NOT NULL IDENTITY(1,1),
    idZaposlenog  INT          NULL,
    idProjekta    INT          NULL,
    datum         DATE         NOT NULL,
    brojSati      DECIMAL(5,2) NOT NULL,
    opis          NVARCHAR(500) NULL,
    CONSTRAINT PK_EvidencijaSati PRIMARY KEY (idEvidencije),
    CONSTRAINT FK_Evidencija_Zaposleni FOREIGN KEY (idZaposlenog) 
        REFERENCES Zaposleni(idZaposlenog),
    CONSTRAINT FK_Evidencija_Projekat FOREIGN KEY (idProjekta) 
        REFERENCES Projekat(idProjekta)
);

CREATE TABLE Faktura (
    idFakture   INT           NOT NULL IDENTITY(1,1),
    idProjekta  INT           NULL,
    mesec       INT           NULL,
    godina      INT           NULL,
    ukupnoSati  DECIMAL(10,2) NULL,
    iznos       DECIMAL(12,2) NULL,
    status      NVARCHAR(50)  NULL,
    CONSTRAINT PK_Faktura PRIMARY KEY (idFakture),
    CONSTRAINT FK_Faktura_Projekat FOREIGN KEY (idProjekta) 
        REFERENCES Projekat(idProjekta)
);
