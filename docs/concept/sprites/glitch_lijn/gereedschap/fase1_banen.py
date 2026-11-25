"""Fase 1 (Jordi, 25 nov): "hij moet niet creepy zijn, plus het mag iets natuurlijker voelen als
assets die niet helemaal goed aansluiten door het geglitch allemaal, plus de mappen mogen nog iets
vager en onduidelijker gepixeld zijn, nog iets meer missingno".
Opbouw: een paar echte kaartstukken (kaartbrok.py) als bronvlakken; de sprite is een stapel
horizontale banen van wisselende hoogte, elke baan uit een bron met een kleine verschuiving
(stukken lopen door maar sluiten net niet aan). Kaarten grover gepixeld (2x2-cellen) en per stuk
teruggebracht naar weinig tinten. Dichtst in het midden: banen zijn daar breed, aan de rand kort
en onderbroken. Gezicht: neutraal en vaag (2 kleine donkere vlekjes, korte streep), niet creepy.
Gebruik: python3 fase1_banen.py ROM UITMAP"""
import sys, os, random, math
from PIL import Image
sys.path.insert(0,os.path.dirname(__file__))
import kaartbrok
from gen3_afmeting import lees
rom=open(sys.argv[1],'rb').read(); uit=sys.argv[2]; os.makedirs(uit,exist_ok=True)
def grof(im,tinten=4):
    a=im.getchannel('A'); w,h=im.size
    s=im.resize((max(1,w//2),max(1,h//2)),Image.NEAREST).resize((w,h),Image.NEAREST)
    a=a.resize((max(1,w//2),max(1,h//2)),Image.NEAREST).resize((w,h),Image.NEAREST)
    q=s.convert('RGB').quantize(colors=tinten).convert('RGBA'); q.putalpha(a); return q
def bron(r):
    b=kaartbrok.brok(r,4,4)     # 64x64 stuk kaart
    return grof(b,r.choice([5,6,7])) if r.random()<0.7 else b
def databron(r):
    d=rom[r.randrange(0,len(rom)-4096)//4*4:][:2048]
    pal=[(0,0,0)]+[tuple(r.randrange(40,230) for _ in range(3)) for _ in range(3)]*5
    return grof(lees(d,pal,8,0),3)
def maak(seed):
    r=random.Random(seed); bronnen=[bron(r) for _ in range(6)]+[databron(r),databron(r)]
    out=Image.new('RGBA',(64,64),(0,0,0,0)); cx,cy=32,33
    y=6+r.randrange(0,4); cur=r.choice(bronnen); dx=0
    while y<60:
        h=r.choice([2,2,3,4,4,6,8,8])
        if r.random()<0.55: cur=r.choice(bronnen)
        dx+=r.choice([-8,-4,-2,0,2,4,8])
        dy=abs(y+h/2-cy)/26.0
        if dy>=1: y+=h; continue
        half=26*math.sqrt(1-dy*dy)*(0.85+0.3*r.random())
        x0,x1=int(cx-half+r.randrange(-3,4)),int(cx+half+r.randrange(-3,4))
        # aan de rand: baan onderbroken
        if dy<0.55 and r.random()<0.5:
            m=r.randrange(x0+6,x1-5) if x1-x0>12 else x0
            segs=[(x0,m),(m,x1)]
        else: segs=[(x0,x1)]
        if dy>=0.55: segs= [(a,min(x1,a+r.randrange(3,10))) for a in range(x0,x1,r.randrange(6,14)) if r.random()<0.7]
        for a,b in segs:
            a,b=max(0,a),min(64,b)
            if b<=a: continue
            src=cur if (a,b)==segs[0] else r.choice(bronnen)
            sx=(a+dx)%48
            stuk=src.crop((sx,y%60,sx+(b-a),y%60+h))
            out.alpha_composite(stuk,(a,y))
        y+=h
    # neutraal, vaag gezicht: twee kleine donkere vlekjes en een korte streep
    px=out.load(); donker=(40,40,48,255)
    for ex,ey in ((26,30),(38,30)):
        for yy in range(ey-2,ey+2):
            for xx in range(ex-1,ex+2):
                if px[xx,yy][3] and r.random()<0.7: px[xx,yy]=donker
    for xx in range(29,36):
        if px[xx,39][3] and r.random()<0.6: px[xx,39]=donker
    al=out.getchannel('A'); q=out.convert('RGB').quantize(colors=15,method=Image.Quantize.MEDIANCUT).convert('RGBA'); q.putalpha(al)
    return q
ims=[maak(s) for s in range(1,11)]
sh=Image.new('RGB',(5*68+4,2*68+4),(255,255,255))
for i,im in enumerate(ims): sh.paste(im,(4+(i%5)*68,4+(i//5)*68),im); im.save(f'{uit}/b{i+1:02d}.png')
sh.resize((sh.size[0]*3,sh.size[1]*3),Image.NEAREST).save(f'{uit}/vel.png')
