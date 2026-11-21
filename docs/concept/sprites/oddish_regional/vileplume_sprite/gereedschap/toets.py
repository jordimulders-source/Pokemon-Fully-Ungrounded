# toets.py SPRITE: kleuren, bbox, losse pixels, lijnpixels midden in een vlak, lichte kleur op de buitenrand
import sys, numpy as np; from PIL import Image
im=Image.open(sys.argv[1]); o=np.asarray(im).astype(int); pal=np.array(im.getpalette()[:48]).reshape(-1,3)
L=lambda k: .299*pal[k][0]+.587*pal[k][1]+.114*pal[k][2]
gebruikt=sorted(set(o.ravel())); print('kleuren incl. transparant:',len(gebruikt),gebruikt, 'transparency',im.info.get('transparency'))
ys,xs=np.where(o>0); print('bbox x%d-%d y%d-%d (%dx%d), %d px'%(xs.min(),xs.max(),ys.min(),ys.max(),xs.max()-xs.min()+1,ys.max()-ys.min()+1,len(xs)))
P=np.pad(o,1)
los=[];lijn=[];licht=[]
for Y,X in zip(ys,xs):
    n4=[P[Y+1+dy,X+1+dx] for dy,dx in ((-1,0),(1,0),(0,-1),(0,1))]
    n8=[P[Y+1+dy,X+1+dx] for dy in (-1,0,1) for dx in (-1,0,1) if dy or dx]
    k=o[Y,X]
    if k not in n8: los.append((X,Y,k))
    if k in (1,2,6) and 0 not in n8 and sum(v in (1,2,6) for v in n8)==0: lijn.append((X,Y,k))
    if 0 in n4 and L(k)>110: licht.append((X,Y,k))
print('losse pixels (geen gelijke 8-buur): %d'%len(los),los)
print('lijnpixel midden in vlak zonder lijnbuur: %d'%len(lijn),lijn)
print('lichte kleur (L>110) op de buitenrand: %d'%len(licht),licht)
print('zwart aandeel %.1f %%'%(100*(o==1).sum()/len(xs)))
