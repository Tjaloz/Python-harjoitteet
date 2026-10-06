class Huone:
    """Pelimaailman paikka (esim. kylän osa).

    Ominaisuudet:
        nimi (str): paikan nimi, jolla siihen liikutaan ("liiku <nimi>")
        kuvaus (str): tarinallinen kuvausteksti, joka tulostetaan saavuttaessa
        esineet (list[Esine]): paikasta kerättävissä olevat esineet
        hahmo (dict | None): mahdollinen pelihahmo paikassa, muotoa
            {"nimi": str, "dialogi": list[str]}. None jos paikassa ei ole ketään.
    """

    def __init__(self, nimi, kuvaus, esineet=None, hahmo=None):
        self.nimi = nimi
        self.kuvaus = kuvaus
        self.esineet = esineet if esineet is not None else []
        self.hahmo = hahmo

    def esittele(self):
        """Tulostaa paikan kuvauksen, siellä olevat esineet ja mahdollisen hahmon."""
        print(f"\n=== {self.nimi.capitalize()} ===")
        print(self.kuvaus)

        if self.esineet:
            nimet = ", ".join(esine.nimi for esine in self.esineet)
            print(f"Täällä on kerättävissä: {nimet}")

        if self.hahmo:
            print(f"Täällä on {self.hahmo['nimi']}. Voit jutella hänelle komennolla 'puhu'.")
