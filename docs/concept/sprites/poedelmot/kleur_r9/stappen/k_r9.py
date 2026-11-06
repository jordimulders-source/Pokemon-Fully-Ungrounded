def P(c,pts):
    for x,y in pts:
        if r[y][x]!='.': r[y][x]=c
# 4. kinboog vloeiend (2-6-2) en vachtplukjes in de kraag
for y in (41,42,43):
    for x in range(17,32):
        if r[y][x] in '34': r[y][x]='A'
P('4',[(18,41)]); P('3',[(19,41),(20,41),(21,42),(22,42),(23,42),(24,42),(25,42),(26,42),(27,41),(28,41)])
for pl in [[(17,45),(18,45),(18,46)],[(24,45),(25,45),(25,46)],[(31,44),(32,44),(32,45)],[(20,43),(21,43),(21,44)]]:
    P('7',pl)
# 5. buik: bolle segmentplaten (naden buigen omlaag naar het midden)
for y in range(47,57):
    for x in range(30,42):
        if r[y][x] in '5679':
            K=lambda xx: round(((xx-36)/3.5)**2) if 32<=xx<=40 else 99
            ks={K(x)} | ({K(x+1)} if x<36 and K(x+1)<99 else set()) | ({K(x-1)} if x>36 and K(x-1)<99 else set())
            naad=any(y in (50-k,53-k) for k in ks)
            r[y][x]='6' if naad else '7'
# klauwtjes: twee klauwtjes per poot (diagonale stompjes 2), daartussen 3; geen 4 op de rand
KL={1:[(18,55),(19,55),(20,55),(19,56),(20,56),(20,57)],2:[(22,55),(23,55),(24,55),(23,56),(24,56)],
    3:[(25,58),(24,59),(25,59),(26,59)],4:[(32,57),(33,57),(33,58)],
    5:[(35,60),(36,60),(37,60),(38,60),(39,60),(36,61),(37,61),(38,61),(39,61)],
    6:[(43,58),(44,58),(45,58),(46,58),(43,59),(44,59),(45,59)]}
KLAUW={(18,55),(19,56),(20,57),(20,55),(22,55),(23,56),(24,55),(24,59),(26,59),(32,57),(33,58),(35,60),(36,61),(38,60),(39,61),(43,58),(43,59),(45,58),(45,59)}
for g in KL.values():
    for p in g:
        if r[p[1]][p[0]]!='.': r[p[1]][p[0]]='2' if p in KLAUW else '3'
# 3. tinten: crème max 3 tinten (A/7/6), 9->7, 5->6, grijs 8 weg
Z=set(tuple(map(int,l.split(','))) for l in open('spriet_zone.txt'))
for y in range(64):
    for x in range(64):
        c=r[y][x]
        if c=='9': r[y][x]='A' if x>=40 and y<=46 else '7'      # vleugelvlak licht (wit-crème zoals het model)
        elif c=='5' and (x,y) not in Z: r[y][x]='6'
        elif c=='8': r[y][x]='3' if y>=55 else '7'
P('7',[(21,41),(22,41),(23,41),(24,41),(25,41),(26,41)])
from collections import Counter
for x,y in [(56,42),(57,35),(58,35)]:
    c=Counter(r[y+dy][x+dx] for dx,dy in ((1,0),(-1,0),(0,1),(0,-1)) if r[y+dy][x+dx] in '67A' and r[y+dy][x+dx]!=r[y][x])
    if c: r[y][x]=c.most_common(1)[0][0]
P('3',[(25,57)]); P('A',[(29,48)])
for x,y in [(53,21),(54,21),(51,22),(52,22),(60,29),(56,39)]: r[y][x]='6'
