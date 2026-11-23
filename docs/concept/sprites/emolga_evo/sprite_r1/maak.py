# Bouwt ronde 1: A0.png, A.png, kaal_A0.png, kaal_A.png, vel.png, en telt afwijkingen per zone t.o.v. de kale reductie.
import sys; sys.path.insert(0,'/home/user/Pokemon-Fully-Ungrounded/docs/concept/sprites/emolga_evo/gereedschap')
sys.path.insert(0,'/home/user/Pokemon-Fully-Ungrounded/docs/concept/sprites/emolga_evo/sprite_r1')
import numpy as np; import bouw_a0, bouw_a, palet
from gezicht_a0 import FIX; from gezicht_a import FIX_A; from controle import rapport; from vel import vel
from gemeen import D as MAP
R=MAP+'sprite_r1/'
a0,k0,st0=bouw_a0.bouw(FIX)
a,_,zone,kk,sta=bouw_a.bouw(FIX,FIX_A)
palet.opslaan(a0,R+'A0.png'); palet.opslaan(a,R+'A.png'); palet.opslaan(k0,R+'kaal_A0.png'); palet.opslaan(kk,R+'kaal_A.png')
rapport(a0,'A0'); rapport(a,'A')
ZONES={'gezicht':(6,49,25,64),'oren':(0,36,25,50),'linkervleugel':(0,0,32,40),'rechtervleugel':(32,0,64,32),'buik/hand':(25,28,64,52)}
def per_zone(o,k,zones):
    d=o!=k; gez=np.zeros((64,64),bool); res={}
    for n,(x0,y0,x1,y1) in zones.items():
        m=np.zeros((64,64),bool); m[y0:y1,x0:x1]=True; m&=~gez; res[n]=int((d&m).sum()); gez|=m
    res['rest']=int((d&~gez).sum()); return res
print('A0 t.o.v. kale reductie:',per_zone(a0,k0,ZONES),'totaal',int((a0!=k0).sum()))
ZA={'gezicht':(4,46,28,64),'oren':(0,26,28,46)}
print('A kopzone t.o.v. kale kopreductie:',per_zone(np.where(zone,a,0),np.where(zone,kk,0),ZA),'| buiten kopzone t.o.v. A0:',int(((a!=a0)&~zone).sum()))
S,OX,OY=bouw_a0.S,bouw_a0.OX,bouw_a0.OY
print(vel([(a0,'A0 r1',S,OX,OY,MAP+'model/model.png',(6,48,26,64)),
           (a,'A r1',S,OX,OY,MAP+'model/kop_opties/A_kopmodel_1024.png',(3,44,29,64))],R+'vel.png'))
