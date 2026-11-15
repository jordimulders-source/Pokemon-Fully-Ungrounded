# Vergroot Gengars Gen 3-gezicht (ogen + grijns) netjes naar factor s: per kleurlaag een vloeiende vorm
# (8x opgeblazen + gaussisch verzacht), daarna per doelpixel de laag met de grootste dekking (met voorrang
# voor dunne lijnen). Niets getekend: alle vormen komen uit Gengar. Gebruik: python3 schaal.py 1.25 [1.15 ...]
from PIL import Image; import numpy as np, sys
g=Image.open('graphics/pokemon/gengar/anim_front.png'); gi=np.array(g)[:64].astype(int)
pal=np.array(g.getpalette()[:48]).reshape(16,3)
X0,X1,Y0,Y1=15,40,23,42
sub=gi[Y0:Y1,X0:X1]
FACE={1,2,3,4,5,6,7,14,15}
# gezichtsmasker zoals gezicht.py: indexen + 13 naast oog/tand
fm=np.zeros_like(sub,bool)
for y in range(sub.shape[0]):
    for x in range(sub.shape[1]):
        v=sub[y,x]; nb=sub[max(0,y-1):y+2,max(0,x-1):x+2].flatten()
        core={1,2,3,4,5,6,7}
        if v in core: fm[y,x]=True
        elif v in (14,15):   # lijnen alleen als ze binnen 2 px van oog/tand liggen (niet Gengars lijfomtrek)
            w=sub[max(0,y-2):y+3,max(0,x-2):x+3]
            fm[y,x]= bool(np.isin(w,list(core)).any())
lab=np.where(fm,sub,0)   # 0 = geen gezicht
classes=[c for c in np.unique(lab)]
U=8
def blur(a,s):
    r=int(3*s); k=np.exp(-0.5*(np.arange(-r,r+1)/s)**2); k/=k.sum()
    a=np.apply_along_axis(lambda m: np.convolve(m,k,'same'),0,a)
    return np.apply_along_axis(lambda m: np.convolve(m,k,'same'),1,a)
H,W=sub.shape
soft={}
for c in classes:
    m=np.kron((lab==c).astype(float),np.ones((U,U)))
    soft[c]=blur(m,0.30*U)
PRI={15:1.35,14:1.25,3:1.3,0:1.0}
for s in map(float,sys.argv[1:]):
    h,w=int(round(H*s)),int(round(W*s))
    out=np.zeros((h,w),int)
    for j in range(h):
        for i in range(w):
            yy=min(int((j+0.5)/s*U),H*U-1); xx=min(int((i+0.5)/s*U),W*U-1)
            best=max(classes,key=lambda c: soft[c][yy,xx]*PRI.get(c,1.0))
            out[j,i]=best
    np.save(f'docs/concept/sprites/gengas/gezicht_groter/gezicht_{s:.2f}.npy',out)
    rgb=np.full((h,w,3),(150,70,100)); 
    for c in classes:
        if c: rgb[out==c]=pal[c]
    Image.fromarray(rgb.astype('uint8')).resize((w*12,h*12),Image.NEAREST).save(f'docs/concept/sprites/gengas/gezicht_groter/gezicht_{s:.2f}_12x.png')
    print(s,h,w)
rgb=np.full((H,W,3),(150,70,100))
for c in classes:
    if c: rgb[lab==c]=pal[c]
Image.fromarray(rgb.astype('uint8')).resize((W*12,H*12),Image.NEAREST).save('docs/concept/sprites/gengas/gezicht_groter/gezicht_1.00_12x.png')
