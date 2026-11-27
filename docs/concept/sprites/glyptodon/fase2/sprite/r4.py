# Ronde 4: vanaf r3. (A) de 24 opgeruimde pixels uit r3 toetsen: alleen houden als de nieuwe kleur de modeltint is, anders r2.
# (B) oog 1-op-1 uit het model (natief r4 rond het oranje oog), met Larvitar/Onix als referentie voor de omlijning.
import numpy as np
from basis import png,PAL
from modus import modus
from reduceer import X0,Y0,s,LEFT,TOP
nat=np.load('comp_nat.npy'); I=np.load('r3_I.npy').copy(); I2=np.load('r2_I.npy'); I3=I.copy()
def cellen(x,y):
    ya=Y0+(y-TOP)*s; xa=X0+(x-LEFT)*s; out=[]
    for yy in range(int(ya),int(np.ceil(ya+s))):
        for xx in range(int(xa),int(np.ceil(xa+s))):
            w=max(0,min(yy+1,ya+s)-max(yy,ya))*max(0,min(xx+1,xa+s)-max(xx,xa))
            if w>0 and 0<=yy<100 and 0<=xx<100: out.append((w,nat[yy,xx].astype(float)))
    return out
def modeltint(x,y):
    w=modus(x,y,nat); w.pop('.',None)
    k=max(w,key=w.get)
    if k=='#': return 1,w
    if k=='g':
        cs=[(ww,c) for ww,c in cellen(x,y) if c.mean()>=45 and abs(c[0]-c[2])<16]
        c=sum(ww*c for ww,c in cs)/sum(ww for ww,c in cs)
        return [10,11,12,13][int(np.argmin([((np.array(PAL[i])-c)**2).sum() for i in (10,11,12,13)]))],w
    return int(k),w
# A
opg=[(int(x),int(y)) for x,y in np.load('r3_opg.npy')]
houden=[];terug=[]
for x,y in opg:
    t,w=modeltint(x,y)
    if t==I3[y,x]: houden.append((x,y,int(I3[y,x])))
    else: I[y,x]=I2[y,x]; terug.append((x,y,int(I3[y,x]),t,{k:round(v,2) for k,v in w.items()}))
print('gehouden',len(houden),houden); print('terug naar r2',len(terug))
for t in terug: print('  ',t)
# B oog: eerst alles in het oogvak terug naar r2, dan per pixel
for y in range(39,45):
    for x in range(10,18): I[y,x]=I2[y,x]
def oranje(x,y):
    cs=[(w,c) for w,c in cellen(x,y) if c[0]-c[2]>80 and c[0]>170]
    c=sum(w*c for w,c in cs)/sum(w for w,c in cs); return 14 if np.abs(np.array(PAL[14])-c).sum()<np.abs(np.array(PAL[15])-c).sum() else 15
OOG={}
# iris: pixels met oranje als grootste modelaandeel (gemeten: (14,41) O.9, (15,41) O.4/K.2/D.2, (12,42) O.6, (13,42) O.6, (14,42) O.6)
for x,y in [(14,41),(15,41),(12,42),(13,42),(14,42)]: OOG[(x,y)]=(oranje(x,y),'model: oranje grootste aandeel')
# lid/wenkbrauw boven: model zwart (K.7-1.0), Larvitar: zwarte lid-lijn boven de iris
for x,y in [(13,40),(14,40),(15,40),(12,41),(13,41)]: OOG[(x,y)]=(1,'model zwart (K>=0,7) + Larvitar lid-lijn zwart')
# zijkant/onder: model donker (K.6 links, K.5+D onder) -> donkere lijftint 10, zoals Onix (lijnen rond het oog in donkere lijftint)
OOG[(11,42)]=(10,'model K.6/g.3 links van de iris -> donkere lijftint (Onix, Larvitar-zijkant)')
OOG[(12,43)]=(10,'model K.5/g.4 onder de iris -> donkere lijftint (Onix)')
# rest van het vak: modeltint
for x,y in [(15,42),(16,41),(16,40),(13,43),(14,43),(10,42)]:
    t,w=modeltint(x,y); OOG[(x,y)]=(t,'modeltint '+str({k:round(v,2) for k,v in w.items()}))
for (x,y),(v,b) in OOG.items(): I[y,x]=v
print('oog:')
for (x,y),(v,b) in sorted(OOG.items(),key=lambda t:(t[0][1],t[0][0])): print(f'  ({x},{y}) = {v}  [{b}]  (r2 {I2[y,x]}, r3 {I3[y,x]})')
np.save('r4_I.npy',I); png(I,'r4.png'); png(I,'r4_8x.png',8)
print('verschil met r3:',(I!=I3).sum(),' met r2:',(I!=I2).sum())
