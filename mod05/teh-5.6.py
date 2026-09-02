import random

N = int(input("Anna arvottavien pisteiden määrä? "))
n = 0
laskuri = 0

while laskuri < N:
    x = random.randint(-1, 1)
    y = random.randint(-1, 1)
    if x**2 + y**2 < 1:
        n += 1
    laskuri += 1

pii_arvio = 4 * n / N
print(f"Piin likiarvo: {pii_arvio}")