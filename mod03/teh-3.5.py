leiviskat_str = input("Anna leiviskät: ")
leiviskat = float(leiviskat_str)
naulat_str = input("Anna naulat: ")
naulat = float(naulat_str)
luodit_str = input("Anna luodit: ")
luodit = float(luodit_str)
naulaa_yhteensa = leiviskat * 20 + naulat + luodit / 32
grammaa_yhteensa = naulaa_yhteensa * 32 * 13.3
kilogrammat = int(grammaa_yhteensa / 1000)
grammat = grammaa_yhteensa % 1000
print("")
print("Massa nykymittojen mukaan")
print(str(kilogrammat) + "kilogrammaa ja " + str(grammat) + "grammaa")
