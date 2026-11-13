# ov.py PNG x0 y0 x1 y1 Z uit.png (vanuit kleur_r5/): sprite | model met spriteraster en coordinaten; uit.png komt in de tempmap
import sys
from PIL import Image, ImageDraw
import tempfile; S=tempfile.gettempdir()+'/'
B='../'
p=sys.argv[1]; x0,y0,x1,y1,Z=map(int,sys.argv[2:7]); out=sys.argv[7]
im=Image.open(p); im.save(S+'_o.png',transparency=0); sp=Image.open(S+'_o.png').convert('RGBA')
b=Image.new('RGBA',sp.size,(255,255,255,255)); b.alpha_composite(sp); sp=b.convert('RGB')
nat=Image.open(B+'kleur_r1/natief.png').convert('RGB')
mod=Image.new('RGB',(128,128),'white'); mod.paste(nat,(1,14))
W=(x1-x0)*Z; H=(y1-y0)*Z
a=sp.crop((x0,y0,x1,y1)).resize((W,H),Image.NEAREST)
m=mod.crop((2*x0,2*y0,2*x1,2*y1)).resize((W,H),Image.NEAREST)
c=Image.new('RGB',(2*W+40,H+30),'white'); c.paste(a,(30,30)); c.paste(m,(W+40,30))
d=ImageDraw.Draw(c)
for o in (30,W+40):
    for k in range(x0,x1+1):
        X=o+(k-x0)*Z; d.line([(X,30),(X,30+H)],fill=(255,0,0) if k%5==0 else (255,190,190))
        if k%2==0 and k<x1: d.text((X+2,2+ (12 if k%4 else 0)),str(k),fill=(0,0,0))
    for k in range(y0,y1+1):
        Y=30+(k-y0)*Z; d.line([(o,Y),(o+W,Y)],fill=(255,0,0) if k%5==0 else (255,190,190))
for k in range(y0,y1): d.text((2,30+(k-y0)*Z+2),str(k),fill=(0,0,0))
c.save(S+out)
