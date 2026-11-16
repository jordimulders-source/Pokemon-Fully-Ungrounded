# r2 stap A: pieken rechtsonder opnieuw als gevulde taps toelopende vormen (gemeten op het model, rooster g9),
# gas ertussen, zachte selout (L lichtkant, M schaduwkant).
import numpy as np
from gio import from_txt, to_txt, CH
I={c:k for k,c in enumerate(CH)}
G=from_txt('r1.txt'); m=np.load('mask_r1.npy'); ice=np.load('ice_r1.npy')
def Z(y): return 40 if y<25 else (38 if y<41 else 35)
zone=np.zeros((64,64),bool)
for y in range(8,56):
    for x in range(Z(y),64):
        if m[y,x] and not ice[y,x]: zone[y,x]=True
G[zone]=I['W']
# pieken: donker = >=3 van 9 natieve pixels donker (lijn/sp_d/sp_m); per rij-run: links j (2 px bij run>=4), rechts K, midden i
lab=np.load('lab.npy')
dk=np.zeros((64,64),bool); lav=np.zeros((64,64),bool)
for y in range(64):
    for x in range(64):
        y0=3*(y-2); x0=18+3*(x-1)
        if y0<0 or x0<0 or y0+3>200 or x0+3>200: continue
        b=lab[y0:y0+3,x0:x0+3]
        dk[y,x]=np.isin(b,[0,6,7]).sum()>=3; lav[y,x]=(b==10).sum()>=3
spike=np.zeros((64,64),int)
for y in range(64):
    x=0
    while x<64:
        if zone[y,x] and dk[y,x]:
            x1=x
            while x1+1<64 and zone[y,x1+1] and dk[y,x1+1]: x1+=1
            for xx in range(x,x1+1):
                spike[y,xx]=3 if xx==x1 else (1 if (xx==x and x1>x) or (x1-x>=3 and xx==x+1) else 2)
            if x==x1: spike[y,x]=3
            x=x1+1
        else: x+=1
for y in range(64):
    for x in range(64):
        if spike[y,x]: G[y,x]=[0,I['j'],I['i'],I['K']][spike[y,x]]
# lavendel waas in de bovenste gaten (rij <=29), niet vlak bij de rand
rimd=np.zeros((64,64),int)
for y in range(64):
    xs=np.where(m[y])[0]
    if len(xs): rimd[y]=xs.max()-np.arange(64)
for y in range(8,30):
    for x in range(64):
        if zone[y,x] and spike[y,x]==0 and rimd[y,x]>=3 and lav[y,x]: G[y,x]=I['w']
# selout gas: buitenrand L, schaduwkant (uitgang alleen rechts/onder) M
for y in range(64):
    for x in range(64):
        if not m[y,x] or ice[y,x]: continue
        c=CH[G[y,x]]
        if c in 'KjiS' : continue
        out=[(yy,xx) for yy,xx in [(y-1,x),(y+1,x),(y,x-1),(y,x+1)] if not m[yy,xx]]
        if out:
            G[y,x]=I['M'] if all(yy>y or xx>x for yy,xx in out) else I['L']
to_txt(G,'r2_stapA.txt')
