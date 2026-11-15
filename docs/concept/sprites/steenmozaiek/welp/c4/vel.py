# Vel c4 voor Jordi: (1) A greige | A grijs | B greige | B grijs op 8x; (2) kop op 12x (A, B) naast de foto-kop;
# (3) 3x en 1x naast Growlithe, Regirock en de volwassen vorm; (4) lichtcheck A en B (lijn / schaduw / midden / licht).
from PIL import Image, ImageDraw
import numpy as np
G='../../../../../../graphics/pokemon/'
def wit(im):
    im=im.convert('RGBA'); bg=Image.new('RGBA',im.size,(255,255,255,255)); bg.alpha_composite(im); return bg.convert('RGB')
def gba(s):
    im=Image.open(G+s+'/anim_front_gba.png').crop((0,0,64,64)); im.info['transparency']=0; return wit(im.convert('RGBA'))
def png(f): return wit(Image.open(f))
def licht(f):
    a=np.asarray(Image.open(f).convert('RGBA')).astype(int); L=a[...,:3]@np.array([.299,.587,.114]); m=a[...,3]>0
    o=np.full(L.shape+(3,),255,np.uint8)
    o[m&(L<100)]=(30,30,30); o[m&(L>=100)&(L<135)]=(95,95,95); o[m&(L>=135)&(L<170)]=(160,160,160); o[m&(L>=170)]=(230,230,230)
    return Image.fromarray(o)
V=[('A greige','welp_c4_A.png'),('A grijs','welp_c4_A_grijs.png'),('B greige','welp_c4_B.png'),('B grijs','welp_c4_B_grijs.png')]
S=12; kb=(6,16,34,42); kw,kh=(kb[2]-kb[0])*S,(kb[3]-kb[1])*S
foto=Image.open('../../referenties/chavin_jaguar_beeld_jordi.png').convert('RGB').crop((400,50,520,170)).resize((kh,kh),Image.LANCZOS)
W=4*522; H=20+512+40+kh+40+192+10+64+40+192+20
o=Image.new('RGB',(W,H),'white'); d=ImageDraw.Draw(o)
for i,(n,f) in enumerate(V):
    o.paste(png(f).resize((512,512),Image.NEAREST),(i*522,20)); d.text((i*522+4,4),n,fill='black')
y=20+512+40; d.text((4,y-14),'kop 12x: A (boog naar oorbasis) | B (boog om het oog) | foto',fill='black')
o.paste(png('welp_c4_A.png').crop(kb).resize((kw,kh),Image.NEAREST),(0,y)); o.paste(png('welp_c4_B.png').crop(kb).resize((kw,kh),Image.NEAREST),(kw+10,y)); o.paste(foto,(2*kw+20,y))
y+=kh+40; d.text((4,y-14),'3x en 1x',fill='black')
rij=[png(f) for _,f in V]+[gba('growlithe'),gba('regirock'),png('../../af/steenjaguar.png')]
for i,m in enumerate(rij):
    o.paste(m.resize((192,192),Image.NEAREST),(i*200,y)); o.paste(m,(i*200+64,y+192+10))
y+=192+10+64+40; d.text((4,y-14),'lichtcheck (lijn / schaduw 3 / midden 4 / licht 5+): A, B, A grijs',fill='black')
for i,f in enumerate(['welp_c4_A.png','welp_c4_B.png','welp_c4_A_grijs.png']):
    o.paste(licht(f).resize((192,192),Image.NEAREST),(i*200,y))
o.save('vel.png')
