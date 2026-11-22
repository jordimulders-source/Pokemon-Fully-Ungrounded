# vel.png: r15-a_L1 | r16-a_L1 | r16-a_L3 op 6x; close-up schouder/taille (x20-42, rij 24-38) op 12x; 1x licht/donker.
from PIL import Image, ImageDraw
V=[('../sprite_r15/astro_a_L1.png','r15 a_L1'),('astro_a_L1.png','r16 a_L1'),('astro_a_L3.png','r16 a_L3')]
s=6; cw=48*s+8; h6=60*s; zb,zh=22*12,14*12
vel=Image.new('RGB',(3*cw,18+h6+8+zh+8+68*2),(120,120,120)); d=ImageDraw.Draw(vel)
for k,(f,t) in enumerate(V):
    im=Image.open(f).convert('RGBA'); x=k*cw
    bg=Image.new('RGBA',(64,64),(232,236,228,255)); bg.alpha_composite(im)
    vel.paste(bg.crop((8,4,56,64)).resize((48*s,h6),Image.NEAREST).convert('RGB'),(x,18)); d.text((x+4,4),t,fill=(255,255,255))
    vel.paste(bg.crop((20,24,42,38)).resize((zb,zh),Image.NEAREST).convert('RGB'),(x+12,18+h6+8))
    for u,c in enumerate([(248,248,240,255),(40,44,56,255)]):
        b=Image.new('RGBA',(64,64),c); b.alpha_composite(im); vel.paste(b.convert('RGB'),(x+80+u*70,18+h6+8+zh+8))
vel.save('vel.png'); print(vel.size)
