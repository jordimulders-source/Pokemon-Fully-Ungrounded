# modeluitsnede (1024-model) met spriteraster en coördinaten; gebruik: modelgrid.py cx0 cy0 cx1 cy1 K uit.png [overlay.png]
import sys, numpy as np; from PIL import Image, ImageDraw
cx0,cy0,cx1,cy1,K=map(int,sys.argv[1:6])
s=2.8888889; x0=32; y0=8
f=lambda cx,cy:((x0+(cx-6)*s)*5.12-0.12,(y0+(cy-1)*s)*5.12-0.12)
im=Image.open('../../MODEL.png').convert('RGB')
a=f(cx0,cy0); b=f(cx1,cy1)
m=im.crop((int(round(a[0])),int(round(a[1])),int(round(b[0])),int(round(b[1])))).resize(((cx1-cx0)*K,(cy1-cy0)*K),Image.LANCZOS).convert('RGBA')
if len(sys.argv)>7:
    sp=Image.open(sys.argv[7]).convert('RGBA').crop((cx0,cy0,cx1,cy1)).resize(m.size,Image.NEAREST)
    al=np.array(sp); al[...,3]=(al[...,3]>0)*150; m.alpha_composite(Image.fromarray(al))
d=ImageDraw.Draw(m)
for i in range(cx1-cx0+1): d.line([(i*K,0),(i*K,m.size[1])],fill=(0,200,0,255) if (cx0+i)%5==0 else (160,160,160,120))
for j in range(cy1-cy0+1): d.line([(0,j*K),(m.size[0],j*K)],fill=(0,200,0,255) if (cy0+j)%5==0 else (160,160,160,120))
for i in range(cx1-cx0):
    if (cx0+i)%2==0: d.text((i*K+2,1),str(cx0+i),fill=(0,0,0,255))
for j in range(cy1-cy0):
    if (cy0+j)%2==0: d.text((1,j*K+2),str(cy0+j),fill=(0,0,0,255))
m.save(sys.argv[6])
