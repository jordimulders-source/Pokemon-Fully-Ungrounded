# Toon een geïndexeerde sprite op 12x met coördinatenraster, en optioneel het natieve model op dezelfde schaal ernaast
import sys, numpy as np; from PIL import Image, ImageDraw
src,out=sys.argv[1],sys.argv[2]; S=12
im=Image.open(src); p=im.getpalette(); a=np.asarray(im)
ys,xs=np.where(a>0); y0,y1,x0,x1=max(ys.min()-1,0),ys.max()+2,max(xs.min()-1,0),xs.max()+2
c=a[y0:y1,x0:x1]; h,w=c.shape
v=Image.new('RGB',(w*S+30,h*S+30),'white'); d=ImageDraw.Draw(v)
for j in range(h):
    for i in range(w):
        k=c[j,i]; col=(255,255,255) if k==0 else tuple(p[3*k:3*k+3])
        d.rectangle([30+i*S,30+j*S,30+i*S+S-1,30+j*S+S-1],fill=col)
for i in range(w+1):
    d.line([30+i*S,30,30+i*S,30+h*S],fill=(200,200,255) if (x0+i)%5 else (255,0,0))
    if (x0+i)%5==0: d.text((30+i*S,2),str(x0+i),fill='red')
for j in range(h+1):
    d.line([30,30+j*S,30+w*S,30+j*S],fill=(200,200,255) if (y0+j)%5 else (255,0,0))
    if (y0+j)%5==0: d.text((2,30+j*S),str(y0+j),fill='red')
v.save(out)
