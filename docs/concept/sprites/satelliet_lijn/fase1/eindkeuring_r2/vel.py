# Vellen eindkeuring r2. Draaien vanuit fase1/: python3 eindkeuring_r2/vel.py
import numpy as np, importlib.util
from PIL import Image, ImageDraw
def rgba(path):
    im=Image.open(path); i=np.array(im); r=np.array(im.convert('RGBA')); r[i==0,3]=0; return Image.fromarray(r), i
s,si=rgba('sprite_r2/sprite.png'); v,vi=rgba('eindkeuring_r2/voorstel.png')
src=open('eindkeuring_r2/voorstel.py').read()
FIX=[]
for line in src.split('\n'):
    if line.strip().startswith("('"):
        for part in line.split('),('):
            pass
import re
FIX=[(c,int(y),int(x)) for c,y,x in re.findall(r"\('(\w+)',\((\d+),(\d+)\)",src)]
COL={'Z':(255,40,40),'V':(255,160,0),'O':(0,170,255)}
BG=(200,220,200,255)
def up(im,f): return im.resize((im.width*f,im.height*f),Image.NEAREST)
def zwartkaart(im,idx,mark=True):
    Z=8; b=Image.new('RGBA',(512,512),BG); b.paste(up(im,Z),(0,0),up(im,Z)); d=ImageDraw.Draw(b)
    for y,x in np.argwhere(idx==1):
        d.rectangle([x*Z+2,y*Z+2,x*Z+5,y*Z+5],fill=(230,230,230))   # alle zwarte pixels: grijs stipje
    if mark:
        for c,y,x in FIX: d.rectangle([x*Z,y*Z,x*Z+7,y*Z+7],outline=COL[c[0]],width=2)
    for k in range(0,64,8):
        d.text((k*Z+1,1),str(k),fill=(0,0,160)); d.text((1,k*Z+1),str(k),fill=(0,0,160))
    return b
W=512*2+60
c=Image.new('RGBA',(W,512+330),BG); d=ImageDraw.Draw(c)
d.text((10,4),'sprite_r2: elke zwarte pixel = grijs stipje; kader = reparatie (rood P1 om-en-om/lichtkant, oranje P2 verdikt, blauw P3 oog)',fill=(0,0,0))
d.text((10+512+40,20),'voorstel (zelfde stipjes = zwart dat blijft)',fill=(0,0,0))
c.paste(zwartkaart(s,si),(10,36)); c.paste(zwartkaart(v,vi,False),(10+512+40,36))
y0=36+512+16
d.text((10,y0),'voor / na op 1x, 2x (op lichte en donkere achtergrond)',fill=(0,0,0))
x=10
for bgc in ((200,220,200,255),(40,40,48,255)):
    for im in (s,v):
        t=Image.new('RGBA',(64,64),bgc); t.paste(im,(0,0),im); c.paste(t,(x,y0+20)); x+=70
    for im in (s,v):
        t=Image.new('RGBA',(128,128),bgc); t.paste(up(im,2),(0,0),up(im,2)); c.paste(t,(x,y0+20)); x+=136
# echte Gen 3 ernaast op 1x
refs=['voltorb','electrode','magnemite','beldum','lunatone']
x=10; y1=y0+170
d.text((10,y1-16),'Gen 3 ter vergelijking (1x): '+', '.join(refs)+'  |  voorstel',fill=(0,0,0))
for r in refs:
    im=Image.open(f'../../../../../graphics/pokemon/{r}/anim_front_gba.png'); i=np.array(im)[:64]
    a=np.array(im.convert('RGBA'))[:64]; a[i==0,3]=0; t=Image.fromarray(a); c.paste(t,(x,y1),t); x+=70
c.paste(v,(x,y1),v)
c.save('eindkeuring_r2/vel.png')
# voor/na op 8x naast elkaar zonder markering
vn=Image.new('RGBA',(512*2+30,512),BG); vn.paste(up(s,8),(0,0),up(s,8)); vn.paste(up(v,8),(512+30,0),up(v,8)); vn.save('eindkeuring_r2/voor_na_8x.png')
for f in (1,2):
    t=Image.new('RGBA',(64*f*2+10,64*f),BG); t.paste(up(s,f),(0,0),up(s,f)); t.paste(up(v,f),(64*f+10,0),up(v,f)); t.save(f'eindkeuring_r2/voor_na_{f}x.png')
print('ok',len(FIX))
