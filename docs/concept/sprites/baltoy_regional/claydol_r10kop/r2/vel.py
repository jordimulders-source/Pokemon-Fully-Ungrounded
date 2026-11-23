# vel r2: r2 | r10kop | g3r5 op 8x; kop 12x; lijf 12x; 1x licht/donker; variant B (grote ogen)
import os, numpy as np; from PIL import Image, ImageDraw
H=os.path.dirname(os.path.abspath(__file__))
def rgba(p):
    im=Image.open(p)
    if im.mode=='P': im.info['transparency']=0
    return im.convert('RGBA')
A=rgba(os.path.join(H,'claydol_r10kop_r2.png')); B=rgba(os.path.join(H,'claydol_r10kop_r2_B_grote_ogen.png'))
R1=rgba(os.path.join(H,'../claydol_r10kop.png')); G=rgba(os.path.join(H,'../../claydol_gemini_r3/r5/claydol_g3r5_paletB.png'))
W=4*522+10; v=Image.new('RGBA',(W,16+512+30+40*12+30+24*12+20+100),(255,255,255,255)); d=ImageDraw.Draw(v)
for i,(t,im) in enumerate([('r2 (claydol_r10kop_r2)',A),('r10kop (ronde 1)',R1),('g3r5 palet B (3 ogen)',G),('variant B: grote ogen (rijen herhaald)',B)]):
    x=10+i*522; d.text((x,3),t,fill='black'); v.alpha_composite(im.resize((512,512),Image.NEAREST),(x,16))
y=16+512+12; d.text((10,y),'kop 12x (x 8-56, y 0-40): r2 | r10kop',fill='black'); y+=16
for i,im in enumerate([A,R1]): v.alpha_composite(im.crop((8,0,56,40)).resize((48*12,40*12),Image.NEAREST),(10+i*(48*12+20),y))
y+=40*12+12; d.text((10,y),'lijf 12x (x 12-54, y 38-62): r2 | r10kop',fill='black'); y+=16
for i,im in enumerate([A,R1]): v.alpha_composite(im.crop((12,38,54,62)).resize((42*12,24*12),Image.NEAREST),(10+i*(42*12+20),y))
y+=24*12+12
for i,im in enumerate([A,R1,G,B]):
    for j,bg in enumerate([(248,248,240,255),(40,40,48,255)]):
        t=Image.new('RGBA',(80,80),bg); t.alpha_composite(im,(8,8)); v.alpha_composite(t,(10+i*200+j*90,y))
d.text((10+4*200,y+30),'1x licht/donker: r2 | r10kop | g3r5 | variant B',fill='black')
v.crop((0,0,W,y+90)).save(os.path.join(H,'vel.png'))
