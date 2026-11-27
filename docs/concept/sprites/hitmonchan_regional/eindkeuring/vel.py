import numpy as np
from PIL import Image, ImageDraw
R='/home/user/Pokemon-Fully-Ungrounded/'; D=R+'docs/concept/sprites/hitmonchan_regional/'; O=D+'eindkeuring/'
def rgba(p):
    im=Image.open(p)
    if im.mode=='P':
        im.save('/tmp/claude-0/-home-user-Pokemon-Fully-Ungrounded/f28540c1-eb25-5a6c-8e41-5cf2205926c1/scratchpad/ek/_t.png',transparency=0)
        im=Image.open('/tmp/claude-0/-home-user-Pokemon-Fully-Ungrounded/f28540c1-eb25-5a6c-8e41-5cf2205926c1/scratchpad/ek/_t.png')
    return im.convert('RGBA')
def on(im,c):
    b=Image.new('RGBA',im.size,c); b.alpha_composite(im); return b.convert('RGB')
k=rgba(D+'sprite/kandidaat.png'); e=rgba(O+'ek1.png')
g=rgba(R+'graphics/pokemon/hitmonchan/anim_front_gba.png').crop((0,0,64,64))
LB=(235,235,235,255); DB=(40,44,52,255)
S=8
e8=on(e,LB).resize((512,512),Image.NEAREST); e8.save(O+'ek1_8x.png')
k8=on(k,LB).resize((512,512),Image.NEAREST); g8=on(g,LB).resize((512,512),Image.NEAREST)
m=Image.open(D+'gemini/r3.png').convert('RGB')
# model op dezelfde schaal: figuur 81 cellen -> 64 sprite-px => 81*10.24 px -> 512 px hoog
mb=Image.open(R+'docs/concept/sprites/hitmonchan_regional/sprite/natief.png')
# bbox model in r3 pixels
F=9.25;P=10.24
a=np.asarray(m).min(2)<235; ys,xs=np.where(a); crop=m.crop((xs.min(),ys.min(),xs.max()+1,ys.max()+1))
h=512; w=int(crop.width*h/crop.height); m8=Image.new('RGB',(512,512),(235,235,235)); m8.paste(crop.resize((w,h),Image.LANCZOS),((512-w)//2,0))
# diff
K=np.array(Image.open(D+'sprite/kandidaat.png')); T=np.array(Image.open(O+'ek1.png'))
dm=on(e,LB).convert('RGB'); dm=np.array(dm).copy(); dm=(dm*0.35+165).astype('uint8')
for y,x in zip(*np.where(K!=T)): dm[y,x]=(230,0,0)
d8=Image.fromarray(dm).resize((512,512),Image.NEAREST)
W=4*512+5*16; H=16+24+512+24+256+24
v=Image.new('RGB',(W,H),(255,255,255)); dr=ImageDraw.Draw(v)
labels=['kandidaat 8x','ek1 8x','model r3 (zelfde hoogte)','Gen 3 Hitmonchan 8x']
for i,(im,l) in enumerate(zip([k8,e8,m8,g8],labels)):
    x=16+i*(512+16); v.paste(im,(x,40)); dr.text((x,22),l,fill=(0,0,0))
y=40+512+24; dr.text((16,y-16),'1x / 2x licht en donker: kandidaat, ek1, Gen 3',fill=(0,0,0))
x=16
for im in [k,e,g]:
    for c in [LB,DB]:
        b=on(im,c); v.paste(b,(x,y)); v.paste(b.resize((128,128),Image.NEAREST),(x+72,y)); x+=72+128+16
dr.text((x+10,y-16),'diff kandidaat->ek1 (rood = gewijzigd, 25 px)',fill=(0,0,0))
v.paste(d8.resize((256,256),Image.NEAREST),(x+10,y))
v.save(O+'vel.png'); print(v.size)
