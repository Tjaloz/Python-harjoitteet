luokka = input("Anna hyttiluokka (LUX, A, B, C): ")
if luokka == "LUX":
    print("Parvekkeellinen hytti yläkannella.")
elif luokka == "A":
    print("Ikkunallinen hytti autokannen yläpuolella.")
elif luokka == "B":
    print("Ikkunaton hytti autokannen yläpuolella.")
elif luokka == "C":
    print("Ikkunaton hytti autokannen alapuolella.")
else:
    print("Virheellinen hyttiluokka.")
