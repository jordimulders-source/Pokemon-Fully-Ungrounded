# Hulpfuncties: Hitmontop inlezen, rasters plakken, png/vel schrijven.
import os
from PIL import Image, ImageDraw
ROOT=os.path.abspath(os.path.join(os.path.dirname(__file__),'../../../../..'))
HERE=os.path.dirname(os.path.abspath(__file__))
HT_PNG=os.path.join(ROOT,'graphics/pokemon/hitmontop/anim_front.png')
def load_pal(path=os.path.join(HERE,'normal.pal')):
    L=open(path).read().split('\n')[3:19]
    return [tuple(map(int,l.split())) for l in L]
PAL=load_pal()
def ht():
    im=Image.open(HT_PNG); p=im.load()
    return [[p[x,y] for x in range(64)] for y in range(64)]
def copy(g): return [r[:] for r in g]
def blank(): return [[0]*64 for _ in range(64)]
def move(g, box, dx, dy, keep=None, clear=True):
    """verplaats alle pixels in box (x0,y0,x1,y1 incl.) die keep(x,y,v) waar maken"""
    x0,y0,x1,y1=box; pts=[]
    for y in range(y0,y1+1):
        for x in range(x0,x1+1):
            v=g[y][x]
            if v and (keep is None or keep(x,y,v)): pts.append((x,y,v))
    if clear:
        for x,y,v in pts: g[y][x]=0
    for x,y,v in pts:
        if 0<=x+dx<64 and 0<=y+dy<64: g[y+dy][x+dx]=v
def txt(g, x0, y0, rows):
    """'.'/' ' = laten staan, '_' = transparant, 0-F = index"""
    for j,r in enumerate(rows):
        for i,c in enumerate(r):
            if c in '. ': continue
            v=0 if c=='_' else int(c,16)
            g[y0+j][x0+i]=v
def clear_box(g,x0,y0,x1,y1):
    for y in range(y0,y1+1):
        for x in range(x0,x1+1): g[y][x]=0
def save(g, path):
    im=Image.new('P',(64,64)); flat=[]
    for c in PAL: flat+=list(c)
    im.putpalette(flat+[0]*(768-len(flat)))
    im.putdata([v for r in g for v in r]); im.info['transparency']=0
    im.save(path, transparency=0)
def rgba(g):
    im=Image.new('RGBA',(64,64))
    im.putdata([PAL[v]+(255,) for r in g for v in r]); return im
def dump(g):
    return '\n'.join('%2d '%y+''.join('%X'%v if v else '.' for v in r) for y,r in enumerate(g))
def kept(g, base):
    """% van Hitmontops niet-transparante pixels dat op dezelfde plek of verschoven nog gelijk is: hier gewoon op plek gemeten"""
    n=s=0
    for y in range(64):
        for x in range(64):
            if base[y][x]:
                n+=1; s+= g[y][x]==base[y][x]
    return 100*s/n
def vel(items, path, z=8):
    """items: lijst (titel, RGBA-image 64x64 of ander)"""
    pad=10; ims=[]
    for t,im in items:
        if im.size==(64,64): im=im.resize((64*z,64*z),Image.NEAREST)
        ims.append((t,im))
    W=sum(i.width for _,i in ims)+pad*(len(ims)+1); H=max(i.height for _,i in ims)+40
    c=Image.new('RGBA',(W,H),(255,255,255,255)); d=ImageDraw.Draw(c); x=pad
    for t,im in ims:
        c.paste(im,(x,30),im if im.mode=='RGBA' else None); d.text((x,8),t,fill=(0,0,0)); x+=im.width+pad
    c.save(path)

def capsule_mask(pts, radii):
    """ruwe vorm (alleen silhouet) van een ledemaat: polyline met straal per punt"""
    import math
    m=set()
    for k in range(len(pts)-1):
        (ax,ay),(bx,by)=pts[k],pts[k+1]; ra,rb=radii[k],radii[k+1]
        L=max(1e-6,math.hypot(bx-ax,by-ay))
        for y in range(64):
            for x in range(64):
                px,py=x+.5,y+.5
                t=max(0,min(1,((px-ax)*(bx-ax)+(py-ay)*(by-ay))/L/L))
                cx,cy=ax+t*(bx-ax),ay+t*(by-ay); r=ra+t*(rb-ra)
                if math.hypot(px-cx,py-cy)<=r: m.add((x,y))
    return m

def ellipse_mask(cx,cy,rx,ry):
    return {(x,y) for y in range(64) for x in range(64) if ((x+.5-cx)/rx)**2+((y+.5-cy)/ry)**2<=1}

TWIST3=["344","345","453","534"]   # gedraaide lok: donkere streep (5) loopt schuin, zoals Hitmontops randstrepen
TWIST2=["34","45","53","44"]
def lock(g, xl, y0, y1, w=3, phase=0, left=5, right=15, sway=None):
    """een hangende lok: buitenlijn links (lichtkant: 5) en rechts (F), binnen een draaipatroon; ronde punt onderaan"""
    pat=TWIST3 if w==3 else TWIST2
    for k,y in enumerate(range(y0,y1+1)):
        x=xl+(sway(k) if sway else 0)
        inner=pat[(k+phase)%4]
        if y==y1:   row='.'+'F'*w+'.'
        elif y==y1-1: row='%X'%left+inner[:w-1]+'4'+'F' if w==3 else '%X'%left+inner+'F'
        else:       row='%X'%left+inner+'%X'%right
        txt(g,x,y,[row])
