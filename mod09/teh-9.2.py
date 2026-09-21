class auto:
    def __init__(self, rekisteritunnus, huippunopeus):
        self.rekisteritunnus = rekisteritunnus
        self.huippunopeus = huippunopeus
        self.nopeus = 0
        self.matka = 0


    def kiihdyta(self, muutos):
        uusi_nopeus = self.nopeus + muutos
        if uusi_nopeus > self.huippunopeus:
            uusi_nopeus = self.huippunopeus
        elif uusi_nopeus < 0:
            uusi_nopeus = 0
        self.nopeus = uusi_nopeus

auto = auto("ABC-123", 142)

auto.kiihdyta(30)
print("nopeus:", auto.nopeus)

auto.kiihdyta(70)
print("nopeus:", auto.nopeus)

auto.kiihdyta(50)
print("nopeus:", auto.nopeus)

auto.kiihdyta(-200)
print("nopeus:", auto.nopeus)