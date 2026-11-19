# Klasse + toon per natieve modelpixel. Uitvoer: klassen.npy (code per pixel) en _klassen5x.png
from PIL import Image; import numpy as np
b=np.asarray(Image.open('natief.png').convert('RGB')).astype(int)
R,G,B=b[...,0],b[...,1],b[...,2]; H,W=R.shape
lum=0.299*R+0.587*G+0.114*B
yy,xx=np.mgrid[0:H,0:W]
K=np.zeros((H,W),int)  # 0 bg
# codes: 1 zwart, 2/3/4 geel licht/mid/donker, 5/6 wang licht/donker, 7/8/9 staart licht/mid/donker,
# 10/11 grijs licht/donker, 12/13 vleugel licht/donker, 14 creme stip, 15 glans wit
bg=(R>=225)&(G>=225)&(B>=210)
K[bg]=0
blk=(lum<45)&~bg; K[blk]=1
yel=(R>185)&(G>135)&(R-B>50)&~bg&~blk
K[yel&(B>=120)]=2; K[yel&(B<120)&(G>=200)]=3; K[yel&(B<120)&(G<200)]=4
red=(R>110)&(R-G>45)&~bg&~blk&~yel
chk=red&(yy<95); K[chk&(R>=205)]=5; K[chk&(R<205)]=6
tl=red&(yy>=95); K[tl&(R>=195)]=7; K[tl&(R>=160)&(R<195)]=8; K[tl&(R<160)]=9
brn=(R-B>=18)&(lum<130)&(lum>=45)&(R>=G)&~bg&~yel&~red
gry=~brn&(np.abs(R-G)<22)&(np.abs(G-B)<28)&~bg&~blk&~yel&~red
K[gry&(lum>118)]=10; K[gry&(lum<=118)]=11
inw=((xx>105)&(yy>76)&(yy<136))|((xx<80)&(yy>80)&(yy<130))
K[brn&~inw]=1
wng=brn&inw
K[wng&(lum>=85)]=12; K[wng&(lum<85)]=13
wf=np.zeros_like(wng)
for y in range(H):
    c=np.where(wng[y]&(xx[y]>105))[0]
    if len(c): wf[y,c.min():c.max()+1]=True
for x in range(W):
    c=np.where(wng[:,x]&(xx[:,x]>105))[0]
    if len(c): wf[c.min():c.max()+1,x]&=True
pale=wf&~wng&~blk&(lum>=130)&~bg&(yy<125)
K[pale]=14
rest=(K==0)&~bg&~blk&(lum>=130); K[rest]=15
# glans in het oog: lichte grijze pixel omringd door zwart (oog-uitsnede)
np.save('klassen.npy',K)
COL={0:(255,255,255),1:(24,20,16),2:(250,236,150),3:(238,206,86),4:(210,164,52),5:(232,82,58),6:(178,42,34),
7:(200,130,72),8:(186,96,44),9:(123,41,8),10:(170,170,170),11:(90,90,96),12:(156,82,0),13:(98,49,8),14:(240,232,184),15:(255,0,255)}
img=np.zeros((H,W,3),'uint8')
for k,c in COL.items(): img[K==k]=c
Image.fromarray(img).resize((W*5,H*5),0).save('_klassen5x.png')
for k in range(16): print(k,(K==k).sum())
