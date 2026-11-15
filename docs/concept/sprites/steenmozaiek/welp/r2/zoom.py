# zoom.py sx0 sx1 sy0 sy1 uit [npy]: model (natief) met spriterooster | sprite, zelfde schaal
import sys; from PIL import Image, ImageDraw; import numpy as np
from reduceer import X0,X1,Y0,Y1
import os; PAL=np.load('FIN2.npy' if os.path.exists('FIN2.npy') else 'FIN.npy')[1:]
sx0,sx1,sy0,sy1=map(int,sys.argv[1:5]); OUT=sys.argv[5]; NPY=sys.argv[6] if len(sys.argv)>6 else 'onderlaag_50.npy'
TW=np.load(NPY).shape[1]; s=(X1-X0)/TW; Z=int(66/s*1) if False else 20; C=int(round(s*Z))
n=Image.open('natief.png').convert('RGB')
c=n.crop((int(X0+sx0*s),int(Y0+sy0*s),int(X0+sx1*s)+1,int(Y0+sy1*s)+1)); c=c.resize((c.width*Z,c.height*Z),Image.NEAREST)
d=ImageDraw.Draw(c); ox=(X0+sx0*s)-int(X0+sx0*s); oy=(Y0+sy0*s)-int(Y0+sy0*s)
for i in range(sx1-sx0+1): x=(ox+i*s)*Z; d.line([(x,0),(x,c.height)],fill=(0,255,0))
for j in range(sy1-sy0+1): y=(oy+j*s)*Z; d.line([(0,y),(c.width,y)],fill=(0,255,0))
a=np.load(NPY)[sy0:sy1,sx0:sx1]; im=np.full(a.shape+(3,),(235,235,225),'uint8'); m=a>0; im[m]=PAL[a[m]-1] if PAL.shape[0]>=a.max() else 0
sp=Image.fromarray(im).resize(((sx1-sx0)*C,(sy1-sy0)*C),Image.NEAREST); d2=ImageDraw.Draw(sp)
for i in range(sx1-sx0): d2.text((i*C+2,2),str((sx0+i)%10),fill=(0,160,0))
for j in range(sy1-sy0): d2.text((2,j*C+2),str(sy0+j),fill=(0,160,0))
out=Image.new('RGB',(c.width+sp.width+20,max(c.height,sp.height)),(255,255,255)); out.paste(c,(0,0)); out.paste(sp,(c.width+20,0)); out.save(OUT)
