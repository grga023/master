# Oracle SQL Developer Data Modeler - Vodič za seminarski rad
## Student: Ognjen Grgur, MIT 37/24

---

## 1. Preuzimanje i instalacija (BESPLATNO)

1. Idi na: https://www.oracle.com/tools/downloads/sql-developer-data-modeler-downloads.html
2. Skini verziju **"Windows 64-bit with JDK included"** (ne treba ti ništa dodatno)
3. Raspakuj ZIP fajl u bilo koji folder (npr. `C:\OracleDataModeler`)
4. Pokreni `datamodeler.exe` — NEMA instalacije, radi odmah!
5. Ako traži JDK path, odaberi onaj koji je u raspakovanom folderu (`jdk` subfolder)

> ⚠️ Oracle može tražiti nalog — registracija je besplatna na oracle.com

---

## 2. Kreiranje CDM (Conceptual Data Model) — SLIKA 1

### Korak 2.1: Novi Logical Model (CDM ekvivalent)
1. Pokreni Oracle Data Modeler
2. U Browser panelu (levo) vidiš **Logical** model — to je tvoj CDM!
3. Dupli klik na **Logical** → otvara se prazan dijagram

### Korak 2.2: Kreiranje entiteta

Za svaki entitet: **desni klik na dijagram → New Entity** (ili ikonica u toolbar-u)

#### Entitet 1: Odeljenje
- **Name:** Odeljenje
- Tab **Attributes:**
  | Name | Data Type | Mandatory | PK |
  |------|-----------|-----------|-----|
  | idOdeljenja | INTEGER | ✓ | ✓ (UID) |
  | nazivOdeljenja | VARCHAR(100) | ✓ | |

#### Entitet 2: Zaposleni
- **Name:** Zaposleni
- Tab **Attributes:**
  | Name | Data Type | Mandatory | PK |
  |------|-----------|-----------|-----|
  | idZaposlenog | INTEGER | ✓ | ✓ |
  | ime | VARCHAR(50) | ✓ | |
  | prezime | VARCHAR(50) | ✓ | |
  | pozicija | VARCHAR(100) | | |
  | datumZaposlenja | DATE | | |
  | satnica | NUMERIC(10,2) | | |

#### Entitet 3: Klijent
- **Name:** Klijent
- Tab **Attributes:**
  | Name | Data Type | Mandatory | PK |
  |------|-----------|-----------|-----|
  | idKlijenta | INTEGER | ✓ | ✓ |
  | nazivKompanije | VARCHAR(200) | ✓ | |
  | kontaktOsoba | VARCHAR(100) | | |
  | grad | VARCHAR(100) | | |
  | drzava | VARCHAR(100) | | |

#### Entitet 4: Projekat
- **Name:** Projekat
- Tab **Attributes:**
  | Name | Data Type | Mandatory | PK |
  |------|-----------|-----------|-----|
  | idProjekta | INTEGER | ✓ | ✓ |
  | nazivProjekta | VARCHAR(200) | ✓ | |
  | opis | VARCHAR(4000) | | |
  | datumPocetka | DATE | | |
  | datumZavrsetka | DATE | | |
  | budzet | NUMERIC(12,2) | | |
  | status | VARCHAR(50) | | |

#### Entitet 5: Tehnologija
- **Name:** Tehnologija
- Tab **Attributes:**
  | Name | Data Type | Mandatory | PK |
  |------|-----------|-----------|-----|
  | idTehnologije | INTEGER | ✓ | ✓ |
  | nazivTehnologije | VARCHAR(100) | ✓ | |
  | kategorija | VARCHAR(50) | | |

#### Entitet 6: EvidencijaSati
- **Name:** EvidencijaSati
- Tab **Attributes:**
  | Name | Data Type | Mandatory | PK |
  |------|-----------|-----------|-----|
  | idEvidencije | INTEGER | ✓ | ✓ |
  | datum | DATE | ✓ | |
  | brojSati | NUMERIC(5,2) | ✓ | |
  | opis | VARCHAR(500) | | |

#### Entitet 7: Faktura
- **Name:** Faktura
- Tab **Attributes:**
  | Name | Data Type | Mandatory | PK |
  |------|-----------|-----------|-----|
  | idFakture | INTEGER | ✓ | ✓ |
  | mesec | INTEGER | | |
  | godina | INTEGER | | |
  | ukupnoSati | NUMERIC(10,2) | | |
  | iznos | NUMERIC(12,2) | | |
  | status | VARCHAR(50) | | |

### Korak 2.3: Kreiranje veza (Relationships)

Klikni na **New Relation** ikonu u toolbar-u (linija sa rombom), pa klikni na izvorni pa na ciljni entitet:

| # | Veza (Name) | Od (Source) | Ka (Target) | Kardinalnost |
|---|-------------|-------------|-------------|--------------|
| 1 | pripada | Zaposleni | Odeljenje | N:1 (Many-to-One) |
| 2 | realizuje_za | Projekat | Klijent | N:1 |
| 3 | evidentira | EvidencijaSati | Zaposleni | N:1 |
| 4 | za_projekat | EvidencijaSati | Projekat | N:1 |
| 5 | fakturise | Faktura | Projekat | N:1 |
| 6 | koristi | Projekat | Tehnologija | N:M (Many-to-Many) |

**Za N:1 vezu:** Koristi "New 1:N Relation" ikonu — klikni prvo na "1" stranu (Odeljenje), pa na "N" stranu (Zaposleni)

**Za N:M vezu (koristi):** Koristi "New N:M Relation" ikonu — klikni na Projekat pa na Tehnologija

### Korak 2.4: Slika CDM
1. Rasporedi entitete lepo na dijagramu (drag & drop)
2. **File → Print Diagram → To Image File** ili **File → Export → To Image File**
3. Sačuvaj kao PNG — to je **Slika 1 (CDM)**

---

## 3. Generisanje PDM (Physical Data Model) — SLIKA 2

### Korak 3.1: Engineer to Relational (Logical → Physical)
1. U meniju: **Engineer → Engineer to Relational Model**
2. Podesi:
   - **RDBMS:** Microsoft SQL Server 2012 (ili koji imaš)
   - Čekiraj sve entitete
3. Klikni **Engineer**
4. Otvoriće se **Relational** model (= PDM) sa svim tabelama i FK vezama
5. N:M veza (Projekat-Tehnologija) automatski kreira spojnu tabelu!

### Korak 3.2: Slika PDM
1. Otvori Relational dijagram (dupli klik na Relational u Browser panelu)
2. Rasporedi tabele
3. **File → Export → To Image File** → sačuvaj kao PNG — **Slika 2 (PDM)**

---

## 4. BRŽI PUT: Import DDL (Reverse Engineer)

Ako ti se ne kreira ručno, možeš importovati SQL:

1. **File → Import → DDL File**
2. Odaberi fajl: `ITKompanijaDW_reverse_for_Oracle_DM.sql` (kreiran ispod)
3. Podesi **RDBMS: SQL Server**
4. Klikni Import
5. Ovo kreira PDM (Relational model) direktno
6. Za CDM: **Engineer → Engineer to Logical Model** (reverse)

---

## 5. Generisanje DDL iz modela

Ako ti treba SQL iz modela:
1. U Relational modelu: desni klik na model → **Export → DDL File**
2. Odaberi SQL Server kao RDBMS
3. Sačuvaj — dobijaš CREATE TABLE skriptu

---

## 6. Čuvanje projekta

1. **File → Save** (sačuvaj negde, npr. `D:\...\kbp\DataModeler_ITKompanijaDW`)
2. Čuva se kao folder sa XML fajlovima
3. Možeš ga ponovo otvoriti: **File → Open**

---

## NAPOMENE

- **Logical model = CDM** (konceptualni, bez FK, sa relacijama)
- **Relational model = PDM** (fizički, sa tabelama, FK, tipovima)
- Oracle Data Modeler podržava SQL Server, Oracle, PostgreSQL, MySQL...
- Za seminarski su ti dovoljne 2 slike: CDM (Logical) i PDM (Relational)

---

## Rezime koraka za danas:

1. ⬇️ Skini Oracle Data Modeler (ZIP, ~400MB)
2. 📂 Raspakuj i pokreni `datamodeler.exe`
3. 🔄 Importuj DDL (`ITKompanijaDW_reverse_for_Oracle_DM.sql`) → dobijaš PDM
4. 🔄 Engineer to Logical → dobijaš CDM
5. 📸 Eksportuj obe slike (PNG)
6. ✅ Gotovo!
