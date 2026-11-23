# meet6.py: per spritepixel uit het model (gedeelde geometrie): dominante familie/zone, lijnaandeel (zwart of onder de
# familielijndrempel) en helderheid van de vlakpixels -> meet6.npz. Niets getekend: alleen gemeten.
import sys, numpy as np; from PIL import Image
sys.path.insert(0,'../sprite'); from reductie_gedeeld import bron
a=np.asarray(Image.open('../r8/gemini_r8.png').convert('RGB')).astype(float); L=0.30*a[...,0]+0.59*a[...,1]+0.11*a[...,2]
F=np.load('../sprite/model_fam.npz')['f']; Z=np.load('../sprite/model_zone.npz')['z']
LICHT={2,3,4}
def lijn(u,v):
    f=F[v,u]
    if f==1: return True
    if f==3: return L[v,u]<115
    if f==4: return L[v,u]<112
    if f==2: return L[v,u]<(100 if Z[v,u] in LICHT else 60)
    return False
fam=np.zeros((64,64),int); zon=np.zeros((64,64),int); lf=np.zeros((64,64)); hel=np.zeros((64,64))
for Y in range(64):
    for X in range(64):
        tw=0; lw=0; hs=0; hw=0; fw=np.zeros(5); zw=np.zeros(16)
        for u,v,w in bron(X,Y):
            if F[v,u]==0: continue
            tw+=w; zw[Z[v,u]]+=w
            if lijn(u,v): lw+=w
            else: hs+=w*L[v,u]; hw+=w; fw[F[v,u]]+=w
        if tw:
            lf[Y,X]=lw/tw; zon[Y,X]=zw[1:].argmax()+1
            if hw: hel[Y,X]=hs/hw; fam[Y,X]=fw.argmax()
np.savez('meet6.npz',fam=fam,zon=zon,lf=lf,hel=hel)
