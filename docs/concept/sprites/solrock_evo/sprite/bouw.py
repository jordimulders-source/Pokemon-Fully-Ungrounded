# Basis (zonder Jordi's breuk): schoon.npy + barsten uit het model + buitenlijn 1 px. Uit: basis.npy/png
import numpy as np; from scipy import ndimage as nd; from npy2png import save
o=np.load('schoon.npy'); b=np.load('barst.npy'); log={}
# barsten in de kern (alleen op grijs), componenten < 3 px niet
m=b&np.isin(o,[2,3,4]); lab,n=nd.label(m|(o==1),structure=np.ones((3,3)))
add=np.zeros_like(m)
for k in range(1,n+1):
    c=lab==k
    if c.sum()>=3: add|=c&m
o[add]=1; log['barst']=int(add.sum())
# buitenlijn: grijze rand tegen transparant -> zwart; creme op de buitenrand -> goud (gekleurde selout)
fig=o>0; t=~fig
edge=fig&(np.roll(t,1,0)|np.roll(t,-1,0)|np.roll(t,1,1)|np.roll(t,-1,1))
e1=edge&np.isin(o,[2,3,4]); o[e1]=1; log['rand_zwart']=int(e1.sum())
np.save('basis.npy',o); save(o,'basis.png'); print(log)
# ring dun maken: ringpixels (licht, straal 16-21.5 vanaf het kernmidden, niet aan een steen) die radiaal dubbel liggen:
# de pixel met de kleinste lichtfractie uit het model valt weg (transparant)
import pickle; F=pickle.load(open('frac.pkl','rb'))
cx,cy=31.1,34.0
def isring(j,i):
    if o[j,i] not in (5,6): return False
    r=np.hypot(i+0.5-cx,j+0.5-cy)
    if not (16<=r<=21.5): return False
    nb=o[max(0,j-1):j+2,max(0,i-1):i+2]
    return not np.isin(nb,[1,2,3,4]).any()
weg=0
for j in range(64):
    for i in range(64):
        if not isring(j,i): continue
        dx,dy=i+0.5-cx,j+0.5-cy
        st=(0,1 if dx>0 else -1) if abs(dx)>abs(dy) else ((1 if dy>0 else -1),0)
        j2,i2=j+st[0],i+st[1]
        if 0<=j2<64 and 0<=i2<64 and isring(j2,i2):
            a_,b_=F[(j,i)]['light'],F[(j2,i2)]['light']
            if a_<b_: o[j,i]=0
            else: o[j2,i2]=0
            weg+=1
print('ring dun:',weg)
# oog rechts: plaatpixel midden in het rood -> lichtrood (model: rood onderlob)
if o[36,29]==8: o[36,29]=11
np.save('basis.npy',o); save(o,'basis.png')
# ring links naast het brokje en onderaan naast de steen dubbel: houd de pixel op de modelstraal (225 modelpx = kolom 12 / rij 52)
for (j,i,v) in [(31,11,0),(33,11,0),(34,11,0),(35,11,1),(53,28,0),(53,29,0),(53,34,0)]:
    o[j,i]=v
np.save('basis.npy',o); save(o,'basis.png')
# brokjes van 2-3 px breed werden door de buitenlijnregel helemaal zwart: de grijze modelpixel (kaal) terug als glans
kaal=np.load('kaal.npy')
for (j,i) in [(20,12),(51,17)]:
    o[j,i]=kaal[j,i]
np.save('basis.npy',o); save(o,'basis.png')
# rechteroog: onderlob in rij 37 (modelrood 24-25 %, eronder de zwarte oogkas) -> zwart, zodat het oog 2 rijen rood is zoals in het model
for (j,i) in [(37,28),(37,29)]:
    assert o[j,i]==11, (j,i,o[j,i]); o[j,i]=1
np.save('basis.npy',o); save(o,'basis.png')
