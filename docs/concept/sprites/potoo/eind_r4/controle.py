# Controle eind_r4 t.o.v. eind_r3: diff buiten zone, bovenrand per kolom, open randen, losse pixels, clusters < 3 px, kleuren.
import numpy as np; from PIL import Image
from scipy import ndimage
o=np.array(Image.open('../eind_r3/potoo.png')); n=np.array(Image.open('potoo.png'))
Z=lambda x,y: 18<=x<=42 and 0<=y<=5
d=[(int(x),int(y)) for y,x in np.argwhere(o!=n)]
print('gewijzigd',len(d),'px; buiten zone x18-42 y0-5:',[p for p in d if not Z(*p)])
print('rijen y>=6 identiek:',bool((o[6:]==n[6:]).all()),'| palet gelijk:',Image.open('../eind_r3/potoo.png').getpalette()==Image.open('potoo.png').getpalette())
print('bovenste pixel per kolom x22-40 (r3 -> r4):')
for x in range(22,41):
    f=lambda a: int(np.where(a[:,x]>0)[0].min()); print(f'  x{x}: y{f(o)} -> y{f(n)}')
def openrand(a):
    r=[]
    for y,x in np.argwhere(a>0):
        nb=[a[y+dy,x+dx] if 0<=y+dy<64 and 0<=x+dx<64 else 0 for dx,dy in ((1,0),(-1,0),(0,1),(0,-1))]
        if 0 in nb and a[y,x] not in (1,2,3,4): r.append((int(x),int(y),int(a[y,x])))
    return r
for nm,a in (('r3',o),('r4',n)):
    orr=openrand(a); print(nm,'lichte kleur (niet 1-4) naast transparant:',len(orr),'in zone:',[p for p in orr if Z(p[0],p[1])])
def kleine(a):
    out=[]
    for k in np.unique(a):
        if k==0: continue
        lab,m=ndimage.label(a==k)
        for i in range(1,m+1):
            pts=np.argwhere(lab==i)
            if len(pts)<3: out.append((int(k),[(int(x),int(y)) for y,x in pts]))
    return out
for nm,a in (('r3',o),('r4',n)):
    kl=kleine(a); zk=[c for c in kl if any(Z(*p) for p in c[1])]
    print(nm,'clusters < 3 px (4-buren):',len(kl),'| raken zone:',zk)
    print(nm,'  waarvan losse pixels:',sum(len(c[1])==1 for c in kl),'| aantal kleuren:',len(np.unique(a[a>0])))
lab,m=ndimage.label(n>0); print('r4 aantal losse delen (4-buren, ondoorzichtig):',m,'| r3:',ndimage.label(o>0)[1])
lab,m=ndimage.label(n>0,structure=np.ones((3,3))); print('r4 aantal losse delen (8-buren):',m,'| r3:',ndimage.label(o>0,structure=np.ones((3,3)))[1])
