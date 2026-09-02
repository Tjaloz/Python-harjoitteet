luvut = []
while True:
    luku = input("Anna luku (tyhjä lopettaa): ")
    if luku == "":
        break
    luvut.append(float(luku))

if luvut:
    print(f"Pienin: {min(luvut)}")
    print(f"Suurin: {max(luvut)}")
else:
    print("Yhtään lukua ei annettu.")