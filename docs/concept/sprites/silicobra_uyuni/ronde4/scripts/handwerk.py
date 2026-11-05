# Ronde 4: met de hand getypte segmenten (x, tekst) op het raster van ronde 2. Streepje weg + halsband.
B='/home/user/Pokemon-Fully-Ungrounded/docs/concept/sprites/silicobra_uyuni/'
g=[list(l.rstrip('\n')) for l in open(B+'ronde2/silicobra_uyuni_raster.txt')][:64]
R={
15:[(19,'.')],
31:[(28,'ccddddd')],
32:[(25,'dddccccccddddee'),(40,'O')],
33:[(17,'t'),(18,'rqqq'),(22,'cdd'),(25,'ccccccccdddd'),(37,'sss'),(40,'t'),(41,'.')],
34:[(18,'traaqqrr'),(26,'ccccccdd'),(34,'rsssss'),(40,'t'),(41,'..')],
35:[(18,'trqqaaqrqr'),(28,'cccc'),(32,'rssssst'),(39,'t'),(40,'...')],
36:[(19,'t'),(20,'rqqqqrrrqrrrrrassst'),(39,'t'),(40,'..')],
37:[(20,'ts'),(22,'rrrrrrrrrr'),(32,'sssst'),(37,'t'),(38,'..')],
38:[(21,'tsss'),(25,'rrrrrrq'),(32,'sstt'),(36,'O'),(37,'..')],
39:[(23,'hdsss'),(28,'rrss'),(32,'tt'),(34,'e'),(35,'O'),(36,'..')],
40:[(23,'hcgff'),(28,'sstt'),(32,'dd'),(34,'O'),(35,'.')],
41:[(24,'hgffff'),(30,'ddde'),(34,'O'),(35,'.')],
42:[(31,'dd')],
43:[(31,'de')],
44:[(32,'e')],
}
for y,segs in R.items():
    for x,t in segs:
        for i,c in enumerate(t): g[y][x+i]=c
open(B+'ronde4/silicobra_uyuni_raster.txt','w').write('\n'.join(''.join(r) for r in g)+'\n')
for y in range(12,46): print('%2d'%y,''.join(g[y][14:48]))
