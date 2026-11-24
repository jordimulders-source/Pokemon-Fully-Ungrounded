from PIL import Image, ImageDraw
C='/home/user/Pokemon-Fully-Ungrounded/docs/concept/sprites/capybarrel/'
def on(p,col): im=Image.open(p).convert('RGBA'); bg=Image.new('RGBA',im.size,col+(255,)); bg.alpha_composite(im); return bg.convert('RGB')
S=8; cw=46*S; ch=35*S; gap=20; p=738/46
V=Image.new('RGB',(3*(cw+gap)+gap, 36+ch+40+24*12+40+170),(255,255,255)); d=ImageDraw.Draw(V)
m=Image.open(C+'referenties/model_r3.png').convert('RGB')
for k,(img,t) in enumerate([(on(C+'sprite/r4/capybarrel.png',(235,235,235)).crop((9,25,55,60)).resize((cw,ch),Image.NEAREST),'r4'),
                           (on(C+'sprite/r3/capybarrel_3.png',(235,235,235)).crop((9,25,55,60)).resize((cw,ch),Image.NEAREST),'r3 (oog 3)'),
                           (m.crop((143,254-16,881,799)).resize((cw,ch),Image.LANCZOS),'model r3')]):
    V.paste(img,(gap+k*(cw+gap),36)); d.text((gap+k*(cw+gap),20),t,fill=(0,0,0))
# ton 12x: figuur x19-40, y4-28
y=36+ch+30; x0,x1,y0,y1=19,40,4,28; Z=12
d.text((gap,y),'ton 12x: r4 | model (zelfde uitsnede)',fill=(0,0,0))
V.paste(on(C+'sprite/r4/capybarrel.png',(235,235,235)).crop((9+x0,26+y0,9+x1,26+y1)).resize(((x1-x0)*Z,(y1-y0)*Z),Image.NEAREST),(gap,y+16))
box=(int(143+x0*p),int(799-(34-y0)*p),int(143+x1*p),int(799-(34-y1)*p))
V.paste(m.crop(box).resize(((x1-x0)*Z,(y1-y0)*Z),Image.LANCZOS),(gap+(x1-x0)*Z+20,y+16))
y2=y+16+(y1-y0)*Z+20
d.text((gap,y2),'1x en 2x op licht/donker',fill=(0,0,0))
for j,col in enumerate([(248,248,240),(40,48,64)]):
    o=on(C+'sprite/r4/capybarrel.png',col); V.paste(o,(gap+j*70,y2+18)); V.paste(o.resize((128,128),Image.NEAREST),(gap+160+j*140,y2+18))
V.save(C+'sprite/r4/vel.png'); print(V.size)
