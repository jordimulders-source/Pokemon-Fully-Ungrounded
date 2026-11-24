# Bewijs (alfa- en kopdiff, RGB) voor A en B + voor_na.png (voor | A | B | Furret | Kangaskhan, 6x en 1x)
from PIL import Image, ImageDraw
import os
H=os.path.dirname(os.path.abspath(__file__)); R=os.path.join(H,'../../../../../..')
v=Image.open(os.path.join(H,'../../../olinguito_v2/af/olinguito.png'))
# kopzone: kop met masker, oog, snoet, neus, oor, kruin, nekschaduw en de lijn eromheen
KOP={(x,y) for x in range(0,32) for y in range(0,39)}|{(x,y) for x in range(0,25) for y in range(39,46)}|{(x,y) for x in range(25,29) for y in range(39,42)}|{(24,42),(25,42),(26,42)}
def rgb(im):
    a=im.convert('RGBA'); return a.load()
vr=rgb(v); vp=v.load()
for naam in ('na.png','na_B.png'):
    n=Image.open(os.path.join(H,naam)); assert n.mode=='P' and n.size==(64,64)
    nr=rgb(n); np_=n.load()
    alfa=sum((vp[x,y]==0)!=(np_[x,y]==0) for x in range(64) for y in range(64))
    kop=sum(vr[x,y]!=nr[x,y] for x,y in KOP)
    idx=sum(vp[x,y]!=np_[x,y] for x in range(64) for y in range(64))
    kl=len({np_[x,y] for x in range(64) for y in range(64)}-{0})
    print(naam,'alfadiff',alfa,'kopdiff(RGB)',kop,'pixels andere index',idx,'kleuren',kl,'index5',n.getpalette()[15:18])
ims=[v,Image.open(os.path.join(H,'na.png')),Image.open(os.path.join(H,'na_B.png'))]+[Image.open(os.path.join(R,'graphics/pokemon/%s/anim_front_gba.png'%s)).crop((0,0,64,64)) for s in ('furret','kangaskhan')]
lab=['voor','A','B','Furret (Gen 3)','Kangaskhan (Gen 3)']
z=6; W=len(ims)*(64*z+10)
o=Image.new('RGB',(W,64*z+64+40),'white'); d=ImageDraw.Draw(o)
for i,(im,l) in enumerate(zip(ims,lab)):
    a=im.convert('RGBA'); X=i*(64*z+10); b=a.resize((64*z,64*z),Image.NEAREST)
    o.paste(b,(X,14),b); o.paste(a,(X+64*z//2-32,64*z+30),a); d.text((X+4,1),l,fill=(0,0,0))
o.save(os.path.join(H,'voor_na.png'))
