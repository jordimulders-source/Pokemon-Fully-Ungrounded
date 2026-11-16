# Vel r15: r15 | r14 | model 8x; koeienvanger 12x r15 | r14 | model; kop 8x r15 | r14 | model; 1x/2x op licht en donker.
import sys; sys.path.insert(0,'/home/user/Pokemon-Fully-Ungrounded/docs/concept/sprites/spooktrein_fase3/sprite_r15')
from toon import *
a=np.array(Image.open(D+'sprite_r15/sprite.png')); r=np.array(Image.open(D+'sprite_r14/sprite.png'))
F=(0,0,64,64); kb=(0,43,28,60); hb=(0,17,34,46)
rows=[('r15 | r14 | model, 8x',[crop(a,F,8),crop(r,F,8),mod(F,8)]),
      ('koeienvanger 12x: r15 | r14 | model (model 1 rij hoger, zoals r14)',[crop(a,kb,12),crop(r,kb,12),mod(kb,12,-1)]),
      ('kop 8x: r15 | r14 | model',[crop(a,hb,8),crop(r,hb,8),mod(hb,8)])]
W=max(sum(i.size[0]+16 for i in rr) for _,rr in rows)+20; H=sum(max(i.size[1] for i in rr)+30 for _,rr in rows)+190
V=Image.new('RGB',(W,H),(225,225,225)); d=ImageDraw.Draw(V); y=6
for t,rr in rows:
    d.text((10,y),t,fill=(0,0,0)); x=10
    for i in rr: V.paste(i,(x,y+16)); x+=i.size[0]+16
    y+=max(i.size[1] for i in rr)+30
d.text((10,y),'1x / 2x op licht en donker: r15 | r14',fill=(0,0,0)); x=10
for s in (a,r):
    for bg in ((255,255,255),(48,48,64)):
        q=rgb(s,bg); V.paste(q,(x,y+16)); V.paste(q.resize((128,128),Image.NEAREST),(x+70,y+16)); x+=220
V.save(D+'sprite_r15/vel.png'); print(V.size)
