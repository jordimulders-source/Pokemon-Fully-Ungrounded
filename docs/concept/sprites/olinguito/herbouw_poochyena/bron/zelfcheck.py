# Uitsnedes op 8x (kop + per poot), onderlaag (basis | overtekening | resultaat) en compare (1x en 3x).
from PIL import Image, ImageDraw
R='../../../../../../'
res=Image.open('../anim_front.png').convert('RGBA').crop((0,0,64,64))
base=Image.open(R+'graphics/pokemon/poochyena/anim_front.png').convert('RGBA').crop((0,0,64,64))
def bg(im,c=(200,205,215,255)):
    b=Image.new('RGBA',im.size,c); b.alpha_composite(im); return b
def clean(p):
    im=Image.open(p).convert('RGBA')
    if im.size==(64,128): im=im.crop((0,0,64,64))
    px=im.load(); key=im.getpixel((0,0))
    for y in range(im.height):
        for x in range(im.width):
            if px[x,y]==key: px[x,y]=(0,0,0,0)
    return im
res=clean('../anim_front.png'); base=clean(R+'graphics/pokemon/poochyena/anim_front.png')
crops={'kop':(5,14,36,37),'voorpoot_dichtbij':(9,36,28,54),'voorpoot_ver':(22,40,40,55),
       'achterpoot_dichtbij':(38,36,53,52),'achterpoot_ver':(33,37,43,47),'staart':(45,27,62,54)}
for n,b in crops.items():
    c=bg(res.crop(b)); c.resize((c.width*8,c.height*8),Image.NEAREST).save('zelfcheck_%s.png'%n)
# onderlaag: basis | basis vaag + omlijning resultaat | resultaat
def fade(im,a=0.35):
    o=im.copy(); px=o.load()
    for y in range(64):
        for x in range(64):
            r,g,b,al=px[x,y]
            if al: px[x,y]=(int(255-(255-r)*a),int(255-(255-g)*a),int(255-(255-b)*a),255)
    return o
over=fade(base); rp=Image.open('../anim_front.png').crop((0,0,64,64)); op=over.load()
for y in range(64):
    for x in range(64):
        i=rp.getpixel((x,y))
        if i in (1,2): op[x,y]=(200,30,30,255)
        elif i: op[x,y]=(op[x,y][0],op[x,y][1],op[x,y][2],255) if op[x,y][3] else (90,150,230,255)
panels=[bg(base),bg(over),bg(res)]
W=64*3*4+16; on=Image.new('RGBA',(W,256),(255,255,255,255))
for i,p in enumerate(panels): on.paste(p.resize((256,256),Image.NEAREST),(i*(256+8),0))
on.save('../onderlaag.png')
# compare: resultaat, basis, ronde 23, Galar-Linoone op 1x en 3x
refs=[res,base,clean(R+'docs/concept/sprites/olinguito/ronde23/anim_front.png'),clean(R+'docs/concept/sprites/olinguito/referenties/galar_linoone_front.png')]
cw=len(refs)*(64*3+8); cmp=Image.new('RGBA',(cw,64*3+64+12),(200,205,215,255))
for i,p in enumerate(refs):
    cmp.alpha_composite(p,(i*(64+8)+4,4))
    cmp.alpha_composite(p.resize((192,192),Image.NEAREST),(i*(192+8),64+12))
cmp.save('../compare.png')
