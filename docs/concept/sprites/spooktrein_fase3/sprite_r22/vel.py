# Vel r22: 12x drempel60 | drempel75 | r21 | model ; zwartkaarten model (60/75) naast die van de sprites; 16x drempels; 1x/2x.
import sys; sys.path.insert(0,'/home/user/Pokemon-Fully-Ungrounded/docs/concept/sprites/spooktrein_fase3/sprite_r18')
from vel import *
box=(0,42,28,60); Z=12
P=lambda n:D+'sprite_r22/'+n
def zk(M,a=None):
    o=Image.new('RGBA',((box[2]-box[0])*Z,(box[3]-box[1])*Z),(255,255,255,255)); d=ImageDraw.Draw(o)
    for y in range(box[1],box[3]):
        for x in range(box[0],box[2]):
            c=None
            if a is not None and a[y,x]==1: c=(0,0,0)
            if M is not None and M[y,x]: c=(200,0,0) if c is None else (0,0,0)
            if a is not None and a[y,x]==1 and M is not None and not M[y,x]: c=(0,0,200)
            if c: d.rectangle(((x-box[0])*Z,(y-box[1])*Z,(x-box[0]+1)*Z-1,(y-box[1]+1)*Z-1),fill=c)
    return o
A=lambda p:np.array(Image.open(p)).astype(int)
r1=rij([label(z(P('drempel60.png'),Z,box),'r22 lum<60'),label(z(P('drempel75.png'),Z,box),'r22 lum<75'),label(z(D+'sprite_r21/sprite.png',Z,box),'r21'),label(model_sprite_box(box,-1,Z),'model')])
r2=rij([label(zk(np.load(P('drempel60_mz.npy')),A(P('drempel60.png'))),'zwart 60: zwart=beide, rood=alleen model, blauw=alleen sprite'),
        label(zk(np.load(P('drempel75_mz.npy')),A(P('drempel75.png'))),'zwart 75'),label(zk(None,A(D+'sprite_r21/sprite.png')),'zwart r21')])
M8=model_sprite_box((0,0,64,64),-1,8)
def klein(Zk): return rij([z(P('drempel60.png'),Zk),z(P('drempel75.png'),Zk),z(D+'sprite_r21/sprite.png',Zk),M8.resize((64*Zk,64*Zk),Image.LANCZOS)],gap=8)
r3=rij([label(klein(1),'1x 60|75|r21|model'),label(klein(2),'2x 60|75|r21|model')],gap=30)
r4=rij([label(z(P('sprite.png'),8),'r22 8x (gekozen)'),label(z(D+'sprite_r21/sprite.png',8),'r21 8x'),label(M8,'model 8x')])
kolom([r1,r2,r3,r4]).convert('RGB').save(P('vel.png'))
