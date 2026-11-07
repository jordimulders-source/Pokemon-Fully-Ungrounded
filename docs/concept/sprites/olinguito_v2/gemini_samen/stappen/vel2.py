# vel2.py nieuw.png vorig.png out.png : nieuw | vorig | Gemini (8x), kop + poten nieuw|Gemini (12x), 1x licht/donker
import sys
from PIL import Image, ImageDraw
G='/home/user/Pokemon-Fully-Ungrounded/docs/concept/sprites/olinguito_v2/gemini_samen/'
def on(p,col):
    im=Image.open(p).convert('RGBA'); b=Image.new('RGBA',im.size,col); b.alpha_composite(im); return b.convert('RGB')
model=Image.open(G+'stappen/model_512.png').convert('RGB')
o=Image.new('RGB',(1576,512+20+336+20+80),(235,235,235)); d=ImageDraw.Draw(o)
o.paste(on(sys.argv[1],(255,255,255)).resize((512,512),0),(0,0)); o.paste(on(sys.argv[2],(255,255,255)).resize((512,512),0),(532,0)); o.paste(model,(1064,0))
for i,t in enumerate(['nieuw','vorige ronde','Gemini v4']): d.text((10+532*i,5),t,fill=(200,0,0))
y=532; box=(10,18,36,46); z=12; W=(box[2]-box[0])*z; H=(box[3]-box[1])*z
o.paste(on(sys.argv[1],(255,255,255)).crop(box).resize((W,H),0),(0,y)); o.paste(model.crop(tuple(v*8 for v in box)).resize((W,H),Image.LANCZOS),(W+8,y))
d.text((5,y+2),'kop nieuw',fill=(200,0,0)); d.text((W+13,y+2),'kop Gemini',fill=(200,0,0))
pb=(18,42,34,62); W2=(pb[2]-pb[0])*z*0+192; H2=240
o.paste(on(sys.argv[1],(255,255,255)).crop(pb).resize((W2,H2),0),(2*W+30,y)); o.paste(model.crop(tuple(v*8 for v in pb)).resize((W2,H2),Image.LANCZOS),(2*W+30+W2+8,y))
d.text((2*W+35,y+2),'voorpoten nieuw',fill=(200,0,0)); d.text((2*W+43+W2,y+2),'Gemini',fill=(200,0,0))
y2=y+356
for i,c in enumerate([(255,255,255),(152,208,160),(40,40,48),(90,90,90)]): o.paste(on(sys.argv[1],c),(10+80*i,y2))
o.paste(model.resize((64,64),Image.BOX),(340,y2))
o.save(sys.argv[3])
