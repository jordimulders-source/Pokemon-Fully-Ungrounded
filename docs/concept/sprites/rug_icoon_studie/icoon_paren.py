"""Vel: front (GBA, verkleind tot icoonhoogte) | icoon frame 1 | icoon frame 2, op 4x en 1x.
python3 icoon_paren.py uit.png soort ..."""
import sys,numpy as np
from PIL import Image,ImageDraw
def load(p,pal=None):
    im=Image.open(p); ix=np.array(im)
    if pal:
        L=open(pal).read().split('\n'); P=[tuple(int(v) for v in L[3+k].split()[:3]) for k in range(16)]
    else:
        q=im.getpalette()[:48]; P=[tuple(q[3*k:3*k+3]) for k in range(16)]
    o=np.zeros(ix.shape+(4,),np.uint8)
    for k in range(1,16): o[ix==k]=P[k]+(255,)
    return Image.fromarray(o)
sps=sys.argv[2:]; C=4; Z=4; cw=3*32*Z+40; ch=32*Z+50
img=Image.new('RGB',(C*cw,((len(sps)+C-1)//C)*ch),(115,197,164)); d=ImageDraw.Draw(img)
for n,sp in enumerate(sps):
    D='graphics/pokemon/'+sp
    f=load(D+'/anim_front_gba.png',D+'/normal_gba.pal').crop((0,0,64,64)); f=f.crop(f.getbbox())
    ic=load(D+'/icon_gba.png'); i1=ic.crop((0,0,32,32)); i2=ic.crop((0,32,32,64)); h=i1.getbbox()[3]-i1.getbbox()[1]
    s=h/f.size[1]; fs=f.resize((max(1,round(f.size[0]*s)),h),Image.BOX)
    a=np.array(fs); a[...,3]=np.where(a[...,3]>110,255,0); fs=Image.fromarray(a)
    c=Image.new('RGBA',(32,32)); c.paste(fs,(16-fs.size[0]//2,30-h),fs)
    x,y=(n%C)*cw,(n//C)*ch; d.text((x+4,y+2),sp,fill=0)
    for k,p in enumerate([c,i1,i2]):
        q=p.resize((128,128),Image.NEAREST); img.paste(q,(x+4+k*(128+8),y+12),q); img.paste(p,(x+4+k*(128+8)+48,y+12+128+2),p)
img.save(sys.argv[1])
