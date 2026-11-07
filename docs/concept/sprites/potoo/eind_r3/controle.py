# Controle eind_r3 t.o.v. eind_r2: diff buiten zone, randprofiel, open randen, losse pixels, clusters < 3 px, aantal kleuren.
import numpy as np; from PIL import Image
from scipy import ndimage
o=np.array(Image.open('../eind_r2/potoo.png')); n=np.array(Image.open('potoo.png'))
Z=lambda x,y: 40<=x<=47 and 28<=y<=50
d=[(int(x),int(y)) for y,x in np.argwhere(o!=n)]
print('gewijzigd',len(d),'px; buiten zone x40-47 y28-50:',[p for p in d if not Z(*p)])
print('palet gelijk:',Image.open('../eind_r2/potoo.png').getpalette()==Image.open('potoo.png').getpalette())
print('rechterrand per rij (y24-58) r2 -> r3:')
for y in range(24,59):
    print(f'  {y}: {np.where(o[y]>0)[0].max()} -> {np.where(n[y]>0)[0].max()}')
def openrand(a):
    r=[]
    for y,x in np.argwhere(a>0):
        nb=[a[y+dy,x+dx] if 0<=y+dy<64 and 0<=x+dx<64 else 0 for dx,dy in ((1,0),(-1,0),(0,1),(0,-1))]
        if 0 in nb and a[y,x]!=1: r.append((int(x),int(y),int(a[y,x])))
    return r
for nm,a in (('r2',o),('r3',n)):
    orr=openrand(a); print(nm,'open randen (niet-zwart naast transparant):',len(orr),'in zone:',[p for p in orr if Z(p[0],p[1])])
def kleine(a):
    out=[]
    for k in np.unique(a):
        if k==0: continue
        lab,m=ndimage.label(a==k)
        for i in range(1,m+1):
            pts=np.argwhere(lab==i)
            if len(pts)<3: out.append((int(k),[(int(x),int(y)) for y,x in pts]))
    return out
for nm,a in (('r2',o),('r3',n)):
    kl=kleine(a); zk=[c for c in kl if any(Z(*p) for p in c[1])]
    print(nm,'clusters < 3 px (4-buren):',len(kl),'| raken zone:',zk)
    print(nm,'  waarvan losse pixels:',sum(len(c[1])==1 for c in kl),'| aantal kleuren:',len(np.unique(a[a>0])))
