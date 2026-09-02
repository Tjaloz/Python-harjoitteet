luvut = []
while True:
    syote = input("Anna luku (tyhjä lopettaa): ")
    if syote == "":
        break
    luvut.append(float(syote))

luvut.sort(reverse=True)
print("Viisi suurinta lukua:", luvut[:5])