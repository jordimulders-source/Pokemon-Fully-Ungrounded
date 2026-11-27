# Ronde 2: vanaf r1 (r1_I.npy), benoemde reparaties van Claude. Elke stap gemeten op comp_nat (= r4/r6/r3_3-cellen).
import numpy as np
from basis import png,PAL
from staart import staart
I=np.load('r2basis_I.npy').copy(); I0=I.copy()
def near(c,idx): return idx[int(np.argmin([((np.array(PAL[i])-c)**2).sum() for i in idx]))]
# 1. STAART uit r3_3 per pixel
R=staart(); TH=0.30
tm=np.zeros((64,64),bool)
for (y,x),r in R.items():
    if r['a3']>=0.2 and r['a3']>=r['ao'] and r['a3']+r['ao']>=TH: tm[y,x]=True
# niet over de schildrand/poot heen: pixels die in r1 een ander materiaal hadden en waar r3_3 minder dan de helft dekt blijven
dk={}
for (y,x),r in R.items(): dk[(y,x)]=r['d']+r['k']
D=np.zeros((64,64)); 
for (y,x),v in dk.items(): D[y,x]=v
for y,x in zip(*np.where(tm)):
    r=R[(y,x)]
    if r['k']>=0.45: I[y,x]=1; continue
    if r['g']>=0.45 and r['c'] is not None: I[y,x]=near(r['c'],[10,11,12,13]); continue
    rug=D[y,x]>=D[y-1,x] and D[y,x]>=D[y+1,x]
    if D[y,x]>=0.3 and rug: I[y,x]=5; continue
    if r['c'] is None: I[y,x]=5; continue
    I[y,x]=r['t']
# buitenrand staart -> lijn
op=I>0; P=np.pad(op,1)
rand=op&~(P[:-2,1:-1]&P[2:,1:-1]&P[1:-1,:-2]&P[1:-1,2:])
I[tm&rand]=1
# tip van de staart is grijze steen tot natief rij 49 (sprite rij 35)
for y,x in zip(*np.where(tm)):
    if y<=35 and I[y,x]>1 and R[(y,x)]['c'] is not None: I[y,x]=near(R[(y,x)]['c'],[10,11,12,13])
# losse zwarte pixels binnen de staart (niet aan de buitenlijn vast) -> donkerste staarttint
for y,x in zip(*np.where(tm)):
    if I[y,x]!=1 or rand[y,x]: continue
    if sum(I[y+dy,x+dx]==1 for dy,dx in ((0,1),(0,-1),(1,0),(-1,0)))<=1 and not any(rand[y+dy,x+dx] and I[y+dy,x+dx]==1 for dy,dx in ((0,1),(0,-1),(1,0),(-1,0))): I[y,x]=5
n_staart=(I!=I0).sum()
# 2+3. STEKEL en BAND: modus per pixel uit de r6-cellen (scherp, geen gemiddelde), rijen 7-25, kolommen 11-23
from modus import modus
nat=np.load('comp_nat.npy')
I1=I.copy()
op=I>0; P=np.pad(op,1); rand=op&~(P[:-2,1:-1]&P[2:,1:-1]&P[1:-1,:-2]&P[1:-1,2:])
for y in range(7,26):
    for x in range(11,24):
        if I[y,x]==0 or rand[y,x]: continue
        w=modus(x,y,nat); k=max(w,key=w.get)
        if k=='.': continue
        I[y,x]=1 if k=='#' else (11 if k=='g' else int(k))
# stekel: linkerkolom selout (2), licht 2 px breed (natief licht = 2 cellen = 1,4 px; Claude: 'breder zoals het model')
for y in range(8,21):
    xs=[x for x in range(11,24) if I[y,x] in (2,3,4)]
    if not xs: continue
    l=min(xs)
    if I[y,l-1]==0: I[y,l]=2; a=l+1          # buitenrand: selout, licht begint ernaast
    else: a=l                                  # links zit de zwarte voetlijn: licht begint direct
    if I[y,a] in (3,4): I[y,a]=4
    if 10<=y<=19 and I[y,a+1] in (3,4): I[y,a+1]=4
I[22,15]=9          # stekelvoet-boog: natief x26-28 = sprite kolom 16-17, kolom 15 is ring
n_band=(I!=I1).sum()
# 4. OVERLAPLIJNEN poot over lijf/kop weer zwart (model: natief x38-40 en x55-56 doorlopend zwart, kin-/poot-lijn natief rij 68-70)
I2=I.copy()
zones=[(24,26,46,62),   # linkerrand middelste poot
       (34,35,48,54),   # rechterrand middelste poot
       (9,18,48,51),    # kin / bovenkant voorste poot
       (36,41,49,54)]   # achterpoot tegen de buik
for x0,x1,y0,y1 in zones:
    for y in range(y0,y1):
        for x in range(x0,x1+1):
            if I[y,x]==10: I[y,x]=1
n_overlap=(I!=I2).sum()
print('overlap zwart',n_overlap)
# 5. RECHTER SCHILDSTREEP (r6): beige-fractie per pixel, rug in x-richting -> streep (tint 8/9 naar modus)
I3=I.copy(); Bf=np.zeros((64,64)); Wt={}
for y in range(16,47):
    for x in range(32,48):
        if I[y,x]<2: continue
        w=modus(x,y,nat); Bf[y,x]=w.get(8,0)+w.get(9,0); Wt[(y,x)]=w
for y in range(16,47):
    for x in range(33,47):
        if I[y,x]<2 or I[y,x] in (8,9): continue
        if Bf[y,x]>=0.3 and Bf[y,x]>=Bf[y,x-1] and Bf[y,x]>=Bf[y,x+1]:
            w=Wt[(y,x)]; I[y,x]=9 if w.get(9,0)>w.get(8,0) else 8
n_streep=(I!=I3).sum(); print('streep',n_streep, sorted(zip(*np.where(I!=I3))))
print('staart',n_staart,'stekel+band',n_band)
np.save('r2_I.npy',I); png(I,'r2.png'); png(I,'r2_8x.png',8)
print('staart: pixels anders dan r1:',(I!=I0).sum())
