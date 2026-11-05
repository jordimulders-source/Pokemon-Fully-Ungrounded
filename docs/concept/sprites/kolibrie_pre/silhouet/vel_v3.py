import sys; sys.path.insert(0,'.')
import vel, numpy as np
from PIL import Image, ImageDraw
R='../../../../../'
A=np.asarray(Image.open('silhouet_v3a_hand_1x.png'))<128
B=np.asarray(Image.open('silhouet_v3b_hand_1x.png'))<128
f1=Image.open('../referenties/jordi_1_zittend_jong.webp').convert('RGB').crop((200,140,740,710)).resize((230,243))
f5=Image.open('../referenties/jordi_5_uitvlieger_hand.webp').convert('RGB').crop((500,780,880,1100)).transpose(Image.FLIP_LEFT_RIGHT).resize((288,243))
f3=Image.open('../referenties/jordi_3_nestjongen.png').convert('RGB').crop((0,225,220,447)).resize((243,243))
V=Image.new('RGB',(1060,740),(235,235,235)); d=ImageDraw.Draw(V)
d.text((10,8),'Kolibrie pre-evo, silhouet v3: zittend, vleugels ingeklapt, open bedelbekje (foto 3). Kop links zoals de eindvorm.',fill=0)
V.paste(f1,(10,30)); V.paste(vel.render(A,4).crop((0,48,256,256)),(250,40)); V.paste(vel.render(A,1),(515,40)); V.paste(vel.render(A,2),(515,120))
d.text((250,252),f'A rechtop (foto 1)  {A.sum()} px',fill=0)
V.paste(f5,(10,290)); V.paste(vel.render(B,4).crop((0,48,256,256)),(310,300)); V.paste(vel.render(B,1),(575,300)); V.paste(vel.render(B,2),(575,380))
d.text((310,512),f'B bolletje (foto 5)  {B.sum()} px',fill=0)
V.paste(f3,(800,30)); d.text((800,276),'bek: foto 3',fill=0)
kol=vel.sil_of(R+'docs/concept/sprites/kolibrie/af/kolibrie.png',False)
V.paste(vel.render(kol,2),(800,320)); d.text((800,452),'eindvorm (2x)',fill=0)
x=10
for n in ['natu','togepi','pichu','fletchling','pikipek','taillow']:
    r=vel.sil_of(R+f'graphics/pokemon/{n}/anim_front.png'); V.paste(vel.render(r,2),(x,550)); d.text((x,680),f'{n} {r.sum()}',fill=0); x+=140
d.text((10,705),'Gen 3/4-referenties (2x). Formaatdoel pre-evo ±550-750 px.',fill=0)
V.save('vel_v3.png')
