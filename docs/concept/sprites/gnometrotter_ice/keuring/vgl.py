import sys; sys.path.insert(0,'../../gnometrotter_rock/sprite')
from kijk import model_op_schaal, sprite
from PIL import Image, ImageDraw
A='../sprite_r2/gnometrotter_ice_gatdicht.png'; MA='../r3/gemini_r3_lijf.png'
B='../sprite_hybride/gnometrotter_ice_hybride_gatdicht.png'; MB='../hybride/model_hybride.png'
R='../../gnometrotter_rock/sprite_r4/gnometrotter_rock.png'; G='../../gnomad/af/gnomad.png'
def grid(im,s,S=12):
    im=im.resize((64*s,64*s),Image.NEAREST) if s>1 else im; d=ImageDraw.Draw(im); s=S
    for i in range(0,64,5):
        d.line([(i*s,0),(i*s,64*s)],fill=(255,0,0) if i%10==0 else (255,180,180)); d.line([(0,i*s),(64*s,i*s)],fill=(255,0,0) if i%10==0 else (255,180,180))
    return im
for nm,s,m in [('A',A,MA),('B',B,MB)]:
    W=Image.new('RGB',(3*520,512),'white')
    W.paste(sprite(s).resize((512,512),Image.NEAREST),(0,0)); W.paste(model_op_schaal(m,512),(520,0)); W.paste(sprite(R).resize((512,512),Image.NEAREST),(1040,0)); W.save(f'vgl8_{nm}.png')
    W=Image.new('RGB',(6*200,200),(255,255,255))
    for i,im in enumerate([sprite(s),model_op_schaal(m,64),sprite(R),sprite(G),sprite(s,(40,40,48)),model_op_schaal(m,64)]):
        W.paste(im.resize((192,192),Image.NEAREST),(i*200,4))
    W.save(f'vgl1x3_{nm}.png')
    for z,(x0,y0,x1,y1) in {'kop':(10,0,50,40),'onder':(0,28,64,64)}.items():
        a=grid(sprite(s),12).crop((x0*12,y0*12,x1*12,y1*12)); b=grid(model_op_schaal(m,64*12),1).crop((x0*12,y0*12,x1*12,y1*12))
        W=Image.new('RGB',(a.width*2+10,a.height),'white'); W.paste(a,(0,0)); W.paste(b,(a.width+10,0)); W.save(f'z_{z}_{nm}.png')
