# Vel eindkeuring r3: sprite 8x | model verkleind 8x | voorstel-uitsnede; 1x/2x op licht/donker; Gen 3 (gba) ernaast.
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
spr=rgba('../sprite_r3/sprite.png')
mod=Image.open('../model/model_gekozen_natief.png').convert('RGBA')
mod8=mod.resize((round(99*8*0.787),)*2,Image.LANCZOS)
LIGHT=(232,232,232,255); DARK=(40,40,48,255)
W=Image.new('RGBA',(1200,1060),(255,255,255,255)); d=ImageDraw.Draw(W)
W.paste(on(spr,(200,200,200,255),8),(10,24)); d.text((10,6),'sprite r3, 8x',fill='black')
W.paste(mod8,(540,24)); d.text((540,6),'model (natief, x0,787), 8x',fill='black')
y0=560; x=10
refs=['voltorb','electrode','magnemite','beldum','lunatone']
for col,lab in ((LIGHT,'licht'),(DARK,'donker')):
    for s in (1,2):
        W.paste(on(spr,col,s),(x,y0)); d.text((x,y0-14),f'r3 {s}x {lab}',fill='black'); x+=64*s+12
x=10; y1=y0+150
for n in refs:
    g=rgba(G+n+'/anim_front_gba.png',(0,0,64,64))
    W.paste(on(g,LIGHT,2),(x,y1)); W.paste(on(g,LIGHT,1),(x,y1+136)); d.text((x,y1-14),n+' (gba)',fill='black'); x+=140
W.paste(on(spr,LIGHT,2),(x,y1)); W.paste(on(spr,LIGHT,1),(x,y1+136)); d.text((x,y1-14),'r3',fill='black')
W.convert('RGB').save('vel.png')
