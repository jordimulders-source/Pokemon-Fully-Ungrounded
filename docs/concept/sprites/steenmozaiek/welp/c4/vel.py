# Vel c3: (1) kop op 12x: c2 | c3 A | c3 B | foto-kop; (2) hele sprite 3x en 1x: A, B, A grijs, B grijs, Regirock, Golem;
# (3) lichtcheck: A en B in 4 niveaus: lijn <100 L, schaduw <135, midden <170, licht om het lichtverloop te zien.
from PIL import Image, ImageDraw
import numpy as np
G='../../../../../../graphics/pokemon/'
def wit(im):
    im=im.convert('RGBA'); bg=Image.new('RGBA',im.size,(255,255,255,255)); bg.alpha_composite(im); return bg.convert('RGB')
def gba(s):
    im=Image.open(G+s+'/anim_front_gba.png').crop((0,0,64,64)); im.info['transparency']=0; return wit(im.convert('RGBA'))
def png(f): return wit(Image.open(f))
def licht(f):
    im=Image.open(f).convert('RGBA'); a=np.asarray(im).astype(int); L=a[...,:3]@np.array([.299,.587,.114])
    o=np.full(L.shape+(3,),255,np.uint8); m=a[...,3]>0
    o[m&(L<100)]=(30,30,30); o[m&(L>=100)&(L<135)]=(95,95,95); o[m&(L>=135)&(L<170)]=(160,160,160); o[m&(L>=170)]=(230,230,230)
    return Image.fromarray(o)
S=12; kb=(6,16,34,42); kw,kh=(kb[2]-kb[0])*S,(kb[3]-kb[1])*S
foto=Image.open('../../referenties/chavin_jaguar_beeld_jordi.png').convert('RGB').crop((400,50,520,170)).resize((kh,kh),Image.LANCZOS)
W=max(3*(kw+10)+kh, 6*200)+20; H=20+kh+40+192+20+64+40+192+20
o=Image.new('RGB',(W,H),'white'); d=ImageDraw.Draw(o)
for i,(n,f) in enumerate([('c2 (zonder koplijnen)','../c2/welp_c2.png'),('c3 A: wenkbrauwboog -> oorbasis','welp_c3_A.png'),('c3 B: boog om het oog met staartje','welp_c3_B.png')]):
    o.paste(png(f).crop(kb).resize((kw,kh),Image.NEAREST),(i*(kw+10),20)); d.text((i*(kw+10)+2,4),n,fill='black')
o.paste(foto,(3*(kw+10),20)); d.text((3*(kw+10)+2,4),'foto: kop',fill='black')
y=20+kh+40; d.text((4,y-14),'3x en 1x',fill='black')
rij=[png('welp_c3_A.png'),png('welp_c3_B.png'),png('welp_c3_A_grijs.png'),png('welp_c3_B_grijs.png'),gba('regirock'),gba('golem')]
for i,m in enumerate(rij):
    o.paste(m.resize((192,192),Image.NEAREST),(i*200,y)); o.paste(m,(i*200+64,y+192+10))
y2=y+192+10+64+30; d.text((4,y2-14),'lichtcheck (lijn / schaduw 3 / midden 4 / licht 5+): A, B, A grijs',fill='black')
for i,f in enumerate(['welp_c3_A.png','welp_c3_B.png','welp_c3_A_grijs.png']):
    o.paste(licht(f).resize((192,192),Image.NEAREST),(i*200,y2))
o.save('vel.png')
