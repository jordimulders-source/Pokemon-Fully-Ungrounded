# vel.png: r1 (spleettop rij 35) + r2-varianten rij 34/33/32, variant A, op 8x en 1x
from PIL import Image, ImageDraw
V=[('../sprite_r1/astro_A.png','r1: rij 35'),('astro_A_rij34.png','rij 34 (S=7)'),('astro_A_rij33.png','rij 33 (S=8)'),('astro_A_rij32.png','rij 32 (S=10)')]
s=8; vel=Image.new('RGB',(4*(64*s+10),64*s+30+100),(120,120,120)); d=ImageDraw.Draw(vel)
for k,(f,t) in enumerate(V):
    im=Image.open(f).convert('RGBA'); x=k*(64*s+10)
    bg=Image.new('RGBA',(64*s,64*s),(232,236,228,255)); bg.alpha_composite(im.resize((64*s,64*s),Image.NEAREST))
    vel.paste(bg.convert('RGB'),(x,20)); d.text((x+4,4),t,fill=(255,255,255))
    for u,c in enumerate([(248,248,240,255),(40,44,56,255)]):
        b=Image.new('RGBA',(64,64),c); b.alpha_composite(im); vel.paste(b.convert('RGB'),(x+10+u*70,64*s+30+10))
vel.save('vel.png'); print(vel.size)
