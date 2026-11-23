# delen.py: onderdelen van het roze en blauwe lijf UIT HET MODEL. Het model wordt geknipt langs zijn eigen donkere lijnen
# (helderheid < 100): samenhangende roze/blauwe vlakken (1 px geerodeerd, > 250 modelpx) = delen; lijn- en barstpixels krijgen
# het dichtstbijzijnde deel. Per spritepixel: deel met het grootste gewicht. -> deel.npy (sprite) + deel_model.png (controle)
import sys, numpy as np; from scipy import ndimage as nd; from PIL import Image
sys.path.insert(0,'../sprite')
from reductie_gedeeld import bron
from reductie_ice import laad
a,FG=laad(); L=0.3*a[...,0]+0.59*a[...,1]+0.11*a[...,2]
f=np.load('../sprite/model_fam.npz')['f']
D=np.zeros(f.shape,int); naam={}; k=0
for fam,nm in ((3,'roze'),(4,'blauw')):
    m=nd.binary_erosion((f==fam)&(L>=100),iterations=1); lab,n=nd.label(m)
    for i in range(1,n+1):
        mm=lab==i
        if mm.sum()>250:
            k+=1; D[mm]=k; ys,xs=np.where(mm)
            naam[k]=(nm,(xs.min()-512)/8.1+32,(xs.max()-512)/8.1+32,60-(523-ys.min())/8.1,60-(523-ys.max())/8.1)
    rest=np.isin(f,[fam,1])&(D==0)
    src=np.isin(D,[j for j in naam if naam[j][0]==nm])
    _,(iy,ix)=nd.distance_transform_edt(~src,return_indices=True)
    r=rest&(nd.distance_transform_edt(~src)<12)
    D[r]=D[iy[r],ix[r]]
for j,v in naam.items(): print(j,v[0],'x%.0f-%.0f y%.0f-%.0f'%v[1:])
zone=np.load('../sprite/zone_af.npy'); deel=np.zeros((64,64),int)
for Y,X in zip(*np.where(np.isin(zone,[5,6,7,8,9,12]))):
    w={}
    for u,v,ww in bron(X,Y):
        if D[v,u]: w[D[v,u]]=w.get(D[v,u],0)+ww
    if w: deel[Y,X]=max(w,key=w.get)
np.save('deel.npy',deel)
rng=np.random.default_rng(5); C=np.vstack([[255,255,255],rng.integers(40,230,(40,3))]).astype('uint8')
Image.fromarray(C[D]).crop((260,30,760,530)).save('deel_model.png')
for Y in range(14,58): print('%2d '%Y+''.join(('%x'%deel[Y,X] if deel[Y,X] else '.') for X in range(0,64)))
