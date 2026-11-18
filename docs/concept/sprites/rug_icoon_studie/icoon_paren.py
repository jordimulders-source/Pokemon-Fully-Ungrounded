"""Vel: front (GBA, verkleind tot icoonhoogte) | icoon frame 1 | icoon frame 2, op 4x en 1x.
python3 icoon_paren.py uit.png [--new] soort ...  (--new: in-game set, bv. Gen 9)"""
import sys,numpy as np
from PIL import Image,ImageDraw
def load(p,pal=None):
    im=Image.open(p); ix=np.array(im)
    if pal:
        L=open(pal).read().split('\n'); n=int(L[2]); P=[tuple(int(v) for v in L[3+k].split()[:3]) for k in range(n)]+[(0,0,0)]*(16-n)
    else:
        q=im.getpalette()[:48]; P=[tuple(q[3*k:3*k+3]) for k in range(16)]
    o=np.zeros(ix.shape+(4,),np.uint8)
    for k in range(1,16): o[ix==k]=P[k]+(255,)
    return Image.fromarray(o)
import os,re
args=sys.argv[2:]; NEW='--new' in args; sps=[a for a in args if a!='--new']
IPI={}
for fn in os.listdir('src/data/pokemon/species_info'):
    for mm in re.finditer(r'\[SPECIES_([A-Z0-9_]+)\]\s*=\s*\{(.*?)\n    \},',open('src/data/pokemon/species_info/'+fn).read(),re.S):
        v=re.search(r'iconPalIndex = (?:P_GBA_STYLE_SPECIES_ICONS \? \d : )?(\d)',mm.group(2))
        if v: IPI[mm.group(1).lower()]=int(v.group(1))
C=4; Z=4; cw=3*32*Z+40; ch=32*Z+50
img=Image.new('RGB',(C*cw,((len(sps)+C-1)//C)*ch),(115,197,164)); d=ImageDraw.Draw(img)
for n,sp in enumerate(sps):
    D='graphics/pokemon/'+sp
    if NEW:
        fp=D+'/anim_front.png' if os.path.exists(D+'/anim_front.png') else D+'/front.png'
        f=load(fp,D+'/normal.pal').crop((0,0,64,64)); f=f.crop(f.getbbox())
        ic=load(D+'/icon.png','graphics/pokemon/icon_palettes/pal%d.pal'%IPI.get(sp,0))
    else:
        f=load(D+'/anim_front_gba.png',D+'/normal_gba.pal').crop((0,0,64,64)); f=f.crop(f.getbbox())
        ic=load(D+'/icon_gba.png')
    i1=ic.crop((0,0,32,32)); i2=ic.crop((0,32,32,64)); h=i1.getbbox()[3]-i1.getbbox()[1]
    s=h/f.size[1]; fs=f.resize((max(1,round(f.size[0]*s)),h),Image.BOX)
    a=np.array(fs); a[...,3]=np.where(a[...,3]>110,255,0); fs=Image.fromarray(a)
    c=Image.new('RGBA',(32,32)); c.paste(fs,(16-fs.size[0]//2,30-h),fs)
    x,y=(n%C)*cw,(n//C)*ch; d.text((x+4,y+2),sp,fill=0)
    for k,p in enumerate([c,i1,i2]):
        q=p.resize((128,128),Image.NEAREST); img.paste(q,(x+4+k*(128+8),y+12),q); img.paste(p,(x+4+k*(128+8)+48,y+12+128+2),p)
img.save(sys.argv[1])
