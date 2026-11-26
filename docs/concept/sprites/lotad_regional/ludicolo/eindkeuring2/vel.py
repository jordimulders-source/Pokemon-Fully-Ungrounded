# vergelijk.png: voor (af = mond_V2) | na (e2) | model (gemiddelde modelkleur per spritepixel, ../eindkeuring/meet.py) op 8x,
# gezichtsuitsnede op 20x, daaronder 1x en 2x op licht en donker naast gaucho-Lotad/-Lombre en de maatstaf-sprites.
import os, sys, numpy as np; from PIL import Image, ImageDraw
H=os.path.dirname(os.path.abspath(__file__)); P=lambda *a: os.path.join(H,*a); sys.path.insert(0,P('..','eindkeuring'))
SP=P('..','..','..')
from meet import MC
def rgba(f):
    im=Image.open(f); a=np.array(im); pal=np.array(im.getpalette()[:48]).reshape(16,3)
    out=np.zeros(a.shape+(4,),'uint8'); out[...,:3]=pal[a]; out[...,3]=np.where(a>0,255,0); return Image.fromarray(out)
def op(im,bg):
    b=Image.new('RGBA',im.size,bg+(255,)); b.alpha_composite(im); return b.convert('RGB')
voor=rgba(P('..','af','ludicolo_gaucho.png')); na=rgba(P('ludicolo_gaucho_e2.png'))
na.resize((512,512),Image.NEAREST).save(P('ludicolo_gaucho_e2_8x.png'))
fig=np.array(voor)[...,3]>0; mod=MC.astype('uint8').copy(); mod[~fig]=200
x0,y0,x1,y1=5,0,58,64; Z=8; w=(x1-x0)*Z; h=(y1-y0)*Z; BG=(200,200,200)
fx0,fy0,fx1,fy1=13,23,38,39; FZ=20; fw=(fx1-fx0)*FZ; fh=(fy1-fy0)*FZ
W=Image.new('RGB',(3*w+40,30+h+20+fh+20+2*72+30+2*136+30),(255,255,255)); d=ImageDraw.Draw(W)
mi=Image.fromarray(mod)
for i,(t,im) in enumerate([('voor (af = mond_V2)',op(voor,BG)),('na (eindkeuring 2)',op(na,BG)),('model gemini_r6, gemiddelde kleur per spritepixel',mi)]):
    W.paste(im.crop((x0,y0,x1,y1)).resize((w,h),Image.NEAREST),(i*(w+20),30)); d.text((i*(w+20)+4,8),t,fill=(0,0,0))
    W.paste(im.crop((fx0,fy0,fx1,fy1)).resize((fw,fh),Image.NEAREST),(i*(w+20),30+h+20))
G=lambda *a: os.path.join(SP,*a)
refs=[('voor',voor),('na',na),('gaucho-Lotad',rgba(G('lotad_regional','af','lotad_gaucho.png'))),('gaucho-Lombre',rgba(G('lotad_regional','lombre','af','lombre_gaucho.png'))),
      ('Dundragoon',rgba(G('dundragoon','af','dundragoon.png'))),('Skinguin',rgba(G('skinguin','af','skinguin.png'))),
      ('Zapacha',rgba(G('viscacha','af','viscacha.png'))),('Princadee',rgba(G('awki','af','awki.png')))]
yb=30+h+20+fh+20
for r,bg in enumerate([(248,248,248),(40,44,52)]):
    for i,(n,im) in enumerate(refs): W.paste(op(im,bg),(i*70,yb+r*72))
for i,(n,im) in enumerate(refs): d.text((i*70+2,yb+2*72+2),n[:11],fill=(0,0,0))
yb2=yb+2*72+30
for r,bg in enumerate([(248,248,248),(40,44,52)]):
    for i,(n,im) in enumerate(refs[:4]): W.paste(op(im,bg).resize((128,128),Image.NEAREST),(i*136,yb2+r*136))
for i,(n,im) in enumerate(refs[:4]): d.text((i*136+2,yb2+2*136+4),n+' (2x)',fill=(0,0,0))
W.save(P('vergelijk.png')); print(W.size)
