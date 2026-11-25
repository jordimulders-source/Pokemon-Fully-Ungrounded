# r22 keuzevel: rij 1 = r18 | r20 | 7 | 8 | 9 (16x, blauwe lijn = as van de V: midden bovenrand -> punt, rood kader = punt),
# rij 2 = micro-varianten 1-6, rij 3 = alles op 1x (en 2x)
from PIL import Image, ImageDraw
bg=(200,230,200,255); C=(20,20,40,38); Z=16
def L(p): return Image.open(p).convert('RGBA').crop((0,0,64,64))
AS={'r18':(31.0,30.5),'r20':(32.0,30.5),'7':(31.0,29.5),'8':(31.0,28.5),'9':(31.0,27.5)}   # (midden bovenrand, midden punt) in pixelcoord.
items=[('r18','../sprite_r18/bokser.png'),('r20','r20_basis.png'),('7','var/v7_as1.png'),('8','var/v8_as2.png'),('9','var/v9_as3.png'),
       ('1','var/v1_flank_recht.png'),('2','var/v2_punt_lager.png'),('3','var/v3_punt_hoger.png'),('4','var/v4_boven_links.png'),('5','var/v5_rechts_extra.png'),('6','var/v6_1en5.png')]
def tegel(lab,p):
    i=L(p).crop(C); i=i.resize((i.width*Z,i.height*Z),Image.NEAREST); t=Image.new('RGBA',(i.width,i.height+20),bg); t.paste(i,(0,0),i)
    d=ImageDraw.Draw(t)
    if lab in AS:
        tx,px=AS[lab]
        d.line([((tx-C[0])*Z,(25.5-C[1])*Z),((px-C[0])*Z,(33.5-C[1])*Z)],fill=(0,80,255,255),width=3)
        q=(px-.5-C[0])*Z,(33-C[1])*Z; d.rectangle((q[0],q[1],q[0]+Z-1,q[1]+Z-1),outline=(220,0,0,255),width=2)
    d.text((6,i.height+4),lab,fill=(0,0,0,255)); return t
T=[tegel(l,p) for l,p in items]; w,h=T[0].size
W=Image.new('RGBA',(6*(w+8),2*(h+8)+150),bg)
for k,t in enumerate(T[:5]): W.paste(t,(k*(w+8),0))
for k,t in enumerate(T[5:]): W.paste(t,(k*(w+8),h+8))
d=ImageDraw.Draw(W)
for k,(l,p) in enumerate(items):
    i=L(p); W.paste(i,(k*130,2*(h+8)+4),i); i2=i.resize((128,128),Image.NEAREST)
    d.text((k*130+2,2*(h+8)+66),l,fill=(0,0,0,255))
W.save('v_keuzevel_16x.png')
