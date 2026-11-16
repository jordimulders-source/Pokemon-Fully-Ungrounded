# r25 = r24 (af/spooktrein.png) + strenge-keuring-reparaties (16 nov).
# Alleen bestaande paletindexen; 8 px + 1 paletwaarde (index 7 lichter: contraststap).
# Bevroren (assert): groen (2-6, 13), silhouet, koeienvanger-zone x0-30/y44-60, buiten de lijst diff 0.
import numpy as np
from PIL import Image
D='/home/user/Pokemon-Fully-Ungrounded/docs/concept/sprites/spooktrein_fase3/'
im=Image.open(D+'sprite_r24/sprite.png'); r=np.array(im).astype(int); pal=list(im.getpalette())
a=r.copy(); FIX=[]
def zet(x,y,oud,nieuw,reden):
    assert a[y,x]==oud,(x,y,a[y,x],oud); a[y,x]=nieuw; FIX.append((x,y,oud,nieuw,reden))
# M1 contraststap: plaatlicht 7 (178,153,138) lum 159 lag 14 boven plaatgrijs 10 (lum 145) -> zelfde tint/verzadiging, lum 182 (stap 37)
pal[21:24]=[204,175,158]
# M2 schoorsteenlip: dambord 7/10 (twee bijna gelijke tinten) -> lichte lip links/boven, 10 eronder
zet(15,16,10,7,'dambord 7/10 schoorsteenlip'); zet(14,17,10,7,'idem')
# M3 chassis achter de wagen: zwarte klont 8x2 met 11 ertussen (zwart/donker om en om) -> donkerste grijs 12 binnen 1-px-lijn (model: donkergrijze as)
for x in (47,48,49): zet(x,40,1,12,'zwarte klont chassis')
zet(50,40,11,12,'11 tussen zwart in klont')
# M4 kop/kier-aansluiting: zwart 3 breed (x28-30, y33-34) -> plaatwig 12 loopt 1 px door, twee 1-px-lijnen
zet(29,33,1,12,'zwarte klont kop/kier'); zet(29,34,1,12,'idem')
# bewijs
GR=[2,3,4,5,6,13]; g=np.isin(r,GR)|np.isin(a,GR)
assert (a[g]==r[g]).all(),'groen gewijzigd'
assert ((a==0)==(r==0)).all(),'silhouet gewijzigd'
assert (a[44:61,0:31]==r[44:61,0:31]).all(),'koeienvanger-zone gewijzigd'
m=np.zeros_like(a,bool)
for x,y,*_ in FIX: m[y,x]=True
assert ((a!=r)==m).all(),'buiten de lijst gewijzigd'
assert set(np.unique(a))<=set(np.unique(r)),'nieuwe index'
print('gewijzigd',int(m.sum()),'px + palet 7')
o=Image.fromarray(a.astype(np.uint8),'P'); o.putpalette(pal)
o.save(D+'sprite_r25/sprite.png',transparency=0)
o.resize((512,512),Image.NEAREST).save(D+'sprite_r25/sprite_8x.png',transparency=0)
