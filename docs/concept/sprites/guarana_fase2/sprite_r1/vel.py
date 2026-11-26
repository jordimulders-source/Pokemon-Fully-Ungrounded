# vel.png: sprite 8x | model verkleind 8x; close-ups van de drie trossen op 12x naast het model (natief met spriteraster); 1x op licht en donker.
import sys, numpy as np; sys.path.insert(0,'sprite_r1'); from gemeen2 import *
from PIL import Image, ImageDraw
SP=sys.argv[1] if len(sys.argv)>1 else 'sprite_r1/guarana2_r1.png'; UIT=sys.argv[2] if len(sys.argv)>2 else 'sprite_r1/vel.png'
o=np.array(Image.open(SP)); BG=(255,255,255)
s8=rgb(o,BG).resize((512,512),0); m8=Image.open('sprite_r1/model_64.png').resize((512,512),0)
N=Image.open(NATIEF).convert('RGB')
def close(x0,y0,x1,y1,z=12):
    a=rgb(o,BG).crop((x0,y0,x1,y1)).resize(((x1-x0)*z,(y1-y0)*z),0)
    ua=(x0-X0)/S+U0; va=(y0-Y0)/S+V0; ub=(x1-X0)/S+U0; vb=(y1-Y0)/S+V0
    n=N.crop((round(ua),round(va),round(ub),round(vb))).resize(a.size,Image.LANCZOS)
    for t in (a,n):
        d=ImageDraw.Draw(t)
        for X in range(x0,x1+1): d.line([((X-x0)*z,0),((X-x0)*z,a.height)],fill=(225,225,235))
        for Y in range(y0,y1+1): d.line([(0,(Y-y0)*z),(a.width,(Y-y0)*z)],fill=(225,225,235))
    t=Image.new('RGB',(a.width*2+8,a.height),'white'); t.paste(a,(0,0)); t.paste(n,(a.width+8,0)); return t
cl=[close(2,20,23,40),close(19,9,38,28),close(40,18,61,38)]
W=max(1040,sum(c.width for c in cl[:2])+20)
H=512+30+max(c.height for c in cl)+20+cl[2].height+30+140
vel=Image.new('RGB',(W,H),'white'); d=ImageDraw.Draw(vel)
vel.paste(s8,(0,20)); vel.paste(m8,(528,20)); d.text((4,4),'guarana fase 2 r1 (8x)',fill='black'); d.text((532,4),'model (natief, BOX naar 64) 8x',fill='black')
y=552; d.text((4,y-14),'close-ups 12x: sprite | model (natief)',fill='black')
vel.paste(cl[0],(0,y)); vel.paste(cl[1],(cl[0].width+20,y)); y2=y+max(cl[0].height,cl[1].height)+20
vel.paste(cl[2],(0,y2)); y3=y2+cl[2].height+20
x=cl[2].width+40
for bg in ((255,255,255),(240,232,208),(152,208,160),(40,40,48),(16,24,40)):
    vel.paste(rgb(o,bg),(x,y2)); x+=72
x=cl[2].width+40; d.text((x,y2+70),'1x op licht en donker',fill='black')
m1=Image.open('sprite_r1/model_64.png'); vel.paste(m1,(x,y2+90)); d.text((x+70,y2+110),'model 1x',fill='black')
vel=vel.crop((0,0,W,max(y3,y2+170))); vel.save(UIT); print(vel.size)
