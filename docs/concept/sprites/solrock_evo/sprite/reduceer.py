# Kale reductie van het model naar 64x64: per spritepixel klassefracties uit het model (vlakgemiddelde),
# regels "lichtste/donkerste wint" alleen voor dunne lijnen; kleur = dichtstbijzijnde paletkleur van het klassegemiddelde.
# Niets getekend. Uit: kaal.npy (indices), kaal.png
import numpy as np; from PIL import Image
a=np.asarray(Image.open('../referenties/model.png').convert('RGB')).astype(float)
r,g,b=a[...,0],a[...,1],a[...,2]; mx=a.max(2); mn=a.min(2); sat=mx-mn; lum=a.mean(2)
Y,X=np.mgrid[0:1024,0:1024]; d=np.hypot(X-501.5,Y-496)
bg=(mn>235)&(sat<15)
red=(r-g>70)&(g<75)&~bg
warm=(sat>=40)&~red&~bg
plate=warm&(d<200)&(X<600)   # plaat ligt links in de kern; warm rechts = steenrand
light=~bg&~red&~plate&((warm)|(lum>150))
gray=~bg&~red&~plate&~light
blk=gray&(lum<22)
PAL=[(0,0,0),            #0 transparant
 (14,12,14),             #1 K zwart
 (40,38,40),             #2 G1
 (62,60,60),             #3 G2
 (96,92,88),             #4 G3
 (250,238,204),          #5 L1 creme
 (214,186,128),          #6 L2 goud
 (246,190,96),           #7 P1
 (206,130,52),           #8 P2
 (148,90,34),            #9 P3
 (90,50,16),             #10 P4 lijn
 (206,66,60),            #11 R1
 (128,30,32)]            #12 R2
PAL=np.array(PAL,float)
S=11.87; X0=138-0.5*S; Y0=107-1.2*S
def near(c,ids): 
    ids=list(ids); dd=[((PAL[i]-c)**2).sum() for i in ids]; return ids[int(np.argmin(dd))]
out=np.zeros((64,64),int); F={}
for j in range(64):
    for i in range(64):
        x0,x1=X0+i*S,X0+(i+1)*S; y0,y1=Y0+j*S,Y0+(j+1)*S
        xs=slice(max(0,int(round(x0))),min(1024,int(round(x1)))); ys=slice(max(0,int(round(y0))),min(1024,int(round(y1))))
        n=bg[ys,xs].size
        if n==0: continue
        f={k:m[ys,xs].mean() for k,m in dict(bg=bg,red=red,plate=plate,light=light,gray=gray,blk=blk).items()}
        F[(j,i)]=f
        fig=1-f['bg']
        def mean(m): return a[ys,xs][m[ys,xs]].mean(0)
        pl_line=(plate&(lum<100))[ys,xs].mean()+ (blk[ys,xs]&(d[ys,xs]<200)&False).mean()
        if f['red']>=0.25: c=near(mean(red),[11,12])
        elif f['light']>=0.3 and f['light']>=f['plate']*0.6: c=near(mean(light),[5,6])
        elif fig<0.45: c=0
        elif f['plate']>=0.4:
            if f['blk']>=0.3: c=1
            elif pl_line>=0.4: c=10
            else:
                m=(plate&(lum>=100))[ys,xs]; L=lum[ys,xs][m].mean() if m.any() else 90
                c=7 if L>150 else (8 if L>=105 else 9)
        else:
            if f['blk']>=0.4: c=1
            else:
                m=(gray&~blk)[ys,xs]; L=lum[ys,xs][m].mean() if m.any() else 10
                c=2 if L<36 else (3 if L<75 else 4)
        out[j,i]=c
np.save('kaal.npy',out)
import pickle; pickle.dump(F,open('frac.pkl','wb'))
def save(o,fn):
    im=Image.fromarray(o.astype('uint8'),'P'); p=[int(v) for v in PAL.ravel()]; im.putpalette(p+[0]*(768-len(p))); im.save(fn,transparency=0)
save(out,'kaal.png')
ys,xs=np.where(out>0); print('bbox',xs.min(),xs.max(),ys.min(),ys.max())
