# claydol_g3: kale reductie (kaal3) -> technische opschoning. Elke wijziging wordt gelogd met zone.
import numpy as np; from PIL import Image
from kaal3 import kaal
from klas import PAL, dump
from cc import label
S0,A,NY,NX=kaal(); S=S0.copy(); log=[]
comp,n=label(S0>0,diag=True); sizes=np.bincount(comp.ravel()); HOOFD=sizes[1:].argmax()+1
def zone(y,x):
    if comp[y,x] and comp[y,x]!=HOOFD: return 'staf'
    if S0[y,x]==0: return 'rand'
    if y>=40: return 'lijf'
    return 'kop/krans'
def zet(y,x,v,why):
    if S[y,x]!=v: log.append((zone(y,x),y,x,int(S[y,x]),v,why)); S[y,x]=v
T=lambda: np.pad(S==0,1,constant_values=True)
# 1. Buitenlijn: lichte pixels op de buitenrand (door schrappen) -> lijn; links/boven 8 (selout), rechts/onder K (zoals het model)
t=T()
for y,x in zip(*np.where(S>0)):
    rechtsonder=t[y+1,x+2] or t[y+2,x+1]; linksboven=t[y+1,x] or t[y,x+1]
    if rechtsonder and S[y,x]<=7: zet(y,x,10,'rand rechts/onder: K zoals model')
    elif linksboven and S[y,x]<=6: zet(y,x,8,'rand links/boven: selout 8')
# 2. Ruis: losse vlakpixel (8-buur cluster van 1) in een vlak -> meest voorkomende vlaktint eromheen
VLAK=(4,5,6,7)
for it in range(3):
    for v in VLAK+(8,):
        lab,m=label(S==v,diag=True); sz=np.bincount(lab.ravel())
        for y,x in zip(*np.where(S==v)):
            if sz[lab[y,x]]!=1: continue
            nb=S[max(0,y-1):y+2,max(0,x-1):x+2].ravel()
            if v==8 and ((nb==10).sum()>0 or (nb>=11).sum()>0): continue   # lijnpixel aan omlijning/rood = lijn, blijft
            if v==8 and ((nb==2)|(nb==4)).sum()>=3: continue                   # streepje/rand in licht oog/bolletje
            f=[c for c in nb if c in (2,4,5,6,7) and c!=v]
            if len(f)<5: continue
            c=np.bincount(f).argmax(); zet(y,x,int(c),'ruis: losse %d'%v)
np.save('sprite.npy',S)
if __name__=='__main__':
    from collections import Counter
    print('wijzigingen',len(log),Counter((z,w.split(':')[0]) for z,*_,w in log))
    for l in log[:12]: print(l)
    dump(S)

# Palet claydol_g3 (voorstel Claude, alleen kleur): r19-palet als basis; 8 donkerder (modellijn ~80 i.p.v. 98) zodat de
# reliëflijnen het contrast van het model houden; 4-7 iets verder uit elkaar (stappen ~25-28).
P3={0:(255,255,255),2:(230,222,198),4:(202,192,168),5:(180,170,148),6:(152,143,126),7:(122,114,104),8:(84,76,72),10:(40,32,36),
    12:(220,90,86),13:(166,52,60)}
def opslaan(S,pad):
    used=[0]+[v for v in sorted(P3) if v and (S==v).any()]
    assert all(v in P3 for v in np.unique(S)), np.unique(S)
    m={v:i for i,v in enumerate(used)}; idx=np.vectorize(m.get)(S).astype('uint8')
    im=Image.fromarray(idx,'P'); pal=[c for v in used for c in P3[v]]; pal+=[0]*(48-len(pal)); im.putpalette(pal)
    im.save(pad,transparency=0); return used
def rgb(S,bg=(255,255,255)):
    out=np.zeros(S.shape+(3,),'uint8')
    for v,c in P3.items(): out[S==v]=c
    out[S==0]=bg; return Image.fromarray(out)
if __name__=='__main__':
    used=opslaan(S,'claydol_g3.png'); print('kleuren',len(used))
    rgb(S,(255,255,255)).resize((512,512),0).save('claydol_g3_8x.png')
