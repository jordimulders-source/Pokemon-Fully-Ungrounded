# Kanon lager: alleen loop + steel uit r5 (x<X5, y>=Y5 in r5), tentakel verdwijnt achter r10 vanaf XC (r10). Gebruik: python3 plak2.py X5 Y5 XC
import sys; from PIL import Image; import numpy as np
X5,Y5,XC=map(int,sys.argv[1:4]); DY=int(sys.argv[4]) if len(sys.argv)>4 else 0; s=1.24; ox=round(392-360*s); oy=round(221-200*s)+DY
a=np.asarray(Image.open('referenties/gemini_gekozen_r5.png').convert('RGB')); H,W=a.shape[:2]
yy,xx=np.mgrid[0:H,0:W]
M=(np.asarray(Image.open('samenvoeg/kanon_masker.png'))>0)&(a.min(axis=2)<235)&(xx<X5)&(yy>=Y5)
piece=Image.fromarray(np.dstack([a,M*255]).astype('uint8'),'RGBA').resize((round(W*s),round(H*s)),Image.NEAREST)
r10=Image.open('gemini/r10_rupsband.png').convert('RGBA'); out=r10.copy(); out.alpha_composite(piece,(ox,oy))
b=np.asarray(r10); o=np.asarray(out).copy(); Y,X=np.mgrid[0:b.shape[0],0:b.shape[1]]
keep=(X>=XC)&(b[:,:,:3].min(axis=2)<235); o[keep]=b[keep]
Image.fromarray(o).convert('RGB').save('samenvoeg/v2.png')
