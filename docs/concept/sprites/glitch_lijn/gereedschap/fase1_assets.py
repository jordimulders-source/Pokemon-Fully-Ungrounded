"""Fase 1 (Jordi, 25 nov): "minder blur en meer duidelijk assets uit de game die dan half of
gedeeltelijk erin zitten"; dichtheid het grootst in het midden; vaag 2 ogen en een mond.
Brokken: echte kaartstukken (kaartbrok.py), menu/interface-graphics, een paar datastroken
(ROM-bytes als 4bpp). Half: elk brok wordt afgesneden of in banen verschoven. Geen pixelruis.
Gebruik: python3 fase1_assets.py ROM UITMAP"""
import sys, os, random, math, glob
from PIL import Image
sys.path.insert(0,os.path.dirname(__file__))
import kaartbrok
from gen3_afmeting import lees
REPO=kaartbrok.REPO
rom=open(sys.argv[1],'rb').read(); uit=sys.argv[2]; os.makedirs(uit,exist_ok=True)
UI=glob.glob(os.path.join(REPO,'graphics/interface/*.png'))+glob.glob(os.path.join(REPO,'graphics/text_window/*.png'))+glob.glob(os.path.join(REPO,'graphics/battle_interface/*.png'))
def ui(r,maxw,maxh):
    for _ in range(30):
        im=Image.open(r.choice(UI))
        if im.mode=='P':
            pal=im.getpalette(); src=im; im=Image.new('RGBA',src.size,(0,0,0,0)); a,b=src.load(),im.load()
            for y in range(src.size[1]):
                for x in range(src.size[0]):
                    v=a[x,y]
                    if v: b[x,y]=tuple(pal[v*3:v*3+3])+(255,)
        else: im=im.convert('RGBA')
        w,h=min(maxw,im.size[0]),min(maxh,im.size[1])
        x,y=r.randrange(0,im.size[0]-w+1),r.randrange(0,im.size[1]-h+1)
        c=im.crop((x,y,x+w,y+h))
        if sum(1 for p in c.getdata() if p[3])>w*h*0.3: return c
    return kaartbrok.brok(r,1,1)
def data(r,w,h):
    d=rom[r.randrange(0,len(rom)-4096)//4*4:][:2048]
    pal=[(0,0,0)]+[tuple(r.randrange(0,256) for _ in range(3)) for _ in range(3)]*5
    return lees(d,pal,8,0).crop((0,0,w,h))
def half(r,b):
    w,h=b.size; k=r.choice(['snij','snij','banen','hoek'])
    if k=='snij':
        x0,y0=r.randrange(0,w//2+1),r.randrange(0,h//2+1); x1,y1=r.randrange(x0+w//3,w+1),r.randrange(y0+h//3,h+1)
        return b.crop((x0,y0,max(x1,x0+4),max(y1,y0+4)))
    if k=='banen':
        o=Image.new('RGBA',(w+8,h),(0,0,0,0)); bh=r.choice([2,4,8])
        for y in range(0,h,bh): o.alpha_composite(b.crop((0,y,w,y+bh)),(r.choice([0,2,4,6,8]),y))
        return o
    m=Image.new('L',(w,h),0); px=m.load(); s=r.choice([1,-1])
    for y in range(h):
        for x in range(w):
            if (x+y*s*1.0)<w*0.9+(r.random()*3): px[x,y]=255
    o=Image.new('RGBA',(w,h),(0,0,0,0)); o.paste(b,(0,0),m); return o
def maak(seed,dicht=55):
    r=random.Random(seed); out=Image.new('RGBA',(64,64),(0,0,0,0)); cx,cy=32,33
    lagen=[]
    for k in range(dicht):
        x=r.gauss(cx,8.5); y=r.gauss(cy,8); d=math.hypot(x-cx,y-cy)
        soort=r.choices(['kaart','ui','data'],[0.6,0.28,0.12])[0]
        if soort=='kaart': b=kaartbrok.brok(r,*(r.choice([(1,1),(2,1),(1,2),(2,2)]) if d<12 else r.choice([(1,1),(1,1),(2,1)])))
        elif soort=='ui': b=ui(r,r.choice([16,24,32]),r.choice([8,16]))
        else: b=data(r,r.choice([16,24,32]),r.choice([2,3,4]))
        b=half(r,b)
        if d>14: b=b.crop((0,0,max(3,b.size[0]//2),max(3,b.size[1]//2)))
        lagen.append((d,b,int(x-b.size[0]/2),int(y-b.size[1]/2)))
    for d,b,x,y in sorted(lagen,key=lambda t:-t[0]):
        out.alpha_composite(b,(max(0,min(64-b.size[0],x)),max(0,min(64-b.size[1],y))) if b.size[0]<=64 and b.size[1]<=64 else (0,0))
    for _ in range(3):  # glitch: verschoven banen
        y0=r.randrange(12,52); hh=r.choice([2,3,4,6]); dx=r.choice([-6,-4,4,6])
        band=out.crop((0,y0,64,y0+hh)); out.paste((0,0,0,0),(0,y0,64,y0+hh)); sh=Image.new('RGBA',(64,64),(0,0,0,0)); sh.paste(band,(dx,y0)); out.alpha_composite(sh)
    px=out.load()
    for y in range(64):   # vaag gezicht: holtes in de kern
        for x in range(64):
            f=False
            for ex,ey,sg in ((25,29,1),(39,28,-1)):
                ddx,ddy=(x-ex)*sg,(y-ey)
                if (ddx/4.5)**2+((ddy+ddx*0.4)/2.2)**2<1: f=True
            if abs(x-32)<9 and abs(y-(40+2.2*math.sin((x-32)/1.7)))<1.2: f=True
            if f and r.random()<0.85: px[x,y]=(0,0,0,0)
    al=out.getchannel('A'); q=out.convert('RGB').quantize(colors=15,method=Image.Quantize.MEDIANCUT).convert('RGBA'); q.putalpha(al)
    return q
ims=[maak(s) for s in range(1,11)]
shh=Image.new('RGB',(5*68+4,2*68+4),(255,255,255))
for i,im in enumerate(ims): shh.paste(im,(4+(i%5)*68,4+(i//5)*68),im); im.save(f'{uit}/a{i+1:02d}.png')
shh.resize((shh.size[0]*3,shh.size[1]*3),Image.NEAREST).save(f'{uit}/vel.png')
