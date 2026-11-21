# zoom.py uit.png y0 y1 x0 x1 S txt [txt..] ; laatste paneel = natief model (2x2 per spritepixel) met fase OY OX uit env
import sys,os,numpy as np; from PIL import Image, ImageDraw; from pal import *
out=sys.argv[1]; y0,y1,x0,x1,S=map(int,sys.argv[2:7]); OY,OX=map(int,os.environ.get('FASE','1 0').split())
nat=np.asarray(Image.open('natief.png').convert('RGB')); bg=np.load('bg.npy')
# spritecoord -> natief: bbox van de reductie
ff=np.load('fam.npy'); 
ims=[rgb(lees(f)) for f in sys.argv[7:]]
H,W=ims[0].shape[:2]; h,w=(nat.shape[0]-OY)//2,(nat.shape[1]-OX)//2
# zoek offset van de bbox in het vakraster
o=np.zeros((h,w),bool)
for j in range(h):
    for i in range(w): o[j,i]=(~bg[OY+2*j:OY+2*j+2,OX+2*i:OX+2*i+2]).sum()>=2
ys,xs=np.where(o); by,bx=ys.min(),xs.min()
m=nat[OY+2*by:OY+2*(by+H),OX+2*bx:OX+2*(bx+W)].copy(); m[bg[OY+2*by:OY+2*(by+H),OX+2*bx:OX+2*(bx+W)]]=232
ims.append(np.asarray(Image.fromarray(m).resize((W,H),Image.NEAREST)) if False else m)
h,w=y1-y0,x1-x0; V=Image.new('RGB',(len(ims)*(w*S+24)+24,h*S+24),(255,255,255)); d=ImageDraw.Draw(V)
for k,r in enumerate(ims):
    ox=24+k*(w*S+24)
    if r.shape[0]==2*H: crop=r[2*y0:2*y1,2*x0:2*x1]
    else: crop=r[y0:y1,x0:x1]
    V.paste(Image.fromarray(crop).resize((w*S,h*S),Image.NEAREST),(ox,24))
    for x in range(w+1): d.line([(ox+x*S,24),(ox+x*S,24+h*S)],fill=(220,90,90) if (x+x0)%5==0 else (205,205,205))
    for y in range(h+1): d.line([(ox,24+y*S),(ox+w*S,24+y*S)],fill=(220,90,90) if (y+y0)%5==0 else (205,205,205))
    for x in range(w):
        if (x+x0)%5==0: d.text((ox+x*S+2,6),str(x+x0),fill=(0,0,0))
for y in range(h):
    if (y+y0)%5==0: d.text((2,24+y*S+2),str(y+y0),fill=(0,0,0))
V.save(out)
