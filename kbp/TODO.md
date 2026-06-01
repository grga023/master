# TODO - Seminarski rad: Data Warehouse IT kompanije
# Student: Ognjen Grgur, MIT 37/24
# Poslednje ažuriranje: 2026-06-01

## STATUS: U toku

---

## ✅ ZAVRŠENO
- [x] SQL skripta za kreiranje baze (tabele, podaci, VIEW-ovi)
- [x] PowerDesigner VBS skripta (backup, nije potrebna)
- [x] DDL fajl za Oracle Data Modeler import
- [x] Vodič za Oracle Data Modeler (zamena za PowerDesigner)
- [x] README sa kompletnim kontekstom

## 🔲 SLEDEĆI KORACI (po prioritetu)

### 1. CDM i PDM slike (Oracle Data Modeler)
- [ ] Skinuti Oracle SQL Developer Data Modeler (ZIP, besplatan)
      Link: https://www.oracle.com/tools/downloads/sql-developer-data-modeler-downloads.html
- [ ] Import DDL: File → Import → DDL File → `ITKompanijaDW_reverse_for_Oracle_DM.sql`
- [ ] Dobiti PDM (Relational) → eksportovati sliku (Slika 2)
- [ ] Engineer → Engineer to Logical Model → dobiti CDM → eksportovati sliku (Slika 1)

### 2. SQL Server baza i dijagram
- [ ] Pokrenuti `ITKompanijaDW_kreiranje.sql` u SSMS
- [ ] Napraviti Database Diagram u SSMS (Slika 3)
      (desni klik na Database Diagrams → New → dodaj sve tabele)

### 3. OLAP kocka (BIDS / SSDT)
- [ ] Kreirati Analysis Services projekat
- [ ] Definisati Data Source (ITKompanijaDW baza)
- [ ] Definisati Data Source View (VIEW-ovi)
- [ ] Kreirati kocku cbProduktivnost (mere: SUM(brojSati), SUM(TrosakRada))
- [ ] Kreirati kocku cbPrihodi (mere: SUM(iznos), SUM(ukupnoSati))
- [ ] Deploy i Process kocke
- [ ] Slike 4-8: DSV, Cube Structure, Dimension Usage, Browser

### 4. Excel Pivot tabele
- [ ] Povezati Excel na OLAP kocku (Data → From Other Sources → Analysis Services)
- [ ] Pivot tabela: Produktivnost po odeljenjima/kvartalima (Slika 9)
- [ ] Pivot tabela: Prihodi po klijentima (Slika 10)
- [ ] Grafikon: Produktivnost (Slika 11)
- [ ] Grafikon: Prihodi (Slika 12)

### 5. Finalni dokument
- [ ] Word dokument sa svim slikama (1-12)
- [ ] Naslovna strana, sadržaj, zaključak
- [ ] Formatiranje po uputstvu fakulteta

---

## NAPOMENE
- Oracle Data Modeler zamenjuje SAP PowerDesigner (besplatan, ista funkcionalnost)
- Za OLAP: treba SQL Server sa Analysis Services (BIDS ili SSDT-BI)
- Ako nemaš BIDS: alternativa je SSDT-BI (SQL Server Data Tools - Business Intelligence)
  Download: https://docs.microsoft.com/en-us/sql/ssdt/download-sql-server-data-tools-ssdt
