# Contactvel frame 1 | frame 2 | verschil. Verschil: grijs = gelijk, rood = alleen in frame 2, blauw = alleen in frame 1, geel = andere kleur.
# Gebruik: python3 vel.py uit.png [_gba] soort1 soort2 ...
import sys,numpy as np
from PIL import Image,ImageDraw
out,suf,names=sys.argv[1],sys.argv[2],sys.argv[3:]
Z=3;cw=64*Z*3+16;rows=[]
for n in names:
    p=f'graphics/pokemon/{n}/anim_front{suf}.png'
    try: im=Image.open(p)
    except Exception: continue
    a=np.array(im); f1,f2=a[:64],a[64:]
    rgb=np.array(im.convert('RGB'))
    t=a[0,0] if suf=='' else 0
    t=0
    A=f1!=t;B=f2!=t
    d=np.full((64,64,3),235,np.uint8)
    d[A&B&(f1==f2)]=(150,150,150); d[A&~B]=(60,90,255); d[~A&B]=(255,50,50); d[A&B&(f1!=f2)]=(240,200,0)
    def big(x):return Image.fromarray(x).resize((64*Z,64*Z),Image.NEAREST)
    bg=lambda x,m:np.where(m[...,None],x,np.uint8([200,225,200]))
    r=Image.new('RGB',(cw,64*Z+14),(255,255,255))
    r.paste(big(bg(rgb[:64],A)),(0,14));r.paste(big(bg(rgb[64:],B)),(64*Z+8,14));r.paste(big(d),(128*Z+16,14))
    ImageDraw.Draw(r).text((2,1),f'{n}{suf}  gelijk {(A&B&(f1==f2)).sum()}  alleen f1 {(A&~B).sum()}  alleen f2 {(~A&B).sum()}  andere kleur {(A&B&(f1!=f2)).sum()}',fill=(0,0,0))
    rows.append(r)
sh=Image.new('RGB',(cw,sum(r.height for r in rows)),(255,255,255));y=0
for r in rows: sh.paste(r,(0,y));y+=r.height
sh.save(out)
