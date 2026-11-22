# vel.png: r12 | r13 (P_rood) op 6x; daaronder de borst op 12x; onderaan 1x licht/donker.
from PIL import Image, ImageDraw
V=[('../sprite_r12/astro_P_rood.png','r12 P_rood'),('astro_P_rood.png','r13 P_rood')]
s=6; cw=48*s+8; h6=60*s; hz=14*12
vel=Image.new('RGB',(2*cw,18+h6+8+hz+8+2*68),(120,120,120)); d=ImageDraw.Draw(vel)
for k,(f,t) in enumerate(V):
    im=Image.open(f).convert('RGBA'); x=k*cw
    bg=Image.new('RGBA',(64,64),(232,236,228,255)); bg.alpha_composite(im)
    vel.paste(bg.crop((8,4,56,64)).resize((48*s,h6),Image.NEAREST).convert('RGB'),(x,18)); d.text((x+4,4),t,fill=(255,255,255))
    vel.paste(bg.crop((24,22,42,36)).resize((18*12,hz),Image.NEAREST).convert('RGB'),(x+36,18+h6+8))
    for u,c in enumerate([(248,248,240,255),(40,44,56,255)]):
        b=Image.new('RGBA',(64,64),c); b.alpha_composite(im); vel.paste(b.convert('RGB'),(x+80+u*70,18+h6+8+hz+8))
vel.save('vel.png'); print(vel.size)
