# Vel eindkeuring r4: sprite 8x | model verkleind (x0,617) 8x; 1x/2x licht/donker; Gen 3 (gba) ernaast; voorstel-uitsnede.
from PIL import Image, ImageDraw
G='../../../../../../graphics/pokemon/'
def rgba(path,crop=None):
    im=Image.open(path)
    if crop: im=im.crop(crop)
    if im.mode=='P':
        a=im.convert('RGBA'); px=a.load(); idx=im.load()
        for y in range(im.height):
            for x in range(im.width):
                if idx[x,y]==0: px[x,y]=(0,0,0,0)
        return a
    return im.convert('RGBA')
def on(im,col,s):
    b=Image.new('RGBA',im.size,col); b.alpha_composite(im); return b.resize((im.width*s,im.height*s),Image.NEAREST)
spr=rgba('../sprite_r4/sprite.png'); r3=rgba('../sprite_r3/sprite.png'); vs=rgba('voorstel.png')
mod=Image.open('../model/model_gekozen_natief.png').convert('RGBA')
mod8=mod.resize((round(99*0.617*8),)*2,Image.LANCZOS)
LIGHT=(232,232,232,255); DARK=(40,40,48,255)
W=Image.new('RGBA',(1240,1120),(255,255,255,255)); d=ImageDraw.Draw(W)
W.paste(on(spr,(200,200,200,255),8),(10,24)); d.text((10,6),'sprite r4, 8x',fill='black')
W.paste(mod8,(540,24)); d.text((540,6),'model (natief, x0,617), 8x',fill='black')
y0=566; x=10
for im,n in ((spr,'r4'),(r3,'r3')):
    for col,lab in ((LIGHT,'licht'),(DARK,'donker')):
        for s in (1,2):
            W.paste(on(im,col,s),(x,y0)); d.text((x,y0-14),f'{n} {s}x {lab}',fill='black'); x+=64*s+10
c=(28,34,44,54)
W.paste(on(spr.crop(c),LIGHT,10),(1040,40)); d.text((1040,24),'r4 (41,35) uitsnede',fill='black')
W.paste(on(vs.crop(c),LIGHT,10),(1040,260)); d.text((1040,244),'voorstel P->m',fill='black')
x=10; y1=y0+170
for n in ['voltorb','magnemite','beldum','lunatone','shuppet']:
    g=rgba(G+n+'/anim_front_gba.png',(0,0,64,64))
    W.paste(on(g,LIGHT,2),(x,y1)); W.paste(on(g,LIGHT,1),(x,y1+140)); d.text((x,y1-14),n+' (gba)',fill='black'); x+=140
W.paste(on(spr,LIGHT,2),(x,y1)); W.paste(on(spr,LIGHT,1),(x,y1+140)); d.text((x,y1-14),'r4',fill='black')
W.convert('RGB').save('vel.png')
