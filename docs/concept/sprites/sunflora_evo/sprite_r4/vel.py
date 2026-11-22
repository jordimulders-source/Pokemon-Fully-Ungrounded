import numpy as np; from PIL import Image, ImageDraw
r4=Image.open('sunflora_evo_r4.png').convert('RGBA'); r3=Image.open('../sprite_r3/sunflora_evo_r3_voet_buiten.png').convert('RGBA')
sf=Image.open('../sprite_r1/sunflora_f1.png').convert('RGBA')
up=lambda im,k: im.resize((im.width*k,im.height*k),Image.NEAREST)
v=Image.new('RGB',(3*532,24+512+20+300),'white'); d=ImageDraw.Draw(v)
for k,(t,im) in enumerate([('r4',r4),('r3 buiten',r3),('Sunflora Gen 3',sf)]):
    b=up(im,8); v.paste(b,(k*532,24),b); d.text((k*532+4,6),t+' (8x)',fill='black')
box=(12,42,50,62)
for k,(t,im) in enumerate([('r4 lijf 12x',r4),('r3 lijf 12x',r3)]):
    c=up(im.crop(box),12); q=Image.new('RGB',c.size,(255,255,255)); q.paste(c,(0,0),c); v.paste(q,(k*(c.width+20),556))
x=2*(38*12+20)
for i,bg in enumerate([(248,248,248),(40,40,48)]):
    q=Image.new('RGB',(64,64),bg); q.paste(r4,(0,0),r4); v.paste(q,(x+i*74,556)); v.paste(up(q,2),(x+i*140,640))
v.save('vel.png'); print(v.size)
