# r19 = r18 + kleine eindkeurderreparaties (alleen bestaande paletindexen, geen nieuwe vormen).
# Bevroren (assert): groene indexen, zwarte gezichtslijnen grote kop, rij 0-19, buiten de genoemde pixels diff 0.
import sys; sys.path.insert(0,'/home/user/Pokemon-Fully-Ungrounded/docs/concept/sprites/spooktrein_fase3/sprite_r18')
import numpy as np
from PIL import Image
from kopmask import masks
D='/home/user/Pokemon-Fully-Ungrounded/docs/concept/sprites/spooktrein_fase3/'
im=Image.open(D+'sprite_r18/sprite.png'); r=np.array(im).astype(int); pal=im.getpalette()
a=r.copy()
FIX=[]  # (x,y,oud,nieuw,reden)
def zet(x,y,oud,nieuw,reden):
    assert a[y,x]==oud,(x,y,a[y,x],oud); a[y,x]=nieuw; FIX.append((x,y,oud,nieuw,reden))
# 1. linkerwang: lichtbruine 1-px-rand langs de buitenlijn (x3) en strook onder de grauwe balk = banding -> middenbruin 8
for y in (33,34,35,36): zet(3,y,14,8,'lichtrand langs buitenlijn (banding)')
for x in (4,5,6):       zet(x,37,14,8,'lichte strook boven de grijns (banding)')
# 2. donkergrijze balk onder het linkeroog (11) -> middengrijs 10 (model-toon 2 = midden, r17 had hier licht 7)
for x,y in ((4,36),(5,36),(6,36),(7,36),(4,35),(8,35),(9,34),(9,33),(10,33)): zet(x,y,11,10,'harde donkere balk onder oog')
# 3. vlekjes < 3 px aan de lichte linkerrand van de kop
zet(6,25,14,7,'eilandje 14 tussen selout en lichte plaat'); zet(6,26,14,7,'idem')
zet(4,29,14,10,'eilandje 14 tussen selout en zwart -> plaat'); zet(4,30,14,10,'idem')
# bewijs bevroren
kop,gez,_=masks(r)
GRS=[2,3,4,5,6,13]; g=np.isin(r,GRS)|np.isin(a,GRS)
assert (a[g]==r[g]).all(),'groen gewijzigd'
assert (a[gez]==r[gez]).all(),'gezichtslijnen gewijzigd'
assert (a[:20]==r[:20]).all(),'rij 0-19 gewijzigd'
m=np.zeros_like(a,bool)
for x,y,*_ in FIX: m[y,x]=True
assert ((a!=r)==m).all(),'buiten de lijst gewijzigd'
assert set(np.unique(a))<=set(np.unique(r)),'nieuwe index'
print('gewijzigd',int(m.sum()),'px')
o=Image.fromarray(a.astype(np.uint8),'P'); o.putpalette(pal)
o.save(D+'sprite_r19/sprite.png',transparency=0)
o.resize((512,512),Image.NEAREST).save(D+'sprite_r19/sprite_8x.png',transparency=0)
with open(D+'sprite_r19/raster.txt','w') as f:
    for row in a: f.write(''.join('.' if q==0 else '%X'%q for q in row)+'\n')
