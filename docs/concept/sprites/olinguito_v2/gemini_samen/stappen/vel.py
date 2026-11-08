# vel.py sprite.png out.png : nieuw | oud | model (8x), kop-close-up (12x) nieuw|model|oud, 1x licht/donker
import sys
from PIL import Image, ImageDraw
D='/home/user/Pokemon-Fully-Ungrounded/docs/concept/sprites/olinguito_v2/'
new=Image.open(sys.argv[1]).convert('RGBA'); old=Image.open(D+'af/olinguito.png').convert('RGBA')
model=Image.open(D+'gemini_samen/stappen/model_512.png').convert('RGBA')
def on(im,col):
    b=Image.new('RGBA',im.size,col); b.alpha_composite(im); return b.convert('RGB')
W=512*3+40; o=Image.new('RGB',(W,512+20+360+20+140),(235,235,235)); d=ImageDraw.Draw(o)
o.paste(on(new,(255,255,255)).resize((512,512),0),(0,0)); o.paste(on(old,(255,255,255)).resize((512,512),0),(532,0)); o.paste(model,(1064,0))
for i,t in enumerate(['nieuw','oud (af)','Gemini v4 (verkleind kader)']): d.text((10+532*i,5),t,fill=(200,0,0))
# kop close-up: nieuw kop (x10-34,y18-46), model zelfde, oud kop (x6-32,y15-43)
y=532; z=12
box=(10,19,34,46); bo=(6,15,32,42)
o.paste(on(new,(255,255,255)).crop(box).resize(((box[2]-box[0])*z,(box[3]-box[1])*z),0),(0,y))
o.paste(model.crop((box[0]*8,box[1]*8,box[2]*8,box[3]*8)).resize(((box[2]-box[0])*z,(box[3]-box[1])*z),Image.LANCZOS),(300,y))
o.paste(on(old,(255,255,255)).crop(bo).resize(((bo[2]-bo[0])*z,(bo[3]-bo[1])*z),0),(600,y))
d.text((5,y+2),'kop nieuw',fill=(200,0,0)); d.text((305,y+2),'kop Gemini',fill=(200,0,0)); d.text((605,y+2),'kop oud',fill=(200,0,0))
# poten close-up
pb=(18,40,50,62); z2=10
o.paste(on(new,(255,255,255)).crop(pb).resize((320,220),0),(940,y)); o.paste(model.crop((pb[0]*8,pb[1]*8,pb[2]*8,pb[3]*8)).resize((320,220),Image.LANCZOS),(1270,y))
d.text((945,y+2),'poten nieuw',fill=(200,0,0)); d.text((1275,y+2),'poten Gemini',fill=(200,0,0))
y2=y+380
for i,c in enumerate([(255,255,255),(152,208,160),(40,40,48),(90,90,90)]):
    o.paste(on(new,c),(10+150*i,y2)); o.paste(on(old,c),(10+150*i,y2+68))
o.paste(model.resize((64,64),Image.BOX),(620,y2))
o.save(sys.argv[2])
