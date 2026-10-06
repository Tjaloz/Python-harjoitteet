"""
Aurinkokylä - Valo kylään (yksinkertaistettu versio)
=====================================================
Komentorivipeli, jossa pelaaja auttaa pientä kylää siirtymään saastuttavasta
dieselgeneraattorista aurinkoenergiaan. Tarina on kuvattu tiedostossa
intro.txt ja projektin README.md:ssä.

"""

import os
import random

# Tallennustiedoston polku lasketaan suhteessa TÄMÄN tiedoston sijaintiin,
# ei siihen mistä kansiosta käsin ohjelma sattuu olevan käynnistetty.
SCRIPT_KANSIO = os.path.dirname(os.path.abspath(__file__))
TALLENNUSTIEDOSTO = os.path.join(SCRIPT_KANSIO, "tallennus.txt")


# ---------------------------------------------------------------------------
# Luokat
# ---------------------------------------------------------------------------
class Esine:
    """Yksittäinen esine: raaka-aine tai valmis osa. Ominaisuudet: nimi, paino."""

    def __init__(self, nimi, paino):
        self.nimi = nimi
        self.paino = paino

    def __str__(self):
        return f"{self.nimi} ({self.paino} kg)"


class Huone:
    """Pelimaailman paikka. Ominaisuudet: nimi, kuvaus, kerättävät esineet
    ja mahdollinen keskusteltava hahmo."""

    def __init__(self, nimi, kuvaus, esineet=None, hahmo=None):
        self.nimi = nimi
        self.kuvaus = kuvaus
        self.esineet = esineet if esineet is not None else []
        self.hahmo = hahmo

    def esittele(self):
        print(f"\n=== {self.nimi.capitalize()} ===")
        print(self.kuvaus)
        if self.esineet:
            nimet = ", ".join(e.nimi for e in self.esineet)
            print(f"Täällä on kerättävissä: {nimet}")
        if self.hahmo:
            print(f"Täällä on {self.hahmo['nimi']}. Jutellaan komennolla 'puhu'.")


class Pelaaja:
    """Pelaaja: nimi, inventaario, sijainti (Huone) ja kylämerkit."""

    def __init__(self, nimi, sijainti):
        self.nimi = nimi
        self.esineet = []
        self.sijainti = sijainti
        self.kylamerkit = 0

    def liiku(self, kohde):
        self.sijainti = kohde

    def kerää_esine(self, nimi):
        for esine in self.sijainti.esineet:
            if esine.nimi == nimi:
                self.sijainti.esineet.remove(esine)
                self.esineet.append(esine)
                return True
        return False

    def lisaa_esine(self, esine):
        self.esineet.append(esine)

    def poista_esine(self, nimi):
        for esine in self.esineet:
            if esine.nimi == nimi:
                self.esineet.remove(esine)
                return True
        return False

    def has_esine(self, nimi):
        return any(esine.nimi == nimi for esine in self.esineet)

    def nayta_inventaario(self):
        print(f"Kylämerkkejä: {self.kylamerkit}")
        if self.esineet:
            print("Inventaario:")
            for esine in self.esineet:
                print("-", esine)
        else:
            print("Inventaario on tyhjä.")

    def ansaitse_merkki(self, maara=1):
        self.kylamerkit += maara

    def kayta_merkkeja(self, maara):
        if self.kylamerkit >= maara:
            self.kylamerkit -= maara
            return True
        return False


# ---------------------------------------------------------------------------
# Pelin asetukset: neljä tarvittavaa osaa ja kolme tapaa hankkia ne.
# Jokainen osa vastaa täsmälleen yhtä raaka-ainetta (RAAKA_AINE) ja yhtä
# hintaa kylämerkkeinä (OSTOHINNAT) - näin rakenna- ja osta-reitit pysyvät
# yksinkertaisina.
# ---------------------------------------------------------------------------
OSTOHINNAT = {
    "aurinkopaneeli": 3,
    "akku": 3,
    "kaapeli": 2,
    "hallintayksikkö": 4,
}

RAAKA_AINE = {
    "aurinkopaneeli": "lasinsiru",
    "akku": "akkukotelo",
    "kaapeli": "kuparikela",
    "hallintayksikkö": "piirilevy",
}

OSIEN_PAINOT = {
    "aurinkopaneeli": 5.0,
    "akku": 10.0,
    "kaapeli": 1.0,
    "hallintayksikkö": 2.0,
}

TARVITTAVAT_OSAT = list(OSTOHINNAT.keys())

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
    },
]


def luo_pelimaailma():
    """Rakentaa kylän viisi paikkaa ja palauttaa ne listana. Ensimmäinen
    (kylätalo) on pelin aloitus- ja lopetuspaikka."""

    kylatalo = Huone(
        "kylätalo",
        "Kylätalo on yhteisön sydän. Seinällä on vanha dieselgeneraattori,\n"
        "joka pitää kylän valot päällä - meluisasti ja saastuttaen.",
        hahmo={
            "nimi": "Kylänvanhin Elsa",
            "dialogi": [
                "\"Tarvitsemme neljä osaa aurinkovoimalaan: aurinkopaneelin, akun,\"",
                "\"kaapelin ja hallintayksikön.\"",
                "\"Voit ostaa ne torilta, rakentaa verstaassa, tai ansaita opettamalla\"",
                "\"koulussa. Tuo kaikki neljä tänne ja asenna ne!\"",
            ],
        },
    )

    tori = Huone(
        "tori",
        "Kylän tori. Täällä voi tehdä pieniä hommia kylämerkkien eteen,\n"
        "ja käyttää merkkejä valmiiden osien ostamiseen.",
    )

    verstas = Huone(
        "verstas",
        "Pölyinen verstas. Täällä kierrätysmateriaalista voi rakentaa\n"
        "tarvittavan osan, jos materiaali on mukana.",
    )

    kierratyspiste = Huone(
        "kierrätyspiste",
        "Kylän kierrätyspiste. Täältä löytyy hyödynnettäviä materiaaleja,\n"
        "jotka muuten päätyisivät kaatopaikalle.",
        esineet=[
            Esine("lasinsiru", 0.1),
            Esine("akkukotelo", 0.5),
            Esine("kuparikela", 0.3),
            Esine("piirilevy", 0.2),
        ],
    )

    koulu = Huone(
        "koulu",
        "Kylän pieni koulu. Opettaja Liisa kaipaisi apua kestävän\n"
        "kehityksen oppitunnilla.",
        hahmo={
            "nimi": "Opettaja Liisa",
            "dialogi": [
                "\"Vastaa oikein kestävän kehityksen kysymykseen, niin koulu\"",
                "\"lahjoittaa hankkeelle yhden osan! Kirjoita 'opeta'.\"",
            ],
        },
    )

    return [kylatalo, tori, verstas, kierratyspiste, koulu]


def lue_tiedosto(tiedostonimi):
    """Lukee tekstitiedoston projektin juuresta. Palauttaa None, jos
    tiedostoa ei löydy."""
    polku = os.path.join(SCRIPT_KANSIO, tiedostonimi)
    try:
        with open(polku, "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        return None


def tallenna_tilanne(pelaaja):
    with open(TALLENNUSTIEDOSTO, "w", encoding="utf-8") as f:
        f.write(pelaaja.nimi + "\n")
        f.write(pelaaja.sijainti.nimi + "\n")
        f.write(str(pelaaja.kylamerkit) + "\n")
        esinerivit = [f"{e.nimi};{e.paino}" for e in pelaaja.esineet]
        f.write(",".join(esinerivit) + "\n")
    print("Peli tallennettu.")


def lataa_tilanne(huoneet):
    """Lataa aiemman tallennuksen. Palauttaa uuden Pelaaja-olion, tai None
    jos tallennusta ei löydy. Poistaa ladatut esineet alkuperäisistä
    huoneistaan, jotta niitä ei voi kerätä kahteen kertaan."""
    if not os.path.exists(TALLENNUSTIEDOSTO):
        print("Tallennusta ei löytynyt.")
        return None

    with open(TALLENNUSTIEDOSTO, "r", encoding="utf-8") as f:
        rivit = f.read().splitlines()

    nimi = rivit[0]
    sijainnin_nimi = rivit[1]
    kylamerkit = int(rivit[2])
    esinerivit = rivit[3].split(",") if rivit[3] else []

    sijainti = next((h for h in huoneet if h.nimi == sijainnin_nimi), None)
    pelaaja = Pelaaja(nimi, sijainti)
    pelaaja.kylamerkit = kylamerkit

    for rivi in esinerivit:
        if not rivi:
            continue
        esine_nimi, paino_str = rivi.split(";")
        pelaaja.esineet.append(Esine(esine_nimi, float(paino_str)))
        for huone in huoneet:
            huone.esineet = [e for e in huone.esineet if e.nimi != esine_nimi]

    print(f"Tallennus ladattu. Tervetuloa takaisin, {nimi}!")
    return pelaaja


def tulosta_puuttuvat_osat(pelaaja):
    puuttuvat = [osa for osa in TARVITTAVAT_OSAT if not pelaaja.has_esine(osa)]
    if puuttuvat:
        print("Puuttuvat osat:", ", ".join(puuttuvat))
    else:
        print("Sinulla on kaikki tarvittavat osat!")


# ---------------------------------------------------------------------------
# Reitti A: osta torilta kylämerkeillä
# ---------------------------------------------------------------------------
def osta_osa(pelaaja):
    ostettavissa = [osa for osa in OSTOHINNAT if not pelaaja.has_esine(osa)]
    if not ostettavissa:
        print("Sinulla on jo kaikki osat!")
        return

    print("Myytävät osat:")
    for osa in ostettavissa:
        print(f"- {osa}: {OSTOHINNAT[osa]} kylämerkkiä")
    print(f"Sinulla on {pelaaja.kylamerkit} kylämerkkiä.")

    valinta = input("Minkä osan haluat ostaa? (tyhjä peruuttaa): ").strip().lower()
    if valinta == "" or valinta not in OSTOHINNAT or pelaaja.has_esine(valinta):
        return

    hinta = OSTOHINNAT[valinta]
    if pelaaja.kayta_merkkeja(hinta):
        pelaaja.lisaa_esine(Esine(valinta, OSIEN_PAINOT[valinta]))
        print(f"Ostit osan: {valinta}")
    else:
        print(f"Ei tarpeeksi kylämerkkejä. Tarvitset {hinta}, sinulla on {pelaaja.kylamerkit}.")


# ---------------------------------------------------------------------------
# Reitti B: rakenna verstaassa kierrätysmateriaalista
# ---------------------------------------------------------------------------
def rakenna_osa(pelaaja):
    rakennettavissa = [osa for osa in RAAKA_AINE if not pelaaja.has_esine(osa)]
    if not rakennettavissa:
        print("Sinulla on jo kaikki osat!")
        return

    print("Mahdolliset reseptit:")
    for osa in rakennettavissa:
        materiaali = RAAKA_AINE[osa]
        tila = "OK" if pelaaja.has_esine(materiaali) else "puuttuu"
        print(f"- {osa}: tarvitaan {materiaali} ({tila})")

    valinta = input("Minkä osan haluat rakentaa? (tyhjä peruuttaa): ").strip().lower()
    if valinta == "" or valinta not in RAAKA_AINE or pelaaja.has_esine(valinta):
        return

    materiaali = RAAKA_AINE[valinta]
    if not pelaaja.has_esine(materiaali):
        print(f"Sinulta puuttuu materiaali: {materiaali}")
        return

    pelaaja.poista_esine(materiaali)
    pelaaja.lisaa_esine(Esine(valinta, OSIEN_PAINOT[valinta]))
    print(f"Rakensit osan: {valinta}")


# ---------------------------------------------------------------------------
# Reitti C: opeta koulussa
# ---------------------------------------------------------------------------
def opeta_koulussa(pelaaja):
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

    print("Oikein! Koulu lahjoittaa hankkeelle osan.")
    print("Puuttuvat osat:", ", ".join(puuttuvat))
    valinta = input("Minkä osan haluat vastaanottaa? (tyhjä peruuttaa): ").strip().lower()
    if valinta in puuttuvat:
        pelaaja.lisaa_esine(Esine(valinta, OSIEN_PAINOT[valinta]))
        print(f"Sait osan: {valinta}")


def tarkista_ikaraja(ika):
    """Palauttaa True, jos annettu ikä täyttää pelin K12-ikäsuosituksen
    (12 vuotta tai yli)."""
    return ika >= 12


# ---------------------------------------------------------------------------
# Pääohjelma
# ---------------------------------------------------------------------------
def kaynnista_peli():
    ika_syote = input("Tämä peli on ikäsuositukseltaan K12. Anna ikäsi: ").strip()
    if not ika_syote.isdigit() or not tarkista_ikaraja(int(ika_syote)):
        print("Tämä peli on tarkoitettu 12 vuotta täyttäneille. Ohjelma sammuu.")
        return

    intro = lue_tiedosto("intro.txt")
    if intro:
        print(intro)

    huoneet = luo_pelimaailma()

    pelaaja = None
    if os.path.exists(TALLENNUSTIEDOSTO):
        vastaus = input("Löytyi aiempi tallennus. Jatketaanko siitä? (k/e): ").strip().lower()
        if vastaus == "k":
            pelaaja = lataa_tilanne(huoneet)

    if pelaaja is None:
        nimi = input("Anna pelaajan nimi: ").strip()
        pelaaja = Pelaaja(nimi, huoneet[0])
        print(f"\nTervetuloa kylään, {nimi}!")

    ohjeet = lue_tiedosto("ohjeet.txt")
    if ohjeet:
        print(ohjeet)
    pelaaja.sijainti.esittele()

    while True:
        komento = input("\nAnna komento: ").strip().lower()

        if komento == "lopeta":
            print("Kiitos pelaamisesta!")
            break

        elif komento == "ohjeet":
            print(lue_tiedosto("ohjeet.txt") or "")

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
                print("Sellaista paikkaa ei löydy. Paikat:", ", ".join(h.nimi for h in huoneet))

        elif komento == "kerää":
            if not pelaaja.sijainti.esineet:
                print("Täällä ei ole mitään kerättävää.")
            else:
                nimet = ", ".join(e.nimi for e in pelaaja.sijainti.esineet)
                print(f"Täällä on: {nimet}")
                valinta = input("Minkä esineen haluat kerätä? ").strip().lower()
                if pelaaja.kerää_esine(valinta):
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
            if pelaaja.sijainti.nimi != "tori":
                print("Hommia saa tehtyä vain torilla.")
            else:
                print("Autat markkinakauppiasta tunnin ajan. Kiitokseksi saat kylämerkin!")
                pelaaja.ansaitse_merkki(1)
                print(f"Kylämerkkejä yhteensä: {pelaaja.kylamerkit}")

        elif komento == "osta":
            if pelaaja.sijainti.nimi != "tori":
                print("Voit ostaa osia vain torilla.")
            else:
                osta_osa(pelaaja)

        elif komento == "rakenna":
            if pelaaja.sijainti.nimi != "verstas":
                print("Voit rakentaa osia vain verstaassa.")
            else:
                rakenna_osa(pelaaja)

        elif komento == "opeta":
            if pelaaja.sijainti.nimi != "koulu":
                print("Voit opettaa vain koulussa.")
            else:
                opeta_koulussa(pelaaja)

        elif komento == "edistyminen":
            kerätyt = [osa for osa in TARVITTAVAT_OSAT if pelaaja.has_esine(osa)]
            prosentti = round(100 * len(kerätyt) / len(TARVITTAVAT_OSAT))
            print(f"Edistyminen: {len(kerätyt)}/{len(TARVITTAVAT_OSAT)} osaa ({prosentti} %)")

        elif komento == "asenna":
            if pelaaja.sijainti.nimi != "kylätalo":
                print("Osat pitää asentaa kylätalolla.")
            elif all(pelaaja.has_esine(osa) for osa in TARVITTAVAT_OSAT):
                print("\nAsennat osat kylätalon katolle. Kylänvanhin Elsa hymyilee:")
                print("\"Nyt kylämme saa puhdasta energiaa auringosta!\"")
                print("\nOnnistuit edistämään kestävää energiantuotantoa (YK:n tavoite 7),")
                print("kierrätystä (tavoite 12) ja kestävän kehityksen opetusta (tavoite 4).")
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
