import sys,numpy as np, ld
from PIL import Image,ImageDraw
def blok(a,Z,step=4):
    ys,xs=np.nonzero(a[...,3]); x0,x1,y0,y1=max(0,xs.min()-1),min(a.shape[1],xs.max()+2),max(0,ys.min()-1),min(a.shape[0],ys.max()+2)
    c=a[y0:y1,x0:x1]; H,W=c.shape[:2]; M=22
    img=Image.new('RGB',(W*Z+M,H*Z+M),(255,255,255)); bg=Image.new('RGB',(W*Z,H*Z),(150,210,180))
    im=Image.fromarray(c).resize((W*Z,H*Z),Image.NEAREST); bg.paste(im,(0,0),im); img.paste(bg,(M,M)); d=ImageDraw.Draw(img)
    for i in range(W+1):
        X=M+i*Z; ab=x0+i; s=ab%step==0
        d.line([(X,M),(X,M+H*Z)],fill=(0,0,0) if s else (170,170,170),width=2 if s else 1)
        if s: d.text((X-5,6),str(ab),fill=(200,0,0))
    for j in range(H+1):
        Y=M+j*Z; ab=y0+j; s=ab%step==0
        d.line([(M,Y),(M+W*Z,Y)],fill=(0,0,0) if s else (170,170,170),width=2 if s else 1)
        if s: d.text((1,Y-5),str(ab),fill=(200,0,0))
    return img
L=sys.argv[2:]; rows=[]
for s in L:
    A=blok(ld.front(s),9); B=blok(ld.icon_gba(s),16)
    r=Image.new('RGB',(A.width+B.width+30,max(A.height,B.height)+20),(255,255,255)); r.paste(A,(0,20)); r.paste(B,(A.width+30,20))
    ImageDraw.Draw(r).text((5,2),s,fill=(0,0,200)); rows.append(r)
W=max(r.width for r in rows); H=sum(r.height for r in rows)
o=Image.new('RGB',(W,H),(255,255,255)); y=0
for r in rows: o.paste(r,(0,y)); y+=r.height
o.save(sys.argv[1])
