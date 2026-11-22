# wijzig_r6.py: r6 = r5 (vorm bevroren) + kleurronde keuring_r5 MOET 1-10 -> raster_r6.txt ; wijzigingen_r6.txt
R=[list(r.rstrip('\n').replace('h','X').replace('p','X')) for r in open('../sprite_r5/raster_r5.txt')]  # MOET 1/8: h en p -> X (samengevoegd)
E={}
def zet(x,y,c,reden):
    assert R[y][x] not in '.', (x,y)
    if R[y][x]!=c: E[(x,y)]=(R[y][x],c,reden); R[y][x]=c
def rij(y,x0,s,reden):
    for i,c in enumerate(s):
        if c!='?': zet(x0+i,y,c,reden)
# MOET 2 kop: l-vlak breedst bovenaan, smaller naar onder; glans op de bolling; wangbolling links
for x,y in [(16,29),(17,29),(21,29),(22,29),(22,28),(17,28)]: zet(x,y,'m','kop: l-vlak smaller naar onder (bolling)')
for x,y in [(20,25),(21,25),(20,26),(21,26)]: zet(x,y,'g','kop: glans op de bolling van het voorhoofd')
for x,y in [(17,35),(17,36)]: zet(x,y,'l','kop: kleine wangbolling links')
# MOET 3 borst: bolling linksboven met glans, d-sikkel langs rechts en onder
rij(43,22,'lllll','borst: bolling linksboven')
rij(44,22,'lggl','borst: bolling + glans'); rij(45,23,'lll','borst: bolling')
rij(44,28,'dd','borst: sikkel rechts'); rij(45,29,'d','borst: sikkel rechts'); rij(46,29,'d','borst: sikkel rechts')
rij(47,29,'d','borst: sikkel rechts'); rij(48,28,'dd','borst: sikkel rechtsonder'); rij(49,27,'dd','borst: sikkel onder')
# MOET 4 armen
rij(44,21,'l','nabije arm: bovenrij licht'); rij(45,20,'lm','nabije arm: boven licht, onder m')
rij(46,17,'lmm','nabije hand: linksboven licht'); 
rij(45,36,'mdd','verre hand: onder donker'); rij(46,37,'d','verre hand: onder donker')
# MOET 5 linkeroor: lichtere voorrand, donker binnenoor
zet(13,31,'l','linkeroor: lichte voorrand'); zet(13,32,'m','linkeroor: voorrand')
# MOET 6 broek: twee dijen (t=k bolling, B plooi/midden, b sikkel rechts en onder)
zet(32,47,'b','broek: schaduwkant rechts')
rij(48,30,'BBbb','broek: taille rechts in schaduw')
rij(49,29,'BBBbbb','broek: rechterdij linksboven licht, rechts sikkel')
rij(50,28,'BBBBBbb','broek: t rechts in rij 50 -> B (schaduwkant)')
rij(51,20,'kkkkkkBBBkkkBbb','broek: linkerdij t, kruis B, rechterdij linksboven t, sikkel b')
rij(52,20,'kkkkkBBBBkkkBbb','broek: linkerdij bolling t, kruis B, rechterdij')
rij(53,19,'kkkkkBB??BkkBBbb','broek: linkerdij t, plooi B, rechterdij midden B, sikkel b')
rij(54,20,'BBBBb','broek: linkerdij onder B, b tegen de rafels'); rij(54,29,'BBBBbbb','broek: rechterdij onder, sikkel b')
rij(55,20,'b','broek: rafel onder'); rij(55,22,'BBb','broek: rafel onder'); rij(55,30,'BBBbb','broek: rafel onder, sikkel')
zet(25,56,'b','broek: rafel onder'); rij(56,31,'Bbb','broek: rafel onder, sikkel')
# MOET 7 poten/hoeven: links B, rechts b; hoef één vlak
zet(25,57,'b','linkerpoot: schaduwkant'); zet(24,58,'b','linkerpoot: schaduwkant'); zet(21,59,'k','linkerhoef: één licht vlak (hoef lichter dan de poot)'); zet(22,59,'k','linkerhoef: één licht vlak')
zet(36,57,'b','rechterpoot: schaduwkant'); zet(37,58,'b','rechterpoot: schaduwkant')
rij(59,35,'kkB','rechterhoef: één vlak'); rij(60,35,'kkB','rechterhoef: streep weg'); rij(61,35,'kkB','rechterhoef: één vlak')
# MOET 9 staartstam: licht van boven
rij(50,36,'dddddd','staartstam: bovenrij licht'); 
for x,y in [(42,49),(43,48),(44,47)]: zet(x,y,'d','staartstam: bovenkant licht')
# MOET 10 pijlpunt: geel 2 breed
zet(45,38,'Y','pijlpunt: geel 2 px breed')
# KAN mond: bovenste mondrij donkerrood (keelschaduw)
rij(37,21,'RRR','mond: keelschaduw')
# MOET 8 vlammen: middentint X op de r/O-grens (O met r links of onder -> X), tongen rechts van de kop als X
H=[(x,y) for y in range(12,31) for x in range(10,42)]+[(x,y) for y in range(35,46) for x in range(40,52)]
naar=[]
for x,y in H:
    if R[y][x]=='O' and (R[y][x-1] in 'rR' or R[y+1][x] in 'rR'): naar.append((x,y))
for x,y in naar: zet(x,y,'X','vlam: middentint op de r/O-grens (r -> X -> O -> Y)')
for x,y in [(32,25),(33,25),(35,25),(35,26),(35,27),(34,27),(37,26),(37,27)]: zet(x,y,'X','vlam rechts: tongen in de middentint, r eromheen')
open('raster_r6.txt','w').write('\n'.join(''.join(r) for r in R)+'\n')
with open('wijzigingen_r6.txt','w') as f:
    for (x,y),(a,b,r) in sorted(E.items(),key=lambda t:(t[0][1],t[0][0])): f.write('(%d,%d) %s->%s  %s\n'%(x,y,a,b,r))
print(len(E),'pixels gewijzigd t.o.v. r5 (plus h/p -> X)')
