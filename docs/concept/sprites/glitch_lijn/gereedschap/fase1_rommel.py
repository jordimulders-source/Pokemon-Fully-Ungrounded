"""Fase 1, ronde na Jordi (25 nov): "meer kleur", "duidelijk ook dingen als map assets, menu
dingen, data", "nu is het meer een geest dan echt een glitch".
Collage van HERKENBARE game-assets in hun eigen kleuren (kaarttegels, menu/interface, tekstvenster,
statusiconen, lettertype) + rommeldata (ROM-bytes als 4bpp met een verkeerd palet), op elkaar
gestapeld: dichtst in het midden (brokken vallen vaker en groter in het midden), losse kleine
brokjes eromheen. Glitchy: horizontaal verschoven banen, herhaalde brokken. Geen gaswolk-dither.
Gezicht: vaag, als lege plekken (ogen, mond) in de dichte kern.
Gebruik: python3 fase1_rommel.py ROM UITMAP"""
import sys, os, random, math, glob
from PIL import Image
sys.path.insert(0,os.path.dirname(__file__))
from gen3_missingno import REPO
from gen3_afmeting import lees
from gen3_tileset import bytes4, jasc
rom=open(sys.argv[1],'rb').read(); uit=sys.argv[2]; os.makedirs(uit,exist_ok=True)
def rgba(im):
    im=im.convert('RGBA'); px=im.load(); w,h=im.size
    # kleur 0 / magenta / wit-achtige achtergrond doorzichtig
    if im.mode=='RGBA': pass
    return im
def tileset_beelden():
    out=[]
    for d in glob.glob(os.path.join(REPO,'data/tilesets/*/*')):
        t=os.path.join(d,'tiles.png'); pp=sorted(glob.glob(os.path.join(d,'palettes/0[0-9].pal')))
        if not os.path.exists(t) or not pp: continue
        im=Image.open(t)
        if im.mode!='P': continue
        out.append((im,pp))
    return out
TS=tileset_beelden()
def ts_brok(r,w,h):
    im,pp=r.choice(TS); pal=jasc(r.choice(pp)); W,H=im.size
    x,y=r.randrange(0,W-w)//8*8 if W>w else 0, r.randrange(0,H-h)//8*8 if H>h else 0
    c=im.crop((x,y,x+w,y+h)); o=Image.new('RGBA',(w,h),(0,0,0,0)); px,po=c.load(),o.load()
    for j in range(h):
        for i in range(w):
            v=px[i,j]&0xF
            if v: po[i,j]=pal[v]+(255,)
    return o
UI=[p for p in glob.glob(os.path.join(REPO,'graphics/interface/*.png'))+glob.glob(os.path.join(REPO,'graphics/text_window/*.png'))+glob.glob(os.path.join(REPO,'graphics/fonts/*.png'))]
def ui_brok(r,w,h):
    for _ in range(20):
        im=Image.open(r.choice(UI))
        if im.size[0]<w or im.size[1]<h: continue
        if im.mode=='P':
            pal=im.getpalette(); px=im.load(); o=Image.new('RGBA',(w,h),(0,0,0,0)); po=o.load()
            x,y=r.randrange(0,im.size[0]-w+1),r.randrange(0,im.size[1]-h+1)
            for j in range(h):
                for i in range(w):
                    v=px[x+i,y+j]
                    if v: po[i,j]=tuple(pal[v*3:v*3+3])+(255,)
            if sum(1 for p in o.getdata() if p[3])>w*h*0.2: return o
        else:
            x,y=r.randrange(0,im.size[0]-w+1),r.randrange(0,im.size[1]-h+1)
            o=im.convert('RGBA').crop((x,y,x+w,y+h)); return o
    return ts_brok(r,w,h)
def data_brok(r,w,h):
    im,pp=r.choice(TS); pal=[(0,0,0)]+jasc(r.choice(pp))[1:]
    d=rom[r.randrange(0,len(rom)-4096)//4*4:][:2048]
    big=lees(d,pal,8,0); x,y=r.randrange(0,64-w+1),r.randrange(0,64-h+1)
    return big.crop((x,y,x+w,y+h))
def rommel(seed,sigma=9.0,n=70,kernvul=0):
    r=random.Random(seed); out=Image.new('RGBA',(64,64),(0,0,0,0)); cx,cy=32,33
    for k in range(n):
        x=int(r.gauss(cx,sigma)); y=int(r.gauss(cy,sigma*0.9))
        d=math.hypot(x-cx,y-cy)
        if d<12: w,h=r.choice([(16,8),(8,16),(16,16),(24,8),(8,8)])
        elif d<20: w,h=r.choice([(8,8),(16,4),(8,4),(4,8)])
        else: w,h=r.choice([(4,4),(2,2),(4,2),(3,1),(6,2)])
        soort=r.choices(['ts','ui','data'],[0.45,0.3,0.25])[0]
        b={'ts':ts_brok,'ui':ui_brok,'data':data_brok}[soort](r,w,h)
        out.alpha_composite(b,(max(0,min(64-w,x-w//2)),max(0,min(64-h,y-h//2))))
    # extra dichtheid: kern opvullen met brokken tot hij (bijna) dicht is
    for k in range(kernvul):
        x=int(r.gauss(cx,sigma*0.6)); y=int(r.gauss(cy,sigma*0.55)); w,h=r.choice([(8,8),(16,8),(8,16),(12,12)])
        soort=r.choices(['ts','ui','data'],[0.45,0.3,0.25])[0]
        b={'ts':ts_brok,'ui':ui_brok,'data':data_brok}[soort](r,w,h)
        tmp=Image.new('RGBA',(64,64),(0,0,0,0)); tmp.alpha_composite(b,(max(0,min(64-w,x-w//2)),max(0,min(64-h,y-h//2))))
        tmp.alpha_composite(out); out=tmp   # onder de bestaande laag: vult alleen de gaten
    # glitch: banen verschuiven en een brok herhalen
    for _ in range(3):
        y0=r.randrange(14,50); hh=r.choice([1,2,3,4]); dx=r.choice([-6,-4,-3,3,4,6])
        band=out.crop((0,y0,64,y0+hh)); out.paste((0,0,0,0),(0,y0,64,y0+hh)); out.alpha_composite(band,(max(0,dx),y0),(max(0,-dx),0))
    br=out.crop((24,24,40,32)); out.alpha_composite(br,(r.choice([8,40]),r.choice([20,36])))
    # vaag gezicht: lege plekken in de kern
    px=out.load()
    for y in range(64):
        for x in range(64):
            f=False
            for ex,ey,sg in ((25,29,1),(39,28,-1)):
                ddx,ddy=(x-ex)*sg,(y-ey)
                if (ddx/4.5)**2+((ddy+ddx*0.4)/2.2)**2<1: f=True
            if abs(x-32)<9 and abs(y-(40+2.2*math.sin((x-32)/1.7)))<1.2: f=True
            if f and r.random()<0.8: px[x,y]=(0,0,0,0)
    al=out.getchannel('A'); q=out.convert('RGB').quantize(colors=15).convert('RGBA'); q.putalpha(al)
    return q
ims=[rommel(s,9.5,140,90) for s in range(1,11)]
sh=Image.new('RGB',(5*68+4,2*68+4),(255,255,255))
for i,im in enumerate(ims): sh.paste(im,(4+(i%5)*68,4+(i//5)*68),im); im.save(f'{uit}/r{i+1:02d}.png')
sh.resize((sh.size[0]*3,sh.size[1]*3),Image.NEAREST).save(f'{uit}/vel.png')
