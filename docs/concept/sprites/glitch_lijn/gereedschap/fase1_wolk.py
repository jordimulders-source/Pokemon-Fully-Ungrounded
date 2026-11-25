"""Fase 1 volgens Jordi (25 nov): dichtheid het grootst in het midden (zoals de gaswolk van de
Gen 1-Gastly), glitchy, opgebouwd uit verschillende soorten assets (zoals MissingNo: data die
geen plaatje is), en daaruit komen heel vaag 2 ogen en een mond die creepy lijken.
Rommel: brokjes uit kaarttegels (tilesets), trainerdata en willekeurige ROM-data uit Ungrounded
1.0, Gengar +13; alles teruggebracht naar 4 grijstinten (palet beperkt zoals MissingNo/Gastly).
Gezicht: geen getekende lijnen, alleen een dichtheidsverschil in de wolk (gaten of klonten).
Gebruik: python3 fase1_wolk.py ROM UITMAP"""
import sys, os, random, math, glob
from PIL import Image, ImageDraw
sys.path.insert(0,os.path.dirname(__file__))
from gen3_missingno import REPO
from gen3_afmeting import tiles4bpp, lees
from gen3_tileset import bytes4, jasc
rom=open(sys.argv[1],'rb').read(); uit=sys.argv[2]; os.makedirs(uit,exist_ok=True)
GRIJS=[(0,0,0,0),(248,248,248,255),(168,168,168,255),(88,88,88,255),(16,16,16,255)]
grijspal=[(0,0,0)]+[(i*16,i*16,i*16) for i in range(1,16)]
def toon(p):  # kleur -> 1..4 (licht..donker)
    l=(p[0]*30+p[1]*59+p[2]*11)/100
    return 1 if l>200 else 2 if l>140 else 3 if l>70 else 4
TPALS=[jasc(p) for p in sorted(glob.glob(os.path.join(REPO,'data/tilesets/*/*/palettes/0[0-5].pal')))[:300]]
sets=[p for p in glob.glob(os.path.join(REPO,'data/tilesets/*/*/tiles.png')) if Image.open(p).mode=='P']
gdata,_=tiles4bpp(os.path.join(REPO,'graphics/pokemon/gengar/anim_front_gba.png'))
from gen3_tileset import jasc
from gen3_afmeting import tiles4bpp as _t4
_, GENGARPAL = _t4(os.path.join(REPO,'graphics/pokemon/gengar/anim_front_gba.png'))
KLEUR=False
def bronbeeld(r):
    k=r.choice(['tileset','tileset','trainer','rom','gengar'])
    pal=grijspal
    if KLEUR:
        if k=='tileset': pass
        elif k=='gengar': pal=GENGARPAL
        else: pal=r.choice(TPALS)
    if k=='tileset':
        ts=r.choice(sets); d=bytes4(ts); st=r.randrange(0,max(1,len(d)-2048))//32*32; d=d[st:st+2048]
        if KLEUR:
            pp=sorted(glob.glob(os.path.join(os.path.dirname(ts),'palettes/0[0-9].pal')))
            pal=jasc(r.choice(pp)) if pp else r.choice(TPALS)
    elif k=='trainer': d=rom[0x651000+r.randrange(0,0x5000):][:2048]
    elif k=='rom': d=rom[r.randrange(0,len(rom)-4096)//4*4:][:2048]
    else: d=gdata; 
    return lees(d,pal,r.choice([8,7,9]),13 if k=='gengar' else r.choice([0,5,13]))
BAYER=[[0,8,2,10],[12,4,14,6],[3,11,1,9],[15,7,13,5]]
def wolk(seed,straal=26,stijl='licht',kern=0.45,vaag=0.5):
    """Kern vol (brokken blijven heel, assets zichtbaar), daarbuiten Bayer-dither zoals Gen 1-Gastly;
    toon donkerder naar het midden. Gezicht = lichte, half geditherde gaten in de donkere kern."""
    r=random.Random(seed); bronnen=[bronbeeld(r) for _ in range(7)]
    veld=[[0]*64 for _ in range(64)]
    for _ in range(140):
        b=r.choice(bronnen).load(); w,h=r.choice([(8,8),(16,4),(8,2),(12,6),(4,12),(16,8),(6,6)])
        sx,sy=r.randrange(0,64-w),r.randrange(0,64-h); dx,dy=r.randrange(4,60-w),r.randrange(4,60-h)
        for y in range(h):
            for x in range(w):
                q=b[sx+x,sy+y]
                if q[3]: veld[dy+y][dx+x]=q if KLEUR else toon(q)
    cx,cy=32,33; out=Image.new('RGBA',(64,64),(0,0,0,0)); po=out.load()
    ogen=[(24,29,1.0),(40,28,-1.0)]; mx,my=32,41
    for y in range(64):
        for x in range(64):
            a=math.atan2(y-cy,x-cx); rr=straal*(1+0.13*math.sin(3*a+seed)+0.08*math.sin(7*a+seed))
            d=math.hypot(x-cx,y-cy)/rr
            p=1.0 if d<kern else max(0.0,1-(d-kern)/(1-kern))**1.3
            if p*16<=BAYER[y%4][x%4]+r.random()*3: continue
            if KLEUR:
                c=veld[y][x]
                if not c: continue
                f=False
                for ex,ey,sg in ogen:
                    ddx,ddy=(x-ex)*sg,(y-ey)
                    if (ddx/5.0)**2+((ddy+ddx*0.4)/2.4)**2<1: f=True
                if abs(x-mx)<10 and abs(y-(my+2.5*math.sin((x-mx)/1.8)))<1.3: f=True
                if f and r.random()<vaag: continue
                if not f and d<kern+0.15 and r.random()<0.5: c=tuple(int(v*0.55) for v in c[:3])+(255,)
                po[x,y]=c; continue
            v=veld[y][x] or r.choice([2,3,3,4])
            # donkerder naar het midden
            if d<kern+0.15: v=max(v,3) if r.random()<0.75 else v
            elif d>0.8: v=min(v,2) if r.random()<0.6 else v
            f=False
            for ex,ey,sg in ogen:
                ddx,ddy=(x-ex)*sg,(y-ey)
                if (ddx/5.0)**2+((ddy+ddx*0.4)/2.4)**2<1: f=True
            if abs(x-mx)<10 and abs(y-(my+2.5*math.sin((x-mx)/1.8)))<1.3: f=True
            if f:
                if r.random()<vaag: continue          # gat (wit)
                v=1 if stijl=='licht' else 2           # of lichte rommel
            po[x,y]=GRIJS[v]
    return out
vars=[(s,st,rad) for s in (1,2,3,4) for st in ('licht',) for rad in (24,28)]+[(5,'grijs',26),(6,'grijs',26)]
if len(sys.argv)>3 and sys.argv[3]=='kleur':
    KLEUR=True; vars=[(s,'licht',rad) for s in (3,4,7,8,9) for rad in (24,28)]
sh=Image.new('RGB',(len(vars)*68+4,72),(255,255,255))
for i,(s,st,rad) in enumerate(vars):
    im=wolk(s,rad,st)
    if KLEUR:  # Gen 3: max 15 kleuren + doorzichtig
        al=im.getchannel('A'); q=im.convert('RGB').quantize(colors=15).convert('RGB'); im=q.convert('RGBA'); im.putalpha(al)
    sh.paste(im,(4+i*68,4),im); im.save(f'{uit}/w{i+1:02d}_{st}_{rad}_s{s}.png')
sh.resize((sh.size[0]*3,sh.size[1]*3),Image.NEAREST).save(f'{uit}/vel.png')
