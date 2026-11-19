# Palpaca r4: vanaf r3B. (1) palet gemeten in het model (zie NOTITIES), (2) kopbinnenkant overgenomen uit het model
# (klasse per spritepixel uit px.py: gem. helderheid >=236 ->2, >=216 ->3, >=196 ->4, >=165 ->5, anders 6), (3) Jordi's punten als handreparaties.
import numpy as np; from PIL import Image
from px import meet
R3B=np.array(Image.open('../../r3/palpaca_B.png'))
pal=[]
for l in open('../normal.pal').read().split('\n')[3:19]: pal+=[int(v) for v in l.split()]
def save(a,naam):
    im=Image.fromarray(a.astype('uint8'),'P'); im.putpalette(pal); im.save(naam,transparency=0)
# alleen nieuwe kleuren op r3B (om het kleurverschil los te tonen)
save(R3B,'../r3B_nieuwpalet.png')
a=R3B.copy()
def klas(v): return 2 if v>=236 else 3 if v>=216 else 4 if v>=196 else 5 if v>=165 else 6
H,W=a.shape
def rand(x,y): return any(a[y+dy,x+dx]==0 for dy in(-1,0,1) for dx in(-1,0,1))
kopmodel=[]
for y in range(15,62):
    for x in range(14,50):
        if a[y,x] in (11,15) and not rand(x,y):
            a[y,x]=11 if meet(x,y)[0]>=140 else 15; continue
        if a[y,x] in (2,3,4,5) and not rand(x,y):
            a[y,x]=klas(meet(x,y)[0]); kopmodel.append((x,y))
S={}
def zet(lst,v):
    for p in lst: S[p]=v
# oog: 2 px korter onderaan (rij 29 weg), glans + donker + bruine onderkant
zet([(24,26)],2); zet([(25,26),(24,27),(25,27)],1); zet([(24,28),(25,28)],6); zet([(24,29),(25,29)],4)
# verre oog op de modelplek (18,26)(18,27) + (19,26) (model 161/27)
zet([(18,26),(18,27)],1); zet([(19,26)],6)
# oren: aanzet linkeroor (model rij 18-19 x19-22) en rechteroor (model x28-31 rij 18-22)
zet([(20,18)],6); zet([(21,18)],5); zet([(19,19)],6); zet([(20,19),(21,19)],5)
zet([(29,18)],5); zet([(28,19)],5); zet([(29,20)],6); zet([(29,21)],6); zet([(30,21)],5); zet([(30,22),(31,22)],6); zet([(29,22)],5)
# snuit: neusgat (19,29), mond (18,31)(19,31) + opkrul (21,31), onderkant snuit 4
zet([(19,29)],6); zet([(18,31),(19,31),(21,31)],6); zet([(20,31)],4)
# staartaanzet: lijn onder de staart (model x41-42 rij 40, x42 rij 41) en boven (38,38)
zet([(38,38)],5); zet([(41,40)],6); zet([(42,41)],6)
# voorste achterpoot: schaduw bovenin (model rij 50-53 x35-39)
zet([(35,50),(36,50),(39,50)],5); zet([(37,50),(38,50)],4)
zet([(36,51),(38,51)],5); zet([(37,51)],4); zet([(39,51)],6); zet([(37,52),(38,52)],5); zet([(38,53)],5); zet([(37,53)],4)
# nek niet aanraken (Jordi: 'Nek is prima'): r3B terug op y33-36, x21-29
for y in range(33,37):
    for x in range(21,30): a[y,x]=R3B[y,x]
for (x,y),v in S.items():
    assert a[y,x]!=0,(x,y); a[y,x]=v
import sys
extra=eval(open('extra.txt').read()) if True else {}
for (x,y),v in extra.items(): a[y,x]=v
assert ((a>0)!=(R3B>0)).sum()==0
save(a,'../palpaca.png')
print('kleuren',len(np.unique(a)),'anders dan r3B',(a!=R3B).sum())
