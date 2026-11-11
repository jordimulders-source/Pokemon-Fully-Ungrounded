# Voegt het omcirkelde kanon uit r5 (Jordi) in r10. Gebruik: python3 voeg.py X5 Y5 XC
import sys; from PIL import Image, ImageDraw, ImageFilter; import numpy as np
X5,Y5,XC=map(int,sys.argv[1:4])
J=np.asarray(Image.open('samenvoeg/jordi_omcirkeld.png').convert('RGB')).astype(int)
red=(J[:,:,0]>190)&(J[:,:,1]<90)&(J[:,:,2]<90)
R=Image.fromarray((red*255).astype('uint8')).filter(ImageFilter.MaxFilter(5)); ImageDraw.floodfill(R,(0,0),128)
k=1024/496; m=np.asarray(Image.fromarray(((np.asarray(R)!=128)*255).astype('uint8')).resize((1024,round(282*k)),Image.NEAREST).crop((0,0,1024,559)))>0
a=np.asarray(Image.open('referenties/gemini_gekozen_r5.png').convert('RGB')).astype(int)
yy,xx=np.mgrid[0:559,0:1024]
M=m&(a.min(axis=2)<235)&(xx<X5)&(yy>=Y5)
s=1.24; ox=round(392-360*s); oy=round(221-200*s)
piece=Image.fromarray(np.dstack([a,M*255]).astype('uint8'),'RGBA').resize((round(1024*s),round(559*s)),Image.NEAREST)
r10=Image.open('gemini/r10_rupsband.png').convert('RGBA'); out=r10.copy(); out.alpha_composite(piece,(ox,oy))
b=np.asarray(r10).copy(); o=np.asarray(out).copy()
Y,X=np.mgrid[0:b.shape[0],0:b.shape[1]]
YC=int(sys.argv[4]) if len(sys.argv)>4 else 9999
keep=((X>=XC)|((Y<YC)&(X>=380)))&(b[:,:,:3].min(axis=2)<235)
o[keep]=b[keep]
Image.fromarray(o).convert('RGB').save('samenvoeg/v1.png')
