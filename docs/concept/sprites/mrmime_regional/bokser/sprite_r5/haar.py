# Bokser r5: r4 (oog A, benen, schoenen, buik, vuist, arm) + modelhaar van r3 terug, alleen het stuk haar TUSSEN de twee kuiven weg
# (bovenop de kop) -> kale ronde kopbovenkant (huid + omlijning). Kuiven zelf ongewijzigd uit r3/model.
import numpy as np, json
from PIL import Image
from palet import PAL
r4=np.load('../sprite_r4/bokser.npy')
r3=np.zeros((64,64),int); r3[0:63,10:53]=np.load('../sprite_r3/var/oog_A.npy')
f=r4.copy()
f[0:12,20:64]=r3[0:12,20:64]          # kop rij 0-11 terug naar r3 (modelhaar, oog A); uitgestoken vuist (kol 10-17) blijft r4
Z=json.load(open('../sprite_r1/zones.json')); haar=set((y,x+10) for y,x in Z['haar'])
def voor(y,x): return x <= 43-y              # voorste kuif: band van voorhoofd (31-37,4-6) schuin omhoog naar de punt (39-41,0)
def achter(y,x): return (y<=5 and x>=45) or (y==6 and x>=44) or (y>=7 and x>=42)   # achterste kuif + achterhoofd
tussen=[(y,x) for y in range(0,9) for x in range(30,50) if f[y,x] and ((y,x) in haar or y<6) and not voor(y,x) and not achter(y,x)]
for y,x in tussen: f[y,x]=8 if y>=4 else 0
# ronde kop: huidpixel naast transparant -> omlijning; huid tegen de kuiven krijgt schaduw 7
for y,x in tussen:
    if f[y,x]==8:
        nb=[f[y-1,x],f[y+1,x],f[y,x-1],f[y,x+1]]
        if 0 in nb: f[y,x]=1
        elif any(v in (1,2,4) for v in nb): f[y,x]=7
# snijrand van de kuiven dicht: kuifpixel naast transparant of naast het nieuwe kopstuk -> omlijning
T=set(tussen)
for y in range(0,9):
    for x in range(30,50):
        if f[y,x] in (2,4) and (y,x) not in T:
            for yy,xx in ((y-1,x),(y+1,x),(y,x-1),(y,x+1)):
                if (yy,xx) in T: f[y,x]=1; break
np.save('bokser.npy',f)
p=Image.fromarray(f.astype('uint8'),'P'); pal=[v for c in PAL for v in c]; p.putpalette(pal+[0]*(768-len(pal))); p.save('bokser.png',transparency=0)
d=(f!=r4); hz=np.zeros((64,64),bool); hz[0:12,20:64]=True
print('afwijkend van r4:',int(d.sum()),' buiten haarzone (rij 0-11, kol 20+):',int((d&~hz).sum()),' tussenstuk:',len(tussen))
for j in range(0,12): print('%2d '%j+''.join('.' if v==0 else str(v) for v in f[j,28:54]))
