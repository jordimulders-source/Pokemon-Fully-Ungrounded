# vel r5: r5A | r4A | fase 1 (guarana/af) op 8x, ogen-uitsneden 12x (r5A | r4A), 1x op licht en donker; voor_jordi_r5_8x.png = r5A op 8x (wit)
import sys, numpy as np; sys.path.insert(0,'sprite_r5'); from gemeen2 import *; from PIL import Image, ImageDraw
W=(255,255,255)
a=np.array(Image.open('sprite_r5/guarana2_r5_A.png')); b=np.array(Image.open('sprite_r4/guarana2_r4_A.png'))
f1=Image.open('../guarana/af/guarana.png').convert('RGBA')
V=Image.new('RGB',(1584,1000),'white'); d=ImageDraw.Draw(V)
V.paste(rgb(a,W).resize((512,512),0),(0,20)); V.paste(rgb(b,W).resize((512,512),0),(528,20))
f8=f1.resize((512,512),0); V.paste(f8,(1056,20),f8)
d.text((4,4),'r5 A (8x)',fill='black'); d.text((532,4),'r4 A (8x)',fill='black'); d.text((1060,4),'fase 1 af (8x)',fill='black')
y=560; d.text((4,y-14),'ogen 12x: r5 A | r4 A (tros L, M, R)',fill='black'); x=0
for (x0,y0,x1,y1) in ((4,20,24,40),(18,10,38,26),(40,20,60,40)):
    for o in (a,b):
        c=rgb(o,W).crop((x0,y0,x1,y1)).resize(((x1-x0)*12,(y1-y0)*12),0); V.paste(c,(x,y)); x+=c.width+6
        if x>1300: x=0; y+=c.height+20
    x+=20
xs=0; ys=830
for bg in ((255,255,255),(240,232,208),(152,208,160),(40,40,48),(16,24,40)): V.paste(rgb(a,bg),(xs,ys)); xs+=72
d.text((0,ys+70),'r5 A 1x op licht en donker',fill='black')
V.save('sprite_r5/vel.png')
rgb(a,W).resize((512,512),0).save('sprite_r5/voor_jordi_r5_8x.png')
