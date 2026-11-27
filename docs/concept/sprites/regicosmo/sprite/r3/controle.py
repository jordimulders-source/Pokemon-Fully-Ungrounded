# Controle: kleuren, maat, losse delen, zwart aan de lichtkant (transparante buur links/boven), losse tintpixels per deel.
import sys,os; sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
import numpy as np; from PIL import Image; from scipy import ndimage; import gemeen as g
f=sys.argv[1] if len(sys.argv)>1 else os.path.join(g.D,'regicosmo_r1.png')
im=Image.open(f); a=np.array(im); print(im.mode,im.size,'transparency',im.info.get('transparency'),'kleuren',len(np.unique(a)))
ys,xs=np.where(a>0); print('bbox x%d-%d y%d-%d (%dx%d), %d px'%(xs.min(),xs.max(),ys.min(),ys.max(),xs.max()-xs.min()+1,ys.max()-ys.min()+1,len(xs)))
lab,n=ndimage.label(a>0,np.ones((3,3))); print('losse delen (8-samenhang):',n,'grootte',sorted(np.bincount(lab.ravel())[1:]))
P=np.array(im.getpalette()[:3*256]).reshape(-1,3); zw=[i for i in range(1,len(P)) if tuple(P[i])==(16,16,16)][0]
p=np.pad(a,1)
licht=[(x,y) for y,x in zip(*np.where(a==zw)) if p[y+1,x]==0 or p[y,x+1]==0]
licht_strikt=[(x,y) for (x,y) in licht if not (p[y+1,x+2]==0 or p[y+2,x+1]==0)]
print('zwart met transparante buur links/boven:',len(licht),'waarvan zonder transparante buur rechts/onder:',licht_strikt)
# losse pixels: 4-buren allemaal een andere kleur (geen lijn/stip)
los=[]
for y,x in zip(*np.where(a>0)):
    b=[p[y,x+1],p[y+2,x+1],p[y+1,x],p[y+1,x+2]]
    if a[y,x]!=zw and all(v!=a[y,x] for v in b) and all(v>0 for v in b): los.append((x,y,tuple(P[a[y,x]])))
print('losse binnenpixels (4-buren anders):',len(los))
for l in los: print('  ',l)
