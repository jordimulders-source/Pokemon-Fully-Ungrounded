# Ronde 4: basis r3 variant 3 (Flareon-oog). Alleen hoepels: model meet grijs 1,29 px + zwart 0,42 links / 0,53 rechts (totaal 2,25 px)
# -> 2 px grijs + 1 px zwart aan de schaduwkant (rechts); linker zwartrand wordt het hout ernaast.
import json, numpy as np
from PIL import Image
from collections import Counter
R='/home/user/Pokemon-Fully-Ungrounded/docs/concept/sprites/capybarrel/'
PAL={'.':(0,0,0),'0':(32,20,28),'s':(104,52,40),'C':(226,146,112),'A':(196,114,90),'5':(150,82,70),
     '9':(132,126,132),'3':(90,78,84),'n':(56,44,52),'B':(222,140,72),'7':(182,98,48),'4':(142,68,36),
     'D':(208,208,216),'W':(255,255,255),'h':(86,86,98)}
ORDER=list(PAL)
d=json.load(open(R+'sprite/r3/grid_3.json')); g=[list(r) for r in d['grid']]; r3=[r[:] for r in g]
H,Wd=len(g),len(g[0]); log=[]
op=lambda x,y: 0<=x<Wd and 0<=y<H and g[y][x]!='.'
edge=lambda x,y: any(not op(x+dx,y+dy) for dx,dy in((1,0),(-1,0),(0,1),(0,-1)))
H1={6:23,7:24,8:24,9:25,10:25,11:25,12:26,13:26,14:26,15:26,16:26,17:26,18:25,19:25,20:25,21:25,22:24}
H2={6:33,7:33,8:34,9:34,10:34,11:35,12:35,13:35,14:35,15:35,16:35,17:35,18:35,19:35,20:34,21:34,22:34,23:33,24:33,25:32}
for HH in (H1,H2):
    for y,c0 in HH.items():
        x=c0-1
        if g[y][x]!='0' or edge(x,y): continue
        # hout uit de rij links ervan (zelfde rij, dus planklijn loopt door), anders uit boven/onder
        cand=[g[y][xx] for xx in (x-1,x-2) if 0<=xx<Wd and g[y][xx] in 'B74s']
        if not cand: cand=[g[yy][x] for yy in (y-1,y+1) if g[yy][x] in 'B74']
        if not cand: continue
        new=cand[0]; log.append((x,y,g[y][x],new)); g[y][x]=new
# assert: oog en kop bevroren (canvas x15-31,y26-46 = figuur x6-22,y0-20), silhouet bevroren
for y in range(0,21):
    for x in range(6,23): assert g[y][x]==r3[y][x] or (x,y) in {(e[0],e[1]) for e in log},(x,y)
zonepx=[(e[0],e[1]) for e in log if 6<=e[0]<=22 and e[1]<=20]; print('in kop/oog-zone alleen hoepelrand gewijzigd:',zonepx)
assert all((g[y][x]=='.')==(r3[y][x]=='.') for y in range(H) for x in range(Wd))
OX,OY=d['OX'],d['OY']; img=np.zeros((64,64),'uint8')
for y in range(H):
    for x in range(Wd): img[OY+y,OX+x]=ORDER.index(g[y][x])
pal=sum((list(PAL[k]) for k in ORDER),[])+[0]*3*(256-len(ORDER))
im=Image.fromarray(img,'P'); im.putpalette(pal); im.save(R+'sprite/r4/capybarrel.png',transparency=0)
json.dump({'OX':OX,'OY':OY,'grid':[''.join(r) for r in g],'kaal':d['kaal']},open(R+'sprite/r4/grid.json','w'))
open(R+'sprite/r4/log.txt','w').write(''.join('hoepel (%d,%d) %s->%s  linker zwartrand -> hout (model: zwart links 0,42 px)\n'%e for e in log))
print(len(log),'px gewijzigd t.o.v. r3; niet gewijzigd (rand/geen hout):',[(c0-1,y) for HH in (H1,H2) for y,c0 in HH.items() if g[y][c0-1]=='0'])
