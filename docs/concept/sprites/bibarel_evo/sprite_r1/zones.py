# zones.py: afwijkingen per zone en per stap t.o.v. de kale reductie (basis.png = meerderheidsreductie C in spritepalet + buitenrand)
import numpy as np,sys; sys.path.insert(0,'sprite_r1'); from gemeen import *
B=laad('sprite_r1/basis.png'); S=laad(sys.argv[1] if len(sys.argv)>1 else 'sprite_r1/sprite.png')
Z={'gezicht (oogband/ogen/snuit/neus/tanden) x20-34 y14-27':(20,35,14,28),
   'klep + koepel y6-13':(17,40,6,14),
   'potlood (punt + houtkegel) x0-13 y15-27':(0,13,15,28),
   'stam + hand links x13-20 y10-27':(13,20,10,28),
   'stam rechts x35-54 y9-22':(35,54,9,20),
   'kraag/romp/armen y14-41 (rest)':(0,64,14,42),
   'tuinbroekzone + benen + voeten y42-63':(0,64,42,64)}
taken=np.zeros((64,64),bool); tot=0
for naam,(x0,x1,y0,y1) in Z.items():
    m=np.zeros((64,64),bool); m[y0:y1,x0:x1]=True; m&=~taken; taken|=m
    d=((B!=S)&m).sum(); tot+=d; print('%-55s %4d px afwijkend van %d'%(naam,d,((B>0)|(S>0))[m].sum()))
print('totaal',tot,'van',((B>0)|(S>0)).sum())
st=[('basis','basis.png'),('ruis 1 (alleen 1-px... <3 px tintclusters)','ontruist.png'),('gezichtszone uit reductie A','gezicht.png'),('gezicht per pixel naar model + Bibarel-ogen','gezicht2.png')]
prev=B
for naam,f in st[1:]:
    cur=laad('sprite_r1/'+f); print('stap %-45s %4d px'%(naam,(cur!=prev).sum())); prev=cur
cur=np.load('sprite_r1/voor_selout.npy'); print('stap %-45s %4d px'%('neus/potloodpunt/ruis 2',(cur!=prev).sum())); prev=cur
print('stap %-45s %4d px'%('tuinbroek + selout + losse zwart (rest)',(S!=prev).sum()))
