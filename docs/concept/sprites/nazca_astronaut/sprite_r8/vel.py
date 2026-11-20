# vel.png: P1 | P2 | r4-A op 8x + 1x licht/donker, en Sigilyph (romp) op 8x ter vergelijking
from PIL import Image, ImageDraw
V=[('astro_P1.png','r8 P1'),('astro_P2.png','r8 P2')]
s=8; vel=Image.new('RGB',(2*(64*s+10),64*s+130),(120,120,120)); d=ImageDraw.Draw(vel)
for k,(f,t) in enumerate(V):
    im=Image.open(f).convert('RGBA'); x=k*(64*s+10)
    bg=Image.new('RGBA',(64*s,64*s),(232,236,228,255)); bg.alpha_composite(im.resize((64*s,64*s),Image.NEAREST))
    vel.paste(bg.convert('RGB'),(x,20)); d.text((x+4,4),t,fill=(255,255,255))
    for u,c in enumerate([(248,248,240,255),(40,44,56,255)]):
        b=Image.new('RGBA',(64,64),c); b.alpha_composite(im); vel.paste(b.convert('RGB'),(x+10+u*70,64*s+40))
vel.save('vel.png'); print(vel.size)
