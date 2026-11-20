# vel.png: per variant 8x naast het model (met aangepaste spleet) op dezelfde schaal, plus alle varianten op 1x licht/donker
from PIL import Image, ImageDraw
V=['astro_A.png','astro_A_geel.png','astro_B1.png','astro_B2.png']
n=Image.open('n_edit.png').convert('RGB')
H=58; s=8
mod=n.crop((29,7,29+48,7+87)).resize((int(48*H*s/87),H*s),Image.LANCZOS)
modbox=Image.new('RGB',(64*s,64*s),(255,255,255)); modbox.paste(mod,((64*s-mod.width)//2,6*s))
W=2*64*s+30; rij=64*s+30
vel=Image.new('RGB',(W*2,rij*2+200),(120,120,120)); d=ImageDraw.Draw(vel)
for k,f in enumerate(V):
    im=Image.open(f).convert('RGBA'); x=(k%2)*W; y=(k//2)*rij
    bg=Image.new('RGBA',(64*s,64*s),(232,236,228,255)); big=im.resize((64*s,64*s),Image.NEAREST); bg.alpha_composite(big)
    vel.paste(bg.convert('RGB'),(x,y+20)); vel.paste(modbox,(x+64*s+10,y+20)); d.text((x+4,y+4),f+'  |  model (spleet aangepast)',fill=(255,255,255))
y=2*rij+10
for k,f in enumerate(V):
    im=Image.open(f).convert('RGBA')
    for t,c in enumerate([(248,248,240,255),(40,44,56,255)]):
        b=Image.new('RGBA',(64,64),c); b.alpha_composite(im); vel.paste(b.convert('RGB'),(10+k*150+t*68,y+20))
    b2=Image.new('RGBA',(128,128),(248,248,240,255)); b2.alpha_composite(im.resize((128,128),Image.NEAREST))
d.text((10,y+2),'1x op licht en donker: A, A_geel, B1, B2',fill=(255,255,255))
vel.save('vel.png'); print(vel.size)
