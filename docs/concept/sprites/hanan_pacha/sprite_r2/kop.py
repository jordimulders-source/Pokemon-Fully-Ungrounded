# r2 stap 2: kop + kam + snavel + witte kraag als een geheel uit het MODEL r7 geschaald rond het aanzetpunt van de kraag
# op het lijf (Jordi: "de kop is aan de kleine kant ook" + "en schaal de halsband mee"), daarna dezelfde verkleining.
# Gebruik: python3 kop.py 1.35  -> kop_135.npy (spritematrix, 0 = geen kop)
import sys, numpy as np; from PIL import Image
sys.path.insert(0,'gereedschap'); from klassen import klassen; from reduceer import *
f=float(sys.argv[1])
_,cn,_=klassen('natief_r7.png'); H,W=cn.shape; yy,xx=np.mgrid[0:H,0:W]
poly=(yy>=40)&(yy<=84)&(xx<=78)&(((yy<65)&(xx>=43))|((yy>=65)&(xx>=51)))
km=poly&np.isin(cn,[1,2,3,5])
km|=(yy>=55)&(yy<=67)&(xx>=40)&(xx<=50)&(cn==1)      # zwarte snavelomlijning links/onder (model) hoort bij de kop                     # kopmasker in het natieve raster (rood, wit kraag/snavel, lijnen)
ys,xs=np.where(km); onder=ys>=ys.max()-1
A=np.array([0.1+6.4*(xs[onder].mean()+0.5), 0.1+6.4*(ys.max()+1)])   # aanzetpunt: onderkant midden van de kraag
r7=np.asarray(Image.open('../gemini/r7.png').convert('RGB'))
gy,gx=np.mgrid[0:1024,0:1024]
sx=A[0]+(gx-A[0])/f; sy=A[1]+(gy-A[1])/f
u=np.floor((sx-0.1)/6.4).astype(int); v=np.floor((sy-0.1)/6.4).astype(int)
ok=(u>=0)&(v>=0)&(u<W)&(v<H); m=np.zeros((1024,1024),bool); m[ok]=km[v[ok],u[ok]]
laag=np.zeros((1024,1024,4),'uint8')
xi=np.clip(np.round(sx).astype(int),0,1023); yi=np.clip(np.round(sy).astype(int),0,1023)
laag[m,:3]=r7[yi[m],xi[m]]; laag[m,3]=255
c,L=klas(laag[...,:3],laag[...,3])
o,fr=reduceer(c,L,BG=0.5,box=(0,0,64,64))
# snavel: wit-klasse in het snavelvak van het model (natief x43-51, y55-66) apart verkleind, zodat hij niet opgaat in de witte vleugelband
sn=np.zeros((H,W),bool); sn[55:67,43:52]=(cn[55:67,43:52]==5)
ms=np.zeros((1024,1024),bool); ms[ok]=sn[v[ok],u[ok]]
Lr=laag[...,:3].astype(int)@np.array([299,587,114])/1000
nsn=0; snm=np.zeros((64,64),bool)
for Y in range(64):
    for X in range(64):
        x0,y0=s2o(X,Y); x1,y1=s2o(X+1,Y+1); xa,xb,ya,yb=int(round(x0)),int(round(x1)),int(round(y0)),int(round(y1))
        if xb<=0 or yb<=0: continue
        b=ms[max(0,ya):yb,max(0,xa):xb]
        if b.size and b.sum()/((yb-ya)*(xb-xa))>=0.40 and o[Y,X]!=1:
            o[Y,X]=7 if Lr[max(0,ya):yb,max(0,xa):xb][b].mean()>=222 else 14; nsn+=1; snm[Y,X]=True
print('snavelpixels',nsn)
np.save('kop_%d.npy'%round(f*100),o); np.save('snavel_%d.npy'%round(f*100),snm); print('kop x%.2f: aanzet orig (%.0f,%.0f) sprite (%.1f,%.1f), px %d'%(f,A[0],A[1],*o2s(*A),(o>0).sum()))
