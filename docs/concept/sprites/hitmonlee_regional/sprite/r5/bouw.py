# r5: r4 + toonkaart (pitahaya-les): binnen elk materiaal (rood glas / gloed / doorschijnend) de tint uit de
# gladgestreken modelhelderheid (gauss 0,8 spritepx) met drempels op de eigen toonverdeling. Lijnen (1,2),
# glans (10, 12) en de ringzones blijven uit r4. Materiaalgrenzen = r4-indeling, 3x3-meerderheid tegen spikkels.
from PIL import Image; import numpy as np, sys
from scipy import ndimage
D='docs/concept/sprites/hitmonlee_regional/sprite/'
sys.path.insert(0,D)
from toon import save_idx, save_p64, lab
PAL=eval(open(D+'r4/bouw.py').read().split('PAL=')[1].split(']')[0]+']')
L4=np.load(D+'r4/idx.npy'); H,W=L4.shape
B=np.asarray(Image.open(D+'r3/v1/geschrapt.png').convert('RGB')).astype(float)
F=L4>0
lum=lab(B)[...,0]
def glad(v,m,s=0.8):
    a=ndimage.gaussian_filter(np.where(m,v,0),s); b=ndimage.gaussian_filter(m.astype(float),s)
    return np.where(m,a/np.maximum(b,1e-6),0)
RING=np.zeros((H,W),bool)
RING[9:25,36:48]=True    # trapbeen ringen
RING[37:56,42:58]=True   # standbeen ringen
RING[44:52,5:13]=True    # polsring
mat=np.zeros((H,W),int)  # 1 rood 2 gloed 3 bleek
mat[np.isin(L4,[3,4,5,11])]=1; mat[np.isin(L4,[6,7,8,9])]=2; mat[np.isin(L4,[13,14,15])]=3
vul=F&~np.isin(L4,[1,2,10,12])&~RING
# meerderheid
m2=mat.copy()
for y in range(H):
    for x in range(W):
        if not vul[y,x]: continue
        nb=mat[max(0,y-1):y+2,max(0,x-1):x+2].ravel(); nb=nb[nb>0]
        c=np.bincount(nb,minlength=4); 
        if c[mat[y,x]]<=2: m2[y,x]=c.argmax()
mat=m2
RAMP={1:[3,4,5,11],2:[5,6,7,8,9],3:[13,14,15]}
L=L4.copy()
for k,ramp in RAMP.items():
    m=vul&(mat==k)
    g=glad(lum,F&(mat==k)|(vul&(mat==k)))
    v=g[m]
    qs=np.quantile(v,np.linspace(0,1,len(ramp)+1)[1:-1])
    t=np.searchsorted(qs,g[m])
    L[m]=np.array(ramp)[t]
print('gewijzigd t.o.v. r4:',(L!=L4).sum(),'van',F.sum())
np.save(D+'r5/idx.npy',L)
save_p64(L,PAL,D+'r5/sprite.png'); save_idx(L,PAL,D+'r5/r5_10x.png',10)
