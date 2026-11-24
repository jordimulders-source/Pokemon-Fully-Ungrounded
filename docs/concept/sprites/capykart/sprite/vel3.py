# vel r2: r2A | r2B | r1A | r1B | model verkleind (8x); kop 12x (r2A, r2B, r1A, Capybarrel, model); 1x en 2x op licht/donker
from PIL import Image, ImageDraw
R='/home/user/Pokemon-Fully-Ungrounded/docs/concept/sprites/capykart/'
CB='/home/user/Pokemon-Fully-Ungrounded/docs/concept/sprites/capybarrel/af/capybarrel.png'
op=lambda p: Image.open(p).convert('RGBA')
A2,B2,A1,B1=[op(R+f'sprite/{r}/capykart_{v}.png') for r,v in (('r3','A'),('r3','B'),('r2','A'),('r3','A_blauwgrijs'))]
C=op(CB)
M=op(R+'referenties/model_r5.png').crop((133,112,881,860)).resize((62,62),Image.LANCZOS)
M64=Image.new('RGBA',(64,64),(255,255,255,255)); M64.paste(M,(1,2))
BG=(236,236,236,255); out=Image.new('RGBA',(5*528+8,528+8+400+8+150),BG); d=ImageDraw.Draw(out)
for i,(im,t) in enumerate([(A2,'r3 A beige'),(B2,'r3 B dieper'),(A1,'r2 A'),(B1,'r3 A blauwgrijs'),(M64,'model r5 verkleind')]):
    out.alpha_composite(im.resize((512,512),Image.NEAREST),(8+i*528,8)); d.text((12+i*528,10),t,fill=(0,0,0,255))
y=528+8
def kop(im,box,z=12): return im.crop(box).resize(((box[2]-box[0])*z,(box[3]-box[1])*z),Image.NEAREST)
Mk=op(R+'referenties/model_r5.png').crop((133+10*12,112+7*12,133+40*12,112+38*12)).resize((360,372))
x=8
for im in [kop(A2,(11,9,41,40)),kop(B2,(11,9,41,40)),kop(A1,(11,9,41,40)),kop(C,(5,23,35,54)),Mk]:
    out.alpha_composite(im,(x,y)); x+=im.width+16
y+=400+8
x=8
for bg in [(236,236,236,255),(40,44,52,255)]:
    box=Image.new('RGBA',(3*70+10,70),bg)
    for i,im in enumerate([A2,B2,C]): box.alpha_composite(im,(5+i*70,3))
    out.alpha_composite(box.resize((box.width*2,box.height*2),Image.NEAREST),(x,y)); x+=box.width*2+16
    out.alpha_composite(box,(x,y)); x+=box.width+16
out.save(R+'sprite/r3/vel.png'); print(out.size)
