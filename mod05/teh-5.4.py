import random

arvottu = random.randint(1, 10)
arvaus = 0
while arvaus != arvottu:
    arvaus = int(input("Arvaa luku välistä 1-10: "))
    if arvaus > arvottu:
        print("Liian suuri arvaus!")
    elif arvaus < arvottu:
        print("Liian pieni!")
    else:
        print("Oikein!")