# Ronde 5 (basis r4): 1) open rand (34,6) dicht met lijnindex 2; 2) tanden: scheiding in modelgrijs (157 -> '9'), tweede tand even hoog;
# 3) hoepel 2 één px naar links, daarachter hout tot de achterrand (model: 1,3-1,9 px hout achter hoepel 2).
import json, numpy as np
from PIL import Image
R='/home/user/Pokemon-Fully-Ungrounded/docs/concept/sprites/capybarrel/'
PAL={'.':(0,0,0),'0':(32,20,28),'s':(104,52,40),'C':(226,146,112),'A':(196,114,90),'5':(150,82,70),
     '9':(132,126,132),'3':(90,78,84),'n':(56,44,52),'B':(222,140,72),'7':(182,98,48),'4':(142,68,36),
     'D':(208,208,216),'W':(255,255,255),'h':(86,86,98)}
ORDER=list(PAL)
d=json.load(open(R+'sprite/r4/grid.json')); g=[list(r) for r in d['grid']]; r4=[r[:] for r in g]
H,Wd=len(g),len(g[0]); log=[]
def put(z,x,y,c,w):
    if g[y][x]!=c: log.append((z,x,y,g[y][x],c,w)); g[y][x]=c
op=lambda x,y: 0<=x<Wd and 0<=y<H and g[y][x]!='.'
edge=lambda x,y: any(not op(x+dx,y+dy) for dx,dy in((1,0),(-1,0),(0,1),(0,-1)))
# 1
put('rand',34,6,'s','hoepelpixel aan transparant -> lijnindex 2 zoals tonbovenrand')
# 2
for (x,y,c) in [(3,18,'W'),(4,18,'9'),(5,18,'W'),(3,19,'W'),(4,19,'9'),(5,19,'W')]:
    put('tanden',x,y,c,'twee tanden even hoog, scheiding modelgrijs (model 157)')
# 3
H2={7:33,8:34,9:34,10:34,11:35,12:35,13:35,14:35,15:35,16:35,17:35,18:35,19:35,20:34,21:34,22:34,23:33,24:33,25:32}
for y,c0 in H2.items():
    E=c0+2
    while E+1<Wd and r4[y][E+1] not in 'CA5.': E+=1
    T=r4[y][c0-2] if r4[y][c0-2] in 'B74s' else '4'
    if edge(c0-1,y): continue
    core='9' if y in (8,9,10) else 'h'
    put('hoepel2',c0-1,y,core,'hoepel 2 één px naar links'); put('hoepel2',c0,y,core,'idem')
    put('hoepel2',c0+1,y,'0','zwarte rand schaduwkant')
    for x in range(c0+2,E):
        if not edge(x,y): put('hoepel2',x,y,T,'hout achter hoepel 2 (rijtint ernaast; model 1,3-1,9 px)')
from collections import Counter
for _ in range(3):
    seen=set()
    for y in H2:
        for x in range(30,40):
            if (x,y) in seen or g[y][x] not in 'B74' or g[y][x]==r4[y][x]: continue
            v=g[y][x]; st=[(x,y)]; seen.add((x,y)); cc=[]
            while st:
                cx,cy=st.pop(); cc.append((cx,cy))
                for dx,dy in((1,0),(-1,0),(0,1),(0,-1)):
                    nx,ny=cx+dx,cy+dy
                    if op(nx,ny) and (nx,ny) not in seen and g[ny][nx]==v: seen.add((nx,ny)); st.append((nx,ny))
            if len(cc)<3:
                nb=Counter(g[y2+dy][x2+dx] for x2,y2 in cc for dx,dy in((1,0),(-1,0),(0,1),(0,-1)) if op(x2+dx,y2+dy) and g[y2+dy][x2+dx] in 'B74' and g[y2+dy][x2+dx]!=v)
                if nb:
                    for x2,y2 in cc: put('hoepel2',x2,y2,nb.most_common(1)[0][0],'houtvlakje <3 px -> buurtint')
put('hoepel2',34,25,'s','los houtpixel onderin: sluit aan op tonrand (34,26)')
# controles: oog diff 0, buiten zones diff 0, silhouet 0
zones=lambda x,y: (3<=x<=5 and 18<=y<=19) or (x,y)==(34,6) or (y in H2 and 30<=x<=39)
for y in range(H):
    for x in range(Wd):
        if g[y][x]!=r4[y][x]: assert zones(x,y),(x,y)
for y in range(6,12):
    for x in range(12,18): assert g[y][x]==r4[y][x]
assert all((g[y][x]=='.')==(r4[y][x]=='.') for y in range(H) for x in range(Wd))
OX,OY=d['OX'],d['OY']; img=np.zeros((64,64),'uint8')
for y in range(H):
    for x in range(Wd): img[OY+y,OX+x]=ORDER.index(g[y][x])
pal=sum((list(PAL[k]) for k in ORDER),[])+[0]*3*(256-len(ORDER))
im=Image.fromarray(img,'P'); im.putpalette(pal); im.save(R+'sprite/r5/capybarrel.png',transparency=0)
im2=Image.open(R+'sprite/r5/capybarrel.png').convert('RGBA'); bg=Image.new('RGBA',(64,64),(225,225,225,255)); bg.alpha_composite(im2)
bg.resize((512,512),Image.NEAREST).save(R+'sprite/r5/capybarrel_8x.png')
json.dump({'OX':OX,'OY':OY,'grid':[''.join(r) for r in g],'kaal':d['kaal']},open(R+'sprite/r5/grid.json','w'))
open(R+'sprite/r5/log.txt','w').write(''.join('%s (%d,%d) %s->%s  %s\n'%e for e in log))
from collections import Counter; print(dict(Counter(e[0] for e in log)))
for y in range(5,27): print('%2d '%y+''.join(g[y][29:41]),'  r4:',''.join(r4[y][29:41]))
