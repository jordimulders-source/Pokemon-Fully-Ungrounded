# r2 = r1 + benoemde reparaties (alleen tinten binnen bestaande vlakken; alpha-diff 0 met r1)
import sys; sys.path.insert(0,'r1'); from pal import *
from PIL import Image
r1=np.array(Image.open('r1/anim_front.png'))[:64].astype(int); g=r1.copy(); log=[]
def zet(x,y,v,zone,reden):
    assert g[y,x]!=0, (x,y)
    if g[y,x]!=v: log.append((zone,x,y,int(g[y,x]),v,reden)); g[y,x]=v
# 1a) KOP: sikkelschaduw 3 langs rechter- en onderkant (1 px boven, 2 px lager), licht linksboven blijft
kop={22:[33],23:[33,34],24:[34],25:[35,36],26:[35],27:[35],28:[35],
     31:[39,40],32:[37,38,39],33:[35,36],34:[35,36],35:[35,36],36:[34,35],37:[33,34],38:[30,31],39:[29]}
for y,xs in kop.items():
    for x in xs: zet(x,y,3,'kop sikkel','4 -> 3 (schaduwkant)')
# oor R: rechterrand in schaduw
for x,y in [(41,26),(41,27),(41,28),(41,29),(40,30),(41,30)]: zet(x,y,3,'oor R sikkel','4 -> 3')
# lichte wangplek (5) rechts naast de snuit lag in de schaduwkant: -> 4
for x,y in [(33,34),(32,35),(33,35),(31,36),(32,36)]: zet(x,y,4,'kop wang','5 in schaduwkant -> 4')
# 1b) LIJF: nabije arm rechterhelft en romp rechterzijde een tint donkerder
for y in range(42,51): 
    if g[y,33]==5: zet(33,y,4,'arm R','rechterkolom 5 -> 4')
for x,y in [(36,47),(37,47),(36,48),(37,48),(36,49)]: zet(x,y,3,'romp R','4 -> 3')
# verre arm (links) iets donkerder dan de lichtkant van de nabije arm
for x,y in [(22,44),(22,45),(22,46),(21,47),(21,48)]: zet(x,y,4,'arm L','5 -> 4')
# gezichtsschijf: smalle creme schaduw (6) langs rechter-/onderrand
for x,y in [(32,25),(33,26),(33,27),(34,28),(34,29),(34,30),(34,31),(34,32),(33,33),(32,34),(31,35),(30,36),(29,37),(30,37)]:
    zet(x,y,6,'gezichtsschijf','7 -> 6 rand rechts/onder')
# buik: sikkel rechts (x30) en onder (rij 50-51) bestond al in het model; niets gewijzigd
# 2) LINKERVOET: dambord D/7 -> verticale teenlijn op x20
zet(20,53,13,'voet L','7 -> D (teenlijn)'); zet(19,53,7,'voet L','D -> 7 (teen)')
# 3) STREEP: overgang y28->y29 zachter: rechterrand op y28 in de lichte streeptint
zet(24,28,4,'streep','3 -> 4 (trapje zachter)')
np.save('r2/r2.npy',g)
full=np.zeros((128,64),'uint8'); full[:64]=g; full[64:]=g
im=Image.fromarray(full,'P'); flat=[]
for c in PAL: flat+=list(c)
im.putpalette(flat); im.save('r2/anim_front.png',transparency=0)
open('r2/normal.pal','w').write(open('r1/normal.pal').read())
print('alpha-diff met r1:',int(((g>0)!=(r1>0)).sum()))
from collections import Counter
for z,n in Counter(z for z,*_ in log).items(): print(z,n)
print('totaal',len(log))
