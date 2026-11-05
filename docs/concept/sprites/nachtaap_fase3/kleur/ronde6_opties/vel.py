from PIL import Image, ImageDraw, ImageFont
R='../../referenties/'
try: F=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf',15)
except: F=ImageFont.load_default()
LICHT=(235,235,225,255); DONKER=(48,52,60,255)
def op(f,bg,crop=None,s=1):
    im=Image.open(f).convert('RGBA'); c=Image.new('RGBA',(64,64),bg); c.alpha_composite(im)
    if crop: c=c.crop(crop)
    return c.resize((c.width*s,c.height*s),Image.NEAREST)
kol=[('ronde 6 (basis)','../ronde6/nachtaap_fase3.png'),('optie A: toon + 6 px afronding','optie_A.png'),
     ('optie B: dij breed aan de wortel','optie_B.png'),('optie C: hele dij taps','optie_C.png')]
CW=300; H=30+192+10+64+10+28*8+30
foto_h=H
f6=Image.open(R+'foto6_muriqui_tekening_hangend.png').convert('RGB'); f6=f6.resize((int(f6.width*foto_h/f6.height),foto_h))
f7=Image.open(R+'foto7_gibbon_rug_hangend.jpg').convert('RGB'); f7=f7.resize((int(f7.width*foto_h/f7.height),foto_h))
W=CW*len(kol)+f6.width+f7.width+30
v=Image.new('RGB',(W,H+30),(255,255,255)); d=ImageDraw.Draw(v)
for i,(lab,f) in enumerate(kol):
    x=i*CW+5; d.text((x,5),lab,fill=(0,0,0),font=F)
    v.paste(op(f,LICHT,s=3),(x,30))
    v.paste(op(f,LICHT),(x+200,30)); v.paste(op(f,DONKER),(x+200,30+70)); d.text((x+200,30+140),'1x',fill=(0,0,0),font=F)
    y=30+192+10; v.paste(op(f,DONKER,s=3,crop=None).crop((0,0,192,64*3)).resize((96,96)),(x+200,y-70+0)) if False else None
    d.text((x,y),'8x heup/dij (x24-48, r14-42)',fill=(0,0,0),font=F)
    v.paste(op(f,LICHT,crop=(24,14,48,42),s=8),(x,y+20))
x0=CW*len(kol)+10
v.paste(f6,(x0,30)); d.text((x0,5),'foto 6',fill=(0,0,0),font=F)
v.paste(f7,(x0+f6.width+10,30)); d.text((x0+f6.width+10,5),'foto 7',fill=(0,0,0),font=F)
v.save('vel_opties.png')
