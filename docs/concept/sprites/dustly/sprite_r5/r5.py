# r5: drie scherpere varianten van r4 zonder tekenen. Elke gewijzigde pixel neemt een tint uit zijn 8 buren of uit het gemeten model.
import sys; sys.path.insert(0,'basis'); sys.path.insert(0,'sprite_r1'); import numpy as np
from lab import label; from ribbels import ridges; from PIL import Image; from bgmask import bgmask
r4=np.load('sprite_r5/r4_idx.npy').astype(int); fig=r4>0
FACE=np.zeros((64,64),bool); FACE[24:38,11:29]=True
N8=[(dy,dx) for dy in (-1,0,1) for dx in (-1,0,1) if (dy,dx)!=(0,0)]; N4=((0,1),(1,0),(0,-1),(-1,0))
E=np.zeros((64,64),bool)
for y,x in zip(*np.where(fig)):
    if any(not fig[y+dy,x+dx] for dy,dx in N4): E[y,x]=True
TONE=(3,4,5)
def nbt(o,y,x,allowed):
    return [o[y+dy,x+dx] for dy,dx in N8 if o[y+dy,x+dx] in allowed]
def v1(o,protect):
    o=o.copy(); free=fig&~E&~FACE&~protect
    for it in range(6):
        ch=0
        # spurs/losse pixels: <=1 gelijke 8-buur -> meerderheid van de buurtinten
        for y,x in zip(*np.where(free&np.isin(o,TONE))):
            same=sum(o[y+dy,x+dx]==o[y,x] for dy,dx in N8)
            if same<=2:
                nb=nbt(o,y,x,(3,4,5,6)); nb=[v for v in nb if v!=o[y,x]]
                if nb: o[y,x]=max(set(nb),key=nb.count); ch+=1
        # tintvlekjes < 6 px (8-samenhang) -> meest voorkomende buurtint rond het vlekje
        for t in TONE:
            lab,n=label(o==t,4)
            for i in range(1,n+1):
                m=lab==i
                if m.sum()>=6 or not (m&free).all(): continue
                nb=[]
                for y,x in zip(*np.where(m)): nb+= [v for v in nbt(o,y,x,(3,4,5,6)) if v!=t]
                if nb:
                    v=max(set(nb),key=nb.count); o[m]=v; ch+=int(m.sum())
        if not ch: break
    return o
# V1
V1=v1(r4,np.zeros((64,64),bool))
# V3: bultlijnen uit het model (ribbels), tint = gemeten modelhelderheid (trouw-drempels), beschermd tegen het vlakfilter
a=np.asarray(Image.open('basis/natief.png').convert('RGB')).astype(float); L=a@[.299,.587,.114]
rg,_=ridges(); BL=np.zeros((64,64),int)
for ny,nx in zip(*np.where(rg)):
    sx=9+int((nx-17+0.5)/1.5); sy=8+int((ny-18+0.5)/1.5)
    if fig[sy,sx] and not E[sy,sx] and not FACE[sy,sx] and r4[sy,sx] in (2,3,4,5,6):
        v=2 if L[ny,nx]<58 else (3 if L[ny,nx]<86 else 4)
        BL[sy,sx]=v if not BL[sy,sx] else min(BL[sy,sx],v)
keep=np.zeros((64,64),bool)
for y,x in zip(*np.where(BL>0)):
    if sum(BL[y+dy,x+dx]>0 for dy,dx in N8)>=1: keep[y,x]=True
V3=V1.copy()
for y,x in zip(*np.where(keep)):
    # lijn alleen als hij donkerder is dan het vlak eromheen
    if BL[y,x]<V1[y,x]: V3[y,x]=BL[y,x]
# gaten van 1 px in een bultlijn dichten met de buurlijnkleur
for y,x in zip(*np.where(fig&~E&~FACE&~keep)):
    for (dy,dx) in ((0,1),(1,0),(1,1),(1,-1)):
        if keep[y-dy,x-dx] and keep[y+dy,x+dx] and V3[y-dy,x-dx]<V1[y,x] and V3[y+dy,x+dx]<V1[y,x]:
            V3[y,x]=max(V3[y-dy,x-dx],V3[y+dy,x+dx]); break
# buitenlijn dichte wolk (hoofdcomponent, buiten de slierten): randpixel met vlaktint -> lijnkleur van de buurrandpixels
lab4,n4=label(fig,4); main=np.argmax([ (lab4==i).sum() for i in range(1,n4+1)])+1
for y,x in zip(*np.where(E&(lab4==main)&~FACE)):
    if V3[y,x] in (4,5,6) and not (y>=41 and x>=26):
        thin=not any(fig[y+dy,x+dx] and not E[y+dy,x+dx] for dy,dx in N8)
        if thin: continue
        nb=[V3[y+dy,x+dx] for dy,dx in N8 if E[y+dy,x+dx] and V3[y+dy,x+dx] in (1,2,3,7)]
        if nb: V3[y,x]=max(set(nb),key=nb.count)
for n,o in (('V1',V1),('V3',V3)): np.save(f'sprite_r5/{n}_idx.npy',o)
# controles
def check(n,o,ref=r4):
    sil=((o>0)!=(ref>0)).sum(); face=((o!=ref)&FACE).sum(); bad=[]
    model=np.load('sprite_r1/auto_idx.npy')
    for y,x in zip(*np.where(o!=ref)):
        nb=[o[y+dy,x+dx] for dy,dx in N8]+[ref[y+dy,x+dx] for dy,dx in N8]
        ok=o[y,x] in nb or o[y,x]==model[y,x] or (keep[y,x] and o[y,x]==BL[y,x])
        if not ok: bad.append((x,y,o[y,x]))
    print(n,'gewijzigd t.o.v. r4:',(o!=ref).sum(),'silhouet-diff',sil,'gezicht-diff',face,'tint niet uit buren/model:',len(bad),bad[:5])
check('V1',V1); check('V3',V3)
