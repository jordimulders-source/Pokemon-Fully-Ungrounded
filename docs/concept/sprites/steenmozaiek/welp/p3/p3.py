# p3: keuring p2 (MOET 1-3 + MAG) op welp_p2, alleen benoemde pixels binnen de lijfpatroonzone.
import numpy as np
from PIL import Image
P2=np.array(Image.open('../p2/welp_p2.png')); R=np.array(Image.open('../r11/welp_r11.png')); B=np.load('../p1/basis.npy')
PAL=Image.open('../r11/welp_r11.png').getpalette()
MAG=np.isin(R,[3,4,5,14,6,7,8,11]); a=P2.copy(); log=[]
def zet(x,y,v):
    if not MAG[y,x]: log.append(('OVERGESLAGEN (lijn/leeg)',x,y,v)); return
    a[y,x]=v
basis=lambda x,y: zet(x,y,int(B[y,x]))
# MOET 1: haak rechts van de ring omlaag, onderaan naar links en omhoog naar binnen; oude steel/voet terug naar basis
for x,y in [(30,49),(30,50),(30,51),(30,52),(31,49),(31,50),(31,51),(31,52),(28,52),(28,53),(29,53),(30,53)]: basis(x,y)
# (32,49) is in r11 de beenlijn (index 2): steel op rij 49 daarom op (33,49)=11/(34,49)=9, sluit aan op ring (33,48)/(34,48)
for x,y,v in [(33,49,11),(34,49,9),(32,50,11),(33,50,9),(31,51,11),(32,51,9),
              (30,52,11),(31,52,9),(29,51,11),(29,50,11),(30,50,9)]: zet(x,y,v)
# MOET 2: ring onderaan open: lila buitenwinding (7) op y47 x28-31, y48 x27-31 terug naar basis
for x in range(28,32): zet(x,47,7)
for x in range(27,32): basis(x,48)
# MOET 3: ruis in de linker ringrand
zet(26,43,11)
# MAG schijfvolume: onderste lila rij in 7, één extra 7 aan de schaduwkant van het 8-vlak
for x,y in [(29,45),(30,45),(32,43)]: zet(x,y,7)
# MAG heup: taps eind van de 6-rij
for x,y in [(41,55),(45,55)]: zet(x,y,3)
# MAG rugkrul één winding groter (model: kleine spiraal aan het eind van de rugband), groef open naar links
for y in range(38,43):
    for x in range(37,43):
        if a[y,x] in (6,7,8) or (a[y,x]==3 and (x,y)==(39,39)): basis(x,y)
KRUL={(38,38):8,(39,38):8,(40,38):8,
      (38,39):3,(39,39):3,(40,39):3,(41,39):7,
      (38,40):8,(39,40):8,(40,40):3,(41,40):7,
      (38,41):8,(39,41):3,(40,41):3,(41,41):7,
      (38,42):7,(39,42):7,(40,42):7,(41,42):7}
for (x,y),v in KRUL.items(): zet(x,y,v)
im=Image.fromarray(a.astype('uint8'),'P'); im.putpalette(PAL); im.save('welp_p3.png',transparency=0)
q=Image.open('welp_p3.png').convert('RGBA'); bg=Image.new('RGBA',q.size,(255,255,255,255)); bg.alpha_composite(q)
bg.resize((512,512),Image.NEAREST).save('welp_p3_8x.png')
for l in log: print(*l)
