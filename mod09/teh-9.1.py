class auto:
    def __init__(self, rekisteritunnus, huippunopeus):
        self.rekisteritunnus = rekisteritunnus
        self.huippunopeus = huippunopeus
        self.nopeus = 0
        self.matka = 0
auto = auto("ABC-123", 142)
print("rekisteritunnus:", auto.rekisteritunnus)
print("huippunopeus:", auto.huippunopeus)
print("nopeus:", auto.nopeus)
print("kuljettu matka:", auto.matka)