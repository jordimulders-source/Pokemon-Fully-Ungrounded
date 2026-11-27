# Controle r3 (op de png): maat, kleuren, alpha-diff t.o.v. r2 (silhouet), lichte tint op de buitenrand, zwart aan de lichtkant,
# tinten per vrucht/streng, kleine tintvlakjes, afwijking t.o.v. de kale reductie en t.o.v. r2 per zone.
import sys, numpy as np; sys.path.insert(0,'sprite_r3'); from PIL import Image
sp=sys.argv[1] if len(sys.argv)>1 else 'sprite_r3/guarana2_r3_A.png'
o=np.array(Image.open(sp)); r2=np.array(Image.open('sprite_r2/guarana2_r2.png')); k=np.array(Image.open('sprite_r3/kaal.png'))
fg=o>0; ys,xs=np.where(fg)
print(sp,'maat %dx%d (x%d-%d, y%d-%d)'%(xs.max()-xs.min()+1,ys.max()-ys.min()+1,xs.min(),xs.max(),ys.min(),ys.max()),'kleuren incl. transparant:',len(set(o.ravel())))
print('alpha-diff t.o.v. r2:',int((fg!=(r2>0)).sum()),' t.o.v. kaal:',int((fg!=(k>0)).sum()))
N4=((-1,0),(1,0),(0,-1),(0,1)); N8=[(a,b) for a in (-1,0,1) for b in (-1,0,1) if a or b]
def ok(Y,X): return 0<=Y<64 and 0<=X<64
LIJN={1,2,6,14,15,3,7}
licht=[];zwl=[];los=[]
for Y,X in zip(ys,xs):
    nb=[(dy,dx) for dy,dx in N4 if not ok(Y+dy,X+dx) or not fg[Y+dy,X+dx]]
    if nb and o[Y,X] not in LIJN: licht.append((X,Y,int(o[Y,X])))
    if nb and o[Y,X]==1 and all(d in ((-1,0),(0,-1)) for d in nb): zwl.append((X,Y))
print('lichte tint op de buitenrand:',licht)
print('zwart met alleen achtergrond links/boven:',zwl)
cnt={i:int((o==i).sum()) for i in range(16)}; print('pixels per index:',cnt)
oog=np.load('sprite_r3/oog.npy')
z={'tros L':(0,20,22,42),'tros M':(19,9,38,29),'tros R':(40,18,62,40)}
for n,b in z.items():
    m=np.zeros((64,64),bool); m[b[1]:b[3],b[0]:b[2]]=True
    print('%-7s anders dan r2: %3d  anders dan kaal: %3d (ogen %d)'%(n,((o!=r2)&m).sum(),((o!=k)&m).sum(),((o!=k)&m&oog).sum()))
m=np.ones((64,64),bool)
for b in z.values(): m[b[1]:b[3],b[0]:b[2]]=False
print('rest    anders dan r2: %3d  anders dan kaal: %3d'%(((o!=r2)&m).sum(),((o!=k)&m).sum()))
print('totaal anders dan r2:',int((o!=r2).sum()),' anders dan kaal:',int((o!=k).sum()))
