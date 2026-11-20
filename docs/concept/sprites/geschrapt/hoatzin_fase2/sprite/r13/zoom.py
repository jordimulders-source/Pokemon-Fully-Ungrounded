# zoom.py in.png uit.png x0 y0 x1 y1 K : uitsnede op K-voud met raster (elke 5 groen) naast het model, plus 1x/2x volledig
import sys, numpy as np; from PIL import Image, ImageDraw
f,o=sys.argv[1],sys.argv[2]; x0,y0,x1,y1,K=map(int,sys.argv[3:8])
im=Image.open(f); a=np.asarray(im); pal=np.array(im.getpalette()[:48]).reshape(-1,3)
rgb=np.full(a.shape+(3,),255,'uint8'); rgb[a>0]=pal[a[a>0]]
s=Image.fromarray(rgb).crop((x0,y0,x1,y1)).resize(((x1-x0)*K,(y1-y0)*K),Image.NEAREST)
d=ImageDraw.Draw(s)
for i in range(x1-x0+1):
    if (x0+i)%5==0: d.line([(i*K,0),(i*K,s.size[1])],fill=(0,200,0))
for j in range(y1-y0+1):
    if (y0+j)%5==0: d.line([(0,j*K),(s.size[0],j*K)],fill=(0,200,0))
sc=2.8888889; mx=32; my=8
g=lambda cx,cy:((mx+(cx-6)*sc)*5.12-0.12,(my+(cy-1)*sc)*5.12-0.12)
M=Image.open('../../MODEL.png').convert('RGB'); p=g(x0,y0); q=g(x1,y1)
m=M.crop((int(p[0]),int(p[1]),int(q[0]),int(q[1]))).resize(s.size,Image.LANCZOS)
W=Image.new('RGB',(s.size[0]*2+10,s.size[1]+150),(200,200,200)); W.paste(s,(0,0)); W.paste(m,(s.size[0]+10,0))
full=Image.fromarray(rgb)
for j,bg in enumerate([(248,248,248),(40,40,48)]):
    r=np.full(a.shape+(3,),bg,'uint8'); r[a>0]=pal[a[a>0]]; t=Image.fromarray(r)
    W.paste(t,(8+j*72,s.size[1]+8)); W.paste(t.resize((128,128),Image.NEAREST),(160+j*136,s.size[1]+8))
W.save(o)
