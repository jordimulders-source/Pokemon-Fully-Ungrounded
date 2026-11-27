# Jordi 27 nov: r4 als basis, staart van r3_3, stekel+band van r6 (alleen kopieren)
import sys, os
from PIL import Image
import numpy as np
from PIL import ImageFilter
os.chdir(os.path.join(os.path.dirname(os.path.abspath(__file__)),'..','gemini'))
L=lambda f: np.array(Image.open(f).convert('RGB')).astype(int)
out=L('r4.png'); r33=L('r3_3_Y_A.png'); r6=L('r6.png')
W=(255,255,255); nw=lambda a: a.sum(2)<720
nw2=lambda a: a.sum(2)<750
sdx,sdy,tdx,tdy,cut=[int(v) for v in sys.argv[1:6]]
# r4-staart weg
reg=out[380:830,cut:1024]; reg[nw2(reg)]=W
# r4-stekel weg (grijs + lijn erboven)
b=out[20:345,440:680]
grey=(abs(b[:,:,0]-b[:,:,2])<14)&(b.sum(2)<450)
blk=b.sum(2)<90
yy=np.arange(b.shape[0])[:,None]+20
top=(yy<255)&nw2(b)
E=(grey|blk)&~top&(yy>=255)
E&=~((np.arange(b.shape[1])[None,:]+440)>640)
b[top]=W
# gat in het schild onder de oude stekel: kleur van de pixel eronder
for x in range(b.shape[1]):
    for y in range(b.shape[0]-1,-1,-1):
        if E[y,x] and y+1<b.shape[0]: b[y,x]=b[y+1,x]
# staart r3_3
t=r33[400:790,765:1000]; m=nw(t)
yy,xx=np.mgrid[400:790,765:1000]
m&=(yy>=655)|(xx>=815)
for y,x in zip(*np.where(m)):
    Y,X=400+y+tdy,765+x+tdx
    if 0<=X<1024: out[Y,X]=t[y,x]
# stekel+band r6
s=r6[80:362,240:470]; ms=nw(s)
brown=(s[:,:,0]-s[:,:,2]>25)&(s.sum(2)<420)&(s.sum(2)>90)
col=ms&~brown&(s.sum(2)>=90)
near=np.array(Image.fromarray((col*255).astype('uint8')).filter(ImageFilter.MaxFilter(25)))>0
ms=col|(ms&(s.sum(2)<90)&near)
for y,x in zip(*np.where(ms)): out[80+y+sdy,240+x+sdx]=s[y,x]
# randruis (lichtgrijze antialias van het weggehaalde) naar wit
light=(out.sum(2)>640)&((out.max(2)-out.min(2))<25)
out[light]=W
# losse snippers (kleine eilandjes) weg
from PIL import ImageDraw
mk=Image.fromarray(((out.sum(2)<720)*255).astype('uint8'))
lab=np.array(mk).astype(int)
img=Image.fromarray(np.zeros_like(lab,dtype='uint8')); 
seen=np.zeros(lab.shape,bool)
for y,x in zip(*np.where(lab>0)):
    if seen[y,x]: continue
    tmp=mk.copy(); ImageDraw.floodfill(tmp,(int(x),int(y)),128)
    comp=np.array(tmp)==128; seen|=comp
    if comp.sum()<3000: out[comp]=W
Image.fromarray(out.astype('uint8')).save(sys.argv[6])
