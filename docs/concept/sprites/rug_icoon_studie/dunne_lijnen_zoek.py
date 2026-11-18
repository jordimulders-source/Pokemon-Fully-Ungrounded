"""Zoek fronts met lange 1-px-lijntjes (niet de omlijning) die over het lijf lopen, zoals snorharen over de borst.
Telt per soort componenten van één kleur (geen zwart/donkerste kleur), >=5 px, overal max 1 px dik, met >=60% van hun buren lijfpixels.
python3 dunne_lijnen_zoek.py [n]"""
import os,sys,numpy as np
from PIL import Image
from scipy import ndimage as nd
G='graphics/pokemon'; R=[]
def pal(p):
    L=open(p).read().split('\n'); n=int(L[2]); return np.array([[int(v) for v in L[3+k].split()[:3]] for k in range(n)]+[[0,0,0]]*(16-n))
for sp in os.listdir(G):
    d=f'{G}/{sp}'; fp=d+'/anim_front.png' if os.path.exists(d+'/anim_front.png') else d+'/front.png'
    if not (os.path.exists(fp) and os.path.exists(d+'/icon.png') and os.path.exists(d+'/normal.pal')): continue
    try: a=np.array(Image.open(fp))[:64]; P=pal(d+'/normal.pal')
    except Exception: continue
    lum=P.mean(1); m=a>0; score=0
    for k in np.unique(a[m]):
        if lum[k]<60: continue
        lab,n=nd.label(a==k,structure=np.ones((3,3)))
        for c in range(1,n+1):
            cm=lab==c; s=cm.sum()
            if s<5: continue
            # dunheid: geen 2x2-blok van deze kleur
            b=cm[:-1,:-1]&cm[1:,:-1]&cm[:-1,1:]&cm[1:,1:]
            if b.any(): continue
            # langgerekt: bbox-diagonaal groot t.o.v. aantal
            ys,xs=np.nonzero(cm)
            if max(np.ptp(ys),np.ptp(xs))<4: continue
            ring=nd.binary_dilation(cm,structure=np.ones((3,3)))&~cm
            if ring.sum()==0: continue
            binnen=(m[ring]).mean()
            if binnen>=0.6: score+=s
    if score: R.append((score,sp))
R.sort(reverse=True); n=int(sys.argv[1]) if len(sys.argv)>1 else 40
print(' '.join(f'{sp}({s})' for s,sp in R[:n]))
