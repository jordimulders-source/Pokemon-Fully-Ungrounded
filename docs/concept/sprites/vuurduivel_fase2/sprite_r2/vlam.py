# vlam.py: handvlam en staartvlam opnieuw ingedeeld in de banden van het model (geen tekenwerk).
# Silhouet blijft dat van r1. Per spritepixel: gemiddelde vuurhitte van een 4x4-venster natieve modelpixels rond de 2x2-cel
# (geel/crème 4, oranje 3, oranjerood 2, rood 1, donkerrood 0; niet-vuur telt niet) -> band. Dan: vlekjes < 3 px gaan op
# in de meest voorkomende buurband; buitenrand rood, aan de schaduwkant (rechts) donkerrood, zoals de rand in het model.
import numpy as np
from collections import Counter
CH='.#dgHhBcCRrOAY'
R=[list(r.rstrip('\n')) for r in open('raster_r1.txt')]
R0=[r[:] for r in R]
K=np.load('natief_klas.npy')
HEAT={13:4,8:4,12:3,11:2,14:2,10:1,9:0}
BAND={4:'Y',3:'A',2:'O',1:'r',0:'R'}
DONK={'Y':'A','A':'O','O':'r','r':'R','R':'R'}
FIRE=set('YAOrR')
import sys
SIL='--sil2' in sys.argv   # proef: silhouet >=2 van 4 (verworpen: tongen vallen uiteen in losse pixels)
ZONES={'hand':(4,19,13,28),'staart':(50,33,60,45)}   # vonkjes (9,17),(9,18),(10,18) vallen buiten de handzone
def heat(sx,sy):
    nx=62+(sx-4)*2; ny=6+(sy-5)*2
    w=K[ny-1:ny+3,nx-1:nx+3].ravel()
    h=[HEAT[k] for k in w if k in HEAT]
    return np.mean(h) if h else None
E=[]
VONK={(9,17),(9,18),(10,18)}
def nfig(sx,sy):
    nx=62+(sx-4)*2; ny=6+(sy-5)*2; f=K[ny:ny+2,nx:nx+2].ravel(); return (f>0).sum(), sum(1 for k in f if k in HEAT)
for nm,(x0,y0,x1,y1) in ZONES.items():
    # silhouet van de vlam: r1 gebruikte voor vuur 'figuur vanaf 1 van 4' (vlam zwol op, zijvonken plakten aan de vlam);
    # nu dezelfde regel als de rest van de sprite: figuur bij >=2 van 4, alleen op vuur- of achtergrondpixels van r1
    if SIL:
        for y in range(y0,y1+1):
            for x in range(x0,x1+1):
                if (x,y) in VONK or not (R[y][x] in FIRE or R[y][x]=='.'): continue
                n,nv=nfig(x,y)
                if n>=2 and nv>=1: 
                    if R[y][x]=='.': R[y][x]='O'
                elif R[y][x] in FIRE: R[y][x]='.'
    cel=[(x,y) for y in range(y0,y1+1) for x in range(x0,x1+1) if R[y][x] in FIRE]
    new={}
    for x,y in cel:
        h=heat(x,y); new[(x,y)]=BAND[int(np.clip(np.floor(h+0.5),0,4))] if h is not None else R[y][x]
    def vlekken():
     for it in range(3):
         seen=set()
         for p in cel:
             if p in seen: continue
             c=[p]; st=[p]; seen.add(p)
             while st:
                 a,b=st.pop()
                 for q in ((a+1,b),(a-1,b),(a,b+1),(a,b-1)):
                     if q in new and q not in seen and new[q]==new[p]: seen.add(q); st.append(q); c.append(q)
             if len(c)>=3: continue
             nb=Counter(new[q] for a,b in c for q in ((a+1,b),(a-1,b),(a,b+1),(a,b-1)) if q in new and new[q]!=new[p])
             if nb:
                 for q in c: new[q]=nb.most_common(1)[0][0]
    vlekken()
    # rand: zoals het model een rode buitenrand, donkerrood aan de schaduwkant (achtergrond rechts), anders rood;
    # de vonkjes (los van de vlam, buiten de zone) blijven
    for (x,y),v in list(new.items()):
        if any(R[y+dy][x+dx]=='.' for dx,dy in ((1,0),(-1,0),(0,1),(0,-1))):
            new[(x,y)]='R' if R[y][x+1]=='.' else 'r'
    for (x,y),v in new.items():
        R[y][x]=v
E=[(x,y,R0[y][x],R[y][x]) for y in range(64) for x in range(64) if R0[y][x]!=R[y][x]]
open('raster_vlam%s.txt'%('_sil2' if SIL else ''),'w').write('\n'.join(''.join(r) for r in R)+'\n')
open('vlam_wijzigingen%s.txt'%('_sil2' if SIL else ''),'w').write(''.join('(%d,%d) %s->%s\n'%e for e in E))
print(len(E),'vlampixels anders')
