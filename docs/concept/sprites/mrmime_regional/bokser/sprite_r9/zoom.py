# zoom.py x0 y0 x1 y1 Z out [sprite.npy ...]: model-uitsnede naast sprites, met raster
import sys,numpy as np; from PIL import Image, ImageDraw
sys.path.insert(0,'../sprite_r6'); from palet import PAL
x0,y0,x1,y1,Z=map(int,sys.argv[1:6]); out=sys.argv[6]; fs=sys.argv[7:]
m=Image.open('../r12.png').convert('RGB'); pad=Image.new('RGB',(1424,1424),(255,255,255)); pad.paste(m,(200,200))
p=10.24; ph=10.25; s=88/63
X=lambda c:200+ph+(12+(c-10)*s)*p; Y=lambda r:200+ph+(5+r*s)*p
ims=[pad.crop((int(X(x0)),int(Y(y0)),int(X(x1)),int(Y(y1)))).resize(((x1-x0)*Z,(y1-y0)*Z),Image.LANCZOS)]
for f in fs:
    a=np.load(f)[y0:y1,x0:x1]; rgb=np.array([(200,230,200)]+PAL[1:],'uint8')[a]
    ims.append(Image.fromarray(rgb).resize(((x1-x0)*Z,(y1-y0)*Z),Image.NEAREST))
W=(x1-x0)*Z; o=Image.new('RGB',(len(ims)*(W+8),(y1-y0)*Z),(255,255,255)); d=ImageDraw.Draw(o)
for i,im in enumerate(ims):
    o.paste(im,(i*(W+8),0))
    for k in range(0,x1-x0+1,1): d.line([(i*(W+8)+k*Z,0),(i*(W+8)+k*Z,(y1-y0)*Z)],fill=(255,0,0) if (x0+k)%5==0 else (200,200,255),width=1)
    for k in range(0,y1-y0+1): d.line([(i*(W+8),k*Z),(i*(W+8)+W,k*Z)],fill=(255,0,0) if (y0+k)%5==0 else (200,200,255),width=1)
o.save(out)
