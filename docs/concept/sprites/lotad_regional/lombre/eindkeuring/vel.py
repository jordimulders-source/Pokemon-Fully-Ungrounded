# vergelijk.png: voor (r3 A) | na (eindkeuring) | model (gemini_r1, per spritepixel via meet.py = verkleind model) op 8x;
# daaronder 1x en 2x op licht en donker naast de gaucho-Lotad, Gen 3-Lombre/Ludicolo (_gba) en de maatstaf-sprites.
import os, numpy as np; from PIL import Image, ImageDraw
H=os.path.dirname(os.path.abspath(__file__)); P=lambda *a: os.path.join(H,*a)
ROOT=P('..','..','..','..','..','..'); SP=P('..','..','..')
import sys; sys.path.insert(0,H); from meet import MC
def rgba(f,palf=None):
    im=Image.open(f); a=np.array(im)[:64]
    if palf:
        L=[l.split() for l in open(palf).read().split('\n')[3:] if l.strip()]; pal=np.array([[int(v) for v in l] for l in L])[:16]
    else: pal=np.array(im.getpalette()[:48]).reshape(16,3)
    out=np.zeros((64,64,4),'uint8'); out[...,:3]=pal[a]; out[...,3]=np.where(a>0,255,0); return Image.fromarray(out)
def op(im,bg):
    b=Image.new('RGBA',im.size,bg+(255,)); b.alpha_composite(im); return b.convert('RGB')
voor=rgba(P('..','sprite','r3','lombre_gaucho_r3_A.png')); na=rgba(P('lombre_gaucho_e.png'))
op(na,(255,255,255)).resize((512,512),Image.NEAREST)
na8=na.resize((512,512),Image.NEAREST); na8.save(P('lombre_gaucho_e_8x.png'))
fig=np.array(voor)[...,3]>0
mod=MC.astype('uint8').copy(); mod[~fig]=200
x0,y0,x1,y1=9,4,55,64; Z=8; w=(x1-x0)*Z; h=(y1-y0)*Z; BG=(200,200,200)
W=Image.new('RGB',(3*w+40,h+40+2*72+2*136+60),(255,255,255)); d=ImageDraw.Draw(W)
W.paste(op(voor,BG).crop((x0,y0,x1,y1)).resize((w,h),Image.NEAREST),(0,30))
W.paste(op(na,BG).crop((x0,y0,x1,y1)).resize((w,h),Image.NEAREST),(w+20,30))
W.paste(Image.fromarray(mod[y0:y1,x0:x1]).resize((w,h),Image.NEAREST),(2*w+40,30))
for i,t in enumerate(['voor (r3 A)','na (eindkeuring)','model gemini_r1 per spritepixel (zonder mond-/oogwijzigingen)']): d.text((i*(w+20)+4,8),t,fill=(0,0,0))
G=os.path.join(ROOT,'graphics','pokemon')
refs=[('voor',voor),('na',na),('gaucho-Lotad',rgba(os.path.join(SP,'lotad_regional','af','lotad_gaucho.png'))),
      ('Lombre',rgba(os.path.join(G,'lombre','anim_front_gba.png'),os.path.join(G,'lombre','normal_gba.pal'))),
      ('Ludicolo',rgba(os.path.join(G,'ludicolo','anim_front_gba.png'),os.path.join(G,'ludicolo','normal_gba.pal'))),
      ('Dundragoon',rgba(os.path.join(SP,'dundragoon','af','dundragoon.png'))),('Skinguin',rgba(os.path.join(SP,'skinguin','af','skinguin.png'))),
      ('Zapacha',rgba(os.path.join(SP,'viscacha','af','viscacha.png'))),('Princadee',rgba(os.path.join(SP,'awki','af','awki.png')))]
yb=h+50
for r,bg in enumerate([(248,248,248),(40,44,52)]):
    for i,(n,im) in enumerate(refs): W.paste(op(im,bg),(i*70,yb+r*72))
for i,(n,im) in enumerate(refs): d.text((i*70+2,yb+2*72+2),n[:11],fill=(0,0,0))
yb2=yb+2*72+18
for r,bg in enumerate([(248,248,248),(40,44,52)]):
    for i,(n,im) in enumerate(refs[:5]): W.paste(op(im,bg).resize((128,128),Image.NEAREST),(i*136,yb2+r*136))
for i,(n,im) in enumerate(refs[:5]): d.text((i*136+2,yb2+2*136+4),n+' (2x)',fill=(0,0,0))
W.save(P('vergelijk.png')); print(W.size)
