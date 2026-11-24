# bouw.py ronde 4 (na Jordi: "kraag van r1 was prima", "broek weer precies hetzelfde fout", "het moet gewoon een tuinbroekvorm zijn,
# niet met volledig rechte lijnen, het bovenlichaam moet geen pixelblur zijn, gewoon nette vormen, kijk naar het model en zorg voor
# genoeg kleurtinten en schaduw"). Basis = r1 + neus van r3. Kraag, gezicht, stam, potlood, staart, klep: diff 0.
# Alleen pixel-opdrachten (geen middeling): tuinbroekvorm (randen als curves), crème met 3 tinten r1 (7 licht, 6 schaduw, F diep),
# bovenlichaam: losse vlekjes weg + vormen uit het model (plooi onder de schouder, armcontour, sikkels).
import numpy as np,sys; sys.path.insert(0,'sprite_r1'); from gemeen import *
r1=laad('sprite_r1/sprite.png'); r3=laad('sprite_r3/sprite.png')
o=r1.copy(); zone={}
fg=r1>0; P=np.pad(fg,1); RAND=fg&~(P[:-2,1:-1]&P[2:,1:-1]&P[1:-1,:-2]&P[1:-1,2:])
def z(n,x,y,v):
    assert r1[y,x]!=0, ('silhouet',x,y)
    if RAND[y,x] and n!='neus': return              # buitenlijn/selout (r1) blijft
    o[y,x]=v; zone[(x,y)]=n
def rij(n,y,x0,x1,v):
    for x in range(x0,x1+1): z(n,x,y,v)
# neus van r3
for y,x in zip(*np.where(r3!=r1)):
    if y<25: z('neus',x,y,r3[y,x])
C,S,D=7,6,15   # creme, creme-schaduw, creme-donker
# ---------- 1. borststuk (bib): randen als curve, zak- en zoomlijn als boog ----------
# linkerrand: x21 (r31-33, r1) -> x20 (r34-36) -> x21 (r37-39) -> x22 (r40-41); rechterrand: x37 (r30-32) -> x38 (r33-36) -> x37 (r37-38) -> x36 (r39-40) -> x35 (r41)
L={34:20,35:20,36:20,37:21,38:21,39:21,40:22,41:22}; R={33:38,34:38,35:38,36:37,37:37,38:37,39:36,40:36,41:35}
for y in range(33,42):
    l=L.get(y,21)
    for x in range(19,40):
        if y==33 and x<38: continue
        inbib= l<=x<=R[y]
        if inbib and o[y,x] not in (C,S,D): z('borststuk rand',x,y,C)
        if not inbib and o[y,x] in (C,S,D) and x>=19: z('borststuk rand',x,y,4)
# bib-inhoud: eerst alles creme (r1-bruinband r36 en kaki-lijn r34 weg), dan schaduw onder de vachtbolletjes, zakboog, rechtersikkel
for y in range(34,42):
    for x in range(L[y],R[y]+1):
        if o[y,x]!=C: z('borststuk',x,y,C)
for x in (26,27,28): z('borststuk',x,34,S)                              # schaduw onder de zwarte bolletjes (r33 x26-28)
for x,y in ((24,36),(25,36),(26,37),(27,37),(28,37),(29,38),(30,38),(31,38),(32,37),(33,37)): z('borststuk zakboog',x,y,S)
for x,y in ((38,34),(38,35),(37,36),(37,37),(37,38),(36,39),(36,40),(35,41)): z('borststuk sikkel',x,y,S)   # schaduwkant rechts
for x,y in ((21,39),(22,40),(22,41)): z('borststuk sikkel',x,y,S)
# zijkanten lijf naast het borststuk: bruin met binnenlijn tegen de bib (bestaande r1-tinten 3/4)
for y in (37,38,39,40,41): z('lijf links',L[y]-1,y,3)
# ---------- 2. taille: zoom als boog over de bib, rechts naar de arm omlaag ----------
W={19:42,20:42,36:42,37:42,38:42,39:43,40:43,41:43,42:44}
for x,w in W.items():
    for y in range(38,w):
        inbib= y in L and L[y]<=x<=R[y]
        if o[y,x] in (C,S,D) and not inbib: z('taille',x,y,4)
    if o[w,x] not in (C,S,D): z('taille',x,w,C)
for y in (42,43):
    for x in range(19,44):
        if y>=W.get(x,0) and o[y,x] in (4,3) and x<=42: z('taille',x,y,C)
for x,y in ((22,42),(23,42),(24,43),(25,43),(26,43),(27,44),(28,44),(29,44),(30,43),(31,43),(32,43),(33,42),(34,42)): z('zoom',x,y,S)
for x in range(23,34):                                                  # r1-kaki x27-29 r42 weg (boven de zoom)
    for y in range(42,45):
        if o[y,x]==S and zone.get((x,y))!='zoom': z('broek',x,y,C)
# ---------- 3. broek: buikonderkant als boog, sikkels op dijen/schenen ----------
B={22:51,23:50,24:51,25:51,26:51,27:52,28:52,29:53,30:53,31:53,32:52,33:52,34:51,35:51,36:50,37:50}   # eerste schaduwrij
for x,b in B.items():
    for y in range(46,56):
        if o[y,x] in (C,S,D) and (x,y) not in zone:
            v=C if y<b else S
            if o[y,x]!=v: z('broek buik/kruis',x,y,v)
# linker dij: licht tot een boog (knie), daaronder scheen in schaduw
LB={16:52,17:53,18:53,19:53,20:52,21:52}
for x,b in LB.items():
    for y in range(47,57):
        if o[y,x] in (C,S,D):
            v=C if y<b else S
            if o[y,x]!=v: z('broek linkerbeen',x,y,v)
for x,y in ((22,50),(22,52)): z('broek linkerbeen',x,y,S)                # r1 F-streepje x22 r50-52 -> curve
# diepe schaduw (F) als sikkel: binnenkant linkerscheen tegen het kruis en onderrand
for x,y in ((27,53),(27,54),(26,55),(25,56),(24,56)): z('broek sikkel F',x,y,D)
# rechterbeen: sikkel rechts, breder naar onder (S), F als diepste rand langs de buitenlijn (schaduwkant)
RS={48:(50,99),49:(50,99),50:(50,52),51:(49,51),52:(49,51),53:(48,51),54:(48,50),55:(47,50),56:(46,49),57:(45,48),58:(44,47)}
for y,(s6,sF) in RS.items():
    for x in range(39,53):
        if o[y,x] in (C,S,D) and (x,y) not in zone and not RAND[y,x]:
            v=D if x>=sF else (S if x>=s6 else C)
            if o[y,x]!=v: z('broek rechterbeen',x,y,v)
for x,y in ((38,50),(38,51),(38,52),(38,53),(38,54)):                 # r1 F-kolom x38 (rechte lijn) -> boog als dijrand
    z('broek rechterbeen',x,y,S)
for x,y in ((38,51),(39,52),(39,53),(39,54),(40,55)): z('broek rechterbeen',x,y,D)
# ---------- 4. enkels: manchet als boog (voet hoger aan de zijkanten) ----------
for x,y in ((20,57),(24,57),(45,59),(49,59)): z('enkels',x,y,8)
for x,y in ((21,58),(22,58),(23,58)): z('enkels',x,y,S)
# ---------- 5. bovenlichaam: vlekjes weg, plooi onder de schouder en armcontour uit het model, sikkels ----------
for x,y in ((48,30),(48,31),(41,33)): z('bovenlichaam',x,y,4)
for y,(a,b) in {34:(41,42),35:(40,44),36:(40,44),37:(39,44),38:(40,43),39:(41,42)}.items(): rij('bovenlichaam plooi',y,a,b,3)
for x,y in ((45,35),(45,36),(45,37),(44,38),(44,39),(44,40),(44,41)): z('bovenlichaam armcontour',x,y,2)
z('bovenlichaam',46,35,4); z('bovenlichaam',43,39,4)
# linkerarm: licht (4) linksboven, schaduw (2) onder
for x,y in ((10,28),(11,28),(12,28),(13,28),(14,28),(10,29),(11,29),(12,29),(10,30),(11,30)): z('linkerarm',x,y,4)
for x,y in ((15,34),(16,34),(17,34),(18,33),(19,33),(20,33)): 
    if o[y,x] in (3,4): z('linkerarm',x,y,2)
# ---------- 6. vormen in de broek uit het model: plooi buik/linkerdij (r1-lijn x19-20 r45-48 doorgetrokken) en buik/rechterdij ----------
for x,y in ((20,49),(21,50)): z('broek plooi',x,y,S)
for x,y in ((37,46),(37,47),(38,48),(38,49)): z('broek plooi',x,y,S)
# linkerscheen: licht langs de linkerkant (knie loopt door), rest schaduw, F-sikkel rechts/onder
for x,y in ((16,52),(16,53),(16,54),(17,53),(17,54),(18,53)): z('broek linkerbeen',x,y,C)
z('broek buiksikkel',42,45,S)
# buik: schaduwsikkel rechts naast arm/hand
for x,y in ((40,44),(41,44),(41,45),(42,46),(41,46),(42,47),(41,47)): 
    if o[y,x] in (C,S,D): z('broek buiksikkel',x,y,S)
# rechterarm-onderkant als boog (bolle onderarm) i.p.v. rechte rand r47
for x in (45,46,47): z('bovenlichaam armonderkant',x,48,3)
z('bovenlichaam armonderkant',51,48,3); z('bovenlichaam armonderkant',48,47,3)
for x,y in ((47,29),(48,29),(11,27),(12,27)): z('bovenlichaam',x,y,4)   # losse vlekjes (2 px) -> buurtint
z('broek',25,53,S)                                                     # los zwart-bruin stipje r1 in de scheen
z('broek buiksikkel',42,47,4)
opslaan(o,'sprite_r4/sprite.png',8)
import collections
d=o!=r1; print('gewijzigd t.o.v. r1:',d.sum(),'| buiten de opgegeven zones:',sum(1 for y,x in zip(*np.where(d)) if (x,y) not in zone))
cnt=collections.Counter(zone[(x,y)].split(' ')[0] for y,x in zip(*np.where(d)) if (x,y) in zone); print(dict(cnt))
print('silhouet gelijk:',((o>0)==(r1>0)).all(), '| kleuren:',len(set(o.ravel().tolist())-{0}))
