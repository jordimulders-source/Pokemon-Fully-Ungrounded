# vel: r3 8x | r2 k120 8x | model r7 | Ho-Oh 8x | Moltres 8x ; onder: 1x en 2x op licht en donker. + afwijkingstelling.
import numpy as np; from PIL import Image, ImageDraw
G='../../../../../graphics/pokemon/'
def rgba(p):
    return Image.open(p).convert('RGBA')
def gba(n):
    im=Image.open(G+n+'/anim_front_gba.png').crop((0,0,64,64)); pal=open(G+n+'/normal_gba.pal').read().split('\n')[3:19]
    im.putpalette([int(v) for l in pal for v in l.split()]); a=im.convert('RGBA'); d=np.array(a); d[np.array(im)==0,3]=0; return Image.fromarray(d)
def op(im,bg,s):
    b=Image.new('RGBA',im.size,bg); b.alpha_composite(im); return b.convert('RGB').resize((im.width*s,im.height*s),Image.NEAREST)
LICHT=(240,240,236,255); DONK=(40,40,56,255)
r3=rgba('sprite.png'); r2=rgba('../sprite_r2/sprite_k120.png')
panelen=[('r3 (8x)',op(r3,LICHT,8)),('r2 k120 (8x)',op(r2,LICHT,8)),('model r7',Image.open('../gemini/r7.png').convert('RGB').resize((512,512))),
         ('Ho-Oh Gen 3 (8x)',op(gba('ho_oh'),LICHT,8)),('Moltres Gen 3 (8x)',op(gba('moltres'),LICHT,8))]
W=Image.new('RGB',(5*520+10,520+20+150),(255,255,255)); d=ImageDraw.Draw(W)
for i,(t,p) in enumerate(panelen): W.paste(p,(5+i*520,18)); d.text((5+i*520,3),t,fill=(0,0,0))
x=5; y=560
for bg in (LICHT,DONK):
    for s in (1,2):
        W.paste(op(r3,bg,s),(x,y)); x+=64*s+12
W.save('vel.png'); print('vel.png',W.size)
