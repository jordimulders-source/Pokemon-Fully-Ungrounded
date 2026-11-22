# vel.png: r10-C1 | K1 | K2 | K3 op 6x; onderaan op 1x licht/donker.
from PIL import Image, ImageDraw
RIJ=[[('../sprite_r10/astro_C1.png','r10 C1')]+[('astro_K%d.png'%i,'K%d'%i) for i in (1,2,3)]]
s=6; cw=48*s+8; rh=60*s+22
vel=Image.new('RGB',(4*cw,rh+2*68+16),(120,120,120)); d=ImageDraw.Draw(vel)
for r,rij in enumerate(RIJ):
    for k,(f,t) in enumerate(rij):
        im=Image.open(f).convert('RGBA'); x=k*cw; y=r*rh
        bg=Image.new('RGBA',(64,64),(232,236,228,255)); bg.alpha_composite(im)
        vel.paste(bg.crop((8,4,56,64)).resize((48*s,60*s),Image.NEAREST).convert('RGB'),(x,y+18)); d.text((x+4,y+4),t,fill=(255,255,255))
alle=[f for rij in RIJ for f,_ in rij]
for k,f in enumerate(alle):
    im=Image.open(f).convert('RGBA')
    for u,c in enumerate([(248,248,240,255),(40,44,56,255)]):
        b=Image.new('RGBA',(64,64),c); b.alpha_composite(im); vel.paste(b.convert('RGB'),(10+k*70,rh+8+u*68))
vel.save('vel.png'); print(vel.size)
