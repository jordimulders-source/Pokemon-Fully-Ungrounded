# r14: (1) koeienvanger uit het model met de ijskomeet-methode (onderlaag.py: lijnpixels winnen, anders oppervlaktegemiddelde),
# model 1 rij hoger gelegd zodat de kaak onder de bevroren grijns past; (2) hele sprite 2 px naar rechts; (3) wolkpunten rechts netjes afgesloten.
import sys; sys.path.insert(0,'/home/user/Pokemon-Fully-Ungrounded/docs/concept/sprites/spooktrein_fase3/sprite_r14')
import onderlaag; onderlaag.DY=-1
from kaak2 import *
im=Image.open(D+'sprite_r13/sprite.png'); r=np.array(im)
a=kaak(r,70,0.5)
g=np.isin(r,list(G))|np.isin(a,list(G)); assert (a[g]==r[g]).all(),'groen kaak'
np.save(D+'sprite_r14/kaak_r13coord.npy',a)
# verschuiven
s=np.zeros_like(a); s[:,2:]=a[:,:62]
afgekapt=[(y,x+2) for y in range(64) for x in range(62,64) if a[y,x]!=0]
print('afgekapt (r13-x 62-63):',[(x-2,y) for y,x in afgekapt])
np.save(D+'sprite_r14/geschoven.npy',s)
# wolkpunten: de afgekapte slierten eindigen met de oorspronkelijke ronde punt (r13 x61-63), 2 px korter
WOLK={(29,61):6,(29,62):6}
for y in (33,34,35):
    for x in (61,62,63): WOLK[(y,x)]=r[y,x]
for (y,x),v in WOLK.items(): s[y,x]=v
# bewijs: groen gelijk aan r13 (verschoven) buiten de wolkpunten
rs=np.zeros_like(r); rs[:,2:]=r[:,:62]
gm=(np.isin(rs,list(G))|np.isin(s,list(G)))
for (y,x) in WOLK: gm[y,x]=False
print('groen-diff na verschuiving (buiten', len(WOLK),'wolkpunt-pixels):',int((s[gm]!=rs[gm]).sum()))
print('ijzer gewijzigd t.o.v. r13 (verschoven):',int(((s!=rs)&~gm).sum()) - len([1 for (y,x) in WOLK if s[y,x]!=rs[y,x]]))
o=Image.fromarray(s,'P'); o.putpalette(im.getpalette()); o.save(D+'sprite_r14/sprite.png',transparency=0)
with open(D+'sprite_r14/raster.txt','w') as f:
    for row in s: f.write(''.join('.' if q==0 else '%X'%q for q in row)+'\n')
