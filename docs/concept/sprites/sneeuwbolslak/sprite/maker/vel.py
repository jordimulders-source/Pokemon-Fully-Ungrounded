# vel: r1_B 8x | rN 8x, daaronder beide 1x op licht en donker. gebruik: python3 vel.py rN
import sys
from PIL import Image
D='/home/user/Pokemon-Fully-Ungrounded/docs/concept/sprites/sneeuwbolslak/sprite/'
n=sys.argv[1]
a=Image.open(D+'r1_B.png').convert('RGBA'); b=Image.open(D+'maker/'+n+'.png').convert('RGBA')
W=64*8*2+24; v=Image.new('RGBA',(W,64*8+24+64*2+16),(255,255,255,255))
for k,im in enumerate((a,b)):
    v.paste(im.resize((512,512),Image.NEAREST),(k*(512+24),0),im.resize((512,512),Image.NEAREST))
y=512+24
for k,bg in enumerate(((248,248,248,255),(40,40,48,255))):
    for kk,im in enumerate((a,b)):
        t=Image.new('RGBA',(64,64),bg); t.alpha_composite(im); v.paste(t,(kk*80+k*180,y))
        t2=t.resize((128,128),Image.NEAREST); v.paste(t2,(400+kk*140+k*300,y))
v.save(D+'maker/vel_'+n+'.png')
