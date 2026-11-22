# r11: schaduwopbouw van de kern. Alleen indexwissels binnen de kern (grijs + barsten); vorm, plaat, gezicht, ring, stenen = r10.
import sys,numpy as np; from PIL import Image; from scipy import ndimage as nd
from modellum import lum
a9=np.array(Image.open('../r9/sprite.png')); a10=np.array(Image.open('../r10/A.png'))
l,n=nd.label(np.isin(a9,[2,3,4])); G=np.isin(l,[8,10,15,18,20])          # grijze kernpixels
yy,xx=np.mgrid[0:64,0:64]; cx,cy,R=31.1,34.0,16.3
# 1. bol-term (licht linksboven-voor)
nx=(xx+0.5-cx)/R; ny=(yy+0.5-cy)/R; nz=np.sqrt(np.clip(1-nx**2-ny**2,0,1))
Ld=np.array([-0.6,-0.7,0.45]); Ld/=np.linalg.norm(Ld)
lam=nx*Ld[0]+ny*Ld[1]+nz*Ld[2]
# 2. model-term: grijswaarde van het model per spritepixel, gladgestreken (genormaliseerde convolutie)
m=np.full((64,64),np.nan)
for y,x in zip(*np.where(G)): m[y,x]=lum(x,y)
ok=~np.isnan(m); w=nd.gaussian_filter(ok.astype(float),1.2); ms=nd.gaussian_filter(np.where(ok,m,0),1.2)/np.maximum(w,1e-6)
mn=np.clip((ms-28)/(95-28),0,1)
v=0.65*(lam+1)/2*1.25+0.35*mn
# 3. niveaus op kwantielen binnen de kern: hooglicht / licht / midden / tussentint / schaduw
vals=v[G]; q=np.quantile(vals,[0.24,0.48,0.78,0.95])
LV=np.select([v>=q[3],v>=q[2],v>=q[1],v>=q[0]],[13,4,3,15],2)
o=a10.copy(); o[G]=LV[G]
# 4. vlekjes < 3 px per tint in de kern -> meest voorkomende buurtint (2 rondes)
for _ in range(3):
    for t in (13,4,3,15,2):
        lb,k=nd.label((o==t)&G)
        for i in range(1,k+1):
            mm=lb==i
            if mm.sum()<3:
                for y,x in zip(*np.where(mm)):
                    nb=[o[j,i2] for j in range(y-1,y+2) for i2 in range(x-1,x+2) if G[j,i2] and (j,i2)!=(y,x) and o[j,i2]!=t]
                    if nb: o[y,x]=max(set(nb),key=nb.count)
# 5. barsten (zwart binnen de kern, niet tegen plaat/ring/stenen/transparant)
d=np.hypot(xx+0.5-cx,yy+0.5-cy)
nbr=lambda m_: nd.binary_dilation(m_,np.ones((3,3)))
rand=nbr(~np.isin(a9,[1,2,3,4])&~np.isin(a9,[5,7,8,9,10,11,12]))   # transparant
plaat=nbr(np.isin(a9,[5,7,8,9,10,11,12])&(d<15.5))
buiten=nbr(np.isin(a9,[5,6])&(d>=15.5))|nbr(np.isin(a9,[2,3,4])&~G)|rand
B=(a9==1)&(d<16.5)&~plaat&~buiten
lb,k=nd.label(B,np.ones((3,3))); kort=[];licht=[]
for i in range(1,k+1):
    mm=lb==i; ring=nbr(mm)&G&~mm; buur=o[ring]
    if mm.sum()<=2 and len(buur):
        t=np.bincount(buur).argmax(); kort.append(([(int(x),int(y)) for y,x in zip(*np.where(mm))],int(t))); o[mm]=t
    elif len(buur) and np.mean(np.isin(buur,[13,4]))>=0.6:
        licht.append([(int(x),int(y)) for y,x in zip(*np.where(mm))]); o[mm]=2
np.save('idx.npy',o)
print('korte barststreepjes -> vlaktint:',kort); print('barsten in licht vlak -> 2:',licht)
print('kern voor (r10):',{int(t):int(((a10==t)&G).sum()) for t in (13,4,3,15,2,1)},' barsten zwart',int(B.sum()))
print('kern na  (r11):',{int(t):int(((o==t)&G).sum()) for t in (13,4,3,15,2)},' barsten nog zwart',int(((o==1)&B).sum()))
d_=o!=a10; KZ=G|B; print('wissels t.o.v. r10:',int(d_.sum()),'buiten kern:',int((d_&~KZ).sum()))
