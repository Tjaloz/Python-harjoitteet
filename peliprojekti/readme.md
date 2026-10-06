# Aurinkokylä – Valo kylään

## Idea ja tausta

Aurinkokylä on komentorivipohjainen tarinapeli Pythonilla. Pelaaja saapuu
pieneen kylään vapaaehtoistyöntekijänä. Kylän ainoa sähkönlähde on vanha,
saastuttava dieselgeneraattori. Kylänvanhin Elsa pyytää pelaajan apua kylän
siirtämiseksi puhtaaseen aurinkoenergiaan.

## Tavoite

Pelaajan tehtävänä on hankkia neljä aurinkovoimalan osaa — aurinkopaneeli,
akku, kaapeli ja hallintayksikkö — ja asentaa ne kylätalolla. Kun kaikki
neljä osaa on asennettu, peli on läpäisty.

## Toimintaperiaate

Peli etenee tekstipohjaisen komentovalikon kautta. Pelaaja liikkuu
(`liiku`) kylän viiden paikan välillä — kylätalo, tori, verstas,
kierrätyspiste ja koulu — kerää esineitä (`keraa`), juttelee hahmoille
(`puhu`) ja seuraa etenemistään (`inventaario`, `edistyminen`). Jokaisella
paikalla on oma selkeä rooli pelin etenemisessä.

## Toiminnallisuudet

Tarvittavat osat voi hankkia kolmella vaihtoehtoisella tavalla, joita voi
myös yhdistellä vapaasti:

- **Osta** osat torilta kylämerkeillä, joita ansaitaan tekemällä hommia
  (`tee hommia`, `osta`).
- **Rakenna** osat verstaassa kierrätysmateriaalista, jota löytyy
  kierrätyspisteeltä (`keraa`, `rakenna`).
- **Opeta** koulussa vastaamalla oikein kestävän kehityksen
  monivalintakysymykseen (`opeta`).

Peli tukee myös tilanteen tallentamista ja lataamista (`tallenna`), jotta
kesken jäänyttä peliä voi jatkaa myöhemmin.

## Kestävä kehitys

Peli kytkeytyy konkreettisesti useaan YK:n kestävän kehityksen
tavoitteeseen:

- **Tavoite 7 — Edullista ja puhdasta energiaa:** pelin päämäärä on korvata
  saastuttava dieselgeneraattori uusiutuvalla aurinkoenergialla.
- **Tavoite 12 — Vastuullista kuluttamista:** rakennusreitti perustuu
  kierrätysmateriaalin hyödyntämiseen uuden ostamisen sijaan.
- **Tavoite 4 — Hyvä koulutus:** opetusreitti tuo kestävän kehityksen
  tietoa suoraan osaksi pelimekaniikkaa.

Jokainen kolmesta etenemisreitistä edustaa siis eri tapaa toimia
vastuullisesti: kuluttamista vähentäen, kierrättäen tai tietoa jakaen.

## Rakenne ja ajaminen

Koko peli on yhdessä tiedostossa (`main.py`) selkeyden vuoksi — luokat
(`Esine`, `Huone`, `Pelaaja`), pelin asetukset ja pääsilmukka ovat samassa
paikassa, kommentein jaoteltuina. Vieressä ovat `intro.txt` (tarina) ja
`ohjeet.txt` (komennot).

```
python main.py
```
