import os
from PIL import Image, ImageDraw
D='/home/user/Pokemon-Fully-Ungrounded/docs/concept/sprites/sneeuwbolslak/sprite/maker/'
G='/home/user/Pokemon-Fully-Ungrounded/graphics/pokemon/'
# bron-uitsnede (x0,y0,x1,y1) rond het overgenomen oog
bron={'magcargo':(12,11,28,24),'surskit':(18,22,36,31),'gastrodon':(10,15,30,24),'sliggoo':(15,17,33,28)}
rows=[('r2 (referentie)',D+'r2.png',None)]+[(n,D+f'ogen_{n}.png',n) for n in bron]
def rgba(p):
    im=Image.open(p); im.save('/tmp/claude-0/-home-user-Pokemon-Fully-Ungrounded/ad999ca8-c13b-5eae-9ff1-b8b2864b5586/scratchpad/_t.png',transparency=im.info.get('transparency',0))
    return Image.open('/tmp/claude-0/-home-user-Pokemon-Fully-Ungrounded/ad999ca8-c13b-5eae-9ff1-b8b2864b5586/scratchpad/_t.png').convert('RGBA')
RH=272; v=Image.new('RGBA',(256+12+14*12*1+12+16*0+170+12+260,RH*len(rows)),(255,255,255,255))
W=256+12+180+12+150+12+16*12+10; v=Image.new('RGBA',(W,RH*len(rows)),(255,255,255,255)); dr=ImageDraw.Draw(v)
for k,(lab,p,n) in enumerate(rows):
    y=k*RH; im=rgba(p)
    t=Image.new('RGBA',(64,64),(255,255,255,255)); t.alpha_composite(im); v.paste(t.resize((256,256),Image.NEAREST),(0,y+12))
    kop=t.crop((8,29,23,40)).resize((15*12,11*12),Image.NEAREST); v.paste(kop,(268,y+12))
    for kk,bg in enumerate(((248,248,248,255),(40,40,48,255))):
        tt=Image.new('RGBA',(64,64),bg); tt.alpha_composite(im); v.paste(tt,(268+kk*72,y+150))
    if n:
        f=G+n+'/anim_front_gba.png'
        if not os.path.exists(f): f=G+n+'/anim_front.png'
        s=Image.open(f); s=s.convert('RGBA'); px=s.load(); bg=px[0,0]
        for yy in range(s.size[1]):
            for xx in range(s.size[0]):
                if px[xx,yy]==bg: px[xx,yy]=(255,255,255,255)
        b=bron[n]; c=s.crop(b); sc=12 if (b[2]-b[0])<=16 else 10
        v.paste(c.resize((c.width*sc,c.height*sc),Image.NEAREST),(268+180+12,y+12))
        v.paste(s.crop((0,0,64,64)),(268+180+12,y+12+c.height*sc+6))
    dr.text((4,y+1),lab,fill=(0,0,0,255))
v.save(D+'vel_ogen.png'); print(v.size)
