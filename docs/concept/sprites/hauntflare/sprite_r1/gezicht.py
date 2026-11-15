# Haunters Gen 3-gezicht (ogen + mond) als blok uit graphics/pokemon/haunter/anim_front.png, frame 1.
# Klassen (Haunter-index -> klasse): f oogwit -> W, d pupil -> K, e zwarte lijn -> K, 5 donkere lijn -> L,
# a mond donker -> A, 9 mond licht -> N, huid binnen de mond (tanden) -> T. Huid daarbuiten = 0 (wordt bolroze); tanden zijn bij Haunter huidkleur en worden dus ook bolroze (T -> bol midden, tand donker -> bol schaduw).
# Schaal != 1: per klasse vloeiend (8x opgeblazen + gauss) en per doelpixel de klasse met de grootste dekking
# (methode van docs/concept/sprites/gengas/gezicht_groter/schaal.py). Schrijft gezicht_<s>.npy (0 = geen gezicht).
import sys
from PIL import Image; import numpy as np
from scipy import ndimage as nd
S='docs/concept/sprites/hauntflare/sprite_r1/'
g=Image.open('graphics/pokemon/haunter/anim_front.png'); gi=np.array(g)[:64].astype(int)
X0,X1,Y0,Y1=13,35,28,46            # blok rond ogen + mond
sub=gi[Y0:Y1,X0:X1]
huid=np.isin(sub,[2,3,4])
# huid die vanaf de blokrand bereikbaar is = buitenhuid; de rest (in de mond) = tanden
lab,n=nd.label(huid)
rand=set(np.unique(np.concatenate([lab[0],lab[-1],lab[:,0],lab[:,-1]])))-{0}
tand=huid&~np.isin(lab,list(rand))
kern=np.isin(sub,[15,13,10,9])|tand
dicht=nd.binary_dilation(kern,np.ones((3,3)))
# 'e'-lijnen alleen tegen oog/mond (niet Haunters kaak- en hoofdomtrek); '5' idem
K=(np.isin(sub,[14,13]))&dicht
L=(sub==5)&dicht
C=np.zeros_like(sub)
C[L]=2; C[K]=1; C[sub==15]=3; C[sub==10]=4; C[sub==9]=5; C[tand]=6; C[tand&(sub==4)]=7
# 1 K zwart, 2 L donkere lijn, 3 W oogwit, 4 A mond donker, 5 N mond licht, 6 T tand (Haunter 2/3), 7 tand donker (Haunter 4)
np.save(S+'gezicht_1.00.npy',C)
U=8
def blur(a,s):
    r=int(3*s); k=np.exp(-0.5*(np.arange(-r,r+1)/s)**2); k/=k.sum()
    a=np.apply_along_axis(lambda m: np.convolve(m,k,'same'),0,a)
    return np.apply_along_axis(lambda m: np.convolve(m,k,'same'),1,a)
H,W=C.shape
soft={c:blur(np.kron((C==c).astype(float),np.ones((U,U))),0.30*U) for c in range(8)}
PRI={1:1.35,2:1.2,6:1.2,0:1.0}
# Variant 'schrappen' (zoals het model): rijen/kolommen van het Haunter-blok weglaten die het meest op hun
# buur lijken, gespreid; elke overgebleven pixel blijft een Haunter-pixel. Argument 'k<cols>r<rows>'.
def schrap_blok(C,nc,nr,vr=()):
    def kies(A,n,vr=()):
        cost=np.array([(A[i]!=A[i+1]).sum() for i in range(len(A)-1)])
        g=[]
        for i in np.argsort(cost,kind='stable'):
            if int(i) in vr: continue
            if all(abs(int(i)-j)>=2 for j in g): g.append(int(i))
            if len(g)==n: break
        return sorted(g)
    r=kies(C,nr,vr); c=kies(C.T,nc)
    return np.delete(np.delete(C,r,0),c,1),r,c
SCHRAP=[a for a in sys.argv[1:] if a.startswith('k')]
for a in SCHRAP:
    vr=()
    if a.endswith('o'):            # 'o' = ogen sparen: geen rijen door het nabije oog (Haunter y31-36)
        a2=a[:-1]; vr=set(range(31-Y0,37-Y0))
    else: a2=a
    nc,nr=map(int,a2[1:].split('r')); o,r,c=schrap_blok(C,nc,nr,vr)
    np.save(S+'gezicht_%s.npy'%a,o); print(a,o.shape,'rijen (blok)',r,'kolommen (blok)',c,'| Haunter-y',[v+Y0 for v in r],'Haunter-x',[v+X0 for v in c])
for s in [float(a) for a in sys.argv[1:] if not a.startswith('k')]:
    h,w=int(round(H*s)),int(round(W*s)); o=np.zeros((h,w),int)
    for j in range(h):
        for i in range(w):
            yy=min(int((j+0.5)/s*U),H*U-1); xx=min(int((i+0.5)/s*U),W*U-1)
            o[j,i]=max(range(8),key=lambda c: soft[c][yy,xx]*PRI.get(c,1.0))
    np.save(S+'gezicht_%.2f.npy'%s,o); print(s,o.shape)
pal={0:(250,118,162),1:(36,22,26),2:(200,67,91),3:(255,255,255),4:(154,42,34),5:(238,116,124),6:(250,118,162),7:(240,68,130)}
for s in ['1.00']+[a if a.startswith('k') else '%.2f'%float(a) for a in sys.argv[1:]]:
    o=np.load(S+'gezicht_%s.npy'%s); im=np.array([[pal[v] for v in row] for row in o],'uint8')
    Image.fromarray(im).resize((o.shape[1]*12,o.shape[0]*12),Image.NEAREST).save(S+'gezicht_%s_12x.png'%s)
