# controle.py SPRITE.png: Gen 3-eisen meten (kleuren, kleine tintvlekjes, lichte buitenrand, losse zwarte pixels, zwart-%)
import sys, numpy as np; from PIL import Image
im=Image.open(sys.argv[1]); o=np.asarray(im).astype(int)
CH='.#abcdRSTxyzCDeh'
def label(mask):
    lab=np.zeros(mask.shape,int); n=0
    for y,x in zip(*np.where(mask)):
        if lab[y,x]: continue
        n+=1; st=[(y,x)]; lab[y,x]=n
        while st:
            cy,cx=st.pop()
            for dy,dx in ((1,0),(-1,0),(0,1),(0,-1),(1,1),(1,-1),(-1,1),(-1,-1)):
                yy,xx=cy+dy,cx+dx
                if 0<=yy<64 and 0<=xx<64 and mask[yy,xx] and not lab[yy,xx]: lab[yy,xx]=n; st.append((yy,xx))
    return lab,n
print(sys.argv[1],'formaat',im.size,im.mode,'transp',im.info.get('transparency'),'kleuren gebruikt incl. transp.',len(set(o.ravel())),'palet',len(im.getpalette())//3)
fg=o>0; yy,xx=np.where(fg); print('bbox x%d-%d y%d-%d, %d px'%(xx.min(),xx.max(),yy.min(),yy.max(),fg.sum()))
print('zwart %.1f%% van de figuur'%(100*(o==1).sum()/fg.sum()))
for k in range(2,16):
    lab,n=label(o==k)
    pts=[tuple(int(v) for v in np.argwhere(lab==i)[0][::-1]) for i in range(1,n+1) if (lab==i).sum()<3]
    if pts: print('  tint %s (%d): %d vlekjes <3 px op (x,y) %s'%(CH[k],k,len(pts),pts))
licht={4,5,7,8,10,11,12,13,14,15}
rand=[(int(X),int(Y),CH[o[Y,X]]) for Y,X in zip(yy,xx) if o[Y,X] in licht and (not fg[Y,X-1] or not fg[Y,X+1] or not fg[Y-1,X] or not fg[Y+1,X])]
print('lichte/midden kleur op de buitenrand:',rand)
los=[(int(X),int(Y)) for Y,X in zip(*np.where(o==1)) if all(o[Y+dy,X+dx] not in (0,1) for dy in (-1,0,1) for dx in (-1,0,1) if dy or dx)]
print('losse zwarte pixels:',los)
