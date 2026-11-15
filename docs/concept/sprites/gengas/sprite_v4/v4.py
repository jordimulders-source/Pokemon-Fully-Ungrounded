# v4 = v3 met twee wijzigingen: (1) kern lichtvlek w terug op precies de v2-plekken (v2 = model); (2) r -> m
# (gemeten goedkoopste samenvoeging, zie NOTITIES.md). Verder pixelgelijk aan v3.
import os
D=os.path.dirname(os.path.abspath(__file__))+'/'
v2=[l.rstrip('\n') for l in open(D+'../sprite_v2/raster.txt')][:64]
v3=[l.rstrip('\n') for l in open(D+'../sprite_v3/raster.txt')][:64]
out=[]
for y in range(64):
    r=''
    for x in range(64):
        c=v3[y][x]
        if v2[y][x]=='w' and c=='v': c='w'
        elif c=='r': c='m'
        r+=c
    out.append(r)
open(D+'raster.txt','w').write('\n'.join(out)+'\n')
# diff-bewijs
n={'w terug':0,'r->m':0,'anders':[]}
for y in range(64):
    for x in range(64):
        a,b=v3[y][x],out[y][x]
        if a==b: continue
        if a=='v' and b=='w' and v2[y][x]=='w': n['w terug']+=1
        elif a=='r' and b=='m': n['r->m']+=1
        else: n['anders'].append((y,x,a,b))
print(n)
