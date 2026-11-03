# Salticonda schetsen ronde 1: ruwe concepten op de Sandaconda-sprite (geen eindwerk).
import math
from PIL import Image, ImageDraw
src=Image.open('graphics/pokemon/sandaconda/anim_front.png')
g0=[list(src.get_flattened_data())[y*64:(y+1)*64] for y in range(64)]
C={'T':None,'O':(54,44,42),'O2':(100,86,76),'K':(146,128,104),'S1':(248,244,232),'S2':(228,220,202),'S3':(204,192,170),'S4':(176,160,136),
   'Q1':(184,244,228),'Q2':(96,204,192),'Q3':(44,148,152),'Q4':(24,92,104),'F1':(248,244,232),'F2':(220,204,170),'F3':(186,164,126),'Y':(240,250,200)}
def tr(x,y): return not(0<=x<64 and 0<=y<64) or g0[y][x]==0
def is_out(x,y): return g0[y][x]==3 and any(tr(x+dx,y+dy) for dx in(-1,0,1) for dy in(-1,0,1))
def base():
    g=[['T']*64 for _ in range(64)]
    for y in range(64):
        for x in range(64):
            v=g0[y][x]
            if v==0: continue
            if v==3: g[y][x]='O' if is_out(x,y) else 'Q3'
            elif v==2: g[y][x]='S2'
            elif v==1: g[y][x]='S3'
            elif v in(5,6): g[y][x]='S4' if v==5 else 'S3'
            elif v==4: g[y][x]='O2'
            elif v in(7,8): g[y][x]='O2' if v==7 else 'K'
            elif v==9: g[y][x]='F1'
            elif v==10: g[y][x]='F3'
            elif v in(11,12): g[y][x]='Q2'
            else: g[y][x]='S3'
    return g
def band_shade(g):
    M=[[g[y][x]=='Q3' for x in range(64)] for y in range(64)]
    for y in range(1,63):
        for x in range(1,63):
            if not M[y][x]: continue
            if not M[y-1][x]: g[y][x]='Q1' if x<26 else 'Q2'
            elif not M[y+1][x] or not M[y][x+1]: g[y][x]='Q4'
            else: g[y][x]='Q3' if x>30 else 'Q2'
def cracks(g,size=4.6):
    cs=[(i*size*1.732+(j%2)*size*0.866, j*size*1.5) for j in range(-2,20) for i in range(-2,20)]
    for y in range(64):
        for x in range(64):
            if g[y][x] in('S2','S3') and x>12:
                ds=sorted((x-cx)**2+(y-cy)**2 for cx,cy in cs)[:2]
                if math.sqrt(ds[1])-math.sqrt(ds[0])<0.9: g[y][x]='K'
def cone(g,ax=24,ay=6,by=16,R=9):
    pts=[]
    for y in range(ay,by+1):
        w=R*((y-ay)/(by-ay))**0.55
        for x in range(int(ax-w),int(ax+w)+1):
            if g[y][x] in('T','O'): pts.append((x,y,(x-ax)/max(w,1)))
    for x,y,u in pts: g[y][x]='S1' if u<-0.35 else 'S2' if u<0.3 else 'S3'
    for dx,dy in((-3,5),(-2,6),(3,4),(4,5),(-6,10),(-5,11),(1,9),(2,10),(6,10),(7,11)):
        x,y=ax+dx,ay+dy
        if g[y][x] in('S1','S2','S3'): g[y][x]='S4' if dx<0 else 'K'
def cells(g):
    # accu-hint: zoutstrepen door de band (cellen) + vonkjes
    for y in range(64):
        for x in range(64):
            if g[y][x].startswith('Q') and (x-y)%7 in(0,):
                g[y][x]='S3'
    for x,y in((30,26),(31,25),(38,33),(24,30)):
        if g[y][x].startswith('Q'): g[y][x]='Y'
def sleepy(g):
    for y in range(29,34):
        for x in range(9,19):
            if g0[y][x] in(11,12):
                g[y][x]='S3' if y<=30 else ('Q3' if y==31 else 'Q2')
def outline(g):
    todo=[]
    for y in range(64):
        for x in range(64):
            if g[y][x]=='T' and any(0<=x+dx<64 and 0<=y+dy<64 and g[y+dy][x+dx] not in('T','O') and g0[y+dy][x+dx]==0 for dx,dy in((1,0),(-1,0),(0,1),(0,-1))): todo.append((x,y))
    for x,y in todo: g[y][x]='O'
def render(g,bg):
    im=Image.new('RGB',(64,64),bg)
    for y in range(64):
        for x in range(64):
            c=C[g[y][x]]
            if c: im.putpixel((x,y),c)
    return im
def nobands(g):
    for y in range(64):
        for x in range(64):
            if g[y][x]=='Q3' and g0[y][x]==3: g[y][x]='S3' if x>28 else 'S2'
def rings(g):
    # schone pekelbanden die om de opgerolde heuvel lopen (accu-cellen)
    for cy,th in((22,3),(31,4),(40,3)):
        for x in range(14,60):
            yc=cy+int(5*math.sin(math.pi*(x-14)/46))
            for y in range(yc,yc+th):
                if 0<=y<64 and g[y][x] in('S1','S2','S3','S4','K') and g0[y][x]!=0 and g0[y][x] not in(9,10):
                    t=y-yc
                    g[y][x]='Q1' if t==0 and x<34 else 'Q2' if t==0 else ('Q4' if t==th-1 else ('Q3' if x>36 else 'Q2'))
    for x,y in((26,33),(44,26),(40,43)):
        if g[y][x].startswith('Q'): g[y][x]='Y'
V=[]
g=base(); band_shade(g); cracks(g); sleepy(g); V.append(('A heuvel + pekelring (Sandaconda-band)',g))
g=base(); band_shade(g); cracks(g); cone(g); sleepy(g); outline(g); V.append(('B + zoutkegel bovenop',g))
g=base(); band_shade(g); cracks(g); cone(g); cells(g); sleepy(g); outline(g); V.append(('C + accu: cellen en vonkjes',g))
g=base(); nobands(g); cracks(g); cone(g); rings(g); sleepy(g); outline(g); V.append(('D eigen vorm: schone pekelringen',g))
Z=5; W=64*Z
sh=Image.new('RGB',(W*(len(V)+1),W*2+30),(40,40,40)); d=ImageDraw.Draw(sh)
idx=src.crop((0,0,64,64)); m=Image.new('L',(64,64)); m.putdata([0 if v==0 else 255 for v in idx.get_flattened_data()])
for j,bg in enumerate([(232,226,214),(52,56,70)]):
    t=Image.new('RGB',(64,64),bg); t.paste(idx.convert('RGB'),(0,0),m); sh.paste(t.resize((W,W),Image.NEAREST),(0,30+j*W))
d.text((6,9),'Sandaconda (basis)',fill=(255,255,255))
for k,(n,g) in enumerate(V):
    for j,bg in enumerate([(232,226,214),(52,56,70)]):
        sh.paste(render(g,bg).resize((W,W),Image.NEAREST),((k+1)*W,30+j*W))
    d.text(((k+1)*W+6,9),n,fill=(255,255,255))
sh.save('docs/concept/sprites/salticonda/schetsen_ronde1.png')
