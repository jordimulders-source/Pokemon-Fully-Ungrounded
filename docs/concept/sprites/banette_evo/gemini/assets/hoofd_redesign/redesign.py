# Muts als deel van het hoofd: rand (brim-lijn) weg, mutskleuren naar hoofdtinten. Varianten A/B.
from PIL import Image; import numpy as np, colorsys
a=np.asarray(Image.open('natief_crop.png').convert('RGB')).astype(int)
h,w=a.shape[:2]
def hsv(p): return colorsys.rgb_to_hsv(*[x/255 for x in p])
def cls(p):
    H,S,V=hsv(p)
    if V>0.85 and S<0.12: return '.'
    if V<0.22: return '#'
    if S<0.18: return 'w' if V>0.6 else 'g'
    H*=360
    if H<20 or H>340: return 'R'
    if 200<H<240: return 'B'
    if 240<=H<=330: return 'p'
    return '?'
C=np.array([[cls(a[y,x]) for x in range(w)] for y in range(h)])
lum=a@np.array([.3,.59,.11])
face=np.zeros((h,w),bool); face[21:,11:47]=True
capR=(C=='R')&~face; capB=(C=='B')
P=a[C=='p']; Pl=lum[C=='p']
qs=np.quantile(Pl,[.1,.35,.65,.92]); ramp=[]
for q in qs:
    i=np.argmin(abs(Pl-q)); ramp.append(P[i])
ramp=np.array(ramp)
def toramp(mask,rmp):
    out={}
    l=lum[mask]; qq=np.quantile(l,[.25,.5,.75])
    for (y,x) in zip(*np.where(mask)):
        k=np.searchsorted(qq,lum[y,x]); out[(y,x)]=rmp[k]
    return out
dark=np.clip(ramp*0.55,0,255).astype(int)
def build(left,right,name):
    b=a.copy()
    for m,r in ((capR,left),(capB,right)):
        for (y,x),c in toramp(m,r).items(): b[y,x]=c
    # brim-lijn tussen muts en gezicht weg (rijen 17-22, binnen gezichtsbreedte)
    for y in range(17,23):
        for x in range(12,46):
            if C[y,x]=='#' and C[y+1,x] in 'pR#' and C[y-1,x] in 'RBp?':
                b[y,x]=b[y+1,x] if C[y+1,x]=='p' else b[y-1,x]
    # rolrand vlak maken: voorhoofd loopt door tot rij 15
    for x in range(13,46):
        src=None
        for y in range(21,27):
            if C[y,x]=='p': src=b[y,x]; break
        if src is None: continue
        for y in range(15,22):
            if C[y,x]!='.' : b[y,x]=src
    im=Image.fromarray(b.astype('uint8'))
    im.save(name+'.png'); im.resize((w*10,h*10),Image.NEAREST).save(name+'_10x.png')
build(ramp,dark,'variant_A')
wine=np.array([[70,25,45],[105,35,65],[140,55,90],[170,85,115]])
build(wine,ramp,'variant_B')
