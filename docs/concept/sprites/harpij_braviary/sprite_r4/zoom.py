# zoom.py uit.png y0 y1 x0 x1 S txt [txt..]  (laatste kolom = modelgemiddelde)
import sys,numpy as np; from PIL import Image, ImageDraw; from pal import *
out=sys.argv[1]; y0,y1,x0,x1,S=map(int,sys.argv[2:7]); avg=np.load('avg.npy'); cov=np.load('cov.npy')
ims=[rgb(lees(f)) for f in sys.argv[7:]]+[np.where((cov>=.5)[:,:,None],avg.clip(0,255),232).astype('uint8')]
h,w=y1-y0,x1-x0; V=Image.new('RGB',(len(ims)*(w*S+24)+24,h*S+24),(255,255,255)); d=ImageDraw.Draw(V)
for k,r in enumerate(ims):
    ox=24+k*(w*S+24); V.paste(Image.fromarray(r[y0:y1,x0:x1]).resize((w*S,h*S),Image.NEAREST),(ox,24))
    for x in range(w+1): d.line([(ox+x*S,24),(ox+x*S,24+h*S)],fill=(220,90,90) if (x+x0)%5==0 else (205,205,205))
    for y in range(h+1): d.line([(ox,24+y*S),(ox+w*S,24+y*S)],fill=(220,90,90) if (y+y0)%5==0 else (205,205,205))
    for x in range(w):
        if (x+x0)%5==0: d.text((ox+x*S+2,6),str(x+x0),fill=(0,0,0))
for y in range(h):
    if (y+y0)%5==0: d.text((2,24+y*S+2),str(y+y0),fill=(0,0,0))
V.save(out)
