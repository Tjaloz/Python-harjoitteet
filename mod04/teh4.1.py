pituus = float(input("Anna kuhan pituus senttimetreinä: "))
if pituus < 37:
    puuttuu = 37 - pituus
    print("Kuha on alamittainen, laske se takaisin veteen. ")
    print(f"Alimmasta sallitusta pyyntimitasta puuttuu {puuttuu} cm.")
else:
    print("Kuha on sallitussa pyyntimitassa, voit pitää sen.")