# Ronde 10: basis r9. Alleen neusomlijning en rand linkeroog gesloten langs de modellijn (lijn.py: % zwart / % a per cel
# op het 1024-model). Buiten deze pixels: diff 0 met r9.
import numpy as np; from PIL import Image
D='/home/user/Pokemon-Fully-Ungrounded/docs/concept/sprites/mate/sprite/'
im=Image.open(D+'r9/mate.png'); PAL=im.getpalette(); r9=np.asarray(im).astype(int); a=r9.copy()
K={'#':1,'a':2,'b':3,'c':4,'d':5}
FIX=[
 # neus: C-boog rechts; (26,41) was in r9 door de opschoning c geworden
 (26,41,'a','neus','C-boog rechtsboven: model 0% zwart / 48% donkerbruin'),
 # linkeroog: dikke rand linksboven = zwart binnen (bestond al) + donkerbruine buitenring
 (18,36,'a','linkeroog','buitenring linksboven: model 9/53'),
 (17,37,'a','linkeroog','buitenring links: model 6/50'),
 (17,38,'a','linkeroog','buitenring links: model 12/35'),
 (21,34,'a','linkeroog','bovenrand: model 18/21 (donkerbruin iets meer dan zwart)'),
 (21,38,'a','linkeroog','rand rechtsonder: model 23/22 (gemengd; rand buiten linksboven = a)'),
 (18,39,'a','linkeroog','onderrand links: model 3/25'),
]
for x,y,k,_,_ in FIX: a[y,x]=K[k]
p=Image.fromarray(a.astype('uint8'),'P'); p.putpalette(PAL); p.save(D+'r10/mate.png',transparency=0)
Y,X=np.mgrid[0:64,0:64]; ZN=(X>=18)&(X<=28)&(Y>=40)&(Y<=46); ZO=(X>=16)&(X<=23)&(Y>=33)&(Y<=40)
d=a!=r9; print('buiten neus/linkeroog anders dan r9:',int((d&~(ZN|ZO)).sum()),'| neus:',int((d&ZN).sum()),'| linkeroog:',int((d&ZO).sum()))
