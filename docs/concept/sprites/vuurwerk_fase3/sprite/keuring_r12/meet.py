# Meting r12 sprite_B_p2: palet, transparantie, rand, kleine clusters, vergelijking met r9-reparaties.
import numpy as np; from PIL import Image
from scipy import ndimage
from collections import Counter
im=Image.open('../r12/sprite_B_p2.png'); s=np.array(im); pal=np.array(im.getpalette()[:48]).reshape(16,3)
print('mode',im.mode,im.size,'transparency',im.info.get('transparency'),'palet-len',len(im.getpalette())//3)
u=np.unique(s); print('indices gebruikt',u.tolist())
for i in u: print(i,tuple(pal[i]),'L=%d'%int(.299*pal[i][0]+.587*pal[i][1]+.114*pal[i][2]),int((s==i).sum()))
op=s!=0
lab,n=ndimage.label(op,np.ones((3,3))); sz=np.bincount(lab.ravel())[1:]
big=lab==(np.argmax(sz)+1); print('componenten',n,'grootste',sorted(sz)[-4:])
rb=big&~ndimage.binary_erosion(big,np.ones((3,3)),border_value=0)
print('rand hoofdmassa per index',sorted(Counter(s[rb]).items()))
# rand: alleen randpixels die aan transparant grenzen (4-buren)
t=~op; pad=np.pad(t,1,constant_values=True)
r4=op&(pad[:-2,1:-1]|pad[2:,1:-1]|pad[1:-1,:-2]|pad[1:-1,2:])&big
print('buitenrand (4-buur transp) per index',sorted(Counter(s[r4]).items()))
for i in u:
    if i==0: continue
    L=.299*pal[i][0]+.587*pal[i][1]+.114*pal[i][2]
    if L>120:
        ys,xs=np.where(r4&(s==i))
        if len(xs): print(' lichte idx',i,'op buitenrand:',[(int(x),int(y)) for x,y in zip(xs,ys)])
print('clusters <3 px (4-buren) in hoofdmassa:')
for i in u:
    if i==0: continue
    l,k=ndimage.label(big&(s==i)); c=[(int(np.mean(np.where(l==j)[1])),int(np.mean(np.where(l==j)[0])),int((l==j).sum())) for j in range(1,k+1) if (l==j).sum()<3]
    if c: print(' ',i,len(c),c)
# zwart(1?) / donkerlila om en om op buitenrand
d=sorted(u[1:],key=lambda i:pal[i].sum())[:2]; print('donkerste twee indices',d)
alt=[]
for y,x in zip(*np.where(r4)):
    if s[y,x]!=d[0]: continue
    nb=[(y+dy,x+dx) for dy in(-1,0,1) for dx in(-1,0,1) if (dy or dx) and 0<=y+dy<64 and 0<=x+dx<64 and r4[y+dy,x+dx]]
    if sum(s[p]==d[1] for p in nb)>=2 and sum(s[p]==d[0] for p in nb)==0: alt.append((int(x),int(y)))
print('losse donkerste randpixels tussen 2e donkerste:',alt)
# r9->r12 diff
r9=np.array(Image.open('../r9/sprite_a.png')); r10=np.array(Image.open('../r10/sprite_B.png'))
for nm,a in (('r9',r9),('r10',r10)):
    ys,xs=np.where(a!=s); print('diff met',nm,len(xs), sorted((int(x),int(y)) for x,y in zip(xs,ys)) if len(xs)<40 else '')
# zwart(1) los tussen donkerlila(6) op de buitenrand, en omgekeerd
for a_,b_ in ((1,6),(6,1)):
    alt=[]
    for y,x in zip(*np.where(r4&(s==a_))):
        nb=[(y+dy,x+dx) for dy in(-1,0,1) for dx in(-1,0,1) if (dy or dx) and 0<=y+dy<64 and 0<=x+dx<64 and r4[y+dy,x+dx]]
        if sum(s[p]==b_ for p in nb)>=2 and sum(s[p]==a_ for p in nb)==0: alt.append((int(x),int(y)))
    print('los',a_,'tussen',b_,':',alt)
# gaten in de buitenlijn: transparante pixels die 4-buur zijn van een binnenvlak (niet-lijn) van de hoofdmassa
lijn={1,2,6,9,10,14}
gat=[(int(x),int(y)) for y,x in zip(*np.where(r4)) if s[y,x] not in lijn]
print('niet-lijnkleur op buitenrand hoofdmassa:',gat)
# 8-verbonden clusters <3 px voor vlakkleuren (niet de lijnkleuren)
print('vlak-clusters <3 (8-buren), lijf+kop:')
for i in (3,4,5,7,8,11,12,13,15):
    l,k=ndimage.label(big&(s==i),np.ones((3,3))); c=[(int(np.mean(np.where(l==j)[1])),int(np.mean(np.where(l==j)[0])),int((l==j).sum())) for j in range(1,k+1) if (l==j).sum()<3]
    if c: print(' ',i,c)
