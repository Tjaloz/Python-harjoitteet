"""
Aurinkokylä - Valo kylään
=========================
Komentorivipeli, jossa pelaaja auttaa pientä kylää siirtymään saastuttavasta
dieselgeneraattorista aurinkoenergiaan. Tarina ja tavoite on kuvattu
tarkemmin tiedostossa intro.txt sekä projektin README.md:ssä.

Tämä tiedosto vastaa vain käyttöliittymästä (pääsilmukka ja komennot).
Pelin luokat (Esine, Huone, Pelaaja) ja tiedostonkäsittely ovat omassa
pelimoduulit-paketissaan.
"""

import os
import random

from pelimoduulit import Esine, Huone, Pelaaja, lue_tiedosto, tallenna_tilanne, lataa_tilanne
from pelimoduulit.tiedostot import TALLENNUSTIEDOSTO


# ---------------------------------------------------------------------------
# Pelin asetukset: tarvittavat osat, niiden hinnat (reitti A: osta) ja
# rakennusreseptit (reitti B: rakenna kierrätysmateriaaleista). Näiden lisäksi
# on kolmas reitti (C: opeta koulussa, ks. OPETUSKYSYMYKSET alempana). Kaikki
# kolme reittiä ovat pelaajalle vaihtoehtoisia tapoja edetä alusta loppuun, ja
# niitä voi myös yhdistellä vapaasti (esim. osta kaksi osaa, rakenna yksi,
# ansaitse yksi opettamalla).
# ---------------------------------------------------------------------------
OSTOHINNAT = {
    "aurinkopaneeli": 3,
    "akku": 3,
    "kaapeli": 2,
    "hallintayksikkö": 4,
}

RESEPTIT = {
    "aurinkopaneeli": ["lasinsiru", "alumiinilista"],
    "akku": ["akkukotelo", "sinkkilevy"],
    "kaapeli": ["kuparikela", "muovikouru"],
    "hallintayksikkö": ["piirilevy", "puulevy"],
}

OSIEN_PAINOT = {
    "aurinkopaneeli": 5.0,
    "akku": 10.0,
    "kaapeli": 1.0,
    "hallintayksikkö": 2.0,
}

TARVITTAVAT_OSAT = list(OSTOHINNAT.keys())

# ---------------------------------------------------------------------------
# Reitti C: osan ansaitseminen opettamalla koulussa. Jokaisella yrityksellä
# arvotaan yksi kestävän kehityksen aiheinen kysymys; oikea vastaus palkitaan
# valitsemalla jokin vielä puuttuva osa. Tämä reitti ei vaadi rahaa eikä
# materiaaleja - vain oikean vastauksen - joten sillä voi halutessaan
# läpäistä koko pelin yksinään, aivan kuten osto- ja rakennusreiteilläkin.
# ---------------------------------------------------------------------------
OPETUSKYSYMYKSET = [
    {
        "kysymys": "Mikä seuraavista on esimerkki uusiutuvasta energianlähteestä?",
        "vaihtoehdot": {"a": "hiili", "b": "aurinkoenergia", "c": "maakaasu"},
        "oikea": "b",
    },
    {
        "kysymys": "Mikä YK:n kestävän kehityksen tavoite käsittelee edullista ja puhdasta energiaa?",
        "vaihtoehdot": {"a": "tavoite 4", "b": "tavoite 7", "c": "tavoite 11"},
        "oikea": "b",
    },
    {
        "kysymys": "Mikä näistä vähentää eniten jätettä?",
        "vaihtoehdot": {"a": "ostetaan aina uutena", "b": "kierrätetään ja käytetään uudelleen", "c": "heitetään sekajätteeseen"},
        "oikea": "b",
    }
    {
        "kysymys": "Miksi aurinkopaneelit ovat ympäristöystävällisempiä kuin dieselgeneraattori?",
        "vaihtoehdot": {"a": "ne eivät tuota päästöjä käytön aikana", "b": "ne ovat äänekkäämpiä", "c": "ne tarvitsevat polttoainetta"},
        "oikea": "a",
    },
]


def luo_pelimaailma():
    """Rakentaa kylän paikat, niiden tarinatekstit, kerättävät raaka-aineet
    ja pelihahmot. Palauttaa listan Huone-olioita, joista ensimmäinen
    (kylätalo) on pelin aloitus- ja lopetuspaikka."""

    kylatalo = Huone(
        "kylätalo",
        "Kylätalo on yhteisön sydän. Seinällä riippuu vanha dieselgeneraattori,\n"
        "joka pitää kylän valot päällä - meluisasti, kalliisti ja saastuttaen.\n"
        "Kylänvanhin istuu pöydän ääressä karttojen kanssa.",
        hahmo={
            "nimi": "Kylänvanhin Elsa",
            "dialogi": [
                "\"Tervetuloa kylään! Dieselgeneraattorimme on vanha ja kallis ylläpitää.\"",
                "\"Jos saisimme rakennettua aurinkovoimalan, säästäisimme rahaa ja\"",
                "\"vähentäisimme päästöjä samalla. Tarvitsemme neljä osaa: aurinkopaneelin,\"",
                "\"akun, kaapelin ja hallintayksikön.\"",
                "\"Voit hankkia osat kahdella tavalla: ostaa ne torilta kylämerkeillä,\"",
                "\"tai rakentaa ne itse verstaassa kierrätysmateriaaleista.\"",
                "\"Kun sinulla on kaikki neljä osaa, tule takaisin tänne ja asenna ne!\"",
            ],
        },
    )

    tori = Huone(
        "tori",
        "Kylän tori on täynnä pieniä myyntikojuja. Yksi niistä myy\n"
        "aurinkovoimalan osia valmiina - mutta ne maksavat kylämerkkejä.",
    )

    verstas = Huone(
        "verstas",
        "Pölyinen verstas täynnä työkaluja. Täällä kierrätysmateriaaleista\n"
        "voi rakentaa tarvittavat osat itse, jos löytää oikeat raaka-aineet.",
    )

    kierratyspiste = Huone(
        "kierrätyspiste",
        "Kylän kierrätyspiste, jonne vanhat laitteet tuodaan ennen kuin ne\n"
        "päätyisivät kaatopaikalle. Täällä riittää hyödynnettävää materiaalia.",
        esineet=[
            Esine("kuparikela", 0.3),
            Esine("piirilevy", 0.2),
            Esine("sinkkilevy", 0.3),
            Esine("akkukotelo", 0.5),
        ],
    )

    metsa = Huone(
        "metsä",
        "Kylän reunalla kasvava metsä, jonka siistimisen yhteydessä on\n"
        "löytynyt käyttökelpoisia materiaaleja vanhoista rakennusjätteistä.",
        esineet=[
            Esine("lasinsiru", 0.1),
            Esine("puulevy", 1.0),
            Esine("muovikouru", 0.2),
            Esine("alumiinilista", 0.4),
        ],
    )

    ranta = Huone(
        "ranta",
        "Kylän rantaa pitkin ajelehtii valitettavan paljon muoviroskaa.\n"
        "Kalastaja Jussi kerää sitä päivittäin, ettei se päätyisi järveen.",
        hahmo={
            "nimi": "Kalastaja Jussi",
            "dialogi": [
                "\"Moi! Autatko keräämään muoviroskaa rannalta?\"",
                "\"Puhdas järvi hyödyttää koko kylää - ja voin maksaa avusta\"",
                "\"kylämerkeillä, joilla saa tarvikkeita torilta.\"",
                "\"Kirjoita 'tee hommia' niin ryhdytään töihin!\"",
            ],
        },
    )

    koulu = Huone(
        "koulu",
        "Kylän pieni koulu kaikuu lasten naurusta. Opettaja Liisa yrittää\n"
        "opettaa oppilaille kestävästä kehityksestä, ja kaipaisi siihen apua.",
        hahmo={
            "nimi": "Opettaja Liisa",
            "dialogi": [
                "\"Tule auttamaan minua opetustunnilla! Jos osaat vastata oppilaiden\"",
                "\"puolesta kestävän kehityksen kysymykseen oikein, koulu lahjoittaa\"",
                "\"kylän hankkeelle yhden osan kiitokseksi.\"",
                "\"Kirjoita 'opeta' niin kokeillaan!\"",
            ],
        },
    )

    return [kylatalo, tori, verstas, kierratyspiste, metsa, ranta, koulu]


def tulosta_ohjeet():
    ohjeet = lue_tiedosto("ohjeet.txt")
    if ohjeet:
        print(ohjeet)


def tulosta_puuttuvat_osat(pelaaja):
    puuttuvat = [osa for osa in TARVITTAVAT_OSAT if not pelaaja.has_esine(osa)]
    if puuttuvat:
        print("Puuttuvat osat:", ", ".join(puuttuvat))
    else:
        print("Sinulla on kaikki tarvittavat osat!")


# ---------------------------------------------------------------------------
# Reitti A: osien ostaminen torilta kylämerkeillä
# ---------------------------------------------------------------------------
def osta_osa(pelaaja):
    if pelaaja.sijainti.nimi != "tori":
        print("Voit ostaa osia vain torilla.")
        return

    ostettavissa = [osa for osa in OSTOHINNAT if not pelaaja.has_esine(osa)]
    if not ostettavissa:
        print("Sinulla on jo kaikki osat!")
        return

    print("Torilla myytävät osat:")
    for osa in ostettavissa:
        print(f"- {osa}: {OSTOHINNAT[osa]} kylämerkkiä")
    print(f"Sinulla on {pelaaja.kylamerkit} kylämerkkiä.")

    valinta = input("Minkä osan haluat ostaa? (tyhjä peruuttaa): ").strip().lower()
    if valinta == "":
        return

    if valinta not in OSTOHINNAT:
        print("Sellaista osaa ei myydä torilla.")
        return

    if pelaaja.has_esine(valinta):
        print("Sinulla on jo tämä osa.")
        return

    hinta = OSTOHINNAT[valinta]
    if pelaaja.kayta_merkkeja(hinta):
        pelaaja.lisaa_esine(Esine(valinta, OSIEN_PAINOT[valinta]))
        print(f"Ostit osan: {valinta}")
    else:
        print(f"Ei tarpeeksi kylämerkkejä. Tarvitset {hinta}, sinulla on {pelaaja.kylamerkit}.")


# ---------------------------------------------------------------------------
# Reitti B: osien rakentaminen verstaassa kierrätysmateriaaleista
# ---------------------------------------------------------------------------
def rakenna_osa(pelaaja):
    if pelaaja.sijainti.nimi != "verstas":
        print("Voit rakentaa osia vain verstaassa.")
        return

    rakennettavissa = [osa for osa in RESEPTIT if not pelaaja.has_esine(osa)]
    if not rakennettavissa:
        print("Sinulla on jo kaikki osat!")
        return

    print("Mahdolliset reseptit:")
    for osa in rakennettavissa:
        materiaalit = RESEPTIT[osa]
        tila = []
        for materiaali in materiaalit:
            merkki = "OK" if pelaaja.has_esine(materiaali) else "puuttuu"
            tila.append(f"{materiaali} ({merkki})")
        print(f"- {osa}: tarvitaan " + " + ".join(tila))

    valinta = input("Minkä osan haluat rakentaa? (tyhjä peruuttaa): ").strip().lower()
    if valinta == "":
        return

    if valinta not in RESEPTIT:
        print("Sellaista reseptiä ei ole.")
        return

    if pelaaja.has_esine(valinta):
        print("Sinulla on jo tämä osa.")
        return

    materiaalit = RESEPTIT[valinta]
    if not all(pelaaja.has_esine(materiaali) for materiaali in materiaalit):
        print("Sinulta puuttuu tarvittavia materiaaleja.")
        return

    for materiaali in materiaalit:
        pelaaja.poista_esine(materiaali)

    pelaaja.lisaa_esine(Esine(valinta, OSIEN_PAINOT[valinta]))
    print(f"Rakensit osan: {valinta}")


# ---------------------------------------------------------------------------
# Reitti C: osan ansaitseminen opettamalla koulussa
# ---------------------------------------------------------------------------
def opeta_koulussa(pelaaja):
    if pelaaja.sijainti.nimi != "koulu":
        print("Voit opettaa vain koulussa.")
        return

    puuttuvat = [osa for osa in TARVITTAVAT_OSAT if not pelaaja.has_esine(osa)]
    if not puuttuvat:
        print("Sinulla on jo kaikki osat!")
        return

    kysymys = random.choice(OPETUSKYSYMYKSET)
    print(f"\n{kysymys['kysymys']}")
    for kirjain, vaihtoehto in kysymys["vaihtoehdot"].items():
        print(f"  {kirjain}) {vaihtoehto}")

    vastaus = input("Vastauksesi (a/b/c): ").strip().lower()

    if vastaus != kysymys["oikea"]:
        print("Ei aivan oikein - yritä myöhemmin uudelleen toisella kysymyksellä!")
        return

    print("Oikein! Oppilaat innostuvat, ja koulu lahjoittaa hankkeelle osan.")
    print("Puuttuvat osat:", ", ".join(puuttuvat))
    valinta = input("Minkä osan haluat vastaanottaa? (tyhjä peruuttaa): ").strip().lower()

    if valinta == "":
        return
    if valinta not in puuttuvat:
        print("Valitse jokin listatuista puuttuvista osista.")
        return

    pelaaja.lisaa_esine(Esine(valinta, OSIEN_PAINOT[valinta]))
    print(f"Sait osan: {valinta}")


# ---------------------------------------------------------------------------
# Omat lisätoiminnallisuudet:
# tekstikartta paikoista sekä etenemisyhteenveto.
# ---------------------------------------------------------------------------
def nayta_kartta(huoneet):
    print("\nKylän paikat:")
    for huone in huoneet:
        print(f"- {huone.nimi}")


def nayta_edistyminen(pelaaja):
    kerätyt = [osa for osa in TARVITTAVAT_OSAT if pelaaja.has_esine(osa)]
    prosentti = round(100 * len(kerätyt) / len(TARVITTAVAT_OSAT))
    print(f"\nEdistyminen: {len(kerätyt)}/{len(TARVITTAVAT_OSAT)} osaa kerätty ({prosentti} %)")
    print(f"Kylämerkkejä: {pelaaja.kylamerkit}")
    if kerätyt:
        print("Kerätyt osat:", ", ".join(kerätyt))


# ---------------------------------------------------------------------------
# Pääohjelma
# ---------------------------------------------------------------------------
def kaynnista_peli():
    intro = lue_tiedosto("intro.txt")
    if intro:
        print(intro)

    huoneet = luo_pelimaailma()
    kylatalo = huoneet[0]

    pelaaja = None
    if os.path.exists(TALLENNUSTIEDOSTO):
        vastaus = input("Löytyi aiempi tallennus. Haluatko jatkaa siitä? (k/e): ").strip().lower()
        if vastaus == "k":
            pelaaja = lataa_tilanne(huoneet, Pelaaja)

    if pelaaja is None:
        nimi = input("Anna pelaajan nimi: ").strip()
        pelaaja = Pelaaja(nimi, kylatalo)
        print(f"\nTervetuloa kylään, {nimi}!")

    tulosta_ohjeet()
    pelaaja.sijainti.esittele()

    while True:
        komento = input("\nAnna komento: ").strip().lower()

        if komento == "lopeta":
            print("Kiitos pelaamisesta!")
            break

        elif komento == "ohjeet":
            tulosta_ohjeet()

        elif komento == "katso":
            pelaaja.sijainti.esittele()

        elif komento == "inventaario":
            pelaaja.nayta_inventaario()
            tulosta_puuttuvat_osat(pelaaja)

        elif komento == "liiku":
            kohteen_nimi = input("Minne haluat liikkua? ").strip().lower()
            kohde = next((h for h in huoneet if h.nimi == kohteen_nimi), None)
            if kohde:
                pelaaja.liiku(kohde)
                pelaaja.sijainti.esittele()
            else:
                print("Sellaista paikkaa ei löydy.")

        elif komento == "keraa":
            if not pelaaja.sijainti.esineet:
                print("Täällä ei ole mitään kerättävää.")
            elif len(pelaaja.sijainti.esineet) == 1:
                esine = pelaaja.sijainti.esineet[0]
                pelaaja.keraa_esine(esine.nimi)
                print(f"Keräsit esineen: {esine.nimi}")
            else:
                nimet = ", ".join(e.nimi for e in pelaaja.sijainti.esineet)
                print(f"Täällä on: {nimet}")
                valinta = input("Minkä esineen haluat kerätä? ").strip().lower()
                if pelaaja.keraa_esine(valinta):
                    print(f"Keräsit esineen: {valinta}")
                else:
                    print("Sellaista esinettä ei löytynyt täältä.")

        elif komento == "puhu":
            hahmo = pelaaja.sijainti.hahmo
            if hahmo:
                print(f"\n{hahmo['nimi']}:")
                for rivi in hahmo["dialogi"]:
                    print(rivi)
            else:
                print("Täällä ei ole ketään, jonka kanssa jutella.")

        elif komento == "tee hommia":
            if pelaaja.sijainti.nimi != "ranta":
                print("Täällä ei ole hommia tarjolla juuri nyt.")
            else:
                print("Keräät muoviroskaa rannalta puoli tuntia. Järvi kiittää!")
                pelaaja.ansaitse_merkki(1)
                print(f"Ansaitsit 1 kylämerkin. Kylämerkkejä yhteensä: {pelaaja.kylamerkit}")

        elif komento == "osta":
            osta_osa(pelaaja)

        elif komento == "rakenna":
            rakenna_osa(pelaaja)

        elif komento == "opeta":
            opeta_koulussa(pelaaja)

        elif komento == "kartta":
            nayta_kartta(huoneet)

        elif komento == "edistyminen":
            nayta_edistyminen(pelaaja)

        elif komento == "asenna":
            if pelaaja.sijainti.nimi != "kylätalo":
                print("Osat pitää asentaa kylätalolla.")
            elif all(pelaaja.has_esine(osa) for osa in TARVITTAVAT_OSAT):
                print("\nAsennat aurinkopaneelin, akun, kaapelin ja hallintayksikön")
                print("kylätalon katolle. Kylänvanhin Elsa hymyilee leveästi:")
                print("\"Nyt kylämme saa puhdasta energiaa auringosta - ei enää")
                print("meluisaa ja saastuttavaa dieselgeneraattoria!\"")
                print("\nOnnittelut! Autoit kylää kohti puhtaampaa energiantuotantoa")
                print("(YK:n kestävän kehityksen tavoite 7: Edullista ja puhdasta")
                print("energiaa), vähemmän jätettä kierrätyksen avulla (tavoite 12)")
                print("ja levitit tietoa kestävästä kehityksestä (tavoite 4).")
                print("\n*** PELI LÄPÄISTY ***")
                break
            else:
                print("Sinulta puuttuu vielä osia.")
                tulosta_puuttuvat_osat(pelaaja)

        elif komento == "tallenna":
            tallenna_tilanne(pelaaja)

        else:
            print("Tuntematon komento. Kirjoita 'ohjeet' nähdäksesi käytettävissä olevat komennot.")


if __name__ == "__main__":
    kaynnista_peli()
