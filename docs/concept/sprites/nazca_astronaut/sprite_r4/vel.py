# vel.png: A | B1 | B2 op 8x + 1x licht/donker; daaronder de kop r3-rij28 vs r4 op 12x
from PIL import Image, ImageDraw
V=[('astro_A.png','A'),('astro_B1.png','B1: boven wit, onder rood'),('astro_B2.png','B2: boven rood, onder wit')]
s=8; K=12; kop=(22,5,46,27)  # kopuitsnede (png)
kw=(kop[2]-kop[0])*K; kh=(kop[3]-kop[1])*K
vel=Image.new('RGB',(3*(64*s+10),64*s+130+kh+30),(120,120,120)); d=ImageDraw.Draw(vel)
for k,(f,t) in enumerate(V):
    im=Image.open(f).convert('RGBA'); x=k*(64*s+10)
    bg=Image.new('RGBA',(64*s,64*s),(232,236,228,255)); bg.alpha_composite(im.resize((64*s,64*s),Image.NEAREST))
    vel.paste(bg.convert('RGB'),(x,20)); d.text((x+4,4),t,fill=(255,255,255))
    for u,c in enumerate([(248,248,240,255),(40,44,56,255)]):
        b=Image.new('RGBA',(64,64),c); b.alpha_composite(im); vel.paste(b.convert('RGB'),(x+10+u*70,64*s+30+10))
y=64*s+130
for k,(f,t) in enumerate([('../sprite_r3/astro_A_rij28.png','kop r3 (12x)'),('astro_A.png','kop r4 (12x)')]):
    im=Image.open(f).convert('RGBA').crop(kop); bg=Image.new('RGBA',im.size,(232,236,228,255)); bg.alpha_composite(im)
    vel.paste(bg.convert('RGB').resize((kw,kh),Image.NEAREST),(10+k*(kw+20),y+20)); d.text((10+k*(kw+20),y+4),t,fill=(255,255,255))
vel.save('vel.png'); print(vel.size)
