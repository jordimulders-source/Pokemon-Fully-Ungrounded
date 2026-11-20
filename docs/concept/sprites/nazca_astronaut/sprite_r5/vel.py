# vel.png: P1 | P2 | r4-A op 8x + 1x licht/donker, en Sigilyph (romp) op 8x ter vergelijking
from PIL import Image, ImageDraw
V=[('astro_P1.png','P1: Sigilyph-kleuren'),('astro_P2.png','P2: ons palet'),('../sprite_r4/astro_A.png','r4-A')]
s=8; vel=Image.new('RGB',(3*(64*s+10)+30*s,64*s+130),(120,120,120)); d=ImageDraw.Draw(vel)
for k,(f,t) in enumerate(V):
    im=Image.open(f).convert('RGBA'); x=k*(64*s+10)
    bg=Image.new('RGBA',(64*s,64*s),(232,236,228,255)); bg.alpha_composite(im.resize((64*s,64*s),Image.NEAREST))
    vel.paste(bg.convert('RGB'),(x,20)); d.text((x+4,4),t,fill=(255,255,255))
    for u,c in enumerate([(248,248,240,255),(40,44,56,255)]):
        b=Image.new('RGBA',(64,64),c); b.alpha_composite(im); vel.paste(b.convert('RGB'),(x+10+u*70,64*s+40))
sig=Image.open('../../../../../graphics/pokemon/sigilyph/anim_front.png')
pal=open('../../../../../graphics/pokemon/sigilyph/normal.pal').read().split('\n')[3:19]
sig.putpalette([v for l in pal for v in map(int,l.split())])
sig=sig.convert('RGB').crop((20,20,48,46)).resize((28*s,26*s),Image.NEAREST)
x=3*(64*s+10); vel.paste(sig,(x,20)); d.text((x+4,4),'Sigilyph romp (8x)',fill=(255,255,255))
vel.save('vel.png'); print(vel.size)
