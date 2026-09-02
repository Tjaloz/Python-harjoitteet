import random
import datetime

nimi = input("Anna pelaajan nimi: ")
ika = int(input("Anna pelaajan ikä: "))
if ika < 12:
    print("Pelaaja on liian nuori, ohjelma sammuu.")
else:
    print ("Tervetuloa peliin!")
print(f"Pelaajan nimi on {nimi} ja ikä on {ika}")

while True:
        komento = input("Anna komento (aika, päivämäärä, kolikko, lopeta): ")
        if komento == "aika":
            print("Kello on:", datetime.datetime.now().strftime("%H:%M:%S"))
        elif komento == "päivämäärä":
            print("Päivämäärä on:", datetime.datetime.now().strftime("%d.%m.%Y"))
        elif komento == "kolikko":
            kolikko = random.choice(["kruuna", "klaava"])
            print("Kolikon heitto:", kolikko)
        elif komento == "lopeta":
            print("Ohjelma lopetetaan.")
            break
        else:
            print("Tuntematon komento. Yritä uudelleen.")
