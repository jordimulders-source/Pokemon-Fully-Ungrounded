# Vel v4: v4 8x | v3 8x; v4 1x en 2x op licht/donker
from PIL import Image, ImageDraw
D='docs/concept/sprites/hauntflare/'
def opwit(im,bg=(255,255,255)):
    im=im.convert('RGBA'); w=Image.new('RGBA',im.size,bg+(255,)); w.alpha_composite(im); return w.convert('RGB')
v4=Image.open(D+'sprite_v4/hauntflare_v4.png'); v3=Image.open(D+'sprite_v3/hauntflare_v3.png')
V=Image.new('RGB',(2*522+10,522+250),(200,200,200)); d=ImageDraw.Draw(V)
for i,(im,t) in enumerate([(v4,'Hauntflare v4'),(v3,'v3')]):
    V.paste(opwit(im).resize((512,512),0),(10+i*522,10)); d.text((10+i*522,524),t,fill=(0,0,0))
for j,bg in enumerate([(248,248,240),(40,40,48),(255,255,255),(0,0,0)]):
    V.paste(opwit(v4,bg),(10+j*80,545)); V.paste(opwit(v4,bg).resize((128,128),0),(360+j*140,545))
V.save(D+'sprite_v4/vel.png')
