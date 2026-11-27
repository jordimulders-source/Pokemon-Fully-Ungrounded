# controle.py SPRITE.png [KAAL.png]: Gen 3-eisen meten (kleuren, kleine tintvlekjes, lichte buitenrand, losse zwarte pixels, gloedaandeel)
import sys, os, numpy as np; from PIL import Image
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__))); from gemeen import *
im=Image.open(sys.argv[1]); o=np.asarray(im).astype(int)
print('formaat',im.size,im.mode,'transp',im.info.get('transparency'),'kleuren incl. transp.',len(set(o.ravel())),'palet',len(im.getpalette())//3)
fg=o>0; yy,xx=np.where(fg); print('bbox x%d-%d y%d-%d (%dx%d), %d px'%(xx.min(),xx.max(),yy.min(),yy.max(),xx.max()-xx.min()+1,yy.max()-yy.min()+1,fg.sum()))
for k in sorted(set(o.ravel())-{0,1}):
    lab,n=label(o==k,acht=False); pts=[tuple(int(v) for v in np.argwhere(lab==i)[0][::-1]) for i in range(1,n+1) if (lab==i).sum()<3]
    if pts: print('  tint %s (%d): %d vlekjes <3 px'%(CH[k],k,len(pts)),pts if len(pts)<=12 else '')
nb4=lambda Y,X:[(Y+dy,X+dx) for dy,dx in ((1,0),(-1,0),(0,1),(0,-1))]
pal=np.array(im.getpalette()[:48]).reshape(-1,3); licht={k for k in range(2,16) if pal[k]@[.299,.587,.114]>170}
rand=[(int(X),int(Y),CH[o[Y,X]]) for Y,X in zip(yy,xx) if o[Y,X] in licht and any(not fg[p] for p in nb4(Y,X))]
print('lichte kleur op de buitenrand:',rand)
los=[(int(X),int(Y)) for Y,X in zip(*np.where(o==1)) if all(o[Y+dy,X+dx] not in (0,1) for dy in (-1,0,1) for dx in (-1,0,1) if dy or dx)]
print('losse zwarte pixels:',los)
st=np.isin(o,[13,14,15])|((o==10)&(np.arange(64)[:,None]>18)); print('gloed/steen: %d/%d'%(np.isin(o,[14,15]).sum(),st.sum()))
if len(sys.argv)>2:
    k=np.asarray(Image.open(sys.argv[2])).astype(int); print('afwijkend van',sys.argv[2],':',(k!=o).sum(),'px')
