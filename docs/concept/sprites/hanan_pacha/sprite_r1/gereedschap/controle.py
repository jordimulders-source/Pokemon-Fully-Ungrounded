# Controle: kleuren, per groep tinten, lichte kleur op de buitenrand, losse zwarte pixels, tintvlekjes, afwijking per zone t.o.v. kaal.
import sys,numpy as np; sys.path.insert(0,'gereedschap'); from gemeen import *
from scipy import ndimage
from PIL import Image
im=Image.open('sprite.png'); o=np.array(im); k=np.load('kaal.npy')
print('maat',im.size,'mode',im.mode,'transp',im.info.get('transparency'),'kleuren incl. transp',len(np.unique(o)) )
ys,xs=np.where(o>0); print('figuur bbox x%d-%d y%d-%d (%dx%d), %d px'%(xs.min(),xs.max(),ys.min(),ys.max(),xs.max()-xs.min()+1,ys.max()-ys.min()+1,len(xs)))
print('gebruik per index',dict(enumerate(np.bincount(o.ravel(),minlength=len(PAL)))))
LICHT={4,5,7,10,12}
rand=[(X,Y) for Y,X in zip(ys,xs) if any(not(0<=Y+dy<64 and 0<=X+dx<64) or o[Y+dy,X+dx]==0 for dy,dx in ((1,0),(-1,0),(0,1),(0,-1))) and o[Y,X] in LICHT]
print('lichte kleur op de buitenrand:',len(rand),rand[:40])
los=[(X,Y) for Y,X in zip(*np.where(o==1)) if not any(o[Y+dy,X+dx] in (0,1,13) for dy in (-1,0,1) for dx in (-1,0,1) if (dy or dx) and 0<=Y+dy<64 and 0<=X+dx<64)]
print('losse zwarte pixels:',los)
for kk in (3,4,7,9,10,12,11):
    lab,n=ndimage.label(o==kk); kl=[int((lab==i).sum()) for i in range(1,n+1)]; print('tint',kk,'vlekjes <3 px:',sum(1 for s in kl if s<3))
Z={'kop':(15,14,27,26),'staart':(18,49,52,64),'poten':(19,43,38,49)}
def zone(X,Y):
    for n,(x0,y0,x1,y1) in Z.items():
        if x0<=X<x1 and y0<=Y<y1: return n
    if Y<40 and X<27: return 'vleugel links'
    if Y<40 and X>=30: return 'vleugel rechts'
    return 'lijf'
d={}
for Y,X in zip(*np.where(o!=k)): d[zone(X,Y)]=d.get(zone(X,Y),0)+1
print('afwijking van kale reductie per zone:',d,'totaal',int((o!=k).sum()),'silhouet-diff',int(((o>0)!=(k>0)).sum()))
