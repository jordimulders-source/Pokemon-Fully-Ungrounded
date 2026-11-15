# Vel c6: (1) a | b | c greige op 8x + c5; (2) koppen op 12x naast de foto-kop; (3) 3x en 1x (greige en grijs) naast
# Regirock, Golem, Growlithe en de volwassen vorm; (4) lichtcheck a/b/c (lijn / schaduw 3 / midden 4 / licht 5+).
from PIL import Image, ImageDraw
import numpy as np
G='../../../../../../graphics/pokemon/'
def wit(im):
    im=im.convert('RGBA'); bg=Image.new('RGBA',im.size,(255,255,255,255)); bg.alpha_composite(im); return bg.convert('RGB')
def gba(s):
    im=Image.open(G+s+'/anim_front_gba.png').crop((0,0,64,64)); im.info['transparency']=0; return wit(im.convert('RGBA'))
def png(f):
    im=Image.open(f); im.info['transparency']=0; return wit(im.convert('RGBA'))
def licht(f):
    a=np.asarray(Image.open(f).convert('RGBA')).astype(int); L=a[...,:3]@np.array([.299,.587,.114]); m=a[...,3]>0
    o=np.full(L.shape+(3,),255,np.uint8)
    o[m&(L<100)]=(30,30,30); o[m&(L>=100)&(L<135)]=(95,95,95); o[m&(L>=135)&(L<170)]=(160,160,160); o[m&(L>=170)]=(230,230,230)
    return Image.fromarray(o)
V=[('c6 a: wenkbrauwvoluut + middenlijn','welp_c6_a.png'),('c6 b: U naar de kruin + boog','welp_c6_b.png'),('c6 c: voluut boven het oog (foto)','welp_c6_c.png'),('c5 (vorige)','../c5/welp_c5.png')]
S=12; kb=(6,16,34,42); kw,kh=(kb[2]-kb[0])*S,(kb[3]-kb[1])*S
foto=Image.open('../../referenties/chavin_jaguar_beeld_jordi.png').convert('RGB').crop((400,50,520,170)).resize((kh,kh),Image.LANCZOS)
W=4*522; H=20+512+40+kh+40+192+10+64+40+192+20
o=Image.new('RGB',(W,H),'white'); d=ImageDraw.Draw(o)
for i,(n,f) in enumerate(V):
    o.paste(png(f).resize((512,512),Image.NEAREST),(i*522,20)); d.text((i*522+4,4),n,fill='black')
y=20+512+40; d.text((4,y-14),'kop 12x: a | b | c | foto',fill='black')
for i,(_,f) in enumerate(V[:3]): o.paste(png(f).crop(kb).resize((kw,kh),Image.NEAREST),(i*(kw+10),y))
o.paste(foto,(3*(kw+10),y))
y+=kh+40; d.text((4,y-14),'3x en 1x: a, b, c (greige), a, b, c (grijs), Regirock, Golem, Growlithe, volwassen',fill='black')
rij=[png(f) for _,f in V[:3]]+[png(f'welp_c6_{v}_grijs.png') for v in 'abc']+[gba('regirock'),gba('golem'),gba('growlithe'),png('../../af/steenjaguar.png')]
for i,m in enumerate(rij):
    o.paste(m.resize((192,192),Image.NEAREST),(i*205,y)); o.paste(m,(i*205+64,y+192+10))
y+=192+10+64+40; d.text((4,y-14),'lichtcheck (lijn / schaduw 3 / midden 4 / licht 5+): a, b, c, c grijs',fill='black')
for i,f in enumerate(['welp_c6_a.png','welp_c6_b.png','welp_c6_c.png','welp_c6_c_grijs.png']):
    o.paste(licht(f).resize((192,192),Image.NEAREST),(i*205,y))
o.save('vel.png')
