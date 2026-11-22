# vel.png: rij a (L1/L2/L3) en rij b (L1/L2/L3) op 6x; onderaan alle zes op 1x licht/donker.
from PIL import Image, ImageDraw
V=[('astro_%s_%s.png'%(m,l),'%s_%s'%(m,l)) for m in 'ab' for l in ('L1','L2','L3')]
s=6; cw=48*s+8; h6=60*s; vel=Image.new('RGB',(3*cw,2*(18+h6)+8+2*68),(120,120,120)); d=ImageDraw.Draw(vel)
for k,(f,t) in enumerate(V):
    im=Image.open(f).convert('RGBA'); x=(k%3)*cw; y=(k//3)*(18+h6)
    bg=Image.new('RGBA',(64,64),(232,236,228,255)); bg.alpha_composite(im)
    vel.paste(bg.crop((8,4,56,64)).resize((48*s,h6),Image.NEAREST).convert('RGB'),(x,y+18)); d.text((x+4,y+4),t,fill=(255,255,255))
    for u,c in enumerate([(248,248,240,255),(40,44,56,255)]):
        b=Image.new('RGBA',(64,64),c); b.alpha_composite(im); vel.paste(b.convert('RGB'),(10+k*70,2*(18+h6)+4+u*68))
vel.save('vel.png'); print(vel.size)
