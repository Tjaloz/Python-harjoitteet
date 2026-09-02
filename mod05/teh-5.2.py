while True:
    tuumat = float(input("Anna tuumat (negatiivinen lopettaa): "))
    if tuumat < 0:
        break
    sentit = tuumat * 2.54
    print(f"{tuumat} tuumaa on {sentit} senttimetriä.")