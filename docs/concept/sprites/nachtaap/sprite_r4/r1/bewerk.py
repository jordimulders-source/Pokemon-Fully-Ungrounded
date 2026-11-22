# r1: kale reductie (kaal.npy) -> technische opschoning -> toegestane afwijkingen (bovenlaag) -> anim_front.png + normal.pal
# Elke pixel die niet uit de kale reductie komt staat hieronder met zone en reden.
import sys; sys.path.insert(0,'r1'); from pal import *
from PIL import Image
import numpy as np
g=np.load('r1/kaal.npy').copy()
a=np.asarray(Image.open('r1/natief.png')).astype(int)
L=np.zeros((64,64)); Ln=(0.3*a[...,0]+0.59*a[...,1]+0.11*a[...,2]); L[1:64,0:63]=Ln[0:63,0:63]
log=[]
def zet(x,y,v,zone,reden):
    if g[y,x]!=v: log.append((zone,x,y,int(g[y,x]),v,reden)); g[y,x]=v

# 0) TINTKEUZE kap (geen vormwijziging): de modeltoon L~135 is op de kap (y<=27) 4 i.p.v. 5,
#    zodat de kap zoals de oude sprite 5 (linksboven) + 4 (rest) heeft; anders vallen 176 en 135 samen.
for y in range(19,28):
    for x in range(64):
        if g[y,x]==5 and L[y,x]<150: zet(x,y,4,'kap-tint','modeltoon 135 -> 4 (oude kap)')

# 1) TECHNISCH: halve randcellen (grijs in het model, raster liep daar half over lijn en wit)
zet(16,24,2,'oor L','halve randcel; selout aan de lichtkant (boven)')
zet(17,24,2,'oor L','halve randcel; selout aan de lichtkant (boven)')
zet(38,24,2,'oor R','halve randcel; bovenrand selout zoals buren (39,24),(40,24)')
zet(31,30,9,'oog R','grijze antialiascel in de oogrand (model: lijnhoek) -> oogrand 9')
# 2) TECHNISCH: buitenlijn lichtkant = gekleurde selout, geen lichte tint op de rand
zet(22,21,3,'kop boven','randpixel had 4 -> selout 3 zoals de rest van de bovenrand')
zet(19,23,3,'kop boven','randpixel had 4 -> selout 3')
zet(18,24,3,'kop boven','randpixel had 4 -> selout 3')
zet(15,26,2,'oor L','randpixel 3 tussen 2-en -> 2 (gelijke selout)')
zet(18,37,3,'kaak L','randpixel had 4 -> selout 3 (zoals (17,36))')
zet(19,38,3,'kaak L','randpixel had 4 -> selout 3')
zet(20,49,2,'arm L','randpixel had 5 -> selout 2 (zoals erboven/eronder)')
# 3) TECHNISCH: geen zwart en donkerlila om en om (bovenrand rechts was 2,1,1,2,2,1)
zet(29,20,2,'kop boven','1 -> 2: bovenrand loopt 3..2 door tot de zijkant, zwart pas vanaf (33,21)')
zet(30,20,2,'kop boven','idem')
# 4) TECHNISCH: onderrand kop, lichte tint op de buitenrand
zet(21,39,1,'kaak L','randpixel 4 boven transparant -> omlijning 1 (schaduwkant onder)')
# 5) TECHNISCH: staartkrul, lichte tint grensde aan het gat
zet(47,37,2,'staart','4 grensde aan het gat in de spiraal -> lijn 2 (krulpunt dicht)')

# 6) TECHNISCH: staartsteel had lichte 5 op de buitenrand (geen selout); 3 sluit aan op de middenkolom van de staart eronder
for y in (40,41,42,43): zet(44,y,3,'staart','5 op de buitenrand -> 3')
zet(44,39,4,'staart','losse 5 tussen 4 en 3 -> 4')
# 7) TECHNISCH: ruis (tintvlakje van 1 px)
zet(25,41,3,'nek','losse 4 in de 3-band onder de kin -> 3')
zet(23,50,5,'been L','losse 4 tussen 5-en -> 5')
zet(21,36,7,'snuit','losse 6 in creme -> 7')
zet(36,26,2,'oor R','verbindt de losse lijnpixel (36,27) met (37,25): taps oorlijntje')

# === TOEGESTANE AFWIJKINGEN (bovenlaag) ===
# A) Streep tussen de ogen: 3 px (4 lichtkant + 3 kern), volgt de kopronding (boven iets rechts, op ooghoogte
#    1 px naar links, onderaan weer naar rechts, schuine onderkant); vrijgekomen ruimte = creme 7.
streep={24:{23:3,24:3}, 25:{22:4,23:3,24:3},
        26:{22:4,23:3,24:3}, 27:{22:4,23:3,24:3}, 28:{22:4,23:3,24:3},
        29:{21:4,22:3,23:3}, 30:{21:4,22:3,23:3}, 31:{21:4,22:3,23:3}, 32:{21:4,22:3,23:3}, 33:{21:4,22:3,23:3},
        34:{22:4,23:3}}
for y in range(26,35):
    for x in range(20,26):
        if g[y,x] in (4,5) and x not in streep[y]: zet(x,y,7,'streep','vrijgekomen -> creme gezichtsschijf')
for y,row in streep.items():
    for x,v in row.items(): zet(x,y,v,'streep','nieuwe streep (2 violette tinten)')
# B) rechteroog: in het model al rond (schuine hoeken op (26,29),(31,29),(26,35),(31,35)); niets te doen.

np.save('r1/r1.npy',g)
# export
full=np.zeros((128,64),'uint8'); full[:64]=g; full[64:]=g
im=Image.fromarray(full,'P'); flat=[]
for c in PAL: flat+=list(c)
im.putpalette(flat); im.save('r1/anim_front.png',transparency=0)
open('r1/normal.pal','w').write('JASC-PAL\r\n0100\r\n16\r\n'+''.join('%d %d %d\r\n'%c for c in PAL))
from collections import Counter
c=Counter(z for z,*_ in log)
for z,x,y,o,n,r in log: print(z,(x,y),o,'->',n,r)
print(dict(c),'totaal',len(log))
