# Schetsen ronde 2: varianten van de zoutkegel (keuzes ronde 1: korst, pekelzak, half oog, kuif): concepten op de echte Silicobra-sprite (geen eindwerk).
import math, sys
from PIL import Image, ImageDraw
SRC='graphics/pokemon/silicobra/anim_front.png'
OUT=sys.argv[1]
src=Image.open(SRC); g0=[list(src.get_flattened_data())[y*64:(y+1)*64] for y in range(64)]
C={ 'T':None,'O':(48,40,44),'K':(112,98,88),'S1':(250,248,240),'S2':(228,222,208),'S3':(186,176,162),'S4':(150,138,126),
    'F2':(214,204,186),'B1':(170,156,138),'Q1':(196,248,232),'Q2':(112,214,198),'Q3':(56,160,160),'Q4':(30,110,120),
    'E1':(170,226,214),'E2':(96,176,170),'E3':(30,130,140),'E4':(120,230,210)}
M={0:'T',10:'O',2:'K',4:'S2',1:'S3',5:'S1',6:'F2',3:'S4',12:'B1',7:'E1',8:'E2',9:'E3',11:'E4'}
def base():
    g=[[M[v] for v in r] for r in g0]
    return g
def body(x,y): return g0[y][x] in (4,1,2) and not (g0[y][x]==2 and any(g0[y+dy][x+dx] in (0,10) for dx,dy in((1,0),(-1,0),(0,1),(0,-1))))
def hexcracks(g,mask,size=4.2,ox=0,oy=0):
    # verwijder vlekken, teken zeshoek-naden
    cs=[]
    for j in range(-2,20):
        for i in range(-2,20):
            cx=ox+i*size*1.732+(j%2)*size*0.866; cy=oy+j*size*1.5; cs.append((cx,cy))
    for y in range(64):
        for x in range(64):
            if not mask(x,y): continue
            ds=sorted((x-cx)**2+(y-cy)**2 for cx,cy in cs)[:2]
            d1,d2=math.sqrt(ds[0]),math.sqrt(ds[1])
            light=(x+y)<52
            g[y][x]='K' if d2-d1<0.9 else ('S2' if light else 'S3')
def outline(g):
    todo=[]
    for y in range(64):
        for x in range(64):
            if g[y][x]=='T' and any(0<=x+dx<64 and 0<=y+dy<64 and g[y+dy][x+dx] not in ('T','O') for dx,dy in((1,0),(-1,0),(0,1),(0,-1))):
                todo.append((x,y))
    for x,y in todo: g[y][x]='O'
def sack(g):
    cx,cy,rx,ry=31,37,8.5,6.5
    for y in range(64):
        for x in range(64):
            e=((x-cx)/rx)**2+((y-cy)/ry)**2
            if e<=1 and g0[y][x] in (0,1,4,2,10):
                if g0[y][x] in (6,12,3,5): continue
                lx=((x-cx)+(y-cy))/ (rx+ry)
                g[y][x]='Q1' if (e<0.25 and lx<-0.2) else 'Q2' if lx<0.15 else 'Q3' if e<0.85 else 'Q4'
    for x,y in((27,35),(33,39),(30,41),(35,35)): g[y][x]='Q1'
def cone(g):
    for y in range(30,45):
        for x in range(36,51):
            if g0[y][x] in (7,8,2,10,3) and y<44: g[y][x]='T'
    ax,ay,bl,br,by=43,29,35,51,45
    for y in range(ay,by):
        t=((y-ay)/(by-ay))**0.6; l=ax-(ax-bl)*t; r=ax+(br-ax)*t
        for x in range(64):
            if l<=x<=r and g[y][x] in('T','O'):
                g[y][x]='S1' if x<ax-1-(t*2) else 'S2' if x<ax+2+t*3 else 'S3'
    for x,y in((41,35),(42,36),(45,34),(46,35),(46,36),(39,40),(40,41),(41,41),(47,40),(48,41),(44,39),(44,40),(43,43),(42,43)):
        if g[y][x] in('S1','S2','S3'): g[y][x]='S4' if x<ax else 'K'
def plates(g):
    hx,hy=26,26
    add=[]
    for y in range(64):
        for x in range(64):
            if g0[y][x]!=0: continue
            a=math.degrees(math.atan2(y-hy,x-hx))
            if not(-120<=a<=15): continue
            near=min((abs(dx)+abs(dy) for dy in range(-3,4) for dx in range(-3,4)
                      if 0<=x+dx<64 and 0<=y+dy<64 and g0[y+dy][x+dx] not in(0,) and abs(dx)+abs(dy)<=3),default=9)
            if near<=2: add.append((x,y,a))
    for x,y,a in add:
        seam=int((a+120)/22)!=int((a+120+3.5)/22)
        g[y][x]='K' if seam else ('S1' if a<-70 else 'S2')
    for y in range(64):
        for x in range(64):
            if g0[y][x]==10 and math.degrees(math.atan2(y-hy,x-hx))>=-120 and math.degrees(math.atan2(y-hy,x-hx))<=15 and x>=18: g[y][x]='K'
def sleepy(g):
    for y in range(21,25):
        for x in range(21,30):
            if g0[y][x] in(7,8,9,11): g[y][x]='S3' if y<23 else ('O' if y==23 else g[y][x])
def render(g):
    im=Image.new('RGBA',(64,64))
    for y in range(64):
        for x in range(64):
            c=C[g[y][x]]
            if c: im.putpixel((x,y),c+(255,))
    return im

def curlsalt(g):
    for y in range(34,46):
        for x in range(36,52):
            if g0[y][x]==7: g[y][x]='S2'
            elif g0[y][x]==8: g[y][x]='S3'
def mound(g,ax,ay,by,R,front=False,clear=False,rake=True):
    if clear:
        for y in range(30,45):
            for x in range(36,52):
                if g0[y][x] in (7,8,2,10,3) and y<44: g[y][x]='T'
    ry=R*0.33
    pts=[]
    for y in range(ay,int(by+ry)+1):
        for x in range(64):
            if y<=by:
                w=R*((y-ay)/(by-ay))**0.45
                if w<0.5 or abs(x-ax)>w: continue
            else:
                w=R*math.sqrt(max(0,1-((y-by)/ry)**2))
                if abs(x-ax)>w: continue
            pts.append((x,y,(x-ax)/max(w,1)))
    for x,y,u in pts:
        if not front and g[y][x] not in('T','O'): continue
        c='S1' if u<-0.3 else 'S2' if u<0.35 else 'S3'
        if u>0.8: c='S4'
        g[y][x]=c
    if rake:
        for k,(dx,dy) in enumerate(((-3,6),(-2,7),(2,5),(3,6),(-5,10),(-4,11),(1,10),(2,11),(5,9))):
            x,y=ax+dx,ay+dy
            if 0<=y<64 and g[y][x] in('S1','S2','S3'): g[y][x]='S3' if dx<0 else 'S4'
def full(g):
    hexcracks(g,lambda x,y: body(x,y) and not (x>=35 and y>=34)); plates(g); sack(g); sleepy(g)
V={}
g=base(); full(g); curlsalt(g); outline(g); V['A zonder kegel']=g
g=base(); mound(g,47,31,42,9); full(g); curlsalt(g); outline(g); V['B kegel achter hem, staart ervoor']=g
g=base(); mound(g,44,30,42,9,clear=True); full(g); outline(g); V['C staart verstopt in de kegel']=g
g=base(); mound(g,53,35,44,6); mound(g,43,30,39,7); full(g); curlsalt(g); outline(g); V['D twee kegels (rij van Colchani)']=g
Z=5; W=64*Z
sh=Image.new('RGB',(W*len(V),W*2+30),(40,40,40)); d=ImageDraw.Draw(sh)
for k,(n,g) in enumerate(V.items()):
    im=render(g)
    for j,bg in enumerate([(232,226,214),(150,190,220)]):
        t=Image.new('RGB',(64,64),bg); t.paste(im,(0,0),im)
        sh.paste(t.resize((W,W),Image.NEAREST),(k*W,30+j*W))
    d.text((k*W+6,9),n,fill=(255,255,255))
sh.save(OUT)
