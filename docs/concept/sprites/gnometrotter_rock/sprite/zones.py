# zones.py: onderdeel per modelpixel (volle resolutie) uit de familiekaart (fam.py) + samenhangende vlakken tussen de modellijnen.
# Schrijft model_zone.npy en model_zone.png. Lijnpixels krijgen het dichtstbijzijnde onderdeel (de voor/achter-regel volgt op spriteniveau).
import numpy as np; from PIL import Image; from scipy import ndimage as nd
ZNAAM={1:'muts+rugkam',2:'haar L',3:'haar R',4:'baard',5:'neus',6:'lijf',7:'arm L+hand',8:'arm R',9:'hand R',10:'riem',11:'stok',12:'broek/benen',13:'zool L',14:'zool R'}
if __name__=='__main__':
    a=np.asarray(Image.open('../r8/gemini_r8.png').convert('RGB')).astype(int); f=np.load('model_fam.npz')['f'].astype(int); lum=a.mean(2)
    Z=np.zeros(f.shape,int)
    def comp(fam,pt):
        lab,_=nd.label(f==fam); x,y=pt
        if f[y,x]!=fam:
            yy,xx=np.where(f[y-15:y+16,x-15:x+16]==fam); i=np.argmin((yy-15)**2+(xx-15)**2); y,x=y-15+yy[i],x-15+xx[i]
        return lab==lab[y,x]
    # grijs
    muts=comp(2,(450,80)); Z[muts]=1
    box=np.zeros_like(muts); box[150:216,510:596]=True
    hr=muts&box&(lum>=140); lab,_=nd.label(hr); hr=lab==lab[180,550]; Z[hr]=3
    Z[comp(2,(370,170))]=2; Z[comp(2,(440,270))]=4
    for pt in ((560,330),(548,342),(450,340),(430,370)): Z[comp(2,pt)&(Z==0)]=10
    Z[comp(2,(318,420))]=11; Z[comp(2,(430,485))]=13; Z[comp(2,(620,500))]=14
    # roze
    Z[comp(3,(425,195))]=5
    for pt in ((500,210),(530,280),(391,280)): Z[comp(3,pt)]=6
    Z[comp(3,(330,305))]=7; Z[comp(3,(683,280))]=8; Z[comp(3,(712,340))]=9
    Z[(f==4)]=12
    for k,n in ZNAAM.items(): print(k,n,(Z==k).sum())
    # rest (lijnen, kleine vlakjes, randpixels) -> dichtstbijzijnde onderdeel
    rest=(f>0)&(Z==0); print('rest',rest.sum())
    _,(iy,ix)=nd.distance_transform_edt(Z==0,return_indices=True)
    Z[rest]=Z[iy[rest],ix[rest]]
    np.savez_compressed('model_zone.npz',z=Z.astype('uint8'))
    rng=np.random.default_rng(3); C=np.vstack([[255,255,255],rng.integers(40,230,(15,3))]).astype('uint8')
    img=C[Z]; img[f==1]=img[f==1]//3
    Image.fromarray(img).crop((260,30,760,530)).save('model_zone.png')
