class Pelaaja:
    """Pelaaja: nimi, hallussa olevat esineet, nykyinen sijainti ja kylämerkit.

    Kylämerkit ovat pelin sisäinen "valuutta", jota pelaaja ansaitsee
    tekemällä hommia ja jolla voi ostaa osia torilta (ks. main.py).

    Ominaisuudet:
        nimi (str)
        esineet (list[Esine]): pelaajan inventaario
        sijainti (Huone): paikka, jossa pelaaja kulloinkin on
        kylamerkit (int): ansaittujen kylämerkkien määrä
    """

    def __init__(self, nimi, sijainti):
        self.nimi = nimi
        self.esineet = []
        self.sijainti = sijainti
        self.kylamerkit = 0

    def liiku(self, kohde):
        self.sijainti = kohde

    def keraa_esine(self, nimi):
        """Yrittää kerätä nimetyn esineen nykyisestä huoneesta inventaarioon.
        Palauttaa True jos onnistui, muuten False."""
        for esine in self.sijainti.esineet:
            if esine.nimi == nimi:
                self.sijainti.esineet.remove(esine)
                self.esineet.append(esine)
                return True
        return False

    def lisaa_esine(self, esine):
        """Lisää esineen suoraan inventaarioon (esim. ostettu tai rakennettu osa)."""
        self.esineet.append(esine)

    def poista_esine(self, nimi):
        """Poistaa nimetyn esineen inventaariosta (esim. rakentamisen raaka-aine).
        Palauttaa True jos esine löytyi ja poistettiin, muuten False."""
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
        """Yrittää käyttää annetun määrän kylämerkkejä. Palauttaa True jos
        merkkejä oli riittävästi (ja ne vähennettiin), muuten False."""
        if self.kylamerkit >= maara:
            self.kylamerkit -= maara
            return True
        return False
