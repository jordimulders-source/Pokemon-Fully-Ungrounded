# Blobfish r4: alleen het mondeind (opkrul rechts, kleiner dan 1 spritepixel in het model -> herstel toegestaan).
# Model: mondlijn stijgt bij x18-19 van onderin rij 49 naar bovenin rij 49 (richting het nabije oog); lip er rond omheen.
#  r4a: (19,48) zwart = eind 1 rij hoger; (19,49) liptoon 9 (= tint van de onderlip/lipeind ernaast) -> 2 px
#  r4b: (19,48) zwart erbij, (19,49) blijft zwart (haakje)                                            -> 1 px
import numpy as np; from PIL import Image
R3=Image.open('r3.png'); r3=np.asarray(R3).astype(int); pal=R3.getpalette()[:3*14]
for naam,zetten in (('r4a',((19,48,1),(19,49,9))),('r4b',((19,48,1),))):
    o=r3.copy()
    for x,y,v in zetten: o[y,x]=v
    assert ((o>0)==(r3>0)).all()
    d=np.argwhere(o!=r3); assert all(16<=x<=21 and 47<=y<=50 for y,x in d)
    p=Image.fromarray(o.astype('uint8'),'P'); p.putpalette(pal+[0]*(768-len(pal))); p.save(f'blobfish_{naam}.png',transparency=0)
    print(naam,'diff',[(int(x),int(y),int(r3[y,x]),int(o[y,x])) for y,x in d])
    for y in range(45,52): print('  %2d '%y+''.join('%x'%o[y,x] if o[y,x] else '.' for x in range(6,24)))
