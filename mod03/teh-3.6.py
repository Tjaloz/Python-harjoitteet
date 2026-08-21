import random

koodi1 = ""
for i in range(3):
    numero = random.randint(0, 9)
    koodi1 = koodi1 + str(numero)

koodi2 = ""
for i in range(4):
    numero = random.randint(1, 6)
    koodi2 = koodi2 + str(numero)

print("kolminumeroinen koodi:" + koodi1)
print("nelinumeroinen koodi:" + koodi2)