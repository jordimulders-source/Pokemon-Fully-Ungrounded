# Eenmalige hulplaag (gids): legt de grove vlakken van lijf, broek en benen neer volgens de pose.
# Het resultaat (raster_draft.txt) is alleen een startpunt; de echte sprite is raster.txt (met de hand bewerkt).
from kop import kop
from pal import ch2i
W=H=64
g=[[0]*W for _ in range(H)]
mat=[['']*W for _ in range(H)]
def put(x,y,c,m):
    if 0<=x<W and 0<=y<H: g[y][x]=ch2i(c); mat[y][x]=m
# verre been (achter), donkerder
far={6:(56,58),7:(56,59),8:(55,59),9:(55,59),10:(54,59),11:(54,60),12:(53,60),13:(53,60),14:(52,60),15:(52,60),16:(52,60)}
for y,(a,b) in far.items():
    for x in range(a,b+1):
        f=(x-a)/max(1,b-a); put(x,y,'7' if f<0.6 else '8','b')
# nabije been
U=lambda x:6+(x-14)*0.28
Lo=lambda x:10.5+(x-14)*0.36
for x in range(15,50):
    for y in range(0,30):
        if U(x)<=y<=Lo(x):
            f=(y-U(x))/(Lo(x)-U(x)); put(x,y,'6' if f<0.3 else ('7' if f<0.75 else '8'),'b')
# heup
hip={14:(48,55),15:(47,57),16:(46,58),17:(46,59),18:(46,59),19:(46,59),20:(46,59),21:(45,59)}
for y in range(14,31):
    if y in hip: l,r=hip[y]
    else: l,r=66-y,79-y
    for x in range(l,r+1):
        if x-y<21: continue
        put(x,y,'8' if x>=r-2 else ('6' if y<=16 else '7'),'b')
# romp (huid)
for y in range(20,47):
    L=66-y; R=79-y
    for x in range(max(L,y-12),R+1):
        if x-y>=21: continue
        if x-y in (19,20): put(x,y,'a' if x-y==19 else 'b','c'); continue
        f=(x-L)/(R-L); put(x,y,'2' if f<0.22 else ('3' if f<0.7 else '4'),'s')
# omlijning
out=[row[:] for row in g]
for y in range(H):
    for x in range(W):
        if g[y][x]==0: continue
        nb=[(x-1,y),(x+1,y),(x,y-1),(x,y+1)]
        emp=[(a,b) for a,b in nb if not(0<=a<W and 0<=b<H) or g[b][a]==0]
        if emp:
            lit=all((a<x or b<y) for a,b in emp)
            m=mat[y][x]
            out[y][x]=ch2i({'s':'5','b':'9','c':'b'}[m]) if lit else 15
g=out
# kop
k=kop()
for y in range(26):
    for x in range(42):
        if k[y][x] and 0<=x-3<W and 0<=y+20<H: g[y+20][x-3]=k[y][x]
open('raster_draft.txt','w').write('\n'.join(''.join('.' if v==0 else '%x'%v for v in r) for r in g)+'\n')
