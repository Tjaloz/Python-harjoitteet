import math

def yksikkohinta(halkaisija_cm, hinta):
    halkaisija_m = halkaisija_cm / 100
    säde = halkaisija_m / 2
    pinta_ala = math.pi * säde ** 2
    return hinta / pinta_ala

halkaisija1 = float(input("Anna ensimmäisen pizzan halkaisija (cm): "))
hinta1 = float(input("Anna ensimmäisen pizzan hinta (€): "))

halkaisija2 = float(input("Anna toisen pizzan halkaisija (cm): "))
hinta2 = float(input("Anna toisen pizzan hinta (€): "))

yksikkohinta1 = yksikkohinta(halkaisija1, hinta1)
yksikkohinta2 = yksikkohinta(halkaisija2, hinta2)

print(f"Ensimmäisen pizzan yksikköhinta: {yksikkohinta1:.4f} €/m²")
print(f"Toisen pizzan yksikköhinta: {yksikkohinta2:.4f} €/m²")

if yksikkohinta1 < yksikkohinta2:
    print("Ensimmäinen pizza on edullisempi.")
elif yksikkohinta1 > yksikkohinta2:
    print("Toinen pizza on edullisempi.")
else:
    print("Pizzat ovat saman arvoisia.")  