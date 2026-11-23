# zones.py (Ice): onderdeel per modelpixel. Omtrek = Rock r8, dus de Rock-zones zijn de plaatsgids: elke pixel krijgt zijn Rock-zone
# als die bij zijn familie past (ijs: muts/haar/baard/riem/stok/zolen; roze: neus/lijf/armen/handen; blauw: broek), anders de
# dichtstbijzijnde passende zone (zo groeit de ijspegelbaard over het Rock-lijf). Lijnen -> dichtstbijzijnde onderdeel.
import numpy as np; from PIL import Image; from scipy import ndimage as nd
ZNAAM={1:'muts+rugkam',2:'haar L',3:'haar R',4:'baard',5:'neus',6:'lijf',7:'arm L+hand',8:'arm R',9:'hand R',10:'riem',11:'stok',12:'broek/benen',13:'zool L',14:'zool R'}
FZ={2:[1,2,3,4,10,11,13,14],3:[5,6,7,8,9],4:[12]}
if __name__=='__main__':
    f=np.load('model_fam.npz')['f'].astype(int); RZ=np.load('../../gnometrotter_rock/sprite/model_zone.npz')['z'].astype(int)
    Z=np.zeros(f.shape,int)
    for fam,zs in FZ.items():
        m=f==fam; ok=m&np.isin(RZ,zs); Z[ok]=RZ[ok]
        src=np.isin(RZ,zs)&(RZ>0)
        _,(iy,ix)=nd.distance_transform_edt(~src,return_indices=True)
        rest=m&~ok; Z[rest]=RZ[iy[rest],ix[rest]]
    rest=(f>0)&(Z==0)
    _,(iy,ix)=nd.distance_transform_edt(Z==0,return_indices=True); Z[rest]=Z[iy[rest],ix[rest]]
    for k,n in ZNAAM.items(): print(k,n,(Z==k).sum())
    np.savez_compressed('model_zone.npz',z=Z.astype('uint8'))
    rng=np.random.default_rng(3); C=np.vstack([[255,255,255],rng.integers(40,230,(15,3))]).astype('uint8')
    img=C[Z]; img[f==1]=img[f==1]//3
    Image.fromarray(img).crop((260,30,760,530)).save('model_zone.png')
