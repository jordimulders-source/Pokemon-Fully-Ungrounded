# vel: resultaat | g3r5 palet B | r10 (8x); kop 12x naast de r10-kop; 1x licht/donker; variant ruw (zonder AA-fix)
import os, numpy as np; from PIL import Image, ImageDraw
H=os.path.dirname(os.path.abspath(__file__))
def rgba(p):
    im=Image.open(p)
    if im.mode=='P': im.info['transparency']=0
    return im.convert('RGBA')
R=rgba(os.path.join(H,'claydol_r10kop.png')); G=rgba(os.path.join(H,'../claydol_gemini_r3/r5/claydol_g3r5_paletB.png'))
V=rgba(os.path.join(H,'claydol_r10kop_ruw.png'))
N=Image.open(os.path.join(H,'natief_r10.png')).convert('RGBA')
W=3*522+10; v=Image.new('RGBA',(W,16+512+30+46*12+20+100),(255,255,255,255)); d=ImageDraw.Draw(v)
for i,(t,im) in enumerate([('claydol_r10kop (resultaat)',R.resize((512,512),Image.NEAREST)),('g3r5 palet B (basis)',G.resize((512,512),Image.NEAREST)),('Gemini r10 natief (99 px, pitch 10,24)',N.resize((495,495),Image.NEAREST))]):
    x=10+i*522; d.text((x,3),t,fill='black'); v.alpha_composite(im,(x,16))
y=16+512+12; d.text((10,y),'kop 12x: resultaat (x 9-54, y 0-39) | r10-kop natief (x 17-82, y 12-67) op 9x',fill='black'); y+=16
k=R.crop((8,0,56,40)).resize((48*12,40*12),Image.NEAREST); v.alpha_composite(k,(10,y))
k2=N.crop((17,12,83,68)).resize((66*9,56*9),Image.NEAREST); v.alpha_composite(k2,(10+48*12+20,y))
y+=56*9+12
for i,im in enumerate([R,G,V]):
    for j,bg in enumerate([(248,248,240,255),(40,40,48,255)]):
        t=Image.new('RGBA',(80,80),bg); t.alpha_composite(im,(8,8)); v.alpha_composite(t,(10+i*200+j*90,y))
d.text((10+3*200,y+30),'1x licht/donker: resultaat | g3r5 | variant ruw (met de 6 r10-AA-pixels op de bandrand)',fill='black')
v=v.crop((0,0,W,y+90)); v.save(os.path.join(H,'vel.png'))
