import sys
mond=sys.argv[1] if len(sys.argv)>1 else 'licht'
RNG={25:(12,17),26:(10,20),27:(8,22),28:(7,24),29:(6,25),30:(6,25),31:(5,26),32:(5,26),33:(5,27),34:(5,27),35:(5,27),36:(5,27),
     37:(6,27),38:(6,27),39:(6,27),40:(7,26),41:(7,26),42:(8,25),43:(8,24),44:(9,23),45:(10,22),46:(11,20),47:(13,18)}
HY={6:38,7:37,8:35,9:34,10:33,11:32,12:31,13:31,14:31,15:30,16:30,17:29,18:29,19:28,20:28,21:28,22:28,23:28,24:29,25:30}
inside={(x,y) for y,(a,b) in RNG.items() for x in range(a,b+1)}
d={}
for (x,y) in inside:
    edge=any((x+a,y+b) not in inside for a,b in((1,0),(-1,0),(0,1),(0,-1))) or y==47
    if edge: d[(x,y)]='F'; continue
    hy=HY.get(x,99)
    if y<=hy: d[(x,y)]='5' if y==hy else ('3' if x+y<=37 else '4')
    else:
        c='3'
        if y<=hy+1 and x<=11: c="2"
        if (x+1,y) in d and False: pass
        d[(x,y)]=c
# schaduw rechts en onder (2 px langs de rand), licht linksboven
for (x,y),c in list(d.items()):
    if c not in '3': continue
    if any(d.get((x+k,y))=='F' for k in (1,2)) and x>=17 or any(d.get((x,y+k))=='F' for k in (1,2)) and x>=13 or y>=45: d[(x,y)]='4'
# kamstrepen: van de haargrens naar achteren (links), richting knot
def lijn(a,b):
    (x0,y0),(x1,y1)=a,b; n=max(abs(x1-x0),abs(y1-y0)); return [(round(x0+(x1-x0)*t/n),round(y0+(y1-y0)*t/n)) for t in range(n+1)]
KNOOP=(5,31)
strepen=[]
for st in [(22,27),(18,28),(14,30),(10,32),(8,35)]:
    strepen+=lijn(st,KNOOP)
for p in strepen:
    if d.get(p) in ('3','4'): d[p]='5'
def blok(B,x0,y0):
    for j,row in enumerate(B):
        for k,ch in enumerate(row):
            if ch!='.': d[(x0+k,y0+j)]=ch
blok([".FF..","FF1F.","FFFFF",".FF.."],19,31)   # Hitmontops grote oog (gespiegeld)
blok([".FF.","FF1F","FFFF",".FF."],13,37)       # Hitmontops kleine oog (gespiegeld)
for p,c in {(23,35):'F',(22,36):'F',(21,37):'5',(20,37):'5',(19,36):'5',        # plooi onder groot oog
            (17,41):'F',(16,42):'F',(15,42):'5',(14,42):'5',(13,41):'5',        # plooi onder klein oog
            (12,34):'5',(14,34):'5',(15,34):'5',(16,34):'5',(17,34):'5',(17,33):'5',(18,32):'4',(18,31):'4'}.items():  # fronslijnen
    d[p]=c
for p in [(13,37),(16,37),(12,36),(19,31),(22,31),(23,30)]:   # zware bovenrand + scherpe buitenhoek
    d[p]='F'
MD={'licht':{(18,44):'5',(22,42):'5',(19,44):'F',(20,44):'F',(21,43):'F'},
    'meer':{(17,44):'5',(18,44):'F',(22,42):'F',(23,41):'5',(19,45):'F',(20,44):'F',(21,43):'F'}}[mond]
d.update(MD)
# hoorn (Hitmontops vorm, klein), licht links
for p,c in {(7,23):'F',(8,23):'F',(6,24):'F',(7,24):'3',(8,24):'4',(9,24):'F',(6,25):'F',(7,25):'3',(8,25):'4',(9,25):'5',(10,25):'F',
            (7,26):'F',(8,26):'3',(9,26):'4',(10,26):'4'}.items(): d[(p[0]+1,p[1]+1)]=c
# knot achterop + bandje
K=[".FFFF.","F3344F","F3454F","F4545F","F4455F",".FFFF."]
for j,row in enumerate(K):
    for k,ch in enumerate(row):
        p=(0+k,28+j)
        if ch!='.' and p not in d: d[p]=ch
x0=min(p[0] for p in d)
for y in sorted({p[1] for p in d}):
    xs=[p[0] for p in d if p[1]==y]
    print(y, x0, ''.join(d.get((x,y),'.') for x in range(x0,max(xs)+1)))
