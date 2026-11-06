import re, sys
VAR=sys.argv[1] if len(sys.argv)>1 else 'A'
s=open('/home/user/Pokemon-Fully-Ungrounded/docs/concept/sprites/hitmontop_evo/stap4_hoofd/ronde2/stap4_r2.py').read()
g=re.search(r"'1M': \"\"\"(.*?)\"\"\"",s,re.S).group(1)
old={}
for l in g.strip().split('\n'):
    y,x0,r=l.split(' ',2)
    for i,c in enumerate(r):
        if c!='.': old[(int(x0)+i,int(y))]=c
# 1. omtrek (links/rechts per rij), rond
L={25:11,26:9,27:8,28:7,29:7,30:6,31:6,32:6,33:6,34:5,35:5,36:5,37:5,38:5,39:6,40:6,41:6,42:6,43:7,44:8,45:10,46:12}
R={25:18,26:20,27:22,28:23,29:25,30:26,31:27,32:27,33:27,34:27,35:27,36:27,37:27,38:27,39:27,40:27,41:27,42:27,43:26,44:25,45:23,46:21}
inside={(x,y) for y in L for x in range(L[y],R[y]+1)}|{(x,47) for x in range(14,20)}
d={}
for p in inside:
    x,y=p
    edge=y==47 or any((x+a,y+b) not in inside for a,b in((1,0),(-1,0),(0,1),(0,-1)))
    d[p]='F' if edge else None
# 5. haar: haargrens als boog, links lager (achter het oor naar de knot)
HY={6:35,7:34,8:33,9:32,10:31,11:31,12:30,13:30,14:29,15:29,16:29,17:29,18:29,19:29,20:29,21:29,22:30,23:30,24:31,25:31,26:32}
for (x,y),c in list(d.items()):
    if c: continue
    hy=HY.get(x,0)
    if y<=hy:
        d[(x,y)]=('5' if x<=9 else '4') if y==hy else ('3' if (y<=27 and x<=13) or (x<=8 and y<=31) else '4')
# kamstrepen: doorlopende lijnen van de haargrens naar de knot
C1=[(21,29),(20,28),(19,28),(18,28),(17,27),(16,27),(15,27),(14,27),(13,26),(12,26),(11,26),(10,26)]
C2=[(14,29),(13,28),(12,28),(11,27),(10,27)]
C3=[(9,32),(9,31),(8,30),(8,29),(8,28)]
for p in C1+C2+C3:
    if d.get(p) in ('3','4'): d[p]='5'
# gezicht uit 1M overnemen (alles onder de haargrens), met reparaties
for (x,y),c in list(d.items()):
    if c is None:
        o=old.get((x,y),'3')
        d[(x,y)]= '3' if o=='F' and (x,y) not in [] and o is None else o
# huid die in 1M omlijning was (oude linkerwand x5 / bodem) of glimlijn -> huid
for (x,y),c in list(d.items()):
    if y>HY.get(x,0) and c=='F' and (x,y) in inside:
        edge=y==47 or any((x+a,y+b) not in inside for a,b in((1,0),(-1,0),(0,1),(0,-1)))
        oogzone=(12<=x<=27 and 33<=y<=43)
        if not edge and not oogzone: d[(x,y)]='3'
    if c=='2': d[(x,y)]='3'
for p in [(11,32),(12,32),(11,33)]: d[p]='2'       # klein glimvlak boven het kleine oog
# 2. groot oog + plooi + vleugel 1 px naar links
oog=[(x,y) for x in range(21,28) for y in range(34,41) if old.get((x,y)) in ('F','1','5') and not (x==27) and not (x==21 and y in (39,))]
oog=[p for p in oog if not (p[0]==26 and p[1]==34 and False)]
vals={p:old[p] for p in oog}
for p in oog: d[p]='3'
for (x,y),c in vals.items(): d[(x-1,y)]=c
for y in range(34,41):
    if d.get((26,y)) in ('3',): d[(26,y)]='4'
# 3. mond (1M) los van de kinschaduw: rij onder de mond en rechts ervan huid
for p in [(19,44),(20,44),(21,44),(22,44),(23,44),(24,43),(25,42),(25,43)]:
    if d.get(p) in ('4',): d[p]='3'
# schaduw onderaan opnieuw langs de nieuwe bodem (sikkel rechtsonder)
for (x,y),c in list(d.items()):
    if c=='3' and y>=44 and any(d.get((x+a,y+b))=='F' for a,b in((0,1),(1,0),(1,1))) and x>=16: d[(x,y)]='4'
    if c=='3' and x>=25 and 31<=y<=43 and d.get((x+1,y))=='F': d[(x,y)]='4'
# hoorn (uit 1M)
for p,c in old.items():
    if p[1]<=25 and 11<=p[0]<=15: d[p]=c
# 4. knot met de hand: op de haarmassa, licht linksboven, vouw (5) waar hij in het haar overgaat, hals >= 4 px
KN={'A':{21: {5: 'F', 6: 'F', 7: 'F', 8: 'F'}, 22: {4: 'F', 5: '3', 6: '3', 7: '3', 8: '4', 9: 'F'}, 23: {3: 'F', 4: '3', 5: '3', 6: '3', 7: '4', 8: '4', 9: '5', 10: 'F'}, 24: {3: 'F', 4: '3', 5: '3', 6: '4', 7: '4', 8: '5', 9: '5', 10: 'F'}, 25: {3: 'F', 4: '3', 5: '4', 6: '4', 7: '5', 8: 'F', 9: 'F', 10: 'F', 11: 'F'}, 26: {4: 'F', 5: '4', 6: '5', 7: 'F', 8: '5', 9: '4', 10: '4'}, 27: {5: 'F', 6: 'F', 7: '5', 8: '5', 9: '4', 10: '4'}},'B':{20: {2: 'F', 3: 'F', 4: 'F', 5: 'F'}, 21: {1: 'F', 2: '3', 3: '3', 4: '3', 5: '4', 6: 'F'}, 22: {0: 'F', 1: '3', 2: '3', 3: '3', 4: '4', 5: '4', 6: '5', 7: 'F'}, 23: {0: 'F', 1: '3', 2: '3', 3: '4', 4: '4', 5: '5', 6: '5', 7: 'F'}, 24: {0: 'F', 1: '3', 2: '4', 3: '4', 4: '5', 5: 'F', 6: 'F', 7: 'F', 8: 'F'}, 25: {1: 'F', 2: '4', 3: '5', 4: 'F', 5: '5', 6: '5', 7: '4', 8: '4', 9: 'F'}, 26: {2: 'F', 3: 'F', 4: 'F', 5: '5', 6: '4', 7: '4', 8: '4', 9: '4'}, 27: {5: 'F', 6: 'F', 7: '5', 8: '4', 9: '4'}}}[VAR]
for y,row in KN.items():
    for x,c in row.items(): d[(x,y)]=c
x0=min(p[0] for p in d)
for y in sorted({p[1] for p in d}):
    xs=[p[0] for p in d if p[1]==y]
    print(y, x0, ''.join(d.get((x,y)) or '.' for x in range(x0,max(xs)+1)))
