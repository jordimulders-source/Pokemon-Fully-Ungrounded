from PIL import Image, ImageDraw
C='/home/user/Pokemon-Fully-Ungrounded/docs/concept/sprites/capybarrel/'
def on(p,col): im=Image.open(p).convert('RGBA'); bg=Image.new('RGBA',im.size,col+(255,)); bg.alpha_composite(im); return bg.convert('RGB')
S=8; cw=46*S; ch=34*S; gap=20
V=Image.new('RGB',(3*(cw+gap)+gap+40, 2*(ch+40)+ 21*10+60 + 200),(255,255,255)); d=ImageDraw.Draw(V)
m=Image.open(C+'referenties/model_r3.png').convert('RGB').crop((143,254,881,799)).resize((cw,ch),Image.LANCZOS)
for r,v in enumerate('AB'):
    y=20+r*(ch+40)
    for k,(img,t) in enumerate([(on(C+f'sprite/r2/capybarrel_{v}.png',(235,235,235)).crop((9,26,55,60)).resize((cw,ch),Image.NEAREST),f'r2 {v}'),
                               (on(C+f'sprite/r1/capybarrel_{v}.png',(235,235,235)).crop((9,26,55,60)).resize((cw,ch),Image.NEAREST),f'r1 {v}'),
                               (m,'model r3')]):
        V.paste(img,(gap+k*(cw+gap),y+16)); d.text((gap+k*(cw+gap),y),t,fill=(0,0,0))
y=20+2*(ch+40)
d.text((gap,y),'kop 10x: model | r2 A | r2 B',fill=(0,0,0))
kop=Image.open(C+'referenties/model_r3.png').convert('RGB').crop((143,254,143+int(23*738/46),254+int(21*738/46))).resize((230,210),Image.LANCZOS)
V.paste(kop,(gap,y+16))
for k,v in enumerate('AB'):
    V.paste(on(C+f'sprite/r2/capybarrel_{v}.png',(235,235,235)).crop((9,26,32,47)).resize((230,210),Image.NEAREST),(gap+(k+1)*250,y+16))
y2=y+16+210+20
d.text((gap,y2),'1x en 2x op licht/donker: A | B',fill=(0,0,0))
for k,v in enumerate('AB'):
    for j,col in enumerate([(248,248,240),(40,48,64)]):
        o=on(C+f'sprite/r2/capybarrel_{v}.png',col)
        V.paste(o,(gap+k*420+j*70,y2+20)); V.paste(o.resize((128,128),Image.NEAREST),(gap+k*420+150+j*135,y2+20))
V.save(C+'sprite/r2/vel.png'); print(V.size)
