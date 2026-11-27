"""Onderdelen van de Gumfish-front (blobfish/af/blobfish.png, 64x64) als polygonen; eerste match wint.
Kopie van viscacha/icoon/onderdelen/delen.py, aangepast. python3 delen.py -> delen_vel.png + delen.npy"""
import os,numpy as np
from PIL import Image,ImageDraw
H=os.path.dirname(os.path.abspath(__file__))+'/'
FRONT=H+'../../../blobfish/af/blobfish.png'
DELEN=[  # naam, kleur, polygoon (x,y)
 ('staartvin',(230,60,60),[(44,25),(59,25),(59,38),(49,38),(46,33),(44,31)]),
 ('borstvin',(240,200,0),[(28,39),(40,39),(40,52),(28,52)]),
 ('kop',(255,130,200),[(6,30),(24,30),(24,40),(23,54),(6,54)]),
 ('romp',(170,120,70),[(22,27),(50,27),(50,56),(22,56)]),
]
fr=np.array(Image.open(FRONT))[:64]; lab=np.zeros((64,64),np.int8)-1
for i,(n,c,poly) in reversed(list(enumerate(DELEN))):
    m=Image.new('L',(64,64),0); ImageDraw.Draw(m).polygon(poly,fill=1,outline=1); m=np.array(m)>0
    lab[m&(fr>0)]=i
if __name__=='__main__':
    np.save(H+'delen.npy',lab)
    P=np.array(Image.open(FRONT).getpalette()[:48]).reshape(16,3)
    o=np.full((64,64,3),255,np.uint8); t=o.copy()
    for k in range(1,16): o[fr==k]=P[k]
    for i,(n,c,_) in enumerate(DELEN): t[lab==i]=c
    mix=(o*0.45+t*0.55).astype(np.uint8); mix[fr==0]=255
    W=Image.new('RGB',(64*8*2+20+220,64*8),'white')
    W.paste(Image.fromarray(o).resize((512,512),Image.NEAREST),(0,0)); W.paste(Image.fromarray(mix).resize((512,512),Image.NEAREST),(532,0))
    d=ImageDraw.Draw(W)
    for i,(n,c,_) in enumerate(DELEN):
        d.rectangle((1060,20+i*26,1078,38+i*26),fill=c); d.text((1084,22+i*26),n,fill=0)
    print('niet ingedeeld:',int(((lab<0)&(fr>0)).sum()))
    W.save(H+'delen_vel.png')
