import random
import datetime

inventaario = []

nimi = input("Anna pelaajan nimi: ")
ika = int(input("Anna pelaajan ikä: "))
if ika < 12:
    print("Pelaaja on liian nuori, ohjelma sammuu.")
else:
    print ("Tervetuloa peliin!")
print(f"Pelaajan nimi on {nimi} ja ikä on {ika}")

def lisaa_esine(lista):
    esine = input("Anna esineen nimi: ")
    lista.append(esine)
    print(f"Esine '{esine}' lisätty inventaarioon.")
def nayta_inventaario(lista):
    if lista:
        print("inventaario:")
        for esine in lista:
            print("-", esine)
    else:
        print("Inventaario on tyhjä.")
def tyhjenna_inventaario(lista):
    lista.clear()
    print("Inventaario tyhjennetty.")

while True:
        komento = input("Anna komento (aika, päivämäärä, kolikko, lisää, näytä, tyhjennä, lopeta): ")
        if komento == "aika":
            print("Kello on:", datetime.datetime.now().strftime("%H:%M:%S"))
        elif komento == "päivämäärä":
            print("Päivämäärä on:", datetime.datetime.now().strftime("%d.%m.%Y"))
        elif komento == "kolikko":
            kolikko = random.choice(["kruuna", "klaava"])
            print("Kolikon heitto:", kolikko)
        elif komento == "lisää":
            lisaa_esine(inventaario)
        elif komento == "näytä":
            nayta_inventaario(inventaario)
        elif komento == "tyhjennä":
            tyhjenna_inventaario(inventaario)
        elif komento == "lopeta":
            print("Ohjelma lopetetaan.")
            break
        else:
            print("Tuntematon komento. Yritä uudelleen.")
