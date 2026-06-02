# Prezentacija: Agenti zasnovani na Velikim jezičkim modelima i planiranje zadataka
## Okvir za PowerPoint prezentaciju (naslovi + bullet pointi)

---

## Slajd 1: Naslovna strana
- Naslov: Agenti zasnovani na Velikim jezičkim modelima i planiranje zadataka
- Predmet: Inteligentni agenti
- Ime studenta, profesor, fakultet, godina

---

## Slajd 2: Sadržaj prezentacije
- Veliki jezički modeli (LLM)
- LLM agenti — definicija i komponente
- Multi-agent sistemi
- Planiranje i paralelno izvršavanje
- Arhitektura Planer-Menadžer-Radnik-Tester
- Primeri primene
- Zaključak

---

## Slajd 3: Šta su Veliki jezički modeli?
- Neuronske mreže trenirane na ogromnim količinama teksta
- Baziraju se na Transformer arhitekturi (self-attention mehanizam)
- Primeri: GPT-4, Claude, LLaMA
- Sposobnosti: razumevanje jezika, generisanje, rezonovanje
- Skaliranje dovodi do emergentnih sposobnosti

---

## Slajd 4: LLM kao osnova za inteligentne agente
- LLM nije sam po sebi agent — potrebna je arhitektura oko njega
- Ključne sposobnosti za agente:
  - Razumevanje složenih instrukcija
  - Chain-of-Thought rasuđivanje
  - Generisanje strukturiranog izlaza (kod, planovi)
  - In-context learning
  - Korišćenje alata (Tool use)

---

## Slajd 5: Definicija LLM agenta
- Autonomni sistem sa LLM-om kao kognitivnim jezgrom
- Komponente: Percepcija, Planiranje, Memorija, Alati, Akcija
- [DIJAGRAM: Komponente LLM agenta — slika iz rada]
- Razlika od prostog chatbot-a: interakcija sa okruženjem, akumulacija iskustva

---

## Slajd 6: Planiranje i rasuđivanje
- Chain-of-Thought (CoT) — korak-po-korak rasuđivanje
- ReAct — iterativno smenjivanje razmišljanja i akcija
- Reflexion — samo-refleksija i učenje iz grešaka
- Tree-of-Thought — paralelno razmatranje strategija
- Ovi mehanizmi su ključ autonomije agenta

---

## Slajd 7: Multi-agent sistemi — Zašto?
- Jedan agent ima ograničenja (kontekst, specijalizacija)
- Multi-agent: više specijalizovanih agenata sarađuje
- Prednosti:
  - Specijalizacija → veći kvalitet
  - Paralelizacija → brže izvršavanje
  - Modularnost → lakše održavanje
  - Izolacija grešaka

---

## Slajd 8: Komunikacioni obrasci
- Centralizovano — jedan koordinator upravlja svima
- Decentralizovano — svi agenti komuniciraju međusobno
- Hijerarhijsko — kombinacija (naš pristup)
- [DIJAGRAM: Tri komunikaciona obrasca — slika iz rada]

---

## Slajd 9: Dekompozicija zadataka
- Složen zahtev → skup manjih, nezavisnih podzadataka
- LLM vrši dekompoziciju analizom zahteva
- Identifikacija zavisnosti između zadataka
- Zadaci bez zavisnosti → kandidati za paralelizaciju
- [DIJAGRAM: Tok planiranja — slika iz rada]

---

## Slajd 10: Paralelno vs. sekvencijalno izvršavanje
- Sekvencijalno: T = T(A) + T(B) + T(C)
- Paralelno: T = max(T(A), T(B), T(C))
- Za N nezavisnih zadataka → ubrzanje faktora N
- [DIJAGRAM: Poređenje — slika iz rada]
- U praksi: delimična paralelizacija (zavisnosti postoje)

---

## Slajd 11: Arhitektura Planer-Menadžer-Radnik-Tester
- Hijerarhijski multi-agent sistem sa 4 uloge
- [DIJAGRAM: Arhitektura — glavna slika iz rada]
- Inspiracija: realni razvojni timovi
- Jasna separacija odgovornosti

---

## Slajd 12: Uloge agenata (detalji)
- **Planer**: Prima zahtev, kreira plan, definiše zadatke i zavisnosti
- **Menadžer**: Koordinira, alocira zadatke, prati status, odlučuje o ponovnim pokušajima
- **Radnik**: Izvršava konkretne zadatke (može ih biti više, rade paralelno)
- **Tester**: Verifikuje rezultate, pokreće testove, šalje feedback

---

## Slajd 13: Tok izvršavanja
1. Korisnik → zahtev
2. Planer → plan sa zadacima
3. Menadžer → alokacija i paralelizacija
4. Radnici → paralelno izvršavanje
5. Tester → verifikacija
6. Povratna informacija → iteracija ako je potrebno

---

## Slajd 14: Iterativno poboljšanje (Write-Review-Fix)
- Ciklus: Write → Review → Fix → Review → Fix...
- Tester nezavisno evaluira (nema pristrasnosti autora)
- Većina zadataka: 1-2 iteracije
- Složeniji: 3-5 iteracija
- Konvergencija ka korektnom rešenju

---

## Slajd 15: Primeri primene
- Automatizacija razvoja softvera (MetaGPT, AutoGen)
- Obrada složenih korisničkih zahteva
- Paralelna analiza više izvora podataka
- Primer iz prakse: Copilot CLI (planer, menadžer, radnik, tester agenti)

---

## Slajd 16: Komparativna analiza — Multi-agent vs. Mono-agent
- **Raslojavanje modela (model tiering)**:
  - Planer: jak model (GPT-4, Claude Opus) — kritična dekompozicija
  - Menadžer: srednji model (Sonnet, GPT-4o) — koordinacija
  - Radnici: slab model (Haiku, GPT-4o-mini) — dobar input kompenzuje
- **Potrošnja tokena** (5 podzadataka):
  - Mono-agent: ~45K tokena na skupom modelu → $0.675
  - Multi-agent: ~23K tokena (samo 4K na skupom) → $0.083
  - **~8× jeftinije** uz isti kvalitet
- [DIJAGRAM: Potrošnja tokena i odnos cena/kvalitet — slika iz rada]

---

## Slajd 17: Zašto je kvalitet uporediv (ili bolji)?
- Fokusirani kontekst — radnik vidi samo svoj zadatak, manje halucinacija
- Specijalizovani promptovi — optimizovani za jednu vrstu posla
- Nezavisna verifikacija — tester nema pristrasnost autora
- Izolacija grešaka — greška jednog radnika ne kontaminira ostale
- Iterativna korekcija iz više perspektiva
- **Kraći kontekst = bolji rezultati** (dokazano u istraživanjima)

---

## Slajd 18: Kada koristiti koji pristup?
- **Multi-agent je bolji za:**
  - Zadatke koji se dekompozuju na nezavisne delove
  - Ograničen budžet
  - Kritična verifikacija
  - Duge sesije (kontekst raste kod mono-agenta)
- **Mono-agent je bolji za:**
  - Jednostavne, nedeljive zadatke
  - Kad je latencija kritičnija od cene
  - Zadaci koji zahtevaju duboki celokupni kontekst

---

## Slajd 19: Ograničenja i izazovi
- Povećana cena (više LLM poziva)
- Latencija koordinacije
- Propagacija grešaka kroz lanac
- Složenost debagovanja
- Aktivna oblast istraživanja

---

## Slajd 20: Zaključak
- LLM agenti: nova paradigma u AI
- Multi-agent: specijalizacija + paralelizacija
- Model tiering: optimalan odnos cene i kvaliteta
- Hijerarhijska arhitektura: efikasna koordinacija
- Iterativna verifikacija: kvalitet izlaza
- Budućnost: efikasnija koordinacija, napredna memorija, formalni protokoli

---

## Slajd 21: Pitanja?
- Hvala na pažnji
- Pitanja i diskusija
