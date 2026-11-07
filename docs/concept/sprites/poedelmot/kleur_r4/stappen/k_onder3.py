import math
DIAG={30:37,31:37,32:38,33:38,34:38,35:38,36:39,37:39,38:39,39:39,40:40,41:40,42:40,43:40,44:41,45:41,46:41,47:41}
B=[('E',49.5,50.2,4.6,4.6),('D',44.3,55.2,3.3,4.1),('b',28.0,57.2,3.0,2.3),('A',18.3,51.6,3.3,4.3),('B',26.3,52.1,4.2,4.4),('C',37.8,57.0,3.3,3.9)]
own={}
for n,cx,cy,rx,ry in B:
    for y in range(44,62):
        for x in range(12,57):
            if r[y][x]!='.' and ((x-cx)/rx)**2+((y-cy)/ry)**2<=1.0: own[(x,y)]=n
# 1) achterlijf: alles onder de kraag (y>=47, x30-44) dat geen pluim is
for y in range(46,58):
    for x in range(29,46):
        if r[y][x]=='.' or (x,y) in own: continue
        if y<47 and x<=DIAG.get(y,41): continue
        if y==46 and x>=42: continue
        ring=[49+round(((x-36)/3.2)**2), 52+round(((x-36)/3.2)**2)]
        c='7' if (x-33)+(y-47)*0.8<3 else '6'
        if y in ring and 32<=x<=40: c='5'
        if y>=55 or (x>=41 and y>=50): c='5'
        r[y][x]=c
# 2) kraag-onderrand (y47) wit met sikkel, boven de pluimen
for x in range(16,30):
    if r[47][x]!='.' and (x,47) not in own: r[47][x]='A' if x<26 else '9'
# 3) pluimen, van achter naar voor
for n,cx,cy,rx,ry in B:
    for (x,y),m in own.items():
        if m!=n: continue
        u=(x-cx)/rx; v=(y-cy)/ry; rr=math.hypot(u,v); lit=-0.6*u-0.8*v
        c='A'
        if lit<-0.25: c='9'
        if rr>0.75 and lit<-0.5: c='8'
        # slagschaduw van de kraag op de bovenkant van A en B
        if n in 'AB' and y<=47: c='9'
        nb=[(x+dx,y+dy) for dx,dy in ((1,0),(-1,0),(0,1),(0,-1))]
        rand=[q for q in nb if own.get(q)!=n and r[q[1]][q[0]]!='.']
        if rand and (u+v)>0.1: c='3'                # contour alleen rechtsonder, waar de pluim over iets anders valt
        r[y][x]=c
# 3b) overlap: achterste pluim krijgt koele slagschaduw naast de voorste
order=[b[0] for b in B]
for (x,y),m in list(own.items()):
    for dx,dy in ((1,0),(-1,0),(0,1),(0,-1),(1,1),(-1,1)):
        q=(x+dx,y+dy); n2=own.get(q)
        if n2 and n2!=m and order.index(n2)>order.index(m) and r[y][x] in 'A9':
            r[y][x]='8'; break
# 4) klauwtjes schuin, klein, verre hoger en donkerder
for (x,y,c) in [(18,55,'2'),(19,55,'4'),(20,55,'3'),(19,56,'4'),(20,56,'3'),(20,57,'2'),
                (22,55,'2'),(23,55,'4'),(24,55,'3'),(23,56,'3'),(24,56,'2'),
                (25,58,'4'),(24,59,'3'),(25,59,'4'),(26,59,'2'),
                (32,57,'3'),(33,57,'4'),(33,58,'2'),
                (35,60,'2'),(36,60,'4'),(37,60,'3'),(38,60,'4'),(39,60,'2'),(36,61,'3'),(37,61,'2'),(38,61,'3'),(39,61,'2'),
                (43,58,'2'),(44,58,'4'),(45,58,'4'),(46,58,'2'),(43,59,'3'),(44,59,'4'),(45,59,'2')]:
    r[y][x]=c
