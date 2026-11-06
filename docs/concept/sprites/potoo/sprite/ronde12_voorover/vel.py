from PIL import Image, ImageDraw, ImageOps
sp=Image.open('potoo.png').convert('RGBA')
def onwit(im,s):
    w=Image.new('RGBA',im.size,(255,255,255,255)); w.alpha_composite(im); return w.resize((im.size[0]*s,im.size[1]*s),Image.NEAREST).convert('RGB')
R='../../referenties/'
fotos=[('ineengedoken (gespiegeld)',ImageOps.mirror(Image.open(R+'jordi_great_potoo_bek_open_ineengedoken.png').convert('RGB')).crop((40,60,440,480))),
 ('tak (gespiegeld)',ImageOps.mirror(Image.open(R+'jordi_great_potoo_tak_bek_open_volledig.png').convert('RGB')).crop((40,100,300,597)))]
H=512; tiles=[(n,f.resize((int(f.size[0]*H/f.size[1]),H))) for n,f in fotos]
W=Image.new('RGB',(512+sum(t.size[0]+20 for _,t in tiles)+170,H+50),'white')
s8=onwit(sp,8); d8=ImageDraw.Draw(s8)
for i in range(0,513,8): d8.line([(i,0),(i,512)],fill=(232,232,236)); d8.line([(0,i),(512,i)],fill=(232,232,236))
s8.paste(onwit(sp,8),(0,0),onwit(sp,8).convert('L').point(lambda v:255 if v<250 else 0))
W.paste(s8,(0,40)); x=532; d=ImageDraw.Draw(W)
d.text((5,12),'r12 (8x, raster = 1 spritepixel): kop = jouw omtrek, lijnen 1 px',fill=(0,0,0))
for n,t in tiles: W.paste(t,(x,40)); d.text((x+5,12),n,fill=(0,0,0)); x+=t.size[0]+20
W.paste(onwit(sp,1),(x,40)); W.paste(onwit(sp,2),(x,120)); d.text((x,12),'1x / 2x (in-game = 1x)',fill=(0,0,0))
W.save('vergelijking.png')
