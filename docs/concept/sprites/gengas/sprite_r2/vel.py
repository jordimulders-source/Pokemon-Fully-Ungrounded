# vel.py: overzichtsvel ronde 1 (alleen weergave)
from PIL import Image, ImageDraw
s=Image.open('gengas_r2.png').convert('RGBA'); k=Image.open('../model/kleurgids_64.png').convert('RGBA')
def wit(im):
    b=Image.new('RGBA',im.size,(255,255,255,255)); b.alpha_composite(im); return b
s_w=wit(s)
W=1100; V=Image.new('RGBA',(W,2500),(235,235,235,255)); d=ImageDraw.Draw(V)
d.text((10,8),'Gengas ronde 2: sprite 8x | kleurgids (model x64/74) 8x',fill=(0,0,0))
V.paste(s_w.resize((512,512),Image.NEAREST),(10,26)); V.paste(k.resize((512,512),Image.NEAREST),(540,26))
y=550; d.text((10,y),'1x op licht en donker, en 2x',fill=(0,0,0)); y+=18
for i,bg in enumerate([(255,255,255,255),(248,248,232,255),(40,40,56,255),(16,16,16,255)]):
    t=Image.new('RGBA',(80,80),bg); t.alpha_composite(s,(8,8)); V.paste(t,(10+i*90,y))
    t2=Image.new('RGBA',(144,144),bg); t2.alpha_composite(s.resize((128,128),Image.NEAREST),(8,8)); V.paste(t2,(380+i*152,y))
y+=170
S=12
def cl(box,x,y,lab):
    x0,y0,x1,y1=box; w,h=(x1-x0)*S,(y1-y0)*S
    V.paste(s_w.crop(box).resize((w,h),Image.NEAREST),(x,y)); V.paste(k.crop(box).resize((w,h),Image.NEAREST),(x+w+8,y))
    d.text((x,y-14),lab+'  (sprite | model)',fill=(0,0,0)); return h
h=cl((8,28,35,47),10,y+14,'gezicht 12x'); y+=h+34
h1=cl((22,0,38,13),10,y+14,'maan boven (hand, voor) 12x'); h2=cl((45,15,63,33),420,y+14,'maan rechtsboven (voet, achter) 12x'); y+=max(h1,h2)+34
h1=cl((38,48,57,64),10,y+14,'maan rechtsonder (hand, voor) 12x'); h2=cl((0,38,15,54),500,y+14,'maan linksonder (voet, achter) 12x'); y+=max(h1,h2)+20
r1=wit(Image.open('../sprite_r1/gengas_r1.png').convert('RGBA'))
d.text((10,y),'r2 | r1 (8x)',fill=(0,0,0)); y+=16
V.paste(s_w.resize((512,512),Image.NEAREST),(10,y)); V.paste(r1.resize((512,512),Image.NEAREST),(540,y)); y+=520
V=V.crop((0,0,W,y)); V.save('vel.png'); print(V.size)
