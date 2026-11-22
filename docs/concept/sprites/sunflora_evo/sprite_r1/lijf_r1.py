# Lijf r1 = reparatie per pixel van de kale reducties (lijfboven_kaal: Sunflora-armen+lijfje op 0.57;
# voeten_kaal: r5-hangvoeten op 0.256). De reductie is op deze maat pap; vormen volgen de bron:
#  - armen: Sunflora-blad (punt buiten-boven, lichte kant boven-links, donkergroen b als lijn aan de lichtkant, zwart onder/rechts)
#  - lijfje: Sunflora-eitje
#  - voeten: r5 (links kleiner/hoger, rechts groter/lager, hangend aan steeltjes)
# Tekens: 1 zwart, b (82,98,41), c (115,172,49), d (156,213,74), e (189,255,115) = Sunflora c/d/e/f.
import numpy as np
ch='.123456789abcdef'
def put(G,y,x,rows):
    for j,r in enumerate(rows):
        for i,t in enumerate(r):
            if t!=' ' and t!='.': G[y+j,x+i]=ch.index(t)
G=np.zeros((14,23),'uint8')
put(G,0,0,["b.........",
           "bebbbb....",
           "beeeddbb..",
           ".bddddddb.",
           "..bcccccc1",
           "...11111.."])
put(G,0,13,[".........b",
            "....bbbbe1",
            "..bbdddde1",
            ".bdddddd1.",
            "1ccccccc1.",
            ".11111...."])
put(G,1,8, ["..bbb..",
            ".bdedd1",
            "bdeddc1",
            "bdddcc1",
            "bdddcc1",
            ".bccc1.",
            "..111.."])
put(G,8,7, ["..b..b",
           "1ed1.b",
           "1dc11edd1",
           ".11.1ddc1",
           "....1dcc1",
           ".....111"])
np.save('lijf_r1.npy',G)
[print(''.join(ch[v] for v in r)) for r in G]
