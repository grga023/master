'******************************************************************************
'* PowerDesigner CDM Script
'* Seminarski rad: Data Warehouse IT kompanije
'* Student: Ognjen Grgur, MIT 37/24
'*
'* UPUTSTVO:
'* 1. Otvori PowerDesigner
'* 2. File -> New Model -> Conceptual Data Model
'* 3. Tools -> Execute Commands -> Run Script (ovaj fajl)
'* ILI rucno kreiraj entitete prema uputstvu ispod
'******************************************************************************

'******************************************************************************
'* AKO SKRIPTA NE RADI - KREIRAJ RUCNO:
'*
'* ENTITETI (Entities) koje treba kreirati u CDM:
'*
'* 1. Odeljenje
'*    - idOdeljenja (Integer, Primary Identifier)
'*    - nazivOdeljenja (Variable characters 100, Mandatory)
'*
'* 2. Zaposleni
'*    - idZaposlenog (Integer, Primary Identifier)
'*    - ime (Variable characters 50, Mandatory)
'*    - prezime (Variable characters 50, Mandatory)
'*    - pozicija (Variable characters 100)
'*    - datumZaposlenja (Date)
'*    - satnica (Decimal 10,2)
'*
'* 3. Klijent
'*    - idKlijenta (Integer, Primary Identifier)
'*    - nazivKompanije (Variable characters 200, Mandatory)
'*    - kontaktOsoba (Variable characters 100)
'*    - grad (Variable characters 100)
'*    - drzava (Variable characters 100)
'*
'* 4. Projekat
'*    - idProjekta (Integer, Primary Identifier)
'*    - nazivProjekta (Variable characters 200, Mandatory)
'*    - opis (Text)
'*    - datumPocetka (Date)
'*    - datumZavrsetka (Date)
'*    - budzet (Decimal 12,2)
'*    - status (Variable characters 50)
'*
'* 5. Tehnologija
'*    - idTehnologije (Integer, Primary Identifier)
'*    - nazivTehnologije (Variable characters 100, Mandatory)
'*    - kategorija (Variable characters 50)
'*
'* 6. EvidencijaSati
'*    - idEvidencije (Integer, Primary Identifier)
'*    - datum (Date, Mandatory)
'*    - brojSati (Decimal 5,2, Mandatory)
'*    - opis (Variable characters 500)
'*
'* 7. Faktura
'*    - idFakture (Integer, Primary Identifier)
'*    - mesec (Integer)
'*    - godina (Integer)
'*    - ukupnoSati (Decimal 10,2)
'*    - iznos (Decimal 12,2)
'*    - status (Variable characters 50)
'*
'* VEZE (Relationships):
'*
'* 1. Zaposleni -- pripada --> Odeljenje     (N:1)
'* 2. Projekat -- ima --> Klijent             (N:1)
'* 3. EvidencijaSati -- evidentira --> Zaposleni  (N:1)
'* 4. EvidencijaSati -- za --> Projekat       (N:1)
'* 5. Faktura -- za --> Projekat              (N:1)
'* 6. Projekat <-- koristi --> Tehnologija    (N:M)
'*
'******************************************************************************

Option Explicit

Dim mdl
Set mdl = ActiveModel

If mdl Is Nothing Then
   MsgBox "Nema aktivnog modela. Otvori Conceptual Data Model prvo."
   Exit Sub
End If

' Provera da li je CDM
If mdl.ClassKind <> cls_Model Then
   MsgBox "Aktivni dokument nije model."
   Exit Sub
End If

Dim diagram
Set diagram = mdl.ActiveDiagram

' === KREIRANJE ENTITETA ===

' 1. Odeljenje
Dim eOdeljenje
Set eOdeljenje = mdl.Entities.CreateNew()
eOdeljenje.Name = "Odeljenje"
eOdeljenje.Code = "Odeljenje"
Dim a1
Set a1 = eOdeljenje.Attributes.CreateNew()
a1.Name = "idOdeljenja"
a1.Code = "idOdeljenja"
a1.DataType = "Integer"
a1.Mandatory = True
Dim id1
Set id1 = eOdeljenje.Identifiers.CreateNew()
id1.Name = "PK_Odeljenje"
id1.Attributes.Add a1
eOdeljenje.PrimaryIdentifier = id1
Dim a1b
Set a1b = eOdeljenje.Attributes.CreateNew()
a1b.Name = "nazivOdeljenja"
a1b.Code = "nazivOdeljenja"
a1b.DataType = "VA100"
a1b.Mandatory = True

' 2. Zaposleni
Dim eZaposleni
Set eZaposleni = mdl.Entities.CreateNew()
eZaposleni.Name = "Zaposleni"
eZaposleni.Code = "Zaposleni"
Dim az1
Set az1 = eZaposleni.Attributes.CreateNew()
az1.Name = "idZaposlenog"
az1.DataType = "Integer"
az1.Mandatory = True
Dim idz
Set idz = eZaposleni.Identifiers.CreateNew()
idz.Name = "PK_Zaposleni"
idz.Attributes.Add az1
eZaposleni.PrimaryIdentifier = idz
Dim az2
Set az2 = eZaposleni.Attributes.CreateNew()
az2.Name = "ime"
az2.DataType = "VA50"
az2.Mandatory = True
Dim az3
Set az3 = eZaposleni.Attributes.CreateNew()
az3.Name = "prezime"
az3.DataType = "VA50"
az3.Mandatory = True
Dim az4
Set az4 = eZaposleni.Attributes.CreateNew()
az4.Name = "pozicija"
az4.DataType = "VA100"
Dim az5
Set az5 = eZaposleni.Attributes.CreateNew()
az5.Name = "datumZaposlenja"
az5.DataType = "Date"
Dim az6
Set az6 = eZaposleni.Attributes.CreateNew()
az6.Name = "satnica"
az6.DataType = "Decimal(10,2)"

' 3. Klijent
Dim eKlijent
Set eKlijent = mdl.Entities.CreateNew()
eKlijent.Name = "Klijent"
eKlijent.Code = "Klijent"
Dim ak1
Set ak1 = eKlijent.Attributes.CreateNew()
ak1.Name = "idKlijenta"
ak1.DataType = "Integer"
ak1.Mandatory = True
Dim idk
Set idk = eKlijent.Identifiers.CreateNew()
idk.Name = "PK_Klijent"
idk.Attributes.Add ak1
eKlijent.PrimaryIdentifier = idk
Dim ak2
Set ak2 = eKlijent.Attributes.CreateNew()
ak2.Name = "nazivKompanije"
ak2.DataType = "VA200"
ak2.Mandatory = True
Dim ak3
Set ak3 = eKlijent.Attributes.CreateNew()
ak3.Name = "kontaktOsoba"
ak3.DataType = "VA100"
Dim ak4
Set ak4 = eKlijent.Attributes.CreateNew()
ak4.Name = "grad"
ak4.DataType = "VA100"
Dim ak5
Set ak5 = eKlijent.Attributes.CreateNew()
ak5.Name = "drzava"
ak5.DataType = "VA100"

' 4. Projekat
Dim eProjekat
Set eProjekat = mdl.Entities.CreateNew()
eProjekat.Name = "Projekat"
eProjekat.Code = "Projekat"
Dim ap1
Set ap1 = eProjekat.Attributes.CreateNew()
ap1.Name = "idProjekta"
ap1.DataType = "Integer"
ap1.Mandatory = True
Dim idp
Set idp = eProjekat.Identifiers.CreateNew()
idp.Name = "PK_Projekat"
idp.Attributes.Add ap1
eProjekat.PrimaryIdentifier = idp
Dim ap2
Set ap2 = eProjekat.Attributes.CreateNew()
ap2.Name = "nazivProjekta"
ap2.DataType = "VA200"
ap2.Mandatory = True
Dim ap3
Set ap3 = eProjekat.Attributes.CreateNew()
ap3.Name = "opis"
ap3.DataType = "Text"
Dim ap4
Set ap4 = eProjekat.Attributes.CreateNew()
ap4.Name = "datumPocetka"
ap4.DataType = "Date"
Dim ap5
Set ap5 = eProjekat.Attributes.CreateNew()
ap5.Name = "datumZavrsetka"
ap5.DataType = "Date"
Dim ap6
Set ap6 = eProjekat.Attributes.CreateNew()
ap6.Name = "budzet"
ap6.DataType = "Decimal(12,2)"
Dim ap7
Set ap7 = eProjekat.Attributes.CreateNew()
ap7.Name = "status"
ap7.DataType = "VA50"

' 5. Tehnologija
Dim eTehnologija
Set eTehnologija = mdl.Entities.CreateNew()
eTehnologija.Name = "Tehnologija"
eTehnologija.Code = "Tehnologija"
Dim at1
Set at1 = eTehnologija.Attributes.CreateNew()
at1.Name = "idTehnologije"
at1.DataType = "Integer"
at1.Mandatory = True
Dim idt
Set idt = eTehnologija.Identifiers.CreateNew()
idt.Name = "PK_Tehnologija"
idt.Attributes.Add at1
eTehnologija.PrimaryIdentifier = idt
Dim at2
Set at2 = eTehnologija.Attributes.CreateNew()
at2.Name = "nazivTehnologije"
at2.DataType = "VA100"
at2.Mandatory = True
Dim at3
Set at3 = eTehnologija.Attributes.CreateNew()
at3.Name = "kategorija"
at3.DataType = "VA50"

' 6. EvidencijaSati
Dim eEvidencija
Set eEvidencija = mdl.Entities.CreateNew()
eEvidencija.Name = "EvidencijaSati"
eEvidencija.Code = "EvidencijaSati"
Dim ae1
Set ae1 = eEvidencija.Attributes.CreateNew()
ae1.Name = "idEvidencije"
ae1.DataType = "Integer"
ae1.Mandatory = True
Dim ide
Set ide = eEvidencija.Identifiers.CreateNew()
ide.Name = "PK_EvidencijaSati"
ide.Attributes.Add ae1
eEvidencija.PrimaryIdentifier = ide
Dim ae2
Set ae2 = eEvidencija.Attributes.CreateNew()
ae2.Name = "datum"
ae2.DataType = "Date"
ae2.Mandatory = True
Dim ae3
Set ae3 = eEvidencija.Attributes.CreateNew()
ae3.Name = "brojSati"
ae3.DataType = "Decimal(5,2)"
ae3.Mandatory = True
Dim ae4
Set ae4 = eEvidencija.Attributes.CreateNew()
ae4.Name = "opis"
ae4.DataType = "VA500"

' 7. Faktura
Dim eFaktura
Set eFaktura = mdl.Entities.CreateNew()
eFaktura.Name = "Faktura"
eFaktura.Code = "Faktura"
Dim af1
Set af1 = eFaktura.Attributes.CreateNew()
af1.Name = "idFakture"
af1.DataType = "Integer"
af1.Mandatory = True
Dim idf
Set idf = eFaktura.Identifiers.CreateNew()
idf.Name = "PK_Faktura"
idf.Attributes.Add af1
eFaktura.PrimaryIdentifier = idf
Dim af2
Set af2 = eFaktura.Attributes.CreateNew()
af2.Name = "mesec"
af2.DataType = "Integer"
Dim af3
Set af3 = eFaktura.Attributes.CreateNew()
af3.Name = "godina"
af3.DataType = "Integer"
Dim af4
Set af4 = eFaktura.Attributes.CreateNew()
af4.Name = "ukupnoSati"
af4.DataType = "Decimal(10,2)"
Dim af5
Set af5 = eFaktura.Attributes.CreateNew()
af5.Name = "iznos"
af5.DataType = "Decimal(12,2)"
Dim af6
Set af6 = eFaktura.Attributes.CreateNew()
af6.Name = "status"
af6.DataType = "VA50"

' === KREIRANJE VEZA (Relationships) ===

' Zaposleni --> Odeljenje (N:1)
Dim r1
Set r1 = mdl.Relationships.CreateNew()
r1.Name = "pripada"
r1.Entity1 = eZaposleni
r1.Entity2 = eOdeljenje
r1.Cardinality1 = "0,n"
r1.Cardinality2 = "1,1"

' Projekat --> Klijent (N:1)
Dim r2
Set r2 = mdl.Relationships.CreateNew()
r2.Name = "realizuje_za"
r2.Entity1 = eProjekat
r2.Entity2 = eKlijent
r2.Cardinality1 = "0,n"
r2.Cardinality2 = "1,1"

' EvidencijaSati --> Zaposleni (N:1)
Dim r3
Set r3 = mdl.Relationships.CreateNew()
r3.Name = "evidentira"
r3.Entity1 = eEvidencija
r3.Entity2 = eZaposleni
r3.Cardinality1 = "0,n"
r3.Cardinality2 = "1,1"

' EvidencijaSati --> Projekat (N:1)
Dim r4
Set r4 = mdl.Relationships.CreateNew()
r4.Name = "za_projekat"
r4.Entity1 = eEvidencija
r4.Entity2 = eProjekat
r4.Cardinality1 = "0,n"
r4.Cardinality2 = "1,1"

' Faktura --> Projekat (N:1)
Dim r5
Set r5 = mdl.Relationships.CreateNew()
r5.Name = "fakturise"
r5.Entity1 = eFaktura
r5.Entity2 = eProjekat
r5.Cardinality1 = "0,n"
r5.Cardinality2 = "1,1"

' Projekat <--> Tehnologija (N:M)
Dim r6
Set r6 = mdl.Relationships.CreateNew()
r6.Name = "koristi"
r6.Entity1 = eProjekat
r6.Entity2 = eTehnologija
r6.Cardinality1 = "0,n"
r6.Cardinality2 = "0,n"

MsgBox "CDM model uspesno kreiran! Entiteta: 7, Veza: 6"
