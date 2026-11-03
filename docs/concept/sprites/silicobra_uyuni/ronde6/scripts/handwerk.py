# Ronde 6 (vanaf 5A): gezichtslijn zoals de originele Silicobra (zachter) + bovenrand band hoger. Met de hand getypte pixels.
B='/home/user/Pokemon-Fully-Ungrounded/docs/concept/sprites/silicobra_uyuni/'
g=[list(l.rstrip('\n')) for l in open(B+'ronde5/silicobra_uyuni_raster.txt')][:64]
def s(y,x,t):
    for i,c in enumerate(t): g[y][x+i]=c
# 1. gezichtslijn (loop van het origineel: index 3/2 tussen gezicht en achterkop), middentint e, onderaan h
LIJN=[(21,17),(22,17),(23,17),(24,17),(25,17),(26,18),(27,18),(29,19),(31,21),(32,22),(32,23),(32,24),(32,25),(32,26),(31,27)]
for x,y in LIJN: g[y][x]='e'
for x,y in LIJN:
    if y>=21: g[y][x]='h'          # zijkant: een tint donkerder dan de bovenkant, nog steeds lichter dan de buitenrand (O)
g[28][31]='h'; g[29][30]='h'
# wang tussen oogring en lijn terug in gezichtskleur, zoals in het origineel (index 6)
g[22][31]='f'; g[25][31]='f'; g[26][31]='f'
# 2. bovenrand band hoger
s(32,34,'rrssss')
s(33,18,'rqqqqqqqrr'); s(33,28,'cccc'); s(33,32,'rrrrssss')
s(34,19,'rqaaaqqqrqrrrrrrsssss')
s(35,28,'r')
open(B+'ronde6/silicobra_uyuni_raster.txt','w').write('\n'.join(''.join(r) for r in g)+'\n')
