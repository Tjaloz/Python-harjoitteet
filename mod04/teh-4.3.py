sukupuoli = input("Anna biologinen sukupuoli (nainen/mies): ")
hb = float(input("Hemoglobiiniarvo (g/l): "))
if sukupuoli == "nainen":
    if hb < 117:
        print("Hemoglobiiniarvo on alhainen.")
    elif hb <= 175:
        print("Hemoglobiini on normaali.")
    else:
        print("Hemoglobiiniarvo on korkea.")
elif sukupuoli == "mies":
    if hb < 134:
        print("Hemoglobiiniarvo on alhainen.")
    elif hb <= 195:
        print("Hemoglobiini on normaali.")
    else:
        print("Hemoglobiiniarvo on korkea.")