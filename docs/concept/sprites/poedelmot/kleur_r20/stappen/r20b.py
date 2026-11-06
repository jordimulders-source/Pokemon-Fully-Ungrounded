# r20b: rechtervoorvleugel (buitenste krulboog naar het model, verzonnen lijnstukjes weg, tan op de modelplekken, rij 30)
#       linkervleugel (tan streken rij 30-34 op de modelplekken). Gemeten met stappen/grid.py (p15 per spritepixel).
F={}
def put(p,c): F[p]=c
# oude krulboog weg (model p15 200-240)
for p in [(54,21),(55,22),(56,23),(56,24),(55,25)]: put(p,'7')
put((54,26),'A')
# nieuwe krulboog (model p15 150-180)
for p in [(55,21),(56,21),(56,22),(57,22),(57,23),(58,23),(57,24),(58,24),(56,25),(57,25),(55,26),(56,26)]: put(p,'5')
# lijnstukjes 444 (51-53,24) en 555 (52-54,26) weg
for p in [(51,24),(52,24),(53,24),(53,26)]: put(p,'A')
put((52,26),'7')
# tan op de modelplekken
for p in [(50,25),(51,25),(50,26),(53,27),(54,27)]: put(p,'5')
# rij 30: 5 op x48-52 (model 140-160), x47 licht (200)
put((47,30),'7')
for x in range(48,53): put((x,30),'5')
# linkervleugel
for p in [(14,30),(15,30)]: put(p,'D')
for p in [(10,31),(11,31),(15,31),(16,31)]: put(p,'D')
for p in [(13,31),(14,31)]: put(p,'A')
for p in [(17,31),(18,31)]: put(p,'5')
for p in [(12,32),(13,32)]: put(p,'D')
for p in [(10,33),(12,33),(13,33)]: put(p,'D')
for p in [(14,33),(15,33)]: put(p,'7')
put((13,34),'D')
W={}
for (x,y),c in F.items(): W.setdefault(y,[]).append((x,c))
# tweede ronde na de controle: binnenkrul loopt door (model p15 150-160), vlakken naar de meting
for p in [(56,27),(57,27),(57,28),(57,29),(55,30)]: F[p]='5'
for p in [(55,28),(59,24),(60,24),(52,25),(53,25),(54,25),(52,26),(54,24),(55,24),(52,27),(12,31)]: F[p]='A'
for p in [(56,30),(53,28),(56,24),(55,25)]: F[p]='7'
for p in [(10,32),(11,33)]: F[p]='D'
F[(11,32)]='7'; F[(11,33)]='D'
F[(17,31)]='3'; F[(18,31)]='4'
W={}
for (x,y),c in F.items(): W.setdefault(y,[]).append((x,c))
F[(11,32)]='D'; F[(11,34)]='7'; F[(12,34)]='7'; F[(51,26)]='A'
W={}
for (x,y),c in F.items(): W.setdefault(y,[]).append((x,c))
F[(55,25)]='A'; F[(56,30)]='A'
W={}
for (x,y),c in F.items(): W.setdefault(y,[]).append((x,c))
