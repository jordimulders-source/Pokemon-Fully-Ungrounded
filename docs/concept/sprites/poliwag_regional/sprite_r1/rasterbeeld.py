# Meethulp: model met de spritecelgrenzen van reduceer.py + coordinaten. python3 rasterbeeld.py c0 c1 r0 r1 schaal uit.png
import sys, numpy as np; from PIL import Image, ImageDraw
z=np.load('reductie.npz'); xs,ys=z['xs'],z['ys']
c0,c1,r0,r1,s=map(int,sys.argv[1:6]); out=sys.argv[6]
im=Image.open('../referenties/gemini_gekozen_v2.png').convert('RGB')
X0,X1,Y0,Y1=int(xs[c0]),int(xs[c1+1]),int(ys[r0]),int(ys[r1+1])
cr=im.crop((X0,Y0,X1,Y1)).resize(((X1-X0)*s,(Y1-Y0)*s),Image.NEAREST)
cv=Image.new('RGB',(cr.size[0]+30,cr.size[1]+20),'white'); cv.paste(cr,(30,20)); d=ImageDraw.Draw(cv)
for i in range(c0,c1+2):
    x=30+(xs[i]-X0)*s; d.line([(x,20),(x,cv.size[1])],fill=(255,0,255))
    if i<=c1: d.text((x+3,4),str(i),fill=(0,0,0))
for j in range(r0,r1+2):
    y=20+(ys[j]-Y0)*s; d.line([(30,y),(cv.size[0],y)],fill=(255,0,255))
    if j<=r1: d.text((3,y+3),str(j),fill=(0,0,0))
cv.save(out)
