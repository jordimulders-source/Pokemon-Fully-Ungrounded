"""r10 = kleur_r9/raster.txt + hals->borst links (zone x16-21, y24-28): lichte holle inkeping (linkerrand 16,16,17,18,19,19 dan 18 = de bestaande buik),
met een tapse schaduw 5 in de holte onder de kin. Rest pixel voor pixel r9."""
import sys
A='/home/user/Pokemon-Fully-Ungrounded/docs/concept/sprites/kolibrie_pre/blender/A/'
g=[list(l.rstrip('\n')) for l in open(A+'kleur_r9/raster.txt')][:64]
STUK=[  # y, x0, pixels ('.' = transparant)
 (24,16,'.2'),
 (25,16,'..255'),
 (26,17,'..25'),
 (27,17,'..25'),
 (28,17,'.2'),
]
for y,x0,p in STUK:
    for i,c in enumerate(p): g[y][x0+i]=c
open(A+'kleur_r10/raster.txt','w').write('\n'.join(''.join(r) for r in g)+'\n')
sys.path.insert(0,A+'kleur_r10'); import palet; palet.build(A+'kleur_r10/raster.txt',A+'kleur_r10/kolibrie_pre.png')
