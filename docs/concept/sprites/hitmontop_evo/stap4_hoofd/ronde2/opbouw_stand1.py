import sys
from PIL import Image
P=Image.open('/home/user/Pokemon-Fully-Ungrounded/graphics/pokemon/hitmontop/anim_front.png').load()
M='0123456789ABCDEF'
def src(i,row): v=P[45-i,row]; return '.' if v==0 else M[v]
mond=sys.argv[1] if len(sys.argv)>1 else 'licht'
RNG={30:(6,14),31:(4,16),32:(3,18),33:(2,19),34:(1,21),35:(1,22),46:(1,23),47:(1,23),48:(2,22),49:(3,22),50:(4,21),51:(6,19),52:(8,17)}
for r in range(36,46): RNG[r]=(1,23)
inside={(i,r) for r,(a,b) in RNG.items() for i in range(a,b+1)}
def H(i): return 40 if i<=3 else 38 if i==4 else 37 if i==5 else 36 if i<=7 else 35 if i<=19 else 36
d={}
for (i,r) in inside:
    edge=any((i+a,r+b) not in inside for a,b in((1,0),(-1,0),(0,1),(0,-1))) or r==52
    if edge: d[(i,r)]='F'; continue
    if r<=H(i):
        d[(i,r)]='5' if r+1>H(i) else '4'
    else:
        c='3'
        if r<=H(i)+1 and i<=9: c='2'
        if i>=21 or (r>=49 and i>=17) or (r>=50 and i>=12): c='4'
        d[(i,r)]=c
def lijn(a,b):
    (x0,y0),(x1,y1)=a,b; n=max(abs(x1-x0),abs(y1-y0)); return [(round(x0+(x1-x0)*t/n),round(y0+(y1-y0)*t/n)) for t in range(n+1)]
groef=[]
for st in [(19,34),(15,34),(11,34),(7,35)]:
    groef+=lijn(st,(2,31))
licht=[(q[0]+1,q[1]) for q in groef if q[0]<12]+[(5,32),(6,32),(4,33),(5,33),(3,34),(4,34),(2,34),(3,35)]
for p in licht:
    if d.get(p)=='4': d[p]='3'
for p in groef:
    if d.get(p) not in (None,'F'): d[p]='5'
# Hitmontop-trekken (gespiegeld), exact; groot oog + plooi + rechterarm wenkbrauw 1 px naar links
for r in range(37,48):
    for i in range(8,23):
        s=src(i,r)
        if s not in 'F514': continue
        klein=(r>=42 and 8<=i<=13); groot=(40<=r<=45 and 17<=i<=22); brauwL=(r<=40 and 10<=i<=15); brauwR=(r<=40 and 16<=i<=18)
        if s=='4' and not (brauwR and r<=38 and i>=17): continue
        if klein or brauwL: d[(i,r)]=s
        elif groot or brauwR:
            if (i,r) in d and d[(i,r)]!='F': d[(i,r)]=s
# hoorn: Hitmontops hoorn als geheel verkleind
for (i,r),c in {(9,27):'F',(10,27):'F',(8,28):'F',(9,28):'3',(10,28):'4',(11,28):'F',(7,29):'F',(8,29):'3',(9,29):'4',(10,29):'5',(11,29):'F',(8,30):'3',(9,30):'4',(10,30):'4'}.items(): d[(i,r)]=c
# mond
M1={'licht':{(15,47):'5',(19,47):'5',(16,48):'F',(17,48):'F',(18,48):'F'},
    'meer':{(14,47):'5',(15,47):'F',(19,47):'F',(20,47):'5',(16,48):'F',(17,48):'F',(18,48):'F'}}[mond]
d.update(M1)
LID=len(sys.argv)>2 and sys.argv[2]=='lid'
if LID:   # zware bovenrand + scherpe buitenhoek (halfdicht), oogpixels zelf blijven
    for p in [(9,42),(12,42),(8,41),(18,40),(21,40),(22,39)]:
        if p in d: d[p]='F'
# knot (achter het hoofd)
K=[".FFFF.","F3344F","F3454F","F4545F","F4455F",".FFFF."]
for j,row in enumerate(K):
    for k,c in enumerate(row):
        p=(-2+k,27+j)
        if c!='.' and p not in d: d[p]=c
for p,c in {(3,30):'F',(3,31):'5'}.items():
    if p not in d: d[p]=c
rows=sorted({r for _,r in d}); x0=min(i for i,_ in d)
for r in rows:
    print(r, x0, ''.join(d.get((i,r),'.') for i in range(x0, max(i for i,rr in d if rr==r)+1)))
