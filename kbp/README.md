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
| `FIX_permisije_za_OLAP.sql` | SQL fix za OLAP permisije |
| `OLAP_kocka_XMLA.xmla` | XMLA skripta - kreira OLAP bazu, dimenzije, kocke |
| `OLAP_kocka_PROCESS.xmla` | XMLA skripta - procesira (puni) kocku |
| `OLAP_kocka_DELETE.xmla` | XMLA skripta - briše OLAP bazu |
| `MDX_upiti_za_kocku.mdx` | MDX upiti za prikaz podataka iz kocke |
| `Excel_Pivot_OLAP.vba` | VBA makro za automatsko kreiranje pivot tabela |
| `OLAP_Pivot_Tabele.xlsx` | Excel sa pivot tabelama i grafikonima (8 sheetova) |
| `UPUTSTVO_Oracle_DataModeler.md` | Vodič za Oracle SQL Developer Data Modeler (CDM/PDM) |
| `UPUTSTVO_OLAP_kocka.md` | Vodič za kreiranje OLAP kocke |
| `TODO.md` | Praćenje progresa |
| `diagrami/` | Folder sa svim slikama (CDM, PDM, dijagrami, analiza) |
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

## Šta je urađeno
- [x] CDM slika (Oracle Data Modeler) → `diagrami/slika 1.png`
- [x] PDM slika (Oracle Data Modeler) → `diagrami/slika2 relation.png`
- [x] Database Diagram u SSMS → `diagrami/diag baze pod.png`
- [x] OLAP kocka (cbProduktivnost + cbPrihodi) kreirana i procesirana
- [x] Pivot tabele i grafikoni → `OLAP_Pivot_Tabele.xlsx` (8 sheetova)
- [x] VIEW rezultati → `diagrami/anal troskova rada.png`, `analiza prihoda.png`, `analiza tehnologija.png`

## Šta je ostalo
- [ ] Napisati/formatirati finalni Word dokument sa svim slikama
- [ ] Naslovna strana, sadržaj, zaključak

## Slike za seminarski (kompletna lista)
| # | Opis | Fajl |
|---|------|------|
| 1 | CDM (Konceptualni model) | `diagrami/slika 1.png` |
| 2 | PDM (Fizički/Relacijski model) | `diagrami/slika2 relation.png` |
| 3 | Database Diagram | `diagrami/diag baze pod.png` |
| 4 | VIEW: Analiza troška rada | `diagrami/anal troskova rada.png` |
| 5 | VIEW: Analiza prihoda | `diagrami/analiza prihoda.png` |
| 6 | VIEW: Analiza tehnologija | `diagrami/analiza tehnologija.png` |
| 7 | Korisni SELECT upiti | `diagrami/korisniSelectModeli.png` |
| 8-11 | Pivot tabele (iz Excel-a) | `OLAP_Pivot_Tabele.xlsx` - screenshotovati sheetove |
| 12 | Grafikon (iz Excel-a) | `OLAP_Pivot_Tabele.xlsx` - screenshotovati chart |

## Kontekst za nastavak sesije
Ako treba ponovo da nastaviš rad sa AI asistentom, daj mu ovaj fajl i reci:
> "Nastavi rad na seminarskom radu Data Warehouse IT kompanije. Kontekst je u README.md u ovom folderu."

AI će znati: studenta, temu, strukturu baze, šta je već urađeno i šta preostaje.
