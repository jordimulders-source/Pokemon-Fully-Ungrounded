# v9 = v8b + keuring v8b (15 nov). Alleen drie zones (diff erbuiten = 0, gemeten):
#  Z1 MOET rechterrand gezichtszone (x30-33, y30-38): m stopte op een rechte verticale naad (9 rijen) tegen de lichte
#     strook x34-36. Nu schuin zoals in het model (sprite_v2 = model: lichte strook schuift naar links naarmate y groter):
#     resultaat: l begint op x34 bij y30-31, x33 bij y32-33, x32 bij y34-36, daaronder de grijnshoek (trapjes 2-2-3).
#  Z2 MAG linksboven (x8-13, y23-31): egale b-vlek weer opgedeeld zoals het model: lichte band loopt tot x12-13 in
#     (rij 24-27, model l), randtint links (x8, rij 29-31, model selout r -> m).
#  Z3 MAG links van het linkeroog (x8-12, y32-36): effen m kreeg de randschaduw van het model (model x8 a/b rij 32-36)
#     als b, met een trapje op (9,33), naar l eronder.
import os
D=os.path.dirname(os.path.abspath(__file__))+'/'
V8=[l.rstrip('\n') for l in open(D+'../sprite_v8/raster_v8b.txt')][:64]
R=[list(r) for r in V8]; log=[]
Z=[(30,33,30,38),(8,13,23,31),(8,12,32,36)]
def inz(x,y): return any(x0<=x<=x1 and y0<=y<=y1 for x0,x1,y0,y1 in Z)
def zet(x,y,c,reden):
    assert inz(x,y),(x,y)
    if R[y][x]!=c: log.append(f'({x},{y}) {R[y][x]}->{c}  {reden}'); R[y][x]=c
for y,xs in ((32,(33,)),(33,(33,)),(34,(32,33)),(35,(32,33)),(36,(32,33)),(37,(31,32,33)),(38,(31,32,33))):
    for x in xs:
        if R[y][x]=='m': zet(x,y,'l','Z1 rand lichte strook schuin (model)')
for (x,y) in ((12,24),(13,24),(12,25),(13,25),(13,26),(13,27)): zet(x,y,'l','Z2 lichte band loopt in zoals model')
for y in (29,30,31): zet(8,y,'m','Z2 randtint (model selout r -> m)')
for (x,y) in ((8,33),(9,33),(8,34),(8,35),(8,36)): zet(x,y,'b','Z3 randschaduw zoals model (a/b -> b)')
open(D+'raster.txt','w').write('\n'.join(''.join(r) for r in R)+'\n')
open(D+'raster.txt.log','w').write('\n'.join(log)+'\n')
print(len(log),'wijzigingen; buiten de zones:',sum(1 for y in range(64) for x in range(64) if V8[y][x]!=R[y][x] and not inz(x,y)))
