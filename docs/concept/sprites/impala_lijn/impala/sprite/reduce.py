# Kale reductie van model_r5 (1024, illustratie, geen natief raster) -> HOOGTE px hoog.
# Per spritecel: alpha = aandeel voorgrond (fg.py/witlab) >= 0.45; cel met >=50% zwarte modellijn = lijn, anders
# vlakgemiddelde over de niet-lijnpixels (kaal_nla) -> dichtstbijzijnde kleur uit het modelpalet (k-means K=16 op de modelvoorgrond). Variant 'mode' = meest
# voorkomende modelpaletkleur in de cel. Zone per cel = meeste niet-lijnpixels per zone (seg.py-vlakken).
# kaal_nla = vlakgemiddelde zonder de zwarte modellijn (vlakkleur onder de lijn).
# Uit: kaal.png/kaal_mode.png (+10x), kaal_lab.npy, kaal_mode_lab.npy, kaal_avg.npy, kaal_zone.npy, kaal_lf.npy (aandeel lijn), model_pal.npy
import sys, numpy as np, json
from PIL import Image
HOOGTE=int(sys.argv[1]) if len(sys.argv)>1 else 63
a=np.asarray(Image.open('../referenties/model_r5.png').convert('RGB')).astype(float)
wl=np.load('witlab.npz')['a']; fg=~((wl==-2)|(wl==1))
seg=np.load('seg.npz')['a']
ZONES={'staal':[14,49],'kuif':[446,800],'oog':[783,803],'neus':[862,873]}
zmap=np.zeros(seg.shape,int)            # 0 vacht, 1 staal, 2 kuif, 3 oog, 4 neus, 5 lijn
for zi,(z,ids) in enumerate(ZONES.items(),1):
    zmap[np.isin(seg,ids)]=zi
ids,cnt=np.unique(seg[seg>=0],return_counts=True); klein=ids[cnt<150]   # randjes anti-aliasing tussen lijn en achtergrond
lijn=fg&((seg<0)|np.isin(seg,klein)); zmap[lijn]=5
nat=a[fg][::5]
rng=np.random.default_rng(3); K=16
C=nat[rng.choice(len(nat),K,replace=False)]
for _ in range(80):
    lab=((nat[:,None,:]-C[None])**2).sum(2).argmin(1)
    C=np.array([nat[lab==k].mean(0) if (lab==k).any() else C[k] for k in range(K)])
C=C[np.argsort(C.sum(1))]
labm=np.zeros(a.shape[:2],int)
for y in range(0,1024,128):
    labm[y:y+128]=((a[y:y+128].reshape(-1,1,3)-C[None])**2).sum(2).argmin(1).reshape(-1,1024)
ys,xs=np.nonzero(fg); x0,x1,y0,y1=xs.min(),xs.max()+1,ys.min(),ys.max()+1
p=(y1-y0)/HOOGTE; W=int(np.ceil((x1-x0)/p))
out=-np.ones((HOOGTE,W),int); mode=-np.ones((HOOGTE,W),int); avg=np.zeros((HOOGTE,W,3)); zone=-np.ones((HOOGTE,W),int); lf=np.zeros((HOOGTE,W)); nla=np.zeros((HOOGTE,W,3)); lfc=np.zeros((HOOGTE,W))
for j in range(HOOGTE):
    for i in range(W):
        xa,xb=int(round(x0+i*p)),int(round(x0+(i+1)*p)); ya,yb=int(round(y0+j*p)),int(round(y0+(j+1)*p))
        f=fg[ya:yb,xa:xb]
        if f.size==0 or f.mean()<0.45: continue
        m=a[ya:yb,xa:xb][f].mean(0); avg[j,i]=m
        mode[j,i]=np.bincount(labm[ya:yb,xa:xb][f],minlength=K).argmax()
        zz=zmap[ya:yb,xa:xb][f]; lf[j,i]=(zz==5).mean()
        nl=zz!=5
        if nl.any(): nla[j,i]=a[ya:yb,xa:xb][f][nl].mean(0)
        q=int(p*0.25); cz=zmap[ya+q:yb-q,xa+q:xb-q]; cf=fg[ya+q:yb-q,xa+q:xb-q]; lfc[j,i]=(cz[cf]==5).mean() if cf.any() else 1
        out[j,i]=0 if lf[j,i]>=0.5 else ((C-nla[j,i])**2).sum(1).argmin()   # kaal: lijncel = modellijn, anders vlakkleur onder de lijn
        nz=zz[zz!=5]; zone[j,i]=np.bincount(nz,minlength=6).argmax() if len(nz) else 5
np.save('kaal_lab.npy',out); np.save('kaal_mode_lab.npy',mode); np.save('model_pal.npy',C)
np.save('kaal_avg.npy',avg); np.save('kaal_zone.npy',zone); np.save('kaal_lf.npy',lf); np.save('kaal_nla.npy',nla); np.save('kaal_lfc.npy',lfc)
json.dump({'x0':int(x0),'y0':int(y0),'p':p,'W':W,'H':HOOGTE},open('kaal_meta.json','w'))
for L,n in [(out,'kaal'),(mode,'kaal_mode')]:
    img=np.zeros((HOOGTE,W,4),'uint8')
    for j in range(HOOGTE):
        for i in range(W):
            if L[j,i]>=0: img[j,i,:3]=C[L[j,i]]; img[j,i,3]=255
    Image.fromarray(img).save(n+'.png'); Image.fromarray(img).resize((W*10,HOOGTE*10),Image.NEAREST).save(n+'_10x.png')
print('pitch',p,'W',W,'px',(out>=0).sum()); [print(k,C[k].astype(int)) for k in range(K)]
