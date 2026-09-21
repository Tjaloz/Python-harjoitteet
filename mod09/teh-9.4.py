import random

class auto:
    def __init__(self, rekisteritunnus, huippunopeus):
        self.rekisteritunnus = rekisteritunnus
        self.huippunopeus = huippunopeus
        self.nopeus = 0
        self.matka = 0


    def kiihdytä(self, muutos):
        uusi_nopeus = self.nopeus + muutos
        if uusi_nopeus > self.huippunopeus:
            uusi_nopeus = self.huippunopeus
        elif uusi_nopeus < 0:
            uusi_nopeus = 0
        self.nopeus = uusi_nopeus

    def kulje(self, tunnit):
        self.matka += self.nopeus * tunnit

autot = []
for i in range(1, 11):
    rekisteritunnus = f"ABC-{i}"
    huippunopeus = random.randint(100, 200)
    autot.append(auto(rekisteritunnus, huippunopeus))

kilpailu_kaynnissa = True
while kilpailu_kaynnissa:
    for auto in autot:
        muutos = random.randint(-10, 15)
        auto.kiihdytä(muutos)
        auto.kulje(1)

    for auto in autot:
        if auto.matka >= 10000:
            kilpailu_kaynnissa = False
            break

print(f"{'rekisteritunnus':<15}{'huippunopeus':<15}{'nopeus':<10}{'matka':<10}")
for auto in autot:
    print(f"{auto.rekisteritunnus:<15}{auto.huippunopeus:<15}{auto.nopeus:<10}{round(auto.matka, 1):<10}")