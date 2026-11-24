"""Capykart r12: twee varianten (crème vanuit r11, wit vanuit r10), alleen tintwissels."""
import os
from PIL import Image
D=os.path.dirname(os.path.abspath(__file__))
def load(p):
    im=Image.open(os.path.join(D,p)); return im,[[im.getpixel((x,y)) for x in range(64)] for y in range(64)]
L=[]
def sw(g,pts,frm,to,why,tag):
    for x,y in pts:
        v=g[y][x]
        if v in frm: g[y][x]=to; L.append(f'{tag}: ({x},{y}) {v:X}->{to:X}  {why}')
        else: L.append(f'{tag}: ({x},{y}) overgeslagen (index {v:X})  {why}')
def save(im,g,name):
    o=Image.new('P',(64,64)); o.putpalette(im.getpalette()); o.putdata([v for r in g for v in r]); o.save(os.path.join(D,name),transparency=0)
    o.convert('RGBA').resize((512,512),Image.NEAREST).save(os.path.join(D,name.replace('.png','_8x.png')))
WANG=[(25,20),(24,21),(25,21),(24,22)]
SNUIT=[(x,y) for y in (20,21) for x in range(17,22)]
HOEP=[(30,48),(31,48),(32,48)]   # onderkant voorste hoepel waar hij achter de kap/wiel duikt: hoepel 8 lag zonder lijn op hout
# crème
im,g=load('../r11/capykart.png'); t='creme'
sw(g,WANG,[2],14,'1 vacht-hooglicht linksboven op de wang',t)
sw(g,SNUIT,[3],2,'2 snuit-voorvlak licht (lichtkant)',t)
sw(g,[(x,15) for x in range(45,50)],[9],5,'3 onderkant geel voorvlak',t)
sw(g,HOEP,[5,6],1,'4 lijn onder de hoepel',t)
save(im,g,'r12_creme.png')
# wit
im,g=load('../r10/capykart.png'); t='wit'
sw(g,WANG,[3],2,'1 wang linksboven 3->2 (alleen waar 3; hier al 2)',t)
sw(g,SNUIT,[3],2,'2 snuit-voorvlak licht',t)
sw(g,HOEP,[5,6],1,'4 lijn onder de hoepel',t)
save(im,g,'r12_wit.png')
# controles
r7=Image.open(os.path.join(D,'../../eindkeuring/capykart_r7.png')).load()
fz=[(x,y) for x in range(28,32) for y in range(16,22)]+[(x,y) for x in range(17,24) for y in range(30,34)]+[(21,15),(22,15),(23,15),(21,16),(22,16),(23,16),(15,22),(16,22),(18,28),(19,28)]+[(x,30) for x in range(25,29)]
for nm,ref in (('r12_creme.png','../r11/capykart.png'),('r12_wit.png','../r10/capykart.png')):
    b=Image.open(os.path.join(D,nm)).load(); r=Image.open(os.path.join(D,ref)).load()
    L.append(f'{nm}: alpha-diff t.o.v. r7 {sum((r7[x,y]==0)!=(b[x,y]==0) for x in range(64) for y in range(64))}; bevroren index-diff t.o.v. {ref.split("/")[1]} {sum(b[p]!=r[p] for p in fz)}')
open(os.path.join(D,'log.txt'),'w').write('\n'.join(L)+'\n'); print('\n'.join(L))
