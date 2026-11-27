"""Onderdelen van de Sunperor-front (koningstiran/af/sapa_inca.png, 64x64) als polygonen; eerste match wint.
Kopie van viscacha/icoon/onderdelen/delen.py, aangepast. python3 delen.py -> delen_vel.png + delen.npy"""
import os,numpy as np
from PIL import Image,ImageDraw
H=os.path.dirname(os.path.abspath(__file__))+'/'
FRONT=H+'../../../koningstiran/af/sapa_inca.png'
DELEN=[  # naam, kleur, polygoon (x,y)
 ('hand',(140,0,200),[(11,40),(21,40),(21,47),(11,47)]),
 ('staf',(240,200,0),[(13,18),(19,18),(19,49),(13,49)]),
 ('kop',(255,130,200),[(20,18),(35,18),(35,28),(29,31),(21,31),(20,28)]),
 ('kroonpunt',(60,60,230),[(7,23),(13,23),(13,33),(7,33)]),
 ('kroon',(255,120,40),[(6,0),(51,0),(51,22),(44,24),(35,22),(35,18),(20,18),(20,23),(7,23)]),
 ('vleugel',(0,170,90),[(37,17),(57,15),(57,35),(38,35),(36,28)]),
 ('poten',(0,110,60),[(20,53),(38,53),(38,63),(20,63)]),
 ('romp',(170,120,70),[(10,26),(42,26),(42,53),(10,53)]),
]
fr=np.array(Image.open(FRONT))[:64]; lab=np.zeros((64,64),np.int8)-1
for i,(n,c,poly) in reversed(list(enumerate(DELEN))):
    m=Image.new('L',(64,64),0); ImageDraw.Draw(m).polygon(poly,fill=1,outline=1); m=np.array(m)>0
    lab[m&(fr>0)]=i
# de staf is goud (frontkleuren 10,11,12,15 + omlijning 1); kroon- en lijfkleuren in het stafvak horen bij kroon/romp
NM=[d[0] for d in DELEN]; st=lab==NM.index('staf')
lab[st&np.isin(fr,[5,6,7,8,9])]=NM.index('kroon'); lab[st&np.isin(fr,[2,3,4])]=NM.index('romp')
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
