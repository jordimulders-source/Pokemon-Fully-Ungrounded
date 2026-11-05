"""Ronde 5: de 29 px uit kleur_r4/KEURING.md (verse eindkeurder) letterlijk toegepast op r4. Controleert de oude waarde."""
g = [list(l.rstrip('\n')) for l in open('../kleur_r4/raster.txt')][:64]
R = [  # (x, y, oud, nieuw)
 (14,14,'D','1'), (15,15,'2','C'),
 (23,40,'2','1'), (24,40,'2','1'), (35,40,'2','1'), (39,41,'2','1'), (25,9,'1','2'), (26,9,'1','2'),
 (36,39,'2','3'), (37,39,'2','3'),
 (31,43,'A','1'), (32,43,'1','A'),
 *[(x,y,'4','B') for x,y in [(32,31),(33,32),(33,33),(34,34),(35,35),(35,36),(36,37),(37,38)]],
 *[(x,y,'B','E') for x,y in [(37,29),(38,30),(38,31),(38,32),(39,33)]], (36,25,'E','B'), (37,26,'E','B'),
 (17,36,None,'.'), (18,36,'6','2'),
]
fout = []
for x, y, oud, nieuw in R:
    if oud is not None and g[y][x] != oud: fout.append((x, y, g[y][x], oud))
    g[y][x] = nieuw
print('aantal', len(R), 'afwijkende oude waarden', fout)
open('raster.txt', 'w').write('\n'.join(''.join(r) for r in g) + '\n')
