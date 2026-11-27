# Gedeelde hulpdelen voor r3 (geen bijwerkingen): natief raster en klassen uit r1/maak.py stap 1-2, r2 als onderlaag.
import os
import numpy as np; from PIL import Image
H=os.path.dirname(os.path.abspath(__file__)); R1=os.path.join(H,'../r1')
src=open(os.path.join(R1,'maak.py')).read().split('# 3) ogen')[0].replace("HIER=os.path.dirname(os.path.abspath(__file__))","HIER=%r"%R1)
ns={}; exec(src,ns)
N,NK,LIJN,PAL,s2m,m2n,n2s=ns['N'],ns['NK'],ns['LIJN'],ns['PAL'],ns['s2m'],ns['m2n'],ns['n2s']
R2=np.array(Image.open(os.path.join(H,'../r2/zandloper_fase2_r2.png'))).astype(int)
def dekking(i,j,fn):
    """oppervlakte per klasse (fn(ni,nj)) van de natieve cellen onder spritepixel (i,j)"""
    x0,y0=s2m(i,j); x1,y1=s2m(i+1,j+1); a0,a1,b0,b1=m2n(x0),m2n(x1),m2n(y0),m2n(y1); w={}
    for nj in range(int(np.floor(b0)),int(np.ceil(b1))):
        for ni in range(int(np.floor(a0)),int(np.ceil(a1))):
            ov=(min(a1,ni+1)-max(a0,ni))*(min(b1,nj+1)-max(b0,nj))
            if ov>0:
                t=fn(ni,nj)
                if t is not None: w[t]=w.get(t,0)+ov
    return w
def toon(p):
    a=np.array(PAL,'uint8')[p]; a[p==0]=(200,230,200); return a
