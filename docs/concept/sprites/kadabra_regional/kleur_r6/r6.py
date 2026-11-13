# r6 = r5 met de ruit 1 px naar rechts (Jordi). r5 (Claude): op r2. Ruit op het voorhoofd (Jordi: "Maak er maar een ruit van", kleiner, op de modelplek), oog_1 (alleen pupil),
# kaart = de goedgekeurde kaart van de charlatan-Alakazam (rechterkaart, gespiegeld zodat de bovenkant naar links helt zoals in het model, licht opnieuw van linksboven).
import sys
R=[list(l.rstrip('\n').ljust(64,'.')[:64]) for l in open('../kleur_r2/raster.txt')][:64]
def row(y,x0,s):
    for k,ch in enumerate(s):
        if ch!='=': R[y][x0+k]=ch
V=sys.argv[1] if len(sys.argv)>1 else 'A'
# ogen (oog_1)
R[21][22]='d'; R[22][22]='w'; R[22][28]='w'; R[22][29]='o'
# klaver weg
R[20][27]='b'; R[21][26]='b'; R[21][25]='a'; R[18][25]='a'; R[18][26]='b'; R[19][25]='a'; R[19][26]='b'; R[20][24]='a'; R[20][25]='a'; R[20][26]='b'
if V=='A':      # ruit 3 breed x 5 hoog
    row(17,26,'t'); row(18,25,'trr'); row(19,25,'rrr'); row(20,25,'rrs'); row(21,26,'s')
else:           # ruit 3 breed x 4 hoog... variant B: 5x5
    row(17,26,'t'); row(18,25,'trr'); row(19,24,'trrrs'); row(20,25,'rrs'); row(21,26,'s')
# kaart
for y in range(16,25):
    for x in range(0,8): 
        if not (y==24 and x>=5): R[y][x]='.'
row(16,4,'d')
row(17,2,'ddwd')
row(18,0,'ddwwwwo')
row(19,0,'dwwwowo')
row(20,0,'dwwooowo')
row(21,1,'dwoooao')
row(22,1,'dwwowaao')
row(23,2,'ooawao')
row(24,2,'ooa')
row(25,2,'.ooo')
open('raster_A.txt' if V=='A' else 'raster_B.txt','w').write('\n'.join(''.join(r) for r in R)+'\n')
