# vel r4: V1 | V2 | V3 | r3b B | Capybarrel af (8x); koppen 12x; 1x-rij op licht en donker
from PIL import Image, ImageDraw
R='/home/user/Pokemon-Fully-Ungrounded/docs/concept/sprites/capykart/'
op=lambda p: Image.open(p).convert('RGBA')
ims=[(op(R+f'sprite/r4/capykart_{k}.png'),k) for k in ('V1','V2','V3')]+[(op(R+'sprite/r3b/capykart_B.png'),'r3b B'),(op('/home/user/Pokemon-Fully-Ungrounded/docs/concept/sprites/capybarrel/af/capybarrel.png'),'Capybarrel af')]
BG=(236,236,236,255); out=Image.new('RGBA',(5*528+8,528+8+384+16+150),BG); d=ImageDraw.Draw(out)
for i,(im,t) in enumerate(ims):
    out.alpha_composite(im.resize((512,512),Image.NEAREST),(8+i*528,8)); d.text((12+i*528,10),t,fill=(0,0,0,255))
y=544; x=8
def kop(im,box,z=12): return im.crop(box).resize(((box[2]-box[0])*z,(box[3]-box[1])*z),Image.NEAREST)
for im,t in ims:
    k=kop(im,(5,23,35,54) if t=='Capybarrel af' else (11,9,41,40)); out.alpha_composite(k,(x,y)); x+=k.width+12
y+=384+16; x=8
for bg in [(236,236,236,255),(40,44,52,255)]:
    box=Image.new('RGBA',(5*70+10,70),bg)
    for i,(im,t) in enumerate(ims): box.alpha_composite(im,(5+i*70,3))
    out.alpha_composite(box.resize((box.width*2,box.height*2),Image.NEAREST),(x,y)); x+=box.width*2+16
out.save(R+'sprite/r4/vel.png'); print(out.size)
