# r4 = r3 + 4 reparaties uit r3/KEURING.md -> picaraio.png, normal.pal, picaraio_8x.png, r4.npy
import numpy as np; from PIL import Image
PAL=[(152,208,160),(24,20,16),(226,150,96),(192,110,60),(142,74,42),(250,242,214),(230,210,166),(196,170,124),
     (232,82,74),(204,196,192),(142,132,130),(78,70,70),(252,226,96),(212,170,52),(255,255,255),(98,48,26)]
r3=np.load('_tmp/r3.npy'); o=r3.copy(); log={}
def zet(naam,lst):
    n=0
    for x,y,v in lst:
        if o[y,x]!=v: o[y,x]=v; n+=1
    log[naam]=log.get(naam,0)+n
# 1 kuifbogen (keurdersmeting; model-lijn ligt op de grens rij 1/2 resp. 4/5, registratieverschil 0,3 px, zie rapport)
zet('1 kuif',[(x,2,0) for x in range(27,32)]+[(x,1,1) for x in range(27,32)]+[(23,3,0),(23,2,1),(34,3,0),(34,2,1),(36,4,0),(36,3,1)]
   +[(24,5,0)]+[(x,5,0) for x in range(28,34)]+[(x,4,1) for x in range(28,34)]+[(36,6,0),(36,5,1)])
#   (37,6) blijft: (37,5) zou (38,7) niet raken; model x37 = rij 5,85-6,2 in de keurdersregistratie
# 2 buiksikkel taps: per rij c-breedte vanaf de bruine rand rechts, rest C (selout k links blijft)
W={**{y:1 for y in range(23,28)},**{y:2 for y in range(28,35)},**{y:3 for y in range(35,39)},**{y:4 for y in range(39,41)}}
L=[]
for y,w in W.items():
    xs=[x for x in range(11,32) if o[y,x] in (5,6,7) and not (o[y,x-1]==0 or (o[y,x]==7 and o[y,x-1] in (0,1) and x<16))]
    xs=[x for x in xs if o[y,x]!=7 or x>16]
    r=max(xs)
    for x in xs: L.append((x,y,6 if x>r-w else 5))
L+=[(x,41,6) for x in range(19,31)]
L+=[(x,42,6 if x<28 else 7) for x in range(22,31)]+[(x,43,6 if x<26 else 7) for x in range(21,31)]
zet('2 buik',L)
# 3 binnenlijnen onderste vleugelveren zwart -> selout 15 (u); pixels die aan achtergrond grenzen blijven zwart
P=[(30,33),(31,33),(31,34),(32,34),(33,34),(32,35),(33,35),(34,35),(35,33),(36,34),(36,35),(37,35),(38,35),(39,33),(40,33),(40,34),(41,34),(42,34)]
zet('3 binnenlijnen',[(x,y,15) for x,y in P if o[y,x]==1 and all(o[y+dy,x+dx]!=0 for dx,dy in ((1,0),(-1,0),(0,1),(0,-1)))])
# 4 onderrand onderste slagpen schuin naar de punt (57,26)
zet('4 slagpen',[(53,28,0),(54,28,0),(55,28,0),(53,27,1),(54,27,1),(55,27,1)])
np.save('r4.npy',o)
p=Image.fromarray(o.astype('uint8'),'P'); p.putpalette([v for c in PAL for v in c]+[0]*(768-48)); p.save('picaraio.png',transparency=0)
open('normal.pal','w').write('JASC-PAL\r\n0100\r\n16\r\n'+''.join('%d %d %d\r\n'%c for c in PAL))
rgb=np.array(PAL,'uint8')[o]; Image.fromarray(rgb).resize((512,512),0).save('picaraio_8x.png')
for k,v in log.items(): print('%-16s %3d px'%(k,v))
print('totaal r3->r4',int((o!=r3).sum()))
