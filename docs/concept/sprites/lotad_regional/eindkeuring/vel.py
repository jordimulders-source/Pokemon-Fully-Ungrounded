# vergelijk.png: voor | na | model (8x; model = natief raster op 4x = zelfde schaal), daaronder 1x op licht en donker
# naast de Gen 3-Lotad en de maatstaf-sprites. lotad_gaucho_e_8x.png: de sprite op 8x.
import os, numpy as np; from PIL import Image, ImageDraw
H=os.path.dirname(os.path.abspath(__file__)); P=lambda *a: os.path.join(H,*a)
SP=P('..','..')
def rgba(f,crop64=True):
    im=Image.open(f); a=np.array(im)[:64]; pal=np.array(im.getpalette()[:48]).reshape(16,3)
    out=np.zeros((64,64,4),'uint8'); out[...,:3]=pal[a]; out[...,3]=np.where(a>0,255,0); return Image.fromarray(out)
def op(im,bg):
    b=Image.new('RGBA',im.size,bg+(255,)); b.alpha_composite(im); return b.convert('RGB')
voor=rgba(P('..','sprite','r3','lotad_gaucho_oogG.png')); na=rgba(P('lotad_gaucho_e.png'))
op(na,(255,255,255)).save('/dev/null','PNG') if False else None
na.resize((512,512),Image.NEAREST).save(P('lotad_gaucho_e_8x.png'))
# model: natieve blokken die bij spritepixels x8..55, y20..63 horen
nat=Image.open(P('..','sprite','r2','natief.png')).convert('RGB')
x0,y0,x1,y1=8,20,56,64
nx0=1+2*(x0-10+37); ny0=1+2*(y0-22+11)
mod=Image.new('RGB',(2*(x1-x0),2*(y1-y0)),(255,255,255))
mod.paste(nat.crop((nx0,max(0,ny0),nx0+2*(x1-x0),ny0+2*(y1-y0))),(0,max(0,-ny0)))
Z=8; w=(x1-x0)*Z; h=(y1-y0)*Z
BG=(200,200,200)
W=Image.new('RGB',(3*w+40,h+40+64*3+40),(255,255,255)); d=ImageDraw.Draw(W)
W.paste(op(voor,BG).crop((x0,y0,x1,y1)).resize((w,h),Image.NEAREST),(0,30))
W.paste(op(na,BG).crop((x0,y0,x1,y1)).resize((w,h),Image.NEAREST),(w+20,30))
W.paste(mod.resize((w,h),Image.NEAREST),(2*w+40,30))
for i,t in enumerate(['voor (r3 oog G)','na (eindkeuring)','model r8_1 (natief, zelfde schaal)']): d.text((i*(w+20)+4,8),t,fill=(0,0,0))
refs=[('lotad',rgba(os.path.join(H,'..','..','..','..','..','graphics','pokemon','lotad','anim_front_gba.png'))),
      ('voor',voor),('na',na),('Dundragoon',rgba(os.path.join(SP,'dundragoon','af','dundragoon.png'))),
      ('Skinguin',rgba(os.path.join(SP,'skinguin','af','skinguin.png'))),('Zapacha',rgba(os.path.join(SP,'viscacha','af','viscacha.png'))),
      ('Princadee',rgba(os.path.join(SP,'awki','af','awki.png')))]
yb=h+50
for r,bg in enumerate([(248,248,248),(40,44,52)]):
    for i,(n,im) in enumerate(refs):
        W.paste(op(im,bg),(i*70,yb+r*72))
    for i,(n,im) in enumerate(refs): d.text((i*70+2,yb+2*72+4),n,fill=(0,0,0))
W.save(P('vergelijk.png'))
