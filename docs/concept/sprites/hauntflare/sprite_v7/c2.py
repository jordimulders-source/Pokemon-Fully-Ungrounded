# C2 = kandidaat C + keuringspunten 1-5 (alleen herkleuren en de mond als geheel 2 px naar links)
import numpy as np, json
from PIL import Image
from scipy import ndimage
from gezicht import st1, a6, F, PAL, bewaar, D
a=np.array(Image.open(D+'/kandidaat_C.png')).astype(int); log=[]
def zet(x,y,v,why):
    log.append([x,y,int(a[y,x]),v,why]); a[y,x]=v
# 1 losse vlekjes in de glans
zet(22,22,9,'1'); zet(23,25,8,'1')
# 4 glansstreep
for p in [(19,20),(19,21),(19,22),(20,20)]: zet(*p,9,'4')
# 2 linker mondhoek: één schuine zwarte lijn
for p in [(21,33),(21,34),(21,35),(22,35)]: zet(*p,7,'2')
zet(23,35,1,'2')
# 3 mond 2 px naar links: mondpixels (niet-bol) + ingesloten tanden in x21-35, y31-38
box=np.zeros((64,64),bool); box[31:39,21:36]=True
mond=box & ~np.isin(a,[6,7,8,9])
mond=ndimage.binary_fill_holes(mond)&box
# tanden die aan de rand van de mond open liggen (V-tanden tussen lipstukken) horen er ook bij:
# bolpixels in de box die links én rechts in dezelfde rij een mondpixel hebben en eronder een mondpixel
for y in range(31,39):
    for x in range(21,36):
        if not mond[y,x] and mond[y,:x].any() and mond[y,x+1:36].any() and mond[y+1:39,x].any(): mond[y,x]=True
ys,xs=np.nonzero(mond); oud=a.copy()
for y,x in zip(ys,xs): a[y,x]=st1[y,x] if F[y,x] or True else a[y,x]
for y,x in zip(ys,xs): a[y,x-2]=oud[y,x]
vrij=[(int(x),int(y)) for y,x in zip(ys,xs) if not mond[y,x+2] if x+2<64]
log.append(['mond -2',int(len(ys)),'px verschoven; vrijgekomen uit stap1:',vrij])
# opruimen: vrijgekomen pixels die met hun eigen tint een vlakje < 3 px vormen -> meest voorkomende boltint van de buren
lab={}
for k in (6,7,8,9):
    L,n=ndimage.label(a==k,structure=np.ones((3,3)))
    for (x,y) in vrij:
        if a[y,x]==k and (L==L[y,x]).sum()<3:
            nb=[a[yy,xx] for yy in range(y-1,y+2) for xx in range(x-1,x+2) if (yy,xx)!=(y,x) and a[yy,xx] in (6,7,8,9) and a[yy,xx]!=k]
            if nb: lab[(x,y)]=max(set(nb),key=nb.count)
for (x,y),v in lab.items(): zet(x,y,int(v),'opruimen vrijgekomen')
im=bewaar(a,D+'/kandidaat_C2.png')
json.dump(log,open(D+'/c2_log.json','w'))
print(len(ys),'mondpx; vrij',vrij)
