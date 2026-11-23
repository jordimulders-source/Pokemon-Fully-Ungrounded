# vel r6: r6 | r5 | r3 op 8x; studievel lijven 12x; lijf 12x r3|r5|r6|r6B + tintgrenzen r5|r6; neus 12x r6|r5|g3r5; 1x/2x
import os,sys; from PIL import Image, ImageDraw
H=os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0,H); os.chdir(os.path.join(H,'../../../../../..'))
from grens import overlay; from gba import gba
B_='docs/concept/sprites/baltoy_regional/'
def rgba(p):
    im=Image.open(p); im.info['transparency']=0; return im.convert('RGBA')
P={'r6':H+'/claydol_r10kop_r6.png','r6B':H+'/claydol_r10kop_r6_B_reflectie.png','r5':H+'/../r5/claydol_r10kop_r5.png','r3':H+'/../r3/claydol_r10kop_r3.png'}
I={k:rgba(p) for k,p in P.items()}; G3=rgba(B_+'claydol_gemini_r3/r5/claydol_g3r5_paletB.png')
v=Image.new('RGBA',(2000,3000),'white'); d=ImageDraw.Draw(v); y=4
for i,k in enumerate(['r6','r5','r3']): d.text((10+i*522,y),k,fill='black'); v.alpha_composite(I[k].resize((512,512),Image.NEAREST),(10+i*522,y+14))
y+=540; d.text((10,y),'studie 12x: Gen 3 Claydol (lijf) | Baltoy r19 (lijf) | Golem (anim_front_gba)',fill='black'); y+=14
cl=gba('claydol',(4,32,60,58)); bl=rgba(B_+'sprite_r19/baltoy_r19.png').crop((8,34,56,62)); go=gba('golem',(8,8,56,56))
v.alpha_composite(cl.resize((672,312),Image.NEAREST),(10,y)); v.alpha_composite(bl.resize((576,336),Image.NEAREST),(692,y)); v.alpha_composite(go.resize((480,480),Image.NEAREST),(1278,y))
y+=490; d.text((10,y),'lijf 12x: r3 | r5 | r6 | r6 variant B (reflectierand)',fill='black'); y+=14
for i,k in enumerate(['r3','r5','r6','r6B']): v.alpha_composite(I[k].crop((13,39,52,61)).resize((468,264),Image.NEAREST),(10+i*478,y))
y+=274; d.text((10,y),'tintgrenzen (blauw) 12x: r3 | r5 | r6 | r6B',fill='black'); y+=14
for i,k in enumerate(['r3','r5','r6','r6B']): v.alpha_composite(overlay(P[k]),(10+i*478,y))
y+=274; d.text((10,y),'neus 12x (x 16-33): r6 | r5 | g3r5 (1 px hoger)',fill='black'); y+=14
for i,(im,y0) in enumerate([(I['r6'],18),(I['r5'],18),(G3,17)]): v.alpha_composite(im.crop((16,y0,34,y0+20)).resize((216,240),Image.NEAREST),(10+i*226,y))
y+=250
for i,k in enumerate(['r6','r6B','r5','r3']):
    for j,bg in enumerate([(248,248,240,255),(40,40,48,255)]):
        q=Image.new('RGBA',(80,80),bg); q.alpha_composite(I[k],(8,8)); v.alpha_composite(q,(10+i*360+j*90,y))
    v.alpha_composite(I[k].resize((128,128),Image.NEAREST),(10+i*360+190,y))
d.text((10,y+132),'1x licht/donker + 2x: r6 | r6B | r5 | r3',fill='black')
v.crop((0,0,1920,y+150)).save(os.path.join(H,'vel.png'))
