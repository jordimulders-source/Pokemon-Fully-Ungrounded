# r4: vierde lijftint (#c0b0d0, model) per pixel gemeten: voor elke lijfpixel (2/3/4/5, buiten de irisschijf, niet de selout)
# de gemiddelde kleur van de lijfklasse-modelpixels in zijn blok -> dichtstbijzijnde van de 4 lijftinten.
import numpy as np, sys; from PIL import Image
o=np.load(sys.argv[1]).copy(); vorig=np.load(sys.argv[2]); UIT=sys.argv[3]
k=np.load('klassen2.npy'); PAL=np.load('pal.npy').astype(float)
a=np.asarray(Image.open('../model.png').convert('RGB')).astype(float)
s=(978-46)/64; H,W=o.shape; T=[2,3,4,5]; ch={}
for j in range(H):
    for i in range(W):
        if o[j,i] not in T or vorig[j,i]!=o[j,i]: continue          # vorig = voor licht.py: selout overslaan
        if np.hypot(i+.5-20,j+.5-24)<6.3: continue                   # irisschijf + witte ring blijven
        if j<13 and 24<=i<50 and j<9: continue                        # antennezone (glans bolletje B)
        y0,y1=int(round(143+j*s)),int(round(143+(j+1)*s)); x0,x1=int(round(46+i*s)),int(round(46+(i+1)*s))
        m=np.isin(k[y0:y1,x0:x1],T)
        if m.sum()<20: continue
        c=a[y0:y1,x0:x1][m].mean(0); n=T[int(np.argmin(((PAL[T]-c)**2).sum(1)))]
        if n!=o[j,i]: ch[(o[j,i],n)]=ch.get((o[j,i],n),0)+1; o[j,i]=n
# losse 3 zonder enige 8-buur 3 -> meest voorkomende 4-buur uit {2,4,5} (geen eenzame tussentint)
los=[]
for j in range(1,H-1):
    for i in range(1,W-1):
        if o[j,i]!=3 or vorig[j,i]==o[j,i] and np.hypot(i+.5-20,j+.5-24)<6.3: continue
        if (o[j-1:j+2,i-1:i+2]==3).sum()>1: continue
        n=[o[q] for q in ((j-1,i),(j+1,i),(j,i-1),(j,i+1)) if o[q] in (2,4,5)]
        if n: o[j,i]=max(set(n),key=n.count); los.append((i,j+7))
np.save(UIT,o); print('lijftint gewijzigd:',ch,'losse 3:',los)
