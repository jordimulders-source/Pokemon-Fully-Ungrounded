import sys; sys.path.insert(0,'../keuring_r20')
from PIL import Image, ImageDraw
from refs import load
def rgba(p, pal=None):
    im=Image.open(p)
    if pal: im=im.copy(); im.putpalette(pal)
    im.info['transparency']=0
    return im.convert('RGBA')
def lichter(pal):
    pal=list(pal); pal[6:9]=[46,46,52]; pal[9:12]=[74,74,80]; return pal
def on(bg,im,s):
    c=Image.new('RGBA',im.size,bg); c.alpha_composite(im); return c.convert('RGB').resize((im.width*s,im.height*s),Image.NEAREST)
if __name__=='__main__':
    base=Image.open('vlieg_r24.png'); P=base.getpalette()[:48]
    r24=rgba('vlieg_r24.png'); r24l=rgba('vlieg_r24.png',lichter(P)); r23=rgba('../sprite_r23/vlieg_r23_L12.png')
    W=(255,255,255,255)
    # vergelijk 1: r23 | r24 | r24 lichter op 8x
    c=Image.new('RGB',(3*520,560),'white'); d=ImageDraw.Draw(c)
    for i,(n,im) in enumerate((('r23',r23),('r24',r24),('r24 lichter',r24l))):
        c.paste(on(W,im,8),(i*520,40)); d.text((i*520+10,10),n,fill=(0,0,0))
    c.save('vergelijk_r23_r24.png')
    # outputs
    on(W,r24,8).save('vlieg_r24_8x.png')
    li=base.copy(); li.putpalette(lichter(P)+[0]*(768-48)); li.save('vlieg_r24_lichter.png',transparency=0)
    on(W,r24l,8).save('vlieg_r24_lichter_8x.png')
    # vel
    kr=Image.open('../sprite_r23/krabbel_jordi_r23.png').convert('RGB')
    zones=[('kop-bovenrand',9,17,26,28),('vizier',16,25,28,37),('naad + strepen + rand',30,27,55,47),('poten',13,43,37,58)]
    S=12
    zw=[(x1-x0)*S for _,x0,y0,x1,y1 in zones]; zh=max((y1-y0)*S for _,x0,y0,x1,y1 in zones)
    Wd=max(580+2*530, sum(2*w+40 for w in zw[:2])+ 2*zw[2]+40)
    H=40+530+30+zh+40+zh+30+300+30+540
    c=Image.new('RGB',(max(Wd,2*(zw[2]+zw[3])+120),H),'white'); d=ImageDraw.Draw(c)
    y=10; d.text((10,y),'r23 met krabbel Jordi  |  r24  |  r24 lichter (index 2 -> 46,46,52; 3 -> 74,74,80)',fill=(0,0,0)); y+=20
    c.paste(kr,(10,y+10)); c.paste(on(W,r24,8).crop((0,96,512,512)).resize((512,416)) if False else on(W,r24,8).crop((0,112,512,512)),(600,y)); c.paste(on(W,r24l,8).crop((0,112,512,512)),(1130,y))
    y+=540
    def zoomcol(im,z):
        n,x0,y0,x1,y1=z; return on(W,im.crop((x0,y0,x1,y1)),S)
    x=10
    for i,z in enumerate(zones[:2]):
        d.text((x,y),z[0]+': r23 | r24',fill=(0,0,0)); a=zoomcol(r23,z); b=zoomcol(r24,z)
        c.paste(a,(x,y+15)); c.paste(b,(x+a.width+10,y+15)); x+=2*a.width+40
    y+=zh+30; x=10
    for z in zones[2:]:
        d.text((x,y),z[0]+': r23 | r24',fill=(0,0,0)); a=zoomcol(r23,z); b=zoomcol(r24,z)
        c.paste(a,(x,y+15)); c.paste(b,(x+a.width+10,y+15)); x+=2*a.width+40
    y+=zh+30
    # 1x en 2x licht/donker naast Gen 3
    refs=[('ninjask',load('ninjask')),('umbreon',load('umbreon')),('volbeat',load('volbeat')),('beldum',load('beldum'))]
    items=[('r24',r24),('r24 lichter',r24l)]+refs
    for bg,yy in (((255,255,255,255),y),((40,40,48,255),y+150)):
        x=10
        for n,im in items:
            c.paste(on(bg,im,1),(x,yy+10)); c.paste(on(bg,im,2),(x+70,yy+10)); x+=210
    d.text((10,y-12),'1x en 2x op licht en donker: r24, r24 lichter, ninjask, umbreon, volbeat, beldum',fill=(0,0,0))
    y+=310
    d.text((10,y),'8x (4x getoond): r24 | ninjask | volbeat | beldum | umbreon',fill=(0,0,0))
    x=10
    for n,im in [('r24',r24)]+refs[:1]+refs[2:]+refs[1:2]:
        c.paste(on(W,im,4),(x,y+15)); x+=262
    c.save('vel.png')
    # aparte 8x-vergelijking met refs
    c2=Image.new('RGB',(5*520,530),'white')
    for i,(n,im) in enumerate([('r24',r24),('ninjask',refs[0][1]),('volbeat',refs[2][1]),('beldum',refs[3][1]),('umbreon',refs[1][1])]):
        c2.paste(on(W,im,8),(i*520,10))
    c2.save('refs8x.png')
