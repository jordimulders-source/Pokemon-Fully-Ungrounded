# vel3.py: r3 | r2 | oud | Gemini (8x); kop r3|oud (12x, oud +2,+3 uitgelijnd); poten r3|Gemini (12x); 1x
from PIL import Image, ImageDraw
G='/home/user/Pokemon-Fully-Ungrounded/docs/concept/sprites/olinguito_v2/'
def on(p,col=(255,255,255)):
    im=Image.open(p).convert('RGBA'); b=Image.new('RGBA',im.size,col); b.alpha_composite(im); return b.convert('RGB')
r3,r2,old=G+'gemini_samen/olinguito_r3.png',G+'gemini_samen/olinguito_r2.png',G+'af/olinguito.png'
model=Image.open(G+'gemini_samen/stappen/model_512.png').convert('RGB')
o=Image.new('RGB',(4*512+60,512+20+360+20+80),(235,235,235)); d=ImageDraw.Draw(o)
for i,(im,t) in enumerate([(on(r3),'r3'),(on(r2),'r2'),(on(old),'oud (af)'),(model,'Gemini v4')]):
    o.paste(im.resize((512,512),0) if im.size!=(512,512) else im,(i*532,0)); d.text((10+i*532,5),t,fill=(200,0,0))
y=532; z=12; kb=(8,19,34,47); W=(kb[2]-kb[0])*z; H=(kb[3]-kb[1])*z
o.paste(on(r3).crop(kb).resize((W,H),0),(0,y)); ob=(kb[0]-2,kb[1]-3,kb[2]-2,kb[3]-3)
o.paste(on(old).crop(ob).resize((W,H),0),(W+8,y))
d.text((5,y+2),'kop r3',fill=(200,0,0)); d.text((W+13,y+2),'kop oud',fill=(200,0,0))
pb=(18,38,50,62); W2=(pb[2]-pb[0])*z; H2=(pb[3]-pb[1])*z; x0=2*W+30
o.paste(on(r3).crop(pb).resize((W2,H2),0),(x0,y)); o.paste(model.crop(tuple(v*8 for v in pb)).resize((W2,H2),Image.LANCZOS),(x0+W2+8,y))
d.text((x0+5,y+2),'poten r3',fill=(200,0,0)); d.text((x0+W2+13,y+2),'poten Gemini',fill=(200,0,0))
y2=y+H2+20 if y+H2+20>y+H+20 else y+H+20
for i,c in enumerate([(255,255,255),(152,208,160),(40,40,48),(90,90,90)]): o.paste(on(r3,c),(10+80*i,y2))
o=o.crop((0,0,o.width,y2+70)); o.save(G+'gemini_samen/vel_r3.png')
