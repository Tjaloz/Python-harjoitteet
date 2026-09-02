oikea_tunnus = "Python"
oikea_salasana = "rules"
yritykset = 0

while yritykset < 5:
    tunnus = input("Anna tunnus: ")
    salasana = input("Anna salasana: ")
    yritykset += 1

    if tunnus == oikea_tunnus and salasana == oikea_salasana:
        print("Tervetuloa!")
        break
    else:
        print("Pääsy evätty.")