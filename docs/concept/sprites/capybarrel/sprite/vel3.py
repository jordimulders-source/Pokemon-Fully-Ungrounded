from PIL import Image, ImageDraw
C='/home/user/Pokemon-Fully-Ungrounded/docs/concept/sprites/capybarrel/'; G='/home/user/Pokemon-Fully-Ungrounded/graphics/pokemon/'
def on(p,col): im=Image.open(p).convert('RGBA'); bg=Image.new('RGBA',im.size,col+(255,)); bg.alpha_composite(im); return bg.convert('RGB')
S=8; cw=46*S; ch=35*S; gap=20
V=Image.new('RGB',(3*(cw+gap)+gap, 40+ch+40+3*(230+30)+40+180),(255,255,255)); d=ImageDraw.Draw(V)
m=Image.open(C+'referenties/model_r3.png').convert('RGB').crop((143,254-16,881,799)).resize((cw,ch),Image.LANCZOS)
for k,(img,t) in enumerate([(on(C+'sprite/r3/capybarrel_1.png',(235,235,235)).crop((9,25,55,60)).resize((cw,ch),Image.NEAREST),'r3 (oog 1)'),
                           (on(C+'sprite/r2/capybarrel_A.png',(235,235,235)).crop((9,25,55,60)).resize((cw,ch),Image.NEAREST),'r2 A'),
                           (m,'model r3')]):
    V.paste(img,(gap+k*(cw+gap),36)); d.text((gap+k*(cw+gap),20),t,fill=(0,0,0))
y=36+ch+30
src={'1':('sealeo',(21,14,23,18)),'2':('igglybuff',(24,28,28,32)),'3':('flareon',(15,27,19,31))}
kop=Image.open(C+'referenties/model_r3.png').convert('RGB').crop((143,254,143+int(23*738/46),254+int(21*738/46))).resize((230,210),Image.LANCZOS)
for i,v in enumerate('123'):
    yy=y+i*260; n,(x0,y0,x1,y1)=src[v]
    d.text((gap,yy),f'oog {v}: bron {n} (blauw kader = overgenomen pixels) | kop r3 {v} (10x) | model',fill=(0,0,0))
    b=on(G+f'{n}/anim_front_gba.png',(235,235,235)).crop((0,0,64,64))
    bx=max(0,x0-8); by=max(0,y0-6); crop=b.crop((bx,by,bx+21,by+21)).resize((210,210),Image.NEAREST)
    dd=ImageDraw.Draw(crop); dd.rectangle([(x0-bx)*10,(y0-by)*10,(x1-bx)*10-1,(y1-by)*10-1],outline=(0,140,255),width=2)
    V.paste(crop,(gap,yy+16))
    V.paste(on(C+f'sprite/r3/capybarrel_{v}.png',(235,235,235)).crop((9,26,32,47)).resize((230,210),Image.NEAREST),(gap+230,yy+16))
    V.paste(kop,(gap+480,yy+16))
    V.paste(on(G+f'{n}/anim_front_gba.png',(235,235,235)).crop((0,0,64,64)).resize((192,192),Image.NEAREST),(gap+740,yy+16))
y2=y+3*260+10
d.text((gap,y2),'1x en 2x op licht/donker: oog 1 | 2 | 3',fill=(0,0,0))
for k,v in enumerate('123'):
    for j,col in enumerate([(248,248,240),(40,48,64)]):
        o=on(C+f'sprite/r3/capybarrel_{v}.png',col)
        V.paste(o,(gap+k*390+j*68,y2+18)); V.paste(o.resize((128,128),Image.NEAREST),(gap+k*390+140+j*120,y2+18))
V.save(C+'sprite/r3/vel.png'); print(V.size)
