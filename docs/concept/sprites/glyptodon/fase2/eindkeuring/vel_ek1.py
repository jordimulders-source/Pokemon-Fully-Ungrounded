# vel_ek1.png: r7_B_lijn 8x | ek1 8x | wijzigingen (los vel) ; daaronder ek1 2x/1x licht+donker naast 3 Gen 3-sprites op 2x
import numpy as np
from PIL import Image,ImageDraw
R='../../../../../../graphics/pokemon/'
def S(f,bg=(255,255,255),crop64=False):
    im=Image.open(f)
    if crop64:
        L=open(f.replace('anim_front_gba.png','normal_gba.pal')).read().split()[3:]
        im.putpalette([int(v) for v in L[:48]]); im.info['transparency']=0
    sp=im.convert('RGBA')
    if crop64: sp=sp.crop((0,0,64,64))
    b=Image.new('RGBA',sp.size,bg+(255,)); b.alpha_composite(sp); return b.convert('RGB')
W=[tuple(p) for p in np.load('ek1_W.npy')]
o=Image.new('RGB',(3*512+40,512+30+300),(235,235,235)); d=ImageDraw.Draw(o)
d.text((10,6),'sprite/r7_B_lijn (gekozen) 8x',fill=0); d.text((532,6),'eindkeuring ek1 8x',fill=0); d.text((1054,6),'gewijzigde pixels (%d): ek1 grijs gedempt, wijziging in volle kleur met magenta kader'%len(W),fill=0)
o.paste(S('../sprite/r7_B_lijn.png').resize((512,512),Image.NEAREST),(10,22))
o.paste(S('ek1.png').resize((512,512),Image.NEAREST),(532,22))
e=S('ek1.png'); a=np.array(e).astype(float); g=a.mean(2,keepdims=True); dim=(0.35*g+0.65*235).repeat(3,2).astype('uint8')
D=Image.fromarray(dim).resize((512,512),Image.NEAREST); dd=ImageDraw.Draw(D)
for x,y in W:
    c=tuple(int(v) for v in a[y,x]); dd.rectangle([x*8,y*8,x*8+7,y*8+7],fill=c if c!=(255,255,255) else (255,255,255),outline=(255,0,255))
o.paste(D,(1054,22))
y0=512+40; d.text((10,y0),'ek1 2x en 1x op licht en donker',fill=0)
o.paste(S('ek1.png').resize((128,128),Image.NEAREST),(10,y0+16)); o.paste(S('ek1.png',(40,44,52)).resize((128,128),Image.NEAREST),(146,y0+16))
o.paste(S('ek1.png'),(282,y0+16)); o.paste(S('ek1.png',(40,44,52)),(282,y0+86))
X=380
for n in ['donphan','rhydon','torkoal']:
    d.text((X,y0),n+' (Gen 3, gba) 2x',fill=0)
    o.paste(S(R+n+'/anim_front_gba.png',crop64=True).resize((128,128),Image.NEAREST),(X,y0+16))
    o.paste(S(R+n+'/anim_front_gba.png',(40,44,52),crop64=True).resize((128,128),Image.NEAREST),(X,y0+150)); X+=140
d.text((X,y0),'ek1 2x (zelfde schaal)',fill=0); o.paste(S('ek1.png').resize((128,128),Image.NEAREST),(X,y0+16)); o.paste(S('ek1.png',(40,44,52)).resize((128,128),Image.NEAREST),(X,y0+150))
o.save('vel_ek1.png')
