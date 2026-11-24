# Vel: r20 8x | r21 8x (omgetinte pixels rood omrand; paletwijziging 2/3 geldt overal) | model 8x;
# daaronder r21 2x naast Gen 3 (Glalie, Magneton, Claydol, Metang, Lunatone) en 1x op licht/donker.
from PIL import Image, ImageDraw
import numpy as np
G='../../../../../graphics/pokemon/'
BG=(200,230,200)
def rgba(path,bg=BG):
    im=Image.open(path); pal=im.getpalette(); a=np.array(im)[:64,:64]
    out=np.zeros((64,64,3),np.uint8)
    for i in range(16): out[a==i]=pal[3*i:3*i+3]
    out[a==0]=bg; return Image.fromarray(out),a
r20,a20=rgba('../sprite/r20/sprite.png'); r21,a21=rgba('r21/sprite.png')
r21.resize((512,512),Image.NEAREST).save('r21/sprite_8x.png')
M=Image.open('../paneel_varianten/panelen_80b.png').convert('RGB')
s=12.703; mod=M.crop((round(103-0*s),round(143-7*s),round(103+64*s),round(143+57*s))).resize((512,512),Image.LANCZOS)
W=3*512+40; V=Image.new('RGB',(W,512+30+2*64*2+40+100),'white'); d=ImageDraw.Draw(V)
V.paste(r20.resize((512,512),Image.NEAREST),(0,24)); d.text((4,4),'r20 8x',fill='black')
r8=r21.resize((512,512),Image.NEAREST); dd=ImageDraw.Draw(r8)
for y,x in zip(*np.where(a20!=a21)): dd.rectangle([x*8,y*8,x*8+7,y*8+7],outline=(255,0,0),width=2)
V.paste(r8,(532,24)); d.text((536,4),'r21 8x (rood = omgetint; lijftinten 2/3 overal nieuw)',fill='black')
V.paste(mod,(1064,24)); d.text((1068,4),'model (panelen_80b) op spriteraster',fill='black')
y0=560; x=0
for n in ['glalie','magneton','claydol','metang','lunatone']:
    im,_=rgba(G+n+'/anim_front.png',(255,255,255)) if False else (None,None)
    p=Image.open(G+n+'/anim_front.png'); pal=p.getpalette(); a=np.array(p)[:64]
    o=np.zeros((64,64,3),np.uint8)
    for i in range(16): o[a==i]=pal[3*i:3*i+3]
    o[a==0]=BG; V.paste(Image.fromarray(o).resize((128,128),Image.NEAREST),(x,y0)); d.text((x,y0+130),n,fill='black'); x+=138
V.paste(r21.resize((128,128),Image.NEAREST),(x,y0)); d.text((x,y0+130),'r21',fill='black'); x+=148
for bg in [(248,248,248),(40,40,48)]:
    t,_=rgba('r21/sprite.png',bg); V.paste(t,(x,y0+32)); x+=74
    t,_=rgba('../sprite/r20/sprite.png',bg); V.paste(t,(x,y0+32)); x+=74
d.text((x-296,y0+100),'1x: r21 | r20 (licht, donker)',fill='black')
V.save('vel.png'); print(V.size)
