# facetten.py: modelvlakken (facetten) = samenhangende pixels binnen één onderdeel, gescheiden door de modellijnen
# (lijn = helderheid < 115 roze / 100 blauw, baard, haar / 60 donker gesteente, 1 px verdikt om lekjes in de Gemini-lijnen te dichten). Facet < 120 modelpx (< 2 spritepx) telt niet.
# -> facet_full.npz (facet-id per modelpixel), facet_full.png (controlebeeld)
import numpy as np; from PIL import Image; from scipy import ndimage as nd
a=np.asarray(Image.open('../r8/gemini_r8.png').convert('RGB')).astype(float); L=a.mean(2)
Z=np.load('../sprite/model_zone.npz')['z'].astype(int)
DREMPEL={1:60,10:60,11:60,13:60,14:60,2:100,3:100,4:100,12:100}   # donker gesteente heeft vlakken rond 90: lager
DR=np.vectorize(lambda z: DREMPEL.get(z,115))(Z)
lijn=nd.binary_dilation(L<DR,iterations=1)
F=np.zeros(Z.shape,np.int32); FZ=[0]; n=0
for z in range(1,15):
    lab,k=nd.label((~lijn)&(Z==z)&(a.min(2)<235))
    s=nd.sum(np.ones_like(lab),lab,index=np.arange(1,k+1))
    for i in np.where(s>=120)[0]: n+=1; F[lab==i+1]=n; FZ.append(z)
np.savez_compressed('facet_full.npz',F=F,FZ=np.array(FZ))
rng=np.random.default_rng(5); C=np.vstack([[255,255,255],rng.integers(60,255,(n,3))]).astype('uint8')
img=C[F]; img[(F==0)&(a.min(2)<235)]=0
Image.fromarray(img).crop((260,30,760,530)).save('facet_full.png'); print('facetten',n)
