import os

from .esine import Esine

# Tiedostopolut lasketaan suhteessa TÄMÄN tiedoston sijaintiin eikä siihen
# mistä kansiosta käsin ohjelma sattuu olevan käynnistetty. Näin intro.txt,
# ohjeet.txt ja tallennus.txt löytyvät aina, vaikka peliä ajettaisiin esim.
# IDE:n projektin juuresta eikä pelimoduulit-paketin tai main.py:n kansiosta.
_PAKETTI_KANSIO = os.path.dirname(os.path.abspath(__file__))
PROJEKTIN_JUURI = os.path.dirname(_PAKETTI_KANSIO)

TALLENNUSTIEDOSTO = os.path.join(PROJEKTIN_JUURI, "tallennus.txt")


def _polku(tiedostonimi):
    return os.path.join(PROJEKTIN_JUURI, tiedostonimi)


def lue_tiedosto(tiedostonimi):
    """Lukee tekstitiedoston projektin juuresta. Palauttaa None, jos tiedostoa
    ei löydy (esim. ohjeet.txt on luonteeltaan valinnainen lisä)."""
    polku = _polku(tiedostonimi)
    try:
        with open(polku, "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        print(f"[Varoitus: tiedostoa '{tiedostonimi}' ei löytynyt kansiosta {PROJEKTIN_JUURI}]")
        return None


def tallenna_tilanne(pelaaja):
    """Tallentaa pelaajan nimen, sijainnin, kylämerkit ja inventaarion
    (esineen nimi JA paino) tekstitiedostoon."""
    with open(TALLENNUSTIEDOSTO, "w", encoding="utf-8") as f:
        f.write(pelaaja.nimi + "\n")
        f.write(pelaaja.sijainti.nimi + "\n")
        f.write(str(pelaaja.kylamerkit) + "\n")
        esinerivit = [f"{esine.nimi};{esine.paino}" for esine in pelaaja.esineet]
        f.write(",".join(esinerivit) + "\n")
    print("Peli tallennettu.")


def lataa_tilanne(huoneet, pelaaja_luokka):
    """Lataa aiemmin tallennetun pelitilanteen. Palauttaa uuden Pelaaja-olion,
    tai None jos tallennusta ei löytynyt.

    Huom: koska pelimaailma (huoneet ja niiden esineet) luodaan joka
    käynnistyskerralla uudestaan, tämä poistaa ladatut esineet vielä
    erikseen niiden alkuperäisistä huoneista, jottei samaa esinettä voisi
    kerätä kahteen kertaan lataamisen jälkeen."""
    if not os.path.exists(TALLENNUSTIEDOSTO):
        print("Tallennusta ei löytynyt.")
        return None

    with open(TALLENNUSTIEDOSTO, "r", encoding="utf-8") as f:
        rivit = f.read().splitlines()

    nimi = rivit[0]
    sijainnin_nimi = rivit[1]
    kylamerkit = int(rivit[2])
    esinerivit = rivit[3].split(",") if rivit[3] else []

    sijainti = None
    for huone in huoneet:
        if huone.nimi == sijainnin_nimi:
            sijainti = huone
            break

    pelaaja = pelaaja_luokka(nimi, sijainti)
    pelaaja.kylamerkit = kylamerkit

    for rivi in esinerivit:
        if not rivi:
            continue
        esine_nimi, paino_str = rivi.split(";")
        pelaaja.esineet.append(Esine(esine_nimi, float(paino_str)))

        # Poistetaan sama esine kaikista huoneista, jotta sitä ei voi kerätä
        # uudelleen (esine on jo kertaalleen kerätty aiemmassa pelisessiossa).
        for huone in huoneet:
            huone.esineet = [e for e in huone.esineet if e.nimi != esine_nimi]

    print(f"Tallennus ladattu. Tervetuloa takaisin, {nimi}!")
    return pelaaja
