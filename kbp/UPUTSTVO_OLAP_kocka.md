# OLAP Kocka - Korak po korak
## SQL Server Analysis Services (BIDS / SSDT-BI)

---

## 0. Šta ti treba instalirano

- **SQL Server** sa uključenim **Analysis Services** (pri instalaciji čekiraj!)
- **BIDS** (Business Intelligence Development Studio) — dolazi sa SQL Server 2008/2012
  ILI
- **SSDT-BI** (SQL Server Data Tools) — besplatan dodatak za Visual Studio
  Download: https://learn.microsoft.com/en-us/sql/ssdt/download-sql-server-data-tools-ssdt

> Kad otvaraš BIDS/SSDT, to je zapravo Visual Studio sa BI templateima.

---

## 1. Kreiranje projekta

1. Otvori **SQL Server Business Intelligence Development Studio** (ili SSDT)
2. `File → New → Project`
3. Odaberi: **Analysis Services Multidimensional and Data Mining Project**
4. Name: `ITKompanijaDW_OLAP`
5. OK

---

## 2. Data Source (veza ka bazi)

1. U Solution Explorer-u: desni klik na **Data Sources** → `New Data Source`
2. Next → `New` → podesi konekciju:
   - Server: `localhost` (ili ime tvog servera, npr. `.\SQLEXPRESS`)
   - Database: `ITKompanijaDW`
3. Test Connection → OK
4. Next → Next → Finish
5. 📸 **Slika 4** - Data Source

---

## 3. Data Source View (DSV) — VIEW-ovi kao tabele

1. Desni klik na **Data Source Views** → `New Data Source View`
2. Odaberi Data Source koji si upravo kreirao → Next
3. Iz liste "Available objects" dodaj (Add >) ove tabele/view-ove:
   - ✅ `Analiza_troska_rada` (VIEW)
   - ✅ `Analiza_prihoda` (VIEW)
   - ✅ `Odeljenje`
   - ✅ `Zaposleni`
   - ✅ `Projekat`
   - ✅ `Klijent`
   - ✅ `Tehnologija`
4. Next → Name: `ITKompanijaDW_DSV` → Finish
5. 📸 **Slika 5** - Data Source View dijagram

---

## 4. Kreiranje OLAP kocke

1. Desni klik na **Cubes** → `New Cube`
2. Odaberi: **Use existing tables** → Next
3. Čekiraj Measure Group tabele:
   - ✅ `Analiza_troska_rada` (fact tabela za produktivnost)
   - ✅ `Analiza_prihoda` (fact tabela za prihode)
4. Next → Odaberi mere (Measures):

### Mere za Analiza_troska_rada:
   - ✅ `brojSati` (SUM)
   - ✅ `TrosakRada` (SUM)
   - ✅ `satnica` (AVG)

### Mere za Analiza_prihoda:
   - ✅ `iznos` (SUM)
   - ✅ `ukupnoSati` (SUM)

5. Next → Odaberi dimenzije:
   - ✅ Zaposleni (ili imeZaposlenog)
   - ✅ Odeljenje (nazivOdeljenja)
   - ✅ Projekat (nazivProjekta)
   - ✅ Klijent (klijent/nazivKompanije)
   - ✅ Vreme (Godina, Kvartal, Mesec)
6. Next → Name: `ITKompanijaDW_Cube` → Finish

📸 **Slika 6** - Cube Structure tab

---

## 5. Dimenzije (ako treba ručno dodati)

Ako wizard nije sve pokupIO:

1. Desni klik na **Dimensions** → `New Dimension`
2. Use existing table → odaberi npr. `Projekat`
3. Key: `idProjekta`, Name: `nazivProjekta`
4. Finish
5. Ponovi za svaku dimenziju

### Vremenska dimenzija (VAŽNO za seminarski):
- Ako nemaš posebnu tabelu za vreme, koristi kolone iz VIEW-a:
  - `Godina` (Year)
  - `Kvartal` (Quarter)
  - `Mesec` (Month)
- Ili napravi Server Time Dimension u wizard-u

---

## 6. Dimension Usage tab

1. Otvori kocku (dupli klik)
2. Klikni na tab **Dimension Usage**
3. Proveri da su dimenzije povezane sa measure grupama
4. Ako fali veza: klikni na ćeliju → podesi relationship type (Regular, fact-based)
5. 📸 **Slika 7** - Dimension Usage

---

## 7. Deploy i Process

1. U Solution Explorer: desni klik na projekat → **Properties**
   - Server: `localhost` (ili tvoj Analysis Services server)
   - Database: `ITKompanijaDW_OLAP`
2. Desni klik na projekat → **Deploy**
   - Ovo šalje kocku na server
3. Kad Deploy završi → desni klik na kocku → **Process**
   - Process Full → Run → puni kocku podacima
4. Treba da piše "Process succeeded"

---

## 8. Browse (pregled kocke)

1. Otvori kocku → tab **Browser**
2. Prevuci mere (brojSati, TrosakRada) u sredinu
3. Prevuci dimenzije (Odeljenje, Projekat) na redove/kolone
4. Vidiš OLAP rezultate!
5. 📸 **Slika 8** - Cube Browser

---

## TROUBLESHOOTING

### "Analysis Services template ne postoji"
→ Nisi instalirao BIDS/SSDT-BI. Instaliraj SSDT sa linka gore.

### "Cannot connect to Analysis Services"
→ Otvori SQL Server Configuration Manager → proveri da je "SQL Server Analysis Services" servis STARTED

### "Process failed"
→ Proveri da je baza `ITKompanijaDW` kreirana i da VIEW-ovi postoje

### Nemam BIDS/SSDT uopšte, šta da radim?
→ Alternativa: Visual Studio 2019 Community (besplatan) + SSDT extension
   Ili: SQL Server 2019 Developer Edition (besplatna) dolazi sa SSDT

---

## POSLE KOCKE → Excel Pivot

1. Otvori Excel
2. `Data → From Other Sources → From Analysis Services`
3. Server: `localhost`
4. Odaberi bazu: `ITKompanijaDW_OLAP`
5. Odaberi kocku → OK
6. Praviš Pivot tabele sa dimenzijama i merama
7. Insert → Chart za grafikone

---

## Slike za seminarski (rekapitulacija):
| # | Šta | Gde |
|---|-----|-----|
| Slika 4 | Data Source | BIDS - Data Sources |
| Slika 5 | Data Source View | BIDS - DSV dijagram |
| Slika 6 | Cube Structure | BIDS - Cube editor |
| Slika 7 | Dimension Usage | BIDS - Dimension Usage tab |
| Slika 8 | Cube Browser | BIDS - Browser tab |
