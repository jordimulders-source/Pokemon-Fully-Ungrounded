# Ronde 2 op claydol_g3: alleen 4 benoemde reparaties; elke wijziging gelogd met zone; diff buiten de zones = 0 (bewezen in diff2.py).
import sys, numpy as np; sys.path.insert(0,'.'); sys.path.insert(0,'r2')
from cc import label
from creme import cremeMasker
from staf import staf2, K as STAFK
G3=np.load('sprite.npy'); S=G3.copy(); log=[]
comp,_=label(G3>0,diag=True); HOOFD=np.bincount(comp.ravel())[1:].argmax()+1
LSTAF=comp==comp[50,5]; RSTAF=comp==comp[45,60]
ZONE={}   # naam -> masker van toegestane wijzigingen
def zet(y,x,v,zone,why):
    if S[y,x]!=v: log.append((zone,int(y),int(x),int(S[y,x]),int(v),why)); S[y,x]=v

# --- 3. Rechterstaf: apart opnieuw geschrapt uit het model (de staf is los). Kolom 83 i.p.v. 78/80/83 (die liepen door de stafkop),
#        plus 3 extra stafrijen 62/78/80 (bijna-duplicaten in de steel, geen rode banden) zodat de bredere kop vrij blijft van het bolletje.
st=staf2([83],[62,78,80]); h,w=st.shape; y0,x0=64-h,64-w
nieuw=np.zeros((64,64),int); nieuw[y0:y0+h,x0:x0+w]=st
# randregel van g3: licht op de rand rechts/onder -> K
t=np.pad(nieuw==0,1,constant_values=True)
for y,x in zip(*np.where(nieuw>0)):
    if (t[y+1,x+2] or t[y+2,x+1]) and nieuw[y,x]<=7: nieuw[y,x]=10
STAFZONE=RSTAF|(nieuw>0)
for y,x in zip(*np.where(STAFZONE)): zet(y,x,int(nieuw[y,x]),'rechterstaf','opnieuw geschrapt uit model')
ZONE['rechterstaf']=STAFZONE

# --- 1. Onderkop rustiger: alleen binnen de onderkop (rijen 31-38, onder ogen en neus, x 15-47, tinten 5-8; ogen/crème/K/rood blijven)
OK=np.zeros((64,64),bool); OK[31:39,15:48]=True; OK&=(comp==HOOFD)
ZONE['onderkop']=OK.copy()
# Vlak = modelhelderheid 3x3 gemiddeld (rustig, schaduwsikkel volgt het model); lijnen = modelbarsten (modelpixel < 95)
# die als lijn doorlopen (8-buur, >= LMIN px); de rest van de korte stukjes gaat op in het vlak.
from kaal3 import kaal
_,A,_,_=kaal(); LUMA=(A*[0.299,0.587,0.114]).sum(2)
Z=OK&np.isin(G3,(5,6,7,8))&~cremeMasker(G3)
# Schaduwsikkel = massieve donkere modelvlakken (model < 100 met >= 6 van 8 buren donker of lijn/rand);
# barsten = de donkerste modelpixels (< 80) die als lijn doorlopen (8-buur >= 3 px); vlak = 3x3-gemiddelde van de
# lichte modelpixels (>= 100): < 146 -> 7, anders 6.
DONK=(LUMA<100)|(G3==10)|(G3==0)
SIK=np.zeros((64,64),bool)
for y,x in zip(*np.where(Z)):
    if LUMA[y,x]<100 and (DONK[y-1:y+2,x-1:x+2].sum()-1>=6 or G3[y+1,x] in (0,10) or G3[min(63,y+2),x] in (0,10)): SIK[y,x]=True   # ook: 1-2 px boven de onderrand
D=Z&(LUMA<80)&~SIK
Ld,_=label(D,diag=True); szd=np.bincount(Ld.ravel())
for y,x in zip(*np.where(Z)):
    if SIK[y,x]: zet(y,x,8,'onderkop','schaduwsikkel (model)'); continue
    if D[y,x] and szd[Ld[y,x]]>=3: zet(y,x,8,'onderkop','barstlijn (model)'); continue
    w=Z[y-1:y+2,x-1:x+2]&(LUMA[y-1:y+2,x-1:x+2]>=100)
    m=LUMA[y-1:y+2,x-1:x+2][w].mean() if w.any() else 120
    zet(y,x,7 if m<146 else 6,'onderkop','vlak naar model 3x3')
for it in range(4):
    for v in (5,6,7):
        Lv,_=label(S==v); sz=np.bincount(Lv.ravel())
        for y,x in zip(*np.where(Z&(S==v))):
            if sz[Lv[y,x]]<3:
                nb=[c for c in S[y-1:y+2,x-1:x+2].ravel() if c in (5,6,7,8) and c!=v]
                if nb: zet(y,x,int(np.bincount(nb).argmax()),'onderkop','spikkel %d'%v)

# --- 2. Steen <=3 tinten: crème-schaduw en steenlicht gescheiden
M=cremeMasker(S)&(comp==HOOFD)
for y,x in zip(*np.where(M&(S==5))): zet(y,x,4,'creme','creme-schaduw 5->4')
STEEN4=(S==4)&~M&~((comp==HOOFD)&(np.arange(64)[None,:]>=49)&(np.arange(64)[:,None]>=31)&(np.arange(64)[:,None]<=37))  # bolletje rechtsonder = creme
for y,x in zip(*np.where(STEEN4)): zet(y,x,5,'steenlicht','steenlicht 4->5')
ZONE['creme']=M; ZONE['steenlicht']=STEEN4|(G3==4)
np.save('r2/sprite_r2.npy',S)
if __name__=='__main__':
    from collections import Counter
    print('wijzigingen',len(log)); print(Counter((z,w.split(' ')[0]) for z,*_,w in log))
