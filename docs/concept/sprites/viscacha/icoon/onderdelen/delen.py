"""Onderdelen van de viscacha-front (64x64), als polygonen; eerste match wint.
python3 delen.py -> delen_vel.png (front met gekleurde onderdelen) en delen.npy (label per pixel)"""
import numpy as np
from PIL import Image,ImageDraw
D='docs/concept/sprites/viscacha/'
DELEN=[  # naam, kleur, polygoon (x,y)
 ('staart',(230,60,60),[(47,14),(63,14),(63,50),(48,50),(48,46),(52,46),(52,30),(49,24)]),
 ('verre oor',(60,60,230),[(8,14),(16,14),(16,27),(9,27)]),
 ('nabije oor',(30,140,255),[(18,15),(28,15),(28,27),(19,27)]),
 ('nekpluk',(240,200,0),[(17,29),(28,28),(28,38),(19,38)]),
 ('kop',(255,130,200),[(0,26),(15,21),(19,21),(28,26),(23,40),(15,42),(8,41),(0,44)]),
 ('opgeheven poot',(140,0,200),[(11,43),(19,43),(20,51),(11,51)]),
 ('bef',(250,240,150),[(14,38),(24,38),(24,47),(15,47)]),
 ('voorpoot',(0,170,90),[(19,46),(27,46),(27,54),(19,54)]),
 ('verre achterpoot',(0,110,60),[(24,50),(37,49),(37,61),(24,61)]),
 ('dij en achtervoet',(255,150,40),[(30,38),(48,38),(51,50),(51,63),(42,63),(36,53),(30,50)]),
 ('romp',(170,120,70),[(22,27),(48,27),(48,52),(22,52)]),
]
fr=np.array(Image.open(D+'af/viscacha.png'))[:64]; lab=np.zeros((64,64),np.int8)-1
for i,(n,c,poly) in reversed(list(enumerate(DELEN))):
    m=Image.new('L',(64,64),0); ImageDraw.Draw(m).polygon(poly,fill=1,outline=1); m=np.array(m)>0
    lab[m&(fr>0)]=i
if __name__=='__main__':
    np.save(D+'icoon/onderdelen/delen.npy',lab)
    L=open(D+'af/normal.pal').read().split('\n'); P=[tuple(int(v) for v in L[3+k].split()[:3]) for k in range(16)]
    o=np.full((64,64,3),255,np.uint8); t=o.copy()
    for k in range(1,16): o[fr==k]=P[k]
    for i,(n,c,_) in enumerate(DELEN): t[lab==i]=c
    mix=(o*0.45+t*0.55).astype(np.uint8); mix[fr==0]=255
    Z=8; W=Image.new('RGB',(64*Z*2+20+220,64*Z),'white')
    W.paste(Image.fromarray(o).resize((512,512),Image.NEAREST),(0,0)); W.paste(Image.fromarray(mix).resize((512,512),Image.NEAREST),(532,0))
    d=ImageDraw.Draw(W)
    for i,(n,c,_) in enumerate(DELEN):
        d.rectangle((1060,20+i*26,1078,38+i*26),fill=c); d.text((1084,22+i*26),n,fill=0)
    print('niet ingedeeld:',int(((lab<0)&(fr>0)).sum()))
    W.save(D+'icoon/onderdelen/delen_vel.png')
