syotetyt_nimet = set()
kaikki_nimet = []

while True:
    nimi = input("Anna nimi (tyhjä lopettaa): ")
    if nimi == "":
        break

    if nimi in syotetyt_nimet:
        print("Aiemmin syötetty nimi")
    else:
        print("Uusi nimi")
        syotetyt_nimet.add(nimi)

    kaikki_nimet.append(nimi)

print("Syötetyt nimet:")
for nimi in kaikki_nimet:
    print(nimi)