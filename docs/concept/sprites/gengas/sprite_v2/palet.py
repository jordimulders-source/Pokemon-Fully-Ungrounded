# Geschrapt model -> 15 kleuren + transparant. Per kleurgroep k-means (geen tekenwerk): elke pixel krijgt de
# dichtstbijzijnde groepskleur. Groepen: omlijning, lijf (6), oogrood (2), tanden (2), manen (3).
from PIL import Image; import numpy as np
D='docs/concept/sprites/gengas/'
a=np.asarray(Image.open(D+'model/model_64_geschrapt.png').convert('RGB')).astype(float)
R,G,B=a[...,0],a[...,1],a[...,2]; lum=0.299*R+0.587*G+0.114*B; sat=a.max(2)-a.min(2)
import sys; sys.path.insert(0,D+'model'); from seg import label
wit=a.min(2)>=232; l2,n=label(wit)
rand=set(l2[0,:])|set(l2[-1,:])|set(l2[:,0])|set(l2[:,-1]); rand.discard(0)
bg=np.isin(l2,list(rand))
out=lum<38
grey=(sat<30)&~bg&~out&(lum<200)
teeth=(lum>=175)&~bg&(sat<70)
red=(R>150)&(R-G>75)&(R-B>45)&(lum>85)&~bg&~teeth
body=~bg&~out&~grey&~teeth&~red
def km(px,k,it=30):
    rng=np.random.default_rng(1); c=px[rng.choice(len(px),k,replace=False)]
    for _ in range(it):
        d=((px[:,None]-c[None])**2).sum(2); l=d.argmin(1)
        c=np.array([px[l==i].mean(0) if (l==i).any() else c[i] for i in range(k)])
    return c
groups=[(out,1),(body,6),(red,2),(teeth,2),(grey,3)]
pal=[(0,255,255)]; idx=np.zeros(bg.shape,int)
for m,k in groups:
    px=a[m]; c=km(px,k) if k>1 else px.mean(0)[None]
    c=c[np.argsort(c@[0.299,0.587,0.114])]
    d=((px[:,None]-c[None])**2).sum(2); l=d.argmin(1)
    idx[m]=len(pal)+l; pal+= [tuple(int(v) for v in x) for x in c]
print(len(pal),pal)
im=Image.fromarray(idx.astype('uint8'),'P'); flat=[v for p in pal for v in p]; im.putpalette(flat+[0]*(768-len(flat)))
im.save(D+'sprite_v2/basis_15.png'); im.convert('RGB').resize((512,512),Image.NEAREST).save(D+'sprite_v2/basis_15_8x.png')
