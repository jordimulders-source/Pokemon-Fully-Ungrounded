# Blobfish r3: r2 + (1) lipband = lipmasker uit het model, (2) ogen leesbaar op de modelplek, (3) borstvin zonder krul.
# Silhouet bevroren (assert). Elke wijziging -> afwijkingen_r3.txt.
import numpy as np; from PIL import Image; from collections import Counter
R2=Image.open('r2.png'); r2=np.asarray(R2).astype(int); pal=R2.getpalette()[:3*14]; PALA=np.array(pal).reshape(-1,3)
OY,OX,ymin,xmin,y0,x0=np.load('kaal_info.npz')['geo']
n=np.asarray(Image.open('natief.png').convert('RGB')).astype(int); L=n@[0.299,0.587,0.114]
R,G=n[...,0],n[...,1]; LIPT=(L>=100)&(L<=200)&(R>=180)&(R-G>=60)       # liptint-cluster (zelfde als lipmasker.py)
def blok(x,y):
    ny=OY+4*(y-y0+ymin); nx=OX+4*(x-x0+xmin); sl=(slice(ny,ny+4),slice(nx,nx+4)); return n[sl].reshape(-1,3),L[sl].ravel(),LIPT[sl].ravel()
def dichtst(c,idx): return min(idx,key=lambda i:((PALA[i]-c)**2).sum())
o=r2.copy(); log=[]
def zet(x,y,v,stap):
    if o[y,x]!=v: log.append((stap,x,y,o[y,x],v)); o[y,x]=v
m=r2>0; pad=np.pad(m,1); rand=m&~(pad[:-2,1:-1]&pad[2:,1:-1]&pad[1:-1,:-2]&pad[1:-1,2:])

# ---- 1 lipband: elke maskerpixel (lipmasker.npy) die niet op de rand ligt en niet op de mondlijn -> liptoon (9/10/11)
#  dichtst bij het gemiddelde van de liptint-pixels in zijn blok. Mondlijn = 1 px zwart, pad gemeten in r2
#  ((8,46) (9,47) (10,48) (11,48) (12..19,49); per blok 3-7 donkere px). Het masker loopt rechts tot x20 (onder het nabije oog).
M=np.load('lipmasker.npy')
MOND={(8,46),(9,47),(10,48),(11,48)}|{(x,49) for x in range(12,20)}
for y,x in zip(*np.where(M)):
    if rand[y,x] or (x,y) in MOND: continue
    b,l,lt=blok(x,y); zet(x,y,dichtst(b[lt].mean(0),(9,10,11)),'L')
for x,y in MOND: zet(x,y,1,'L')

# ---- 2 ogen (2x2 op de modelplek, model: glanspuntje linksboven, pupil rechtsboven, wit sikkeltje onder)
#  nabij: (19,45) 3 donker + 1 wit glanspx -> wit; (20,45) 7 donker -> pupil zwart; (19,46) 5 licht -> wit; (20,46) 12 wit -> wit
#  ver:   (9,41) ring + glanspuntje -> wit; (10,41) 3 donker -> pupil zwart; (9,42) (10,42) 3-4 wit -> wit (= kale reductie r1)
#  Wit = oogwit (219,203,203), gemeten (211,199,200). Zo is elk oog 3 wit + 1 zwart tegen het donkere lijf.
for x,y in ((19,45),(19,46),(20,46),(9,41),(9,42),(10,42)): zet(x,y,12,'O')
for x,y in ((20,45),(10,41)): zet(x,y,1,'O')

# ---- 3 borstvin: krul weg. Straal A ((34,42) (36,41), 5 en 8 straalpx) ligt parallel vlak onder de bovenrand en vormt
#  met de bovenrand en straal B de "@"-krul -> terug naar de lijftint van r1 op die plek (4). Straal B recht vanaf de
#  aanhechting: (32,44) 4 en (33,43) 3 straalpx -> straaltint 11, zodat B van de aanhechting naar de rand loopt.
#  Overige straalpixels van r2 die niet op bovenrand of stralen B/C/D liggen: (37,42) (G, losse glans naast de rand) -> 4.
for x,y in ((34,42),(36,41),(37,42)): zet(x,y,4,'S')
for x,y in ((32,44),(33,43)): zet(x,y,11,'S')

assert ((o>0)==(r2>0)).all(), 'silhouet gewijzigd'
Z={'gezicht (ogen+lippen)':(6,40,23,55),'borstvin':(26,38,42,56)}
def zone(x,y):
    for nm,(a,b,c,d) in Z.items():
        if a<=x<c and b<=y<d: return nm
    return 'rest'
P=list(pal); p=Image.fromarray(o.astype('uint8'),'P'); p.putpalette(P+[0]*(768-len(P))); p.save('blobfish_r3.png',transparency=0)
print(Counter((s,zone(x,y)) for s,x,y,_,_ in log),'totaal',len(log),'kleuren',len(set(o.ravel()))-1)
open('afwijkingen_r3.txt','w').write('\n'.join(f'{s}\t({x},{y})\t{a}->{b}\t{zone(x,y)}' for s,x,y,a,b in log)+'\n')
for y in range(39,54): print('%2d '%y+''.join(('%x'%o[y,x]) if o[y,x] else '.' for x in range(6,40)))
