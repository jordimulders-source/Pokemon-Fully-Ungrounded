# stap 1 (onderlaag): kop r1-17 met de hand; rest = modelhelderheid per zone naar het palet (kleurzones uit SPEC).
# Daarna handwerk in raster.txt (dit script niet opnieuw draaien na handwerk).
import numpy as np
d=np.load('../silhouet/meet.npz'); mean,m=d['mean'],d['m']; red=d['red']; L=mean.mean(2)
H={1:[(30,"do")],2:[(18,"ddd"),(30,"dao")],3:[(18,"daaddd"),(30,"dao")],4:[(18,"dbaaaad"),(30,"dabo")],
5:[(19,"dcbaaadd"),(30,"dabco")],6:[(20,"dcbbaaadd"),(30,"dabbco")],7:[(21,"dcbbbaaaoobbbco")],
8:[(21,"dcbbaaaaadbbbbco")],9:[(22,"dcbaaaaaabbbbbco")],10:[(22,"dcbbaaaaaabbbbbco")],11:[(23,"dcbbaaaaabbbbbbco")],
12:[(23,"dcbbbaaabbbbbbbco")],13:[(24,"dcbbbbbbcccbbbbco")],14:[(23,"dccbbbbbdbbbdbbbco")],15:[(23,"dccbbbbbbocccdbbdco")],
16:[(22,"dccbbbbbbbowoodcbddo")],17:[(21,"dcccbbbbbbbdowwwocowo"),(45,"oo")]}
def grey(l):
    return 'w' if l>=232 else 'a' if l>=195 else 'b' if l>=165 else 'c' if l>=140 else 'd' if l>=100 else 'e' if l>=70 else 'o'
def blk(l):
    return 'o' if l<22 else 'm' if l<50 else 'n' if l<80 else 'p'
def plate(l):
    return 'o' if l<45 else 'k' if l<100 else 'm' if l<125 else 'n' if l<150 else 'p'
def white(l):
    return 'w' if l>=225 else 'a' if l>=195 else 'b' if l>=160 else 'c' if l>=120 else 'd' if l>=75 else 'o'
R=[['.']*64 for _ in range(64)]
for y in range(64):
  for x in range(64):
    if not m[y,x]: continue
    l=L[y,x]
    if y in H: continue
    isplate=((x-18.5)/6.3)**2+((y-23)/5.1)**2<=1.0
    if isplate: R[y][x]=plate(l); continue
    if red[y,x]>0.35: R[y][x]='r' if l>80 else 's'; continue
    if (12<=x<=19 and 28<=y<=33) or (36<=x<=41 and 27<=y<=33):   # bovenarmen -> zwart
        R[y][x]='o' if l<22 else 'm' if l<120 else 'n'; continue
    if 37<=x<=50 and 32<=y<=39:                                     # rechter onderarm -> grijs
        R[y][x]='o' if l<22 else grey(l+125) if l<70 else grey(l+40); continue
    headzone = y<=19 or (y<=27 and x>=29)
    if headzone and l>=60: R[y][x]=grey(l); continue
    if headzone and l<60 and not (23<=x<=36 and y>=23): R[y][x]='o'; continue
    if l<70: R[y][x]=blk(l); continue
    if l>=215: R[y][x]=white(l); continue
    R[y][x]=grey(min(255,l+40))
for y,segs in H.items():
    for x,s in segs:
        for i,ch in enumerate(s): R[y][x+i]=ch
open('raster.txt','w').write('\n'.join(''.join(r) for r in R)+'\n')
