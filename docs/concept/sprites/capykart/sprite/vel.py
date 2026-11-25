# vel: A | B | Capybarrel af | model verkleind (8x); close-up kop 12x (A, B, Capybarrel, model); 1x op licht en donker
from PIL import Image, ImageDraw
R='/home/user/Pokemon-Fully-Ungrounded/docs/concept/sprites/capykart/'
CB='/home/user/Pokemon-Fully-Ungrounded/docs/concept/sprites/capybarrel/af/capybarrel.png'
A=Image.open(R+'sprite/r1/capykart_A.png').convert('RGBA'); B=Image.open(R+'sprite/r1/capykart_B.png').convert('RGBA')
C=Image.open(CB).convert('RGBA')
M=Image.open(R+'referenties/model_r5.png').convert('RGBA').crop((133,112,881,860)).resize((62,62),Image.LANCZOS)
M64=Image.new('RGBA',(64,64),(255,255,255,255)); M64.paste(M,(1,2))
BG=(236,236,236,255); out=Image.new('RGBA',(4*528+8,528+8+400+8+150),BG); d=ImageDraw.Draw(out)
for i,(im,t) in enumerate([(A,'A beige'),(B,'B dieper'),(C,'Capybarrel af'),(M64,'model r5 verkleind')]):
    out.alpha_composite(im.resize((512,512),Image.NEAREST),(8+i*528,8)); d.text((12+i*528,10),t,fill=(0,0,0,255))
y=528+8
def kop(im,box,z=12): return im.crop(box).resize(((box[2]-box[0])*z,(box[3]-box[1])*z),Image.NEAREST)
Mk=Image.open(R+'referenties/model_r5.png').convert('RGBA').crop((133+10*12,112+7*12,133+40*12,112+38*12)).resize((360,372))
x=8
for im in [kop(A,(11,9,41,40)),kop(B,(11,9,41,40)),kop(C,(5,23,35,54)),Mk]:
    out.alpha_composite(im,(x,y)); x+=im.width+16
y+=400+8
for j,bg in enumerate([(236,236,236,255),(40,44,52,255)]):
    box=Image.new('RGBA',(3*70+10,70),bg)
    for i,im in enumerate([A,B,C]): box.alpha_composite(im,(5+i*70,3))
    out.alpha_composite(box.resize((box.width*2,box.height*2),Image.NEAREST),(8+j*(box.width*2+16),y))
    out.alpha_composite(box,(8+2*(box.width*2+16)+j*(box.width+16),y))
out.save(R+'sprite/r1/vel.png'); print(out.size)
