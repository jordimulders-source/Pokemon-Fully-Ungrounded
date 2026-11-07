# vel_opties.png: per kolom ronde 6 / optie A / optie B: 3x licht, 3x donker, 1x, 8x close-up romp/heup/staartwortel
from PIL import Image, ImageDraw
G='/home/user/Pokemon-Fully-Ungrounded/graphics/pokemon/'
R='../../referenties/'
cols=[('ronde 6 (basis)','../ronde6/nachtaap_fase3.png'),('ronde 7 optie B','../ronde7_opties/optie_B.png'),('7b matig','optie_matig.png'),('7b sterk','optie_sterk.png')]
box=(18,16,50,52); k=8
cw=max(192,(box[2]-box[0])*k)+16
W=Image.new('RGBA',(cw*4+300,20+192+8+192+8+64+8+(box[3]-box[1])*k+12),(238,238,242,255))
d=ImageDraw.Draw(W)
for i,(lab,f) in enumerate(cols):
    im=Image.open(f).convert('RGBA'); x=i*cw+8; y=4
    d.text((x,y),lab,fill=(0,0,0)); y+=16
    W.alpha_composite(im.resize((192,192),Image.NEAREST),(x,y)); y+=200
    dk=Image.new('RGBA',(192,192),(40,40,48,255)); dk.alpha_composite(im.resize((192,192),Image.NEAREST)); W.alpha_composite(dk,(x,y)); y+=200
    W.alpha_composite(im,(x,y)); dk=Image.new('RGBA',(64,64),(40,40,48,255)); dk.alpha_composite(im); W.alpha_composite(dk,(x+72,y)); y+=72
    d.text((x,y),'8x romp/heup/staartwortel (x18-49, r16-51)',fill=(0,0,0)); y+=12
    W.alpha_composite(im.crop(box).resize(((box[2]-box[0])*k,(box[3]-box[1])*k),Image.NEAREST),(x,y))
# referenties rechts
x0=cw*4+8; y=4
d.text((x0,y),'foto 6 / foto 7 (Jordi)',fill=(0,0,0)); y+=16
f6=Image.open(R+'foto6_muriqui_tekening_hangend.png').convert('RGBA'); f6.thumbnail((140,260)); W.alpha_composite(f6,(x0,y))
f7=Image.open(R+'foto7_gibbon_rug_hangend.jpg').convert('RGBA'); f7.thumbnail((140,260)); W.alpha_composite(f7,(x0+148,y)); y+=270
d.text((x0,y),'GF 3x: Vigoroth, Zangoose, Aipom',fill=(0,0,0)); y+=14
for j,n in enumerate(['vigoroth','zangoose','aipom']):
    im=Image.open(G+n+'/anim_front_gba.png').convert('RGBA').crop((0,0,64,64)).resize((144,144),Image.NEAREST)
    W.alpha_composite(im,(x0+(j%2)*148,y+(j//2)*148))
y+=300
d.text((x0,y),'GF 8x: Machamp rug, Zangoose staartwortel',fill=(0,0,0)); y+=14
m=Image.open(G+'machamp/back_gba.png').convert('RGBA').crop((10,26,28,48)).resize((144,176),Image.NEAREST); W.alpha_composite(m,(x0,y))
z=Image.open(G+'zangoose/anim_front_gba.png').convert('RGBA').crop((36,30,54,52)).resize((144,176),Image.NEAREST); W.alpha_composite(z,(x0+148,y))
W.save('vel_opties.png'); print(W.size)
