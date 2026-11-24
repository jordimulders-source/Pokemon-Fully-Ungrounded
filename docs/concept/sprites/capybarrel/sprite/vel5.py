from PIL import Image, ImageDraw
C='/home/user/Pokemon-Fully-Ungrounded/docs/concept/sprites/capybarrel/'
def on(p,col): im=Image.open(p).convert('RGBA'); bg=Image.new('RGBA',im.size,col+(255,)); bg.alpha_composite(im); return bg.convert('RGB')
S=8; cw=46*S; ch=35*S; gap=20
V=Image.new('RGB',(3*(cw+gap)+gap, 36+ch+30+170),(255,255,255)); d=ImageDraw.Draw(V)
m=Image.open(C+'referenties/model_r3.png').convert('RGB')
for k,(img,t) in enumerate([(on(C+'sprite/r5/capybarrel.png',(235,235,235)).crop((9,25,55,60)).resize((cw,ch),Image.NEAREST),'r5'),
                           (on(C+'sprite/r4/capybarrel.png',(235,235,235)).crop((9,25,55,60)).resize((cw,ch),Image.NEAREST),'r4'),
                           (m.crop((143,254-16,881,799)).resize((cw,ch),Image.LANCZOS),'model r3')]):
    V.paste(img,(gap+k*(cw+gap),36)); d.text((gap+k*(cw+gap),20),t,fill=(0,0,0))
y2=36+ch+20; d.text((gap,y2),'r5 1x en 2x op licht/donker',fill=(0,0,0))
for j,col in enumerate([(248,248,240),(40,48,64)]):
    o=on(C+'sprite/r5/capybarrel.png',col); V.paste(o,(gap+j*70,y2+18)); V.paste(o.resize((128,128),Image.NEAREST),(gap+160+j*140,y2+18))
V.save(C+'sprite/r5/vel.png')
