# r9: materiaalraster (hand, trap.txt / schuin.txt) + tint (gen.py) + palet per variant -> geindexeerde png.
import sys, numpy as np; from PIL import Image
from gen import B, stuk, tint, H, W
from basis import KL
def lees(f):
    M=np.full((H,W),'',dtype='<U1')
    for l in open(f):
        if not l.strip(): continue
        y=int(l[:2]); s=l[3:].rstrip('\n')
        for i,c in enumerate(s):
            if c in 'gal': M[y,16+i]=c
    assert all((M[y,x]!='')==bool(stuk[y,x]) for y in range(H) for x in range(W)), 'raster past niet op tuniekzone'
    return M
# kleuren per variant: grond (licht, midden, schaduw), accent (l,m,s), lijn (l,s), selout (lichtkant), binnenlijn
def bouw(M, pal, extra):
    KL2=dict(KL); KL2.update(extra)
    R=B.copy(); R[R=='G']='?'; R[R=='H']='?'
    for y in range(H):
        for x in range(W):
            if stuk[y,x]:
                m=M[y,x]; t=tint[y,x]
                if m=='l': R[y,x]=pal['l'][0 if t==0 else 1]
                else: R[y,x]=pal[m][t]
    # buitenlijn tuniek: selout aan de lichtkant (transparant links of boven, tuniekvlak rechts of onder)
    for y in range(26,48):
        for x in range(W):
            if B[y,x]!='K': continue
            nb=[(y,x+1),(y+1,x),(y,x-1),(y-1,x)]
            if not any(stuk[a,b] for a,b in nb): continue
            if (B[y,x-1]=='.' and stuk[y,x+1]) or (B[y-1,x]=='.' and stuk[y+1,x] and x<=31):
                if pal.get('sel'): R[y,x]=pal['sel']
            if (y,x) in [(36,31),(36,32),(37,32),(37,33),(38,34),(39,35)] and pal.get('bin'): R[y,x]=pal['bin']
    return R, KL2
def schrijf(naam,R,KL2):
    keys=['.']+sorted(set(R.ravel())-{'.'}); assert '?' not in keys, 'G/H niet vervangen'
    assert len(keys)<=16, (len(keys),keys)
    im=Image.fromarray(np.vectorize(keys.index)(R).astype('uint8'),'P')
    flat=[v for k in keys for v in KL2[k]]; im.putpalette(flat+[0]*(768-len(flat))); im.save(naam,transparency=0)
    return len(keys)
