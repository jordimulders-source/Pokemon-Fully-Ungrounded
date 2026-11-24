# r3 stap 1: krans opnieuw opbouwen met één schone ronde bolletje-vorm (opdracht: vorm van een rond Gen 3-Claydol-oog,
# regelmatige pixelcirkel). Middelpunten = die van r2 (uit het model, al op .5: 8x8 valt er precies op).
import numpy as np
from basis import S2, KOP, V2, KRS
# O=omlijning, 2=hooglicht, 3=basis, 5=sikkel, P=pupil(9)
VORM={
 8:{'.':["..OOOO..",
         ".O2233O.",
         "O222333O",
         "O233P35O",
         "O333335O",
         "O333355O",
         ".O3555O.",
         "..OOOO.."],
    '-':["..OOOO..",
         ".O2233O.",
         "O222333O",
         "O23PPP5O",
         "O333335O",
         "O333355O",
         ".O3555O.",
         "..OOOO.."]},
 7:{'.':["..OOO..",
         ".O223O.",
         "O22333O",
         "O23P35O",
         "O33335O",
         ".O355O.",
         "..OOO.."],
    '-':["..OOO..",
         ".O223O.",
         "O22333O",
         "O2PPP5O",
         "O33335O",
         ".O355O.",
         "..OOO.."]}}
def asset(rows):
    m={'.':0,'O':10,'2':2,'3':3,'5':5,'P':9}
    return np.array([[m[c] for c in r] for r in rows])
def bouw_krans(S, maat=8, schuif=None, wegr=5.0):
    S=S.copy(); H,W=S.shape; yy,xx=np.mgrid[0:H,0:W]
    stafm=(V2=='staf')|np.roll(V2=='staf',1,1)|np.roll(V2=='staf',-1,1)
    beschermd=KOP|(V2=='punt')|stafm|(yy>=39)
    weg=np.zeros((H,W),bool)
    for n,(cx,cy,t) in KRS.items(): weg|=(np.hypot(xx-cx,yy-cy)<=wegr)
    weg&=~beschermd&(S>0)
    S[weg]=0; plek={}; vlak=np.zeros((H,W),int)   # vlak: welk bolletje (index+1) een pixel heeft
    for k,n in enumerate(KRS):
        cx,cy,t=KRS[n]; a=asset(VORM[maat][t]); dx,dy=(schuif or {}).get(n,(0,0))
        ox=int(round(cx-(maat-1)/2+dx+(0.01 if n[0]=='R' else -0.01))); oy=int(round(cy-(maat-1)/2+dy+0.01)); plek[n]=(ox,oy)
        for j in range(maat):
            for i in range(maat):
                y,x=oy+j,ox+i
                if a[j,i]==0 or not(0<=y<H and 0<=x<W): continue
                if beschermd[y,x] and S[y,x]>0: continue    # achter kop, punt en staf
                if vlak[y,x] and a[j,i]==10 and S[y,x]==10: continue
                S[y,x]=a[j,i]; vlak[y,x]=k+1
    return S,weg,plek,vlak
