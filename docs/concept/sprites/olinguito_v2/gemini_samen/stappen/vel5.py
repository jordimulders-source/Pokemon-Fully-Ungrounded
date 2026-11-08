# vel5.py: r5 | r4 | oud | Gemini (8x); kop r5|Gemini|oud (12x); 1x op 4 achtergronden; r5 naast Gen 3-referenties (4x)
import numpy as np
from PIL import Image, ImageDraw
R='/home/user/Pokemon-Fully-Ungrounded/'; G=R+'docs/concept/sprites/olinguito_v2/'
def on(p,col=(255,255,255)):
    im=Image.open(p).convert('RGBA'); b=Image.new('RGBA',im.size,col); b.alpha_composite(im); return b.convert('RGB')
def ref(n):
    p=Image.open(R+f'graphics/pokemon/{n}/anim_front_gba.png').crop((0,0,64,64)); a=np.array(p)
    rgb=np.array(p.convert('RGB')); rgb[a==0]=255; return Image.fromarray(rgb)
r5,r4,old=G+'gemini_samen/olinguito_r5.png',G+'gemini_samen/olinguito_r4.png',G+'af/olinguito.png'
model=Image.open(G+'gemini_samen/stappen/model_512.png').convert('RGB')
z=12; kb=(9,18,35,47); W=(kb[2]-kb[0])*z; H=(kb[3]-kb[1])*z
o=Image.new('RGB',(4*532,512+20+H+20+90+256+20),(235,235,235)); d=ImageDraw.Draw(o)
for i,(im,t) in enumerate([(on(r5),'r5'),(on(r4),'r4'),(on(old),'oud (af)'),(model,'Gemini v4')]):
    o.paste(im.resize((512,512),0) if im.size!=(512,512) else im,(i*532,0)); d.text((10+i*532,5),t,fill=(200,0,0))
y=532
o.paste(on(r5).crop(kb).resize((W,H),0),(0,y)); o.paste(model.crop(tuple(v*8 for v in kb)).resize((W,H),Image.LANCZOS),(W+10,y))
ob=(kb[0]-2,kb[1]-3,kb[2]-2,kb[3]-3); o.paste(on(old).crop(ob).resize((W,H),0),(2*W+20,y))
for i,t in enumerate(['kop r5','kop Gemini','kop oud']): d.text((5+i*(W+10),y+2),t,fill=(200,0,0))
y2=y+H+20
for i,c in enumerate([(255,255,255),(152,208,160),(40,40,48),(90,90,90)]): o.paste(on(r5,c),(10+80*i,y2))
y3=y2+90
ims=[on(r5)]+[ref(n) for n in ['linoone','zigzagoon','furret','aipom']]
for i,(im,t) in enumerate(zip(ims,['r5','Linoone','Zigzagoon','Furret','Aipom'])):
    o.paste(im.resize((256,256),0),(i*266,y3)); d.text((5+i*266,y3+2),t,fill=(200,0,0))
o.save(G+'gemini_samen/vel_r5.png')
