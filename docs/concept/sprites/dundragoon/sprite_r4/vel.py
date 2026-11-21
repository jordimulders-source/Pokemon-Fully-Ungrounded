# vel.py: r4 | r3 | model op 8x, daaronder 1x (en 2x) op licht en donker. Draaien vanuit dundragoon/.
from PIL import Image
r4=Image.open('sprite_r4/dundragoon_r4.png').convert('RGBA')
r3=Image.open('sprite_r3/dundragoon_r3.png').convert('RGBA')
m=Image.open('referenties/gemini_gekozen_r7.png').convert('RGBA').resize((512,512),Image.LANCZOS)
v=Image.new('RGBA',(3*512+40,512+180),(255,255,255,255))
for i,im in enumerate([r4.resize((512,512),Image.NEAREST),r3.resize((512,512),Image.NEAREST),m]):
    v.paste(im,(i*(512+20),0),im)
bgs=[(255,255,255),(240,232,208),(64,64,72),(0,0,0)]
for j,c in enumerate(bgs):
    for k,(im,s) in enumerate([(r4,1),(r3,1),(r4,2)]):
        t=im.resize((64*s,64*s),Image.NEAREST); x=j*390+k*(70 if k<2 else 70)+ (0 if k<2 else 70)
        bg=Image.new('RGBA',(64*s+8,64*s+8),c+(255,)); bg.paste(t,(4,4),t)
        v.paste(bg,(10+j*390+[0,76,152][k],530))
v.convert('RGB').save('sprite_r4/vel.png')
r4.resize((512,512),Image.NEAREST).save('sprite_r4/dundragoon_r4_8x.png')
