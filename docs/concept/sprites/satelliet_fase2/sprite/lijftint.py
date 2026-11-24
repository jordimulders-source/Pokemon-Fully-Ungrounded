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
        y0,y1=int(round(143+j*s)),int(round(143+(j+1)*s)); x0,x1=int(round(46+i*s)),int(round(46+(i+1)*s))
        m=np.isin(k[y0:y1,x0:x1],T)
        if m.sum()<20: continue
        c=a[y0:y1,x0:x1][m].mean(0); n=T[int(np.argmin(((PAL[T]-c)**2).sum(1)))]
        if n!=o[j,i]: ch[(o[j,i],n)]=ch.get((o[j,i],n),0)+1; o[j,i]=n
np.save(UIT,o); print('lijftint gewijzigd:',ch)
