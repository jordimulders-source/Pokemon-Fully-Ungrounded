import sys
from PIL import Image, ImageDraw
src=Image.open('/home/user/pokemon-fully-ungrounded/docs/concept/sprites/poedelmot/referenties/samengesteld.png').convert('RGB'); x0,y0,x1,y1,S=map(int,sys.argv[2:7])
k=(854-139)/62; X=lambda x:139+(x-1)*k; Y=lambda y:150+(y-17)*k
c=src.crop((int(X(x0)),int(Y(y0)),int(X(x1)),int(Y(y1)))).resize(((x1-x0)*S,(y1-y0)*S),Image.LANCZOS); d=ImageDraw.Draw(c)
for x in range(x0,x1+1):
    d.line([((x-x0)*S,0),((x-x0)*S,c.size[1])],fill=(255,0,0) if x%5==0 else (90,90,90))
    if x%5==0: d.text(((x-x0)*S+1,1),str(x),fill=(255,255,0))
for y in range(y0,y1+1):
    d.line([(0,(y-y0)*S),(c.size[0],(y-y0)*S)],fill=(255,0,0) if y%5==0 else (90,90,90))
    if y%5==0: d.text((1,(y-y0)*S+1),str(y),fill=(255,255,0))
c.save(sys.argv[1])
