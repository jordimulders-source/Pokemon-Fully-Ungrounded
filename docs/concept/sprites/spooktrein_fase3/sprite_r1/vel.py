# Vel: sprite 8x | schrap-onderlaag 8x | BOX-onderlaag 8x | model verkleind; close-ups 12x; 1x en 2x op licht en donker.
from PIL import Image, ImageDraw
def op(f,bg=(255,255,255)):
    im=Image.open(f); im=im.convert('RGBA') if im.mode!='P' else im.convert('RGBA')
    b=Image.new('RGBA',im.size,bg+(255,)); b.alpha_composite(im); return b.convert('RGB')
sp=op('sprite.png'); sch=Image.open('../model/model_64.png').convert('RGB'); box=op('onderlaag.png')
m=Image.open('../model/model.webp').convert('RGB')
# model op dezelfde maat: natief bbox x9-94,y6-88 (pitch 10.24) -> 512 breed, onderaan
x0,y0=int(9*10.24),int(6*10.24); x1,y1=int(95*10.24),int(89*10.24)
mc=m.crop((x0,y0,x1,y1)); mh=round(512*mc.size[1]/mc.size[0]); mc=mc.resize((512,mh),Image.LANCZOS)
mm=Image.new('RGB',(512,512),'white'); mm.paste(mc,(0,512-mh-8))
nat=Image.open('../model/natief.png').convert('RGB')
V=Image.new('RGB',(4*524+12,512+40+400+40+300),(235,235,235)); d=ImageDraw.Draw(V)
for i,(im,t) in enumerate([(sp,'sprite r1 (8x)'),(sch,'schrap-onderlaag model_64 (8x)'),(box,'BOX-onderlaag per kleurgroep (8x)'),(mm,'model verkleind')]):
    V.paste(im.resize((512,512),Image.NEAREST) if im.size[0]==64 else im,(12+i*524,28)); d.text((12+i*524,8),t,fill=(0,0,0))
Y=560; d.text((12,Y),'gezicht 12x: sprite | natief model',fill=(0,0,0))
V.paste(sp.crop((0,24,28,48)).resize((336,288),Image.NEAREST),(12,Y+20))
V.paste(nat.crop((9,38,46,70)).resize((444,384),Image.NEAREST),(360,Y+20))
d.text((830,Y),'kleine geest 12x: sprite | natief model',fill=(0,0,0))
V.paste(sp.crop((14,0,42,15)).resize((336,180),Image.NEAREST),(830,Y+20))
V.paste(nat.crop((28,5,64,24)).resize((432,228),Image.NEAREST),(1180,Y+20))
Y=1000; d.text((12,Y),'1x en 2x op licht en donker',fill=(0,0,0))
x=12
for bg in [(255,255,255),(48,48,64)]:
    s=op('sprite.png',bg)
    V.paste(s,(x,Y+20)); V.paste(s.resize((128,128),Image.NEAREST),(x+80,Y+20)); x+=240
V.save('vel.png'); print(V.size)
