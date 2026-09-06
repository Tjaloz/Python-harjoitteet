def karsi_parittomat(luvut):
    parilliset = []
    for luku in luvut:
        if luku % 2 == 0:
            parilliset.append(luku)
    return parilliset

# testi
alkuperainen = [1, 2, 3, 4, 5, 6, 7, 8]
karsittu = karsi_parittomat(alkuperainen)
print("alkuperäinen lista:", alkuperainen)
print("Karsittu lista:", karsittu)