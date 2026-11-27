# Controle r1: kleuren, maat, lichte kleur op de buitenrand, zwart aan de lichtkant van de buitenlijn, losse zwarte pixels, afwijking t.o.v. kaal per zone.
import sys, numpy as np; sys.path.insert(0,'sprite_r2'); from gemeen2 import *; from PIL import Image
o=np.array(Image.open(sys.argv[1] if len(sys.argv)>1 else 'sprite_r2/guarana2_r2.png')); k=np.array(Image.open('sprite_r2/kaal.png'))
fg=o>0; ys,xs=np.where(fg)
print('maat %dx%d (x%d-%d, y%d-%d)'%(xs.max()-xs.min()+1,ys.max()-ys.min()+1,xs.min(),xs.max(),ys.min(),ys.max()),'kleuren incl. transparant:',len(set(o.ravel())))
print('alpha-diff t.o.v. kaal:',int((fg!=(k>0)).sum()))
N4=((-1,0),(1,0),(0,-1),(0,1))
def ok(Y,X): return 0<=Y<64 and 0<=X<64
licht=[];zwl=[];los=[]
for Y,X in zip(ys,xs):
    nb=[(dy,dx) for dy,dx in N4 if not ok(Y+dy,X+dx) or not fg[Y+dy,X+dx]]
    if nb and o[Y,X] in (5,9,10,11,4,8): licht.append((X,Y,o[Y,X]))
    if nb and o[Y,X]==1 and all(d in ((-1,0),(0,-1)) for d in nb): zwl.append((X,Y))
    if o[Y,X]==1 and not any(ok(Y+dy,X+dx) and o[Y+dy,X+dx] in (1,0) for dy in (-1,0,1) for dx in (-1,0,1) if dy or dx): los.append((X,Y))
print('lichte/midden tint op de buitenrand:',len(licht),licht[:20])
print('zwart met alleen achtergrond links/boven:',len(zwl))
print('losse zwarte pixels:',los)
z={'tros L':(0,22,22,40),'tros M':(19,9,38,28),'tros R':(40,18,60,38),'rank/blad/rest':None}
oog=np.load('sprite_r2/oog.npy')
d=(o!=k)
for n,b in z.items():
    if b: m=np.zeros_like(d); m[b[1]:b[3],b[0]:b[2]]=True
    else: m=np.ones_like(d); [m.__setitem__((slice(bb[1],bb[3]),slice(bb[0],bb[2])),False) for bb in list(z.values())[:3]]
    print('%-15s anders dan kaal: %3d  (waarvan ogen %d)'%(n,(d&m).sum(),(d&m&oog).sum()))
print('totaal anders dan kaal:',d.sum())
