# Ronde 2: met de hand getypte segmenten (x, tekst) per rij, bovenop rijen van ronde 1.
L=dict((int(l.split()[0]),l.split()[1]) for l in open('../ronde1/rijen_x12.txt') if l.strip())
for y in (42,43): L[y]='?'*40
def setr(y,x,s):
    r=list(L[y])
    for i,c in enumerate(s): r[x-12+i]=c
    L[y]=''.join(r)
R={
# --- korst en kuif: platen A (voor), B (boven oog), C1 (hoek), C2 (achter), D (groot achter-onder), F (naast oog)
14:[(24,'adaaaabb')],
15:[(21,'aabbdabbbbbda')],
16:[(21,'abbbcdabbbcdabbb')],
17:[(21,'bccccdbbbbbbdabbc'),(38,'O')],
18:[(26,'dbbbbccdbbbcc'),(39,'O')],
19:[(24,'drrrrd'),(30,'bbccdbbcce'),(40,'O')],
20:[(23,'drbbbbsd'),(31,'cccdbceebc'),(41,'O')],
21:[(23,'rcbbbbcs'),(31,'ccdbdebcccd'),(42,'O')],
22:[(22,'rcccccccs'),(31,'ddbbdbccccd'),(42,'O')],
23:[(22,'rOOccccOOs'),(32,'bbbcecccccd'),(43,'O')],
24:[(22,'rttOOOOtts'),(32,'bbcceccccd'),(42,'d'),(43,'O')],
25:[(22,'rsastOtss'),(31,'cbccecee'),(39,'ccccd'),(44,'O')],
26:[(23,'rqrrOrss'),(31,'cccceccceeccd'),(44,'O')],
27:[(25,'rqqrs'),(30,'fK'),(32,'ccecccccceed'),(44,'O')],
28:[(25,'rrss'),(29,'ff'),(31,'O'),(32,'cdeccccccccde'),(44,'O')],
29:[(26,'ss'),(30,'O'),(31,'cdeccccccccdd'),(44,'O')],
30:[(29,'O'),(30,'cdeccccccddd'),(43,'O')],
31:[(28,'tssssst'),(35,'cccddd'),(41,'O')],
# --- pekelzak
32:[(25,'trrrqqrrrrssscd'),(40,'O')],
33:[(18,'Oabbcddt'),(26,'raarrrrrrrrrsss'),(41,'O')],
34:[(19,'Kbbcdt'),(25,'rqrrrrrrrrrrrrsss'),(42,'O')],
35:[(19,'Kbcddt'),(25,'rqrrrrrrrrrrrrsss'),(42,'O')],
36:[(20,'Kcdt'),(24,'rrrrrrrrrrrrrssss'),(41,'O')],
37:[(21,'Ot'),(23,'rrrgg'),(28,'rrrrarrsssss')],
38:[(22,'Ot'),(24,'r'),(25,'fffg'),(29,'rrrssssrss')],
39:[(23,'Ot'),(25,'ffff'),(29,'rsqsssrst')],
40:[(23,'Ot'),(25,'gfffg'),(30,'sssstt')],
41:[(24,'Og'),(26,'ffff'),(30,'ssttt'),(35,'O')],
}
for y,segs in R.items():
    for x,s in segs: setr(y,x,s)
for y in sorted(L): assert len(L[y])==40,(y,len(L[y]))
open('rijen_x12.txt','w').write(''.join('%d %s\n'%(y,L[y]) for y in sorted(L)))
