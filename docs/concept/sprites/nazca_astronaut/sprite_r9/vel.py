# vel.png: r8-P1 + V1..V5 op 6x; onderaan alle zes op 1x, rij licht en rij donker.
from PIL import Image, ImageDraw
V=[('../sprite_r8/astro_P1.png','r8 P1')]+[('astro_V%d.png'%i,t) for i,t in enumerate(
   ['V1 aardewerk (getrapt)','V2 woestijn (getrapt)','V3 kosmisch (getrapt)','V4 Sigilyph-kleuren (getrapt)','V5 aardewerk (schuin)'],1)]
s=6; cw=48*s+8; H8=60*s; vel=Image.new('RGB',(len(V)*cw,20+H8+10+2*68+6),(120,120,120)); d=ImageDraw.Draw(vel)
for k,(f,t) in enumerate(V):
    im=Image.open(f).convert('RGBA'); x=k*cw
    bg=Image.new('RGBA',(64,64),(232,236,228,255)); bg.alpha_composite(im)
    vel.paste(bg.crop((8,4,56,64)).resize((48*s,H8),Image.NEAREST).convert('RGB'),(x,20)); d.text((x+4,4),t,fill=(255,255,255))
    for u,c in enumerate([(248,248,240,255),(40,44,56,255)]):
        b=Image.new('RGBA',(64,64),c); b.alpha_composite(im); vel.paste(b.convert('RGB'),(20+k*72,20+H8+10+u*68))
vel.save('vel.png'); print(vel.size)
