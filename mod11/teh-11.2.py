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

class Sähköauto(auto):
                def __init__(self, rekisteritunnus, huippunopeus, akkukapasiteetti):
                      super().__init__(rekisteritunnus, huippunopeus)
                      self.akkukapasiteetti = akkukapasiteetti

class Polttomoottoriauto(auto):
    def __init__(self, rekisteritunnus, huippunopeus, tankin_koko):
          super().__init__(rekisteritunnus, huippunopeus)
          self.tankin_koko = tankin_koko

sahkoauto = Sähköauto("ABC-15", 180, 52.5)
polttoauto = Polttomoottoriauto("ACD-123", 165, 32.3)

sahkoauto.kiihdytä(100)
polttoauto.kiihdytä(90)

sahkoauto.kulje(3)
polttoauto.kulje(3)

print(f"Sähköauto {sahkoauto.rekisteritunnus} matkamittari: {sahkoauto.matka} km")
print(f"Polttomoottoriauto {polttoauto.rekisteritunnus} matkamittari: {polttoauto.matka} km")
