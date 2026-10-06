class Esine:
    """Yksittäinen pelimaailman esine.

    Ominaisuudet:
        nimi (str): esineen nimi, jolla siihen viitataan komennoissa
        paino (float): esineen paino kilogrammoina (vain tarinallinen lisä,
            ei vaikuta pelimekaniikkaan)
    """

    def __init__(self, nimi, paino):
        self.nimi = nimi
        self.paino = paino

    def __str__(self):
        return f"{self.nimi} ({self.paino} kg)"
