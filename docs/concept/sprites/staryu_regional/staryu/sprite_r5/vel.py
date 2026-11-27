# vel.png: r5 | r4 | model op schaal (8x), wijzigingen omcirkeld op r5; daaronder 1x en 2x op wit en donker naast Gen 3 Staryu en de maatstaf.
import sys, numpy as np; from PIL import Image, ImageDraw
sys.path.insert(0,'gereedschap_r4'); from gemeen import *
def rgba(p):
    im=Image.open(p); im.save('/tmp/_v.png',transparency=0) if im.mode=='P' and 'transparency' not in im.info else None
    return Image.open(p).convert('RGBA')
def gba(n):
    im=Image.open('../../../../../graphics/pokemon/%s/anim_front_gba.png'%n)
    cols=[tuple(map(int,l.split())) for l in open('../../../../../graphics/pokemon/%s/normal_gba.pal'%n).read().split('\n')[3:] if l.strip()]
    im=im.crop((0,0,64,64)); a=np.asarray(im); out=np.zeros((64,64,4),'uint8')
    for k,c in enumerate(cols): out[a==k]=(*c,255)
    out[a==0,3]=0; return Image.fromarray(out)
def op(im,bg):
    b=Image.new('RGBA',im.size,bg+(255,)); b.alpha_composite(im); return b.convert('RGB')
r5=rgba('sprite_r5/staryu_r5.png'); r4=rgba('sprite_r4/staryu_r4.png')
m=model_op_schaal()
c=(8,8,56,56); K=8; w=48*K
V=Image.new('RGB',(2000,w+40+2*64*2+60),(255,255,255)); d=ImageDraw.Draw(V)
for i,(im,t) in enumerate([(op(r5,(255,255,255)),'r5'),(op(r4,(255,255,255)),'r4'),(m,'model op schaal')]):
    V.paste(im.crop(c).resize((w,w),Image.NEAREST),(i*(w+20),20)); d.text((i*(w+20)+4,4),t,fill=(0,0,0))
a5=np.asarray(Image.open('sprite_r5/staryu_r5.png')); a4=np.asarray(Image.open('sprite_r4/staryu_r4.png'))
for Y,X in zip(*np.where(a5!=a4)):
    x=(X-8)*K; y=(Y-8)*K+20; d.rectangle((x-1,y-1,x+K,y+K),outline=(0,120,255))
mr=m.convert('RGBA'); ma=np.asarray(mr).copy(); ma[(ma[...,:3]>=250).all(2),3]=0; mr=Image.fromarray(ma)
rij=[r5,r4,mr,gba('staryu'),gba('starmie'),gba('taillow')]
for nm in ('skinguin','dundragoon','viscacha','awki'): rij.append(rgba('../../%s/af/%s.png'%(nm,nm)))
y0=w+40
for j,bg in enumerate([(255,255,255),(40,44,52)]):
    x=0
    for im in rij:
        V.paste(op(im,bg),(x,y0+j*130)); V.paste(op(im,bg).resize((128,128),Image.NEAREST),(x+66,y0+j*130)); x+=200
d.text((4,y0+262),'1x en 2x: r5, r4, model, Gen 3 Staryu, Starmie, Taillow, Skinguin, Dundragoon, Zapacha, Princadee (blauw = gewijzigd t.o.v. r4)',fill=(0,0,0))
V.save('sprite_r5/vel.png')
