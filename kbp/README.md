# Seminarski rad: Data Warehouse IT kompanije

## Student
- **Ime:** Ognjen Grgur
- **Broj indeksa:** MIT 37/24
- **Fakultet:** Tehnički fakultet "Mihajlo Pupin" Zrenjanin, Univerzitet u Novom Sadu
- **Predmet:** Koncepti baza podataka

## Tema
Data Warehouse (skladište podataka) za IT kompaniju "DevSoft d.o.o." koja se bavi razvojem softvera, upravljanjem projektima i pružanjem IT usluga klijentima.

## Domen / Poslovanje
- IT kompanija sa odeljenjima: Development, QA, Design, Management, Administration
- Zaposleni rade na projektima za klijente (TechCorp, DataSys, WebPro, CloudNet, AppDev)
- Evidencija radnih sati po projektima
- Mesečno fakturisanje na osnovu utrošenih sati
- Tehnologije: Java, .NET, Python, React, Angular, Flutter, Node.js, AWS, Docker, PostgreSQL, MongoDB

## Struktura baze (8 tabela)
1. **Odeljenje** - organizacione jedinice
2. **Zaposleni** - radnici sa satnicom
3. **Klijent** - kompanije kojima se pružaju usluge
4. **Projekat** - softverski projekti sa budžetom
5. **Tehnologija** - tech stack
6. **ProjekatTehnologija** - N:M veza projekat-tehnologija
7. **EvidencijaSati** - timesheet (fact tabela za DW)
8. **Faktura** - mesečni računi klijentima

## OLAP kocke
- **cbProduktivnost** - analiza produktivnosti zaposlenih po projektima, odeljenjima, vremenu
- **cbPrihodi** - analiza prihoda po klijentima, projektima, tehnologijama

## Dimenzije
- Zaposleni, Odeljenje, Projekat, Klijent, Tehnologija, Vreme (2023-2026)

## Mere
- SUM(brojSati), SUM(TrosakRada), SUM(iznos), AVG(satnica), COUNT(idProjekta)

## VIEW-ovi
- `Analiza_troska_rada` - glavna fact tabela (join EvidencijaSati + Zaposleni + Projekat + Klijent + Odeljenje)
- `Analiza_prihoda` - prihodi po projektima/kvartalima
- `Analiza_tehnologija` - korišćene tehnologije po projektima

## Fajlovi u folderu
| Fajl | Opis |
|------|------|
| `ITKompanijaDW_kreiranje.sql` | Glavni SQL - kreira bazu, tabele, test podatke, VIEW-ove |
| `ITKompanijaDW_reverse_for_Oracle_DM.sql` | DDL za import u Oracle Data Modeler (Reverse Engineer) |
| `UPUTSTVO_Oracle_DataModeler.md` | Vodič za Oracle SQL Developer Data Modeler (CDM/PDM) |
| `PowerDesigner_CDM_script.vbs` | VBScript za PowerDesigner (alternativa, nije potreban) |
| `PowerDesigner_PDM_reverse_engineer.sql` | SQL za Reverse Engineer u PowerDesigner-u (alternativa) |
| `UPUTSTVO.txt` | Detaljan korak-po-korak vodič za izradu |
| `Prodavnica filmova PRIMER.pdf` | Referentni primer seminarskog rada |

## Alati
1. **Oracle SQL Developer Data Modeler** (BESPLATAN) - CDM/PDM modeli
   - Download: https://www.oracle.com/tools/downloads/sql-developer-data-modeler-downloads.html
   - Vodič: `UPUTSTVO_Oracle_DataModeler.md`
   - ~~SAP PowerDesigner 16~~ (nije potreban, plaća se)
2. **SQL Server 2008+ / SSMS** - baza podataka
3. **SQL Server BIDS (ili SSDT)** - OLAP kocka
4. **Microsoft Excel 2010+** - Pivot tabele i grafikoni

## Šta je ostalo da se uradi
- [ ] U Oracle Data Modeler: Import DDL → dobiti PDM → Engineer to Logical → dobiti CDM
- [ ] Eksportovati slike: CDM (Slika 1) i PDM (Slika 2)
- [ ] Pokrenuti SQL skriptu u SSMS i napraviti Database Diagram (Slika 3)
- [ ] U BIDS-u kreirati Analysis Services projekat (Slike 4-8)
- [ ] U Excel-u napraviti Pivot tabele i grafikone (Slike 9-12)
- [ ] Napisati/formatirati finalni Word dokument sa svim slikama

## Brzi start za CDM/PDM (Oracle Data Modeler)
1. Skini ZIP sa oracle.com, raspakuj, pokreni `datamodeler.exe`
2. `File → Import → DDL File` → odaberi `ITKompanijaDW_reverse_for_Oracle_DM.sql`
3. RDBMS: SQL Server → Import → dobijaš PDM (Slika 2)
4. `Engineer → Engineer to Logical Model` → dobijaš CDM (Slika 1)
5. Eksportuj slike: `File → Export → To Image File`

## Kontekst za nastavak sesije
Ako treba ponovo da nastaviš rad sa AI asistentom, daj mu ovaj fajl i reci:
> "Nastavi rad na seminarskom radu Data Warehouse IT kompanije. Kontekst je u README.md u ovom folderu."

AI će znati: studenta, temu, strukturu baze, šta je već urađeno i šta preostaje.
