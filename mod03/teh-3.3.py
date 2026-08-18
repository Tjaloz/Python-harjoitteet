kanta_str= input("Anna suorakulmion kanta")
kanta = float(kanta_str)
korkeus_str= input("Anna suorakulmion korkeus")
korkeus = float(korkeus_str)
piiri = 2*(kanta + korkeus)
pinta_ala = kanta * korkeus
print("Suorakulmion piiri on: " + str(piiri))
print("Suorakulmion pinta-ala on: " + str(pinta_ala))