# vel.png ronde 4: r4 | r3 | model (8x) ; 1x licht/donker ; r4 8x naast Whismur en Voltorb (Gen 3, 8x)
import sys; sys.path.insert(0,'r4')
import numpy as np; from PIL import Image, ImageDraw
from meet import crop
S=8; R='../../../../../graphics/pokemon/'
def rgba(f):
    im=Image.open(f); a=np.asarray(im)[:64]; p=np.array(im.getpalette()[:768]).reshape(-1,3)
    r=np.zeros((64,64,4),'uint8'); r[...,:3]=p[a]; r[...,3]=(a>0)*255; return Image.fromarray(r)
def gen3(n):
    im=Image.open(R+n+'/anim_front_gba.png'); a=np.asarray(im)[:64]
    p=np.array([int(x) for x in open(R+n+'/normal_gba.pal').read().split()[3:]]).reshape(-1,3)
    r=np.zeros((64,64,4),'uint8'); r[...,:3]=p[a]; r[...,3]=(a>0)*255; return Image.fromarray(r)
def op(img,bg): b=Image.new('RGBA',img.size,bg); b.alpha_composite(img); return b.convert('RGB')
W=(64*S+10)*3+150; v=Image.new('RGB',(W,64*S*2+60),(235,235,235)); d=ImageDraw.Draw(v)
r4=rgba('r6/mate.png'); r3=rgba('r5/mate.png'); wit=(255,255,255,255)
for k,(im,t) in enumerate(((op(r4,wit),'r6'),(op(r3,wit),'r5'),(crop,'model (zelfde schaal)'))):
    v.paste(im.resize((64*S,64*S),Image.NEAREST if k<2 else Image.LANCZOS),(k*(64*S+10),20)); d.text((k*(64*S+10)+4,4),t,fill='black')
x=3*(64*S+10)
for j,bg in enumerate((wit,(40,40,48,255))):
    v.paste(op(r4,bg),(x,20+j*70)); v.paste(op(r3,bg),(x+70,20+j*70))
d.text((x,160),'1x: r6 | r5',fill='black')
y=64*S+50; d.text((4,y-16),'r6 naast Voltorb (Gen 3), 8x',fill='black')
for k,im in enumerate((r4,gen3('voltorb'))):
    v.paste(op(im,wit).resize((64*S,64*S),Image.NEAREST),(k*(64*S+10),y))
v.save('r6/vel.png')
op(r4,wit).resize((512,512),Image.NEAREST).save('r6/mate_8x.png')
