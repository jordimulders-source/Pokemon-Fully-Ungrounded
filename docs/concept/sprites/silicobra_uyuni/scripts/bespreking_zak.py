# Bespreking (3 nov): waar zit het streepje + drie opties voor de pekelzak (ruwe schetsen op ronde 2).
import math
from PIL import Image, ImageDraw
D='docs/concept/sprites/silicobra_uyuni/'
r2=Image.open(D+'ronde2/silicobra_uyuni.png'); pal=r2.getpalette()[:48]
g2=[list(r2.get_flattened_data())[y*64:(y+1)*64] for y in range(64)]
o=Image.open('graphics/pokemon/silicobra/anim_front.png'); go=[list(o.get_flattened_data())[y*64:(y+1)*64] for y in range(64)]
TQ=set([11,12,13,14])
def clear_sack():
    g=[r[:] for r in g2]
    for y in range(30,45):
        for x in range(14,43):
            if g[y][x] in TQ or (g[y][x]==1 and any(g2[y+dy][x+dx] in TQ for dx in(-1,0,1) for dy in(-1,0,1))):
                ov=go[y][x]
                g[y][x]={0:0,10:1,1:5,4:6,2:4,6:9,12:10,3:4,7:6,8:5}.get(ov,6)
    return g
def outline(g,ref):
    todo=[]
    for y in range(1,63):
        for x in range(1,63):
            if g[y][x]==0 and any(g[y+dy][x+dx] not in(0,1) and ref[y+dy][x+dx]==0 for dx,dy in((1,0),(-1,0),(0,1),(0,-1))): todo.append((x,y))
    for x,y in todo: g[y][x]=14 if any(g[y+dy][x+dx] in TQ for dx,dy in((1,0),(-1,0),(0,1),(0,-1))) else 1
def shade(x,y,cx,cy,rx,ry):
    u=((x-cx)/rx+(y-cy)/ry)/2
    return 11 if u<-0.45 else 12 if u<0.1 else 13 if u<0.45 else 14
def venster():
    g=clear_sack()
    for y in range(31,43):
        for x in range(16,40):
            if go[y][x] in(1,4,2) and all(go[y+dy][x+dx] not in(0,10,6,12) for dx in(-2,-1,0,1,2) for dy in(-1,0,1)):
                g[y][x]=shade(x,y,27,36,8,5)
    return g
def keelzak():
    g=clear_sack(); ref=[r[:] for r in g]
    cx,cy,rx,ry=18,35,5.5,4.5
    for y in range(64):
        for x in range(64):
            if ((x-cx)/rx)**2+((y-cy)/ry)**2<=1 and g[y][x] in(0,1,5,6,4):
                g[y][x]=shade(x,y,cx,cy,rx,ry)
    outline(g,ref); return g
def halsband():
    g=clear_sack(); ref=[r[:] for r in g]
    for y in range(31,38):
        xs=[x for x in range(14,42) if go[y][x] not in(0,) and not(x>=35 and y>=36)]
        if not xs: continue
        l,r=min(xs)-1,max(xs)+1
        bow=1 if 32<=y<=36 else 0
        for x in range(l-bow,r+bow-1):
            if g[y][x] in(0,1,4,5,6,9,10) and not (go[y][x] in (6,12) and y>=36):
                if y==37 and (x+1)%3==0: continue
                g[y][x]=shade(x,y,(l+r)/2,34,(r-l)/2,3.5)
    outline(g,ref); return g
def render(g,bg):
    im=Image.new('RGB',(64,64),bg)
    for y in range(64):
        for x in range(64):
            v=g[y][x]
            if v: im.putpixel((x,y),tuple(pal[v*3:v*3+3]))
    return im
def naden():
    g=clear_sack()
    for y in range(12,32):
        for x in range(22,46):
            if g[y][x] in(4,5) and not any(g[y+dy][x+dx] in(0,) for dx in(-1,0,1) for dy in(-1,0,1)):
                g[y][x]=13 if g[y][x]==4 else 12
    return g
V=[('ronde 2 (nu)',g2),('4 pekel onder de korst',naden()),('1 venster in de nek',venster()),('2 keelzak vooraan',keelzak()),('3 halsband',halsband())]
Z=7; W=56*Z
sh=Image.new('RGB',(W*5,48*Z*2+40),(40,40,40)); d=ImageDraw.Draw(sh)
for k,(n,g) in enumerate(V):
    for j,bg in enumerate([(232,226,214),(52,56,70)]):
        sh.paste(render(g,bg).crop((4,8,60,56)).resize((W,48*Z),Image.NEAREST),(k*W,40+j*48*Z))
    d.text((k*W+6,14),n,fill=(255,255,255))
sh.save(D+'bespreking/pekelzak_opties.png')
# streepje aanwijzen
z=render(g2,(232,226,214)).crop((8,8,44,34)).resize((36*14,26*14),Image.NEAREST); dd=ImageDraw.Draw(z)
for (x0,y0,x1,y1),t in [((13,18,20,20),'A'),((23,19,29,20),'B')]:
    dd.rectangle(((x0-8)*14-3,(y0-8)*14-3,(x1-8)*14+3,(y1-8)*14+3),outline=(230,30,30),width=3); dd.text(((x0-8)*14,(y0-8)*14-16),t,fill=(230,30,30))
z.save(D+'bespreking/streepje.png')
