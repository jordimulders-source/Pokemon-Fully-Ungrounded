# zones.py (Grass): onderdeel per modelpixel (volle resolutie) uit de familiekaart (fam.py): elk samenhangend vlak tussen de modellijnen
# krijgt een onderdeel op grond van familie + zwaartepunt (gebieden gemeten op het model). Lijnpixels -> dichtstbijzijnde onderdeel.
import numpy as np; from PIL import Image; from scipy import ndimage as nd
from gemeen import ZNAAM
from fam import MODEL
if __name__=='__main__':
    a=np.asarray(Image.open(MODEL).convert('RGB')).astype(int); f=np.load('model_fam.npz')['f'].astype(int)
    L=a.mean(2); lijn=(f==1)|(L<nd.gaussian_filter(L,5)-22)   # donkere modellijnen (ook de donkergroene/-roze) scheiden de vlakken
    lijn=nd.binary_dilation(lijn)
    Z=np.zeros(f.shape,int)
    for fam in (2,3,4,5):
        lab,n=nd.label((f==fam)&~lijn)
        cs=nd.center_of_mass(np.ones_like(lab),lab,range(1,n+1)); sz=nd.sum(np.ones_like(lab),lab,range(1,n+1))
        for i,((cy,cx),s) in enumerate(zip(cs,sz),1):
            m=lab==i
            if fam in (2,3) and s<120: continue    # randjes/antialias (bv. donkere mutsrand die bruin leest): via 'rest' naar het dichtstbijzijnde onderdeel
            if fam==5:     # blad
                if cx>=640: z=16                                   # blaadjes aan de twijg
                elif cx<398 and cy<205: z=2                        # haarplukje L
                elif cx>=505 and cy>=163: z=3                      # haarbladeren R
                elif cy<168 or (cy<190 and cx>=420): z=1           # bladmuts
                else: z=4                                          # baard
            elif fam==3:   # roze hout
                if 375<=cx<=445 and 160<=cy<=225: z=5
                elif cx<330 and cy>=265: z=19                      # vuist L (bol om de stok)
                elif cx<385 and cy>=265: z=7
                elif cx>=668 and cy>=300: z=9
                elif cx>=655 and cy<300: z=8                       # elleboogschijf R
                elif cx>=600 and cy<275: z=18                      # schouderschijf R
                else: z=6
            elif fam==4: z=12
            else:          # bruin (schors)
                if cx<370 and cy>=300: z=11
                elif cy>=452: z=13 if cx<520 else 14
                elif 375<=cy<=440 and s<1500 and (cx<470 or cx>590): z=17   # knoesten op de knieen
                elif cx>=585 and cy<330: z=15                      # rugplank + twijg
                else: z=10
            Z[m]=z
    # haarbladeren R raken de bladmuts zonder donkere lijn: lichtgroen onder/naast de mutspunt = haar R (gemeten op het model)
    yy,xx=np.mgrid[:f.shape[0],:f.shape[1]]
    Z[(f==5)&(xx>=500)&(xx<=600)&(yy>=150)&(yy<=215)&(a[...,1]>=148)]=3
    for k,n in ZNAAM.items(): print(k,n,(Z==k).sum())
    Z[(f==1)|(lijn&(f>0))&(nd.binary_erosion(Z>0)==0)]=Z[(f==1)|(lijn&(f>0))&(nd.binary_erosion(Z>0)==0)]
    rest=(f>0)&(Z==0); print('rest',rest.sum())
    _,(iy,ix)=nd.distance_transform_edt(Z==0,return_indices=True)
    Z[rest]=Z[iy[rest],ix[rest]]
    np.savez_compressed('model_zone.npz',z=Z.astype('uint8'))
    rng=np.random.default_rng(3); C=np.vstack([[255,255,255],rng.integers(40,230,(21,3))]).astype('uint8')
    img=C[Z]; img[f==1]=img[f==1]//3
    Image.fromarray(img).crop((260,30,760,530)).save('model_zone.png')
