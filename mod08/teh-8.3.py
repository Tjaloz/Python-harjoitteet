lentoasemat = {}

while True:
    valinta = input("Valitse toiminto (uusi, haku, lopeta): ").strip().lower() 

    if valinta == "lopeta":
        break

    elif valinta == "uusi":
        koodi = input("Anna lentoaseman ICAO-koodi: ").strip().upper()
        nimi = input("Anna lentoaseman nimi: ").strip()
        lentoasemat[koodi] = nimi
        print("Lentoasema tallennettu.")
       
    elif valinta == "haku":
        koodi = input("Anna lentoaseman ICAO-koodi: ").strip().upper()
        if koodi in lentoasemat:
            print("Lentoasema:", lentoasemat[koodi])
        else:
            print("Lentoasemaa ei löytynyt.")

    else:
        print("Tuntematon toiminto. Yritä uudelleen.")