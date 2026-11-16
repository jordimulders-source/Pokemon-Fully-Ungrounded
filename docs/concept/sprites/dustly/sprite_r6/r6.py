# r6: Gastly-aanpak op V3. (1) gasrand zonder lijn: randpixel met lijntint (1/2/3) waarvan de binnenburen overwegend gas
# (4/5/6) zijn -> meest voorkomende binnenbuurtint (zoals Gastly: gas heeft geen buitenlijn, alleen de dichte kern).
# (2) bultlijnen in het gas tonaal: index 2 binnen gas (binnenburen overwegend 4/5/6) -> 3 (één tint donkerder dan het vlak,
# tint uit de buren). Gezicht en silhouet blijven gelijk. Palet in maak.py.
import sys; sys.path.insert(0,'basis'); import numpy as np
V3=np.load('sprite_r5/V3_idx.npy').astype(int); o=V3.copy(); fig=V3>0
FACE=np.zeros((64,64),bool); FACE[24:38,11:29]=True
N8=[(dy,dx) for dy in (-1,0,1) for dx in (-1,0,1) if (dy,dx)!=(0,0)]; N4=((0,1),(1,0),(0,-1),(-1,0))
E=np.zeros((64,64),bool)
for y,x in zip(*np.where(fig)):
    if any(not fig[y+dy,x+dx] for dy,dx in N4): E[y,x]=True
zone={}
def put(z,x,y,v):
    if o[y,x]!=v: o[y,x]=v; zone[z]=zone.get(z,0)+1
for it in range(2):
    for y,x in zip(*np.where(E&~FACE)):
        if V3[y,x] not in (1,2,3): continue
        inn=[o[y+dy,x+dx] for dy,dx in N8 if fig[y+dy,x+dx] and not E[y+dy,x+dx]]
        gas=[v for v in inn if v in (4,5,6)]
        if inn and len(gas)*2>len(inn):
            put('gasrand',x,y,max(set(gas),key=gas.count))
for y,x in zip(*np.where(fig&~E&~FACE&(V3==2))):
    nb=[V3[y+dy,x+dx] for dy,dx in N8]
    if sum(v in (4,5,6) for v in nb)*2>len(nb) and 3 in nb: put('bultlijn gas',x,y,3)
np.save('sprite_r6/r6_idx.npy',o)
model=np.load('sprite_r1/auto_idx.npy'); bad=[]
for y,x in zip(*np.where(o!=V3)):
    nb=[o[y+dy,x+dx] for dy,dx in N8]+[V3[y+dy,x+dx] for dy,dx in N8]
    if o[y,x] not in nb and o[y,x]!=model[y,x]: bad.append((x,y))
print('diff t.o.v. V3',(o!=V3).sum(),zone,'silhouet',((o>0)!=fig).sum(),'gezicht',((o!=V3)&FACE).sum(),'tint niet uit buren/model',len(bad))
