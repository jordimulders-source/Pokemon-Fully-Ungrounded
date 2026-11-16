# Meting r9 sprite_a: kleuren, randkleuren, kleine clusters per index.
import numpy as np, json; from PIL import Image
from scipy import ndimage
s=np.array(Image.open('../r9/sprite_a.png')); P=json.load(open('../r9/palet.json'))
op=s!=0
print('kleuren incl transp',len(np.unique(s)))
rand=op&~ndimage.binary_erosion(op,np.ones((3,3)),border_value=0)
from collections import Counter
print('randpixels per index',sorted(Counter(s[rand]).items()))
# grote componenten (lijf) vs losse spikkels
lab,n=ndimage.label(op,np.ones((3,3)))
sz=ndimage.sum(op,lab,range(1,n+1)); print('componenten',n,'grootste',sorted(sz)[-3:])
big=lab==(np.argmax(sz)+1)
rb=big&~ndimage.binary_erosion(big,np.ones((3,3)),border_value=0)
print('rand hoofdmassa per index',sorted(Counter(s[rb]).items()))
for i in range(1,16):
    l,k=ndimage.label(big&(s==i)); c=[(int(np.mean(np.where(l==j)[1])),int(np.mean(np.where(l==j)[0])),int((l==j).sum())) for j in range(1,k+1) if (l==j).sum()<3]
    if c: print(i,P[i],'clusters<3 in lijf:',len(c),c[:12])
# los gedeelte buiten de hoofdmassa: waar
ys,xs=np.where(op&~big); print('pixels buiten hoofdmassa',len(xs))
q=op&~big; print(' linksonder x<27,y>28:',int(q[28:,:27].sum()),' kopzone y<30:',int(q[:30].sum()))
print('lichte kleuren op buitenrand hoofdmassa (idx 4,5,7,8,12,13,15):')
for i in (4,5,7,8,12,13,15):
    ys,xs=np.where(rb&(s==i)); print(i,[(int(x),int(y)) for x,y in zip(xs,ys)])
# zwart vs donkerlila (6) op rand: lichtkant check grof
# zwart(1) en donkerlila(6) om en om op de rand: randpixels 1 met >=2 rand-buren 6 en omgekeerd
alt=[]
for y,x in zip(*np.where(rb&(s==1))):
    nb=[(y+dy,x+dx) for dy in(-1,0,1) for dx in(-1,0,1) if (dy or dx) and 0<=y+dy<64 and 0<=x+dx<64 and rb[y+dy,x+dx]]
    if sum(s[p]==6 for p in nb)>=2 and sum(s[p]==1 for p in nb)==0: alt.append((int(x),int(y)))
print('losse zwarte randpixels tussen donkerlila:',alt)
