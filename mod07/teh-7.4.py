def listan_summa(luvut):
    summa = 0
    for luku in luvut:
        summa += luku
    return summa

# testi
testilista = [1, 2, 3, 4, 5]
print("summa:", listan_summa(testilista))  # tulostaa summan 15