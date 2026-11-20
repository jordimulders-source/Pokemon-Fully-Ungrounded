# vel.png: r9 | r8 | model | Pidgeot | Skarmory (8x) + 1x/2x op licht en donker
import numpy as np, os; from PIL import Image, ImageDraw
G='/home/user/Pokemon-Fully-Ungrounded/graphics/pokemon/'
def rgba(p):
    im=Image.open(p); a=np.asarray(im)[:64]; pal=np.array(im.getpalette()[:768]).reshape(-1,3)
    o=np.zeros(a.shape+(4,),'uint8'); o[...,:3]=pal[a]; o[...,3]=(a!=0)*255; return Image.fromarray(o,'RGBA')
s=2.8888889; x0=32; y0=8
f=lambda cx,cy:((x0+(cx-6)*s)*5.12-0.12,(y0+(cy-1)*s)*5.12-0.12)
M=Image.open('../../MODEL.png').convert('RGB'); a=f(0,0); b=f(64,64)
model=M.crop((int(a[0]),int(a[1]),int(b[0]),int(b[1]))).resize((512,512),Image.LANCZOS).convert('RGBA')
rij=[(rgba('hoatzin.png'),'r9'),(rgba('r8.png'),'r8'),(None,'model'),(rgba(G+'pidgeot/anim_front_gba.png'),'Pidgeot'),(rgba(G+'skarmory/anim_front_gba.png'),'Skarmory')]
vel=Image.new('RGB',(40+5*552,512+60+170),(225,225,225)); d=ImageDraw.Draw(vel)
for i,(im,t) in enumerate(rij):
    if im is None: vel.paste(model,(40+i*552,30))
    else:
        w=Image.new('RGBA',(512,512),(255,255,255,255)); w.alpha_composite(im.resize((512,512),Image.NEAREST)); vel.paste(w,(40+i*552,30))
    d.text((40+i*552,10),t+' 8x',fill=(0,0,0))
    if im is None: continue
    for j,bg in enumerate([(248,248,248),(40,40,48)]):
        w=Image.new('RGBA',(64,64),bg+(255,)); w.alpha_composite(im); vel.paste(w,(40+i*552+j*72,580))
        w2=Image.new('RGBA',(128,128),bg+(255,)); w2.alpha_composite(im.resize((128,128),Image.NEAREST)); vel.paste(w2,(40+160+i*552+j*140,580))
vel.save('vel.png'); print(vel.size)
