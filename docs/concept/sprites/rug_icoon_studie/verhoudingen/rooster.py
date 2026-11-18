"""Werkvel om punten af te lezen: front en icoon (frame 1) uitvergroot met pixelrooster en absolute coordinaten.
python3 rooster.py uit.png soort"""
import sys,numpy as np
from PIL import Image,ImageDraw
from laad import front,icoon
def blok(a,Z,step):
    ys,xs=np.nonzero(a[...,3]); x0,x1,y0,y1=max(0,xs.min()-1),min(a.shape[1],xs.max()+2),max(0,ys.min()-1),min(a.shape[0],ys.max()+2)
    c=a[y0:y1,x0:x1]; H,W=c.shape[:2]; M=24
    img=Image.new('RGB',(W*Z+M,H*Z+M),(255,255,255)); bg=Image.new('RGB',(W*Z,H*Z),(150,210,180))
    im=Image.fromarray(c).resize((W*Z,H*Z),Image.NEAREST); bg.paste(im,(0,0),im); img.paste(bg,(M,M)); d=ImageDraw.Draw(img)
    for i in range(W+1):
        X=M+i*Z; ab=x0+i; d.line([(X,M),(X,M+H*Z)],fill=(0,0,0) if ab%step==0 else (120,120,120),width=2 if ab%step==0 else 1)
        if ab%step==0: d.text((X-6,4),str(ab),fill=(200,0,0))
    for j in range(H+1):
        Y=M+j*Z; ab=y0+j; d.line([(M,Y),(M+W*Z,Y)],fill=(0,0,0) if ab%step==0 else (120,120,120),width=2 if ab%step==0 else 1)
        if ab%step==0: d.text((2,Y-5),str(ab),fill=(200,0,0))
    return img
sp=sys.argv[2]; A=blok(front(sp),14,2); B=blok(icoon(sp),20,2)
img=Image.new('RGB',(A.width+B.width+20,max(A.height,B.height)),(255,255,255)); img.paste(A,(0,0)); img.paste(B,(A.width+20,0)); img.save(sys.argv[1])
