# r19: keuring r18 top-5, elk punt gemeten op het model (stappen/px.py, nerfmeting in NOTITIES)
import os
H=os.path.dirname(os.path.abspath(__file__))
R=[list(l.rstrip('\n')) for l in open(os.path.join(H,'basis.txt'))]
Z=set(tuple(map(int,l.split(','))) for l in open(os.path.join(H,'..','spriet_zone.txt')))
F={}
def put(x,y,c): F[(x,y)]=c; R[y][x]=c
# 2 ooglichten
for p in [(17,34),(17,35)]: put(*p,'1')
for p in [(18,34),(18,35)]: put(*p,'A')
for p in [(27,34),(28,34)]: put(*p,'1')
for p in [(27,35),(28,35),(27,36)]: put(*p,'A')
# 3 tan ring rechteroog
for y in (34,35,36,37): put(32,y,'6')
for y in (35,36): put(33,y,'4')
# 4 kraag y43-45 wit, haarstreken op de modelplekken
for x in range(20,36): put(x,43,'A')
for y in (44,45):
    for x in range(16,40):
        if R[y][x]=='7': put(x,y,'A')
for p in [(22,43),(23,43),(22,44),(32,44),(32,45),(32,46),(35,44),(35,45),(36,45),(36,46),(18,45)]: put(*p,'7')
# kin en snuit
for p in [(18,41),(19,41)]: put(*p,'A')
put(20,40,'7'); put(26,42,'7'); put(25,41,'3'); put(26,41,'3')
for x in range(20,25): put(x,39,'7')
put(24,40,'7')
# 5 losse lijnpixels waar het model licht is
for p in [(59,24),(60,24)]: put(*p,'D')
for p in [(58,29),(59,29)]: put(*p,'A')
put(54,37,'A'); put(12,29,'7')
put(39,35,'7'); put(40,35,'7')          # model 204/215: licht (r18 was fout); (38-41,34) blijft zwart (77/74/115/135)
put(30,48,'9'); put(35,48,'7'); put(29,53,'7'); put(46,56,'D')
# 1 sprietnerf op de modelboog, baardjes opnieuw
NERF=[(4,18),(5,18),(6,19),(7,19),(8,19),(9,20),(10,20),(11,20),(12,21),(13,21),(14,22),(15,23),(16,23),(17,24),(18,25),(19,26),
      (30,27),(31,26),(32,25),(33,24),(34,23),(35,23),(36,22),(37,22)]+[(x,21) for x in range(38,42)]+[(x,20) for x in range(42,46)]+[(x,19) for x in range(46,52)]
def ch(x,y): return R[y][x] if 0<=x<64 and 0<=y<64 else '.'
for (x,y) in Z:
    if R[y][x] in 'C6': put(x,y,'1')
for (x,y) in NERF:
    assert (x,y) in Z, (x,y)
    put(x,y,'C')
for (x,y) in Z:
    if R[y][x] not in '14': continue
    nb=[ch(x+dx,y+dy) for dx,dy in ((1,0),(-1,0),(0,1),(0,-1))]
    if '.' in nb or 'C' in nb: put(x,y,'1'); continue
    s=(x+y//3)%3==0 if x<24 else (x-y//2)%3==1
    put(x,y,'6' if s else '1')
W={}
for (x,y),c in F.items(): W.setdefault(y,[]).append((x,c))
