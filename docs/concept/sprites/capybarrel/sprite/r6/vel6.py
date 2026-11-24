from PIL import Image, ImageDraw
C='/home/user/Pokemon-Fully-Ungrounded/docs/concept/sprites/capybarrel/'
G='/home/user/Pokemon-Fully-Ungrounded/graphics/pokemon/'
def on(p,col,box=None):
    im=Image.open(p).convert('RGBA')
    if box: im=im.crop(box)
    bg=Image.new('RGBA',im.size,col+(255,)); bg.alpha_composite(im); return bg.convert('RGB')
S=8; cw=46*S; ch=35*S; gap=20
V=Image.new('RGB',(3*(cw+gap)+gap, 36+ch+30+150+290),(255,255,255)); d=ImageDraw.Draw(V)
m=Image.open(C+'referenties/model_r3.png').convert('RGB')
for k,(img,t) in enumerate([(on(C+'sprite/r6/capybarrel.png',(235,235,235)).crop((9,25,55,60)).resize((cw,ch),Image.NEAREST),'r6'),
                           (on(C+'sprite/r5/capybarrel.png',(235,235,235)).crop((9,25,55,60)).resize((cw,ch),Image.NEAREST),'r5'),
                           (m.crop((143,254-16,881,799)).resize((cw,ch),Image.LANCZOS),'model r3')]):
    V.paste(img,(gap+k*(cw+gap),36)); d.text((gap+k*(cw+gap),20),t,fill=(0,0,0))
y2=36+ch+20; d.text((gap,y2),'r6 en r5 1x op licht/donker',fill=(0,0,0))
for j,(f,col) in enumerate([('r6',(248,248,240)),('r6',(40,48,64)),('r5',(248,248,240)),('r5',(40,48,64))]):
    V.paste(on(C+f'sprite/{f}/capybarrel.png',col),(gap+j*80,y2+18))
y3=y2+120; d.text((gap,y3),'4x: r6 | zigzagoon | numel',fill=(0,0,0))
for j,p in enumerate([C+'sprite/r6/capybarrel.png',G+'zigzagoon/anim_front_gba.png',G+'numel/anim_front_gba.png']):
    V.paste(on(p,(235,235,235),(0,0,64,64)).resize((256,256),Image.NEAREST),(gap+j*276,y3+18))
V.save(C+'sprite/r6/vel.png')
