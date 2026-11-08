# ronde 6: reparaties K1-K4, L1-L3 uit KEURING_R5.md, pixel voor pixel op raster_r5.txt
g=[list(l.rstrip('\n')) for l in open('raster_r5.txt')]
def s(x,y,v,was=None):
    if was is not None: assert g[y][x]==was,(x,y,g[y][x],was)
    g[y][x]=v
# K1
for y in (26,27,28): s(32,y,'.'); s(31,y,'1')
# K2
for y in (34,35,36): s(31,y,'1'); s(32,y,'3')
s(30,37,'1'); s(31,37,'3')
for y in (38,39): s(29,y,'1'); s(30,y,'3')
s(28,40,'1'); s(29,40,'3'); s(28,32,'6','8')
# K3
for x,y in [(22,22),(23,22),(24,22),(22,23),(23,23),(24,23),(23,24),(24,24),(24,25),(25,25),(24,26),(25,26),(26,26),(25,27),(26,27),(27,27),(26,28),(27,28),(27,29),(27,30),(27,31)]: s(x,y,'4','6')
# K4
s(12,37,'1','9')
for x in range(13,19): s(x,37,'2','6')
s(13,38,'6','8'); s(14,38,'6','8')
for x in range(15,21): s(x,38,'2','8')
for x in range(21,25): s(x,38,'6','2')
s(25,38,'8','2')
for x,y in [(17,39),(18,39),(19,39),(18,40),(18,41)]: s(x,y,'6','8')
for x,y in [(23,39),(24,39),(25,39),(22,40),(23,40),(24,40),(22,41),(23,41)]: s(x,y,'8','6')
for y in range(34,38): s(27,y,'8','2')
# L1
for y in (43,44,45,46): s(29,y,'5','4')
# L2
for x,y in [(35,41),(36,41),(35,42)]: s(x,y,'3','4')
# L3
for y in (43,44,45): s(25,y,'1','.'); s(26,y,'3','1')
open('stappen/r6a.txt','w').write('\n'.join(''.join(r) for r in g)+'\n')
# Claude: 8-schaduw achter het oog als sikkel (binnenrand 29,28,27,27,28,28 op rij 32-37) i.p.v. evenwijdige band
g=[list(l.rstrip('\n')) for l in open('stappen/r6a.txt')]
s(27,36,'2','8'); s(27,37,'2','8')
open('raster_r6.txt','w').write('\n'.join(''.join(r) for r in g)+'\n')
