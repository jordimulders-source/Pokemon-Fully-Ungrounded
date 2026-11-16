# Vel r23: 12x r23 | r22 | model met Jordi's teruggerekende lijnen (geel); 8x r23 | r22 | model; 1x/2x.
import sys; sys.path.insert(0,'/home/user/Pokemon-Fully-Ungrounded/docs/concept/sprites/spooktrein_fase3/sprite_r18')
from vel import *
P=np.load(D+'sprite_r23/jordi_lijnen.npy')
box=(0,40,30,60); Z=12
def ov(im):
    d=ImageDraw.Draw(im)
    for x,y in P:
        if box[0]<=x<box[2] and box[1]<=y<box[3]:
            X,Y=(x-box[0])*Z,(y-box[1])*Z; d.rectangle((X-1,Y-1,X+1,Y+1),fill=(255,220,0))
    return im
P23=D+'sprite_r23/sprite.png'; P22=D+'sprite_r22/sprite.png'
r1=rij([label(ov(z(P23,Z,box)),'r23 + lijnen Jordi'),label(ov(z(P22,Z,box)),'r22 + lijnen Jordi'),label(ov(model_sprite_box(box,-1,Z)),'model + lijnen Jordi')])
r1b=rij([label(z(P23,Z,box),'r23 (zonder lijnen)'),label(z(P22,Z,box),'r22'),label(model_sprite_box(box,-1,Z),'model')])
M8=model_sprite_box((0,0,64,64),-1,8)
r2=rij([label(z(P23,8),'r23 8x'),label(z(P22,8),'r22 8x'),label(M8,'model 8x')])
def klein(Zk): return rij([z(P23,Zk),z(P22,Zk),M8.resize((64*Zk,64*Zk),Image.LANCZOS)],gap=8)
r3=rij([label(klein(1),'1x r23|r22|model'),label(klein(2),'2x r23|r22|model')],gap=30)
kolom([r1,r1b,r3,r2]).convert('RGB').save(D+'sprite_r23/vel.png')
