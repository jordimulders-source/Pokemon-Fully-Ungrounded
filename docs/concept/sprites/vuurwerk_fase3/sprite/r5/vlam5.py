# r5 punt 3: losse vlam rechtsboven (x 38-46, y 3-6) opnieuw uit het model: dekking >= 0,35 per spritepixel (12x12 modelpx);
# mediane modelkleur -> dichtstbijzijnde van de rode tinten (12 licht, 11 midden, 10 donker); onderrand (schaduwkant): de
# donkerste 30% van het blok -> 10 / 1 / 11 (de vlam heeft in het model een donkerrode onderrand en een lichtere top).
import json, numpy as np; from PIL import Image
PAL=np.array(json.load(open('palet.json')),float)
M=np.asarray(Image.open('../../referenties/model_v14.png').convert('RGB')).astype(float); lum=M@[0.299,0.587,0.114]
fg=np.load('../r4/model_fg.npz')['fg']
def vlam(a):
    a=a.copy(); FZ=[(y,x) for y in range(3,7) for x in range(38,47)]
    for y,x in FZ: a[y,x]=0
    cov={}; 
    for y,x in FZ:
        sl=(slice(120+12*y,132+12*y),slice(106+12*x,118+12*x)); cov[(y,x)]=fg[sl].mean()
    on={p for p in FZ if cov[p]>=0.35}
    for (y,x) in on:
        sl=(slice(120+12*y,132+12*y),slice(106+12*x,118+12*x)); f=fg[sl]; c=M[sl][f]; l=lum[sl][f]
        rand=(y+1,x) not in on                    # schaduwkant (onderrand) donker; top en punt houden de modelkleur
        if rand: ks=[10,1,11]; col=c[l<=np.percentile(l,30)].mean(0)
        else: ks=[12,11,10]; col=np.median(c,0)
        a[y,x]=ks[int(((PAL[ks]-col)**2).sum(1).argmin())]
    return a
if __name__=='__main__':
    r4=np.asarray(Image.open('../r4/sprite.png')).astype(int); b=vlam(r4); HX='.123456789ABCDEF'
    for y in range(2,8): print(y,''.join(HX[v] for v in r4[y,36:48]),'  ',''.join(HX[v] for v in b[y,36:48]))
