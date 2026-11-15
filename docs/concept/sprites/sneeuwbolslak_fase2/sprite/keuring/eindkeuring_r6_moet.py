# Hulpscript bij EINDKEURING_r6 (alleen MOET M1-M3a). Gebruik vanuit sneeuwbolslak_fase2/: python3 sprite/keuring/eindkeuring_r6_moet.py uit.txt uit.png
import sys; sys.path.insert(0,'sprite/maker')
from pal6 import PAL
from PIL import Image
rows=[list(r) for r in open('sprite/maker/raster_r6.txt').read().split()]
M=[ # (x,y,van,naar)
# M1 barst
(35,26,'#','d'),(35,27,'#','d'),(35,28,'#','d'),(34,29,'#','d'),(36,29,'#','d'),(32,30,'#','d'),(33,30,'#','d'),(36,30,'#','d'),(31,31,'#','d'),(37,31,'#','d'),(30,32,'#','d'),(37,32,'#','d'),(37,33,'#','d'),(36,34,'#','d'),(36,35,'#','d'),(36,36,'b','d'),(37,37,'b','d'),(37,36,'d','a'),
# M2 rechterrand glas
(39,25,'a','b'),(40,26,'a','b'),(40,27,'a','b'),(40,28,'a','c'),(40,29,'b','c'),(41,29,'a','c'),(41,30,'a','e'),(41,31,'a','e'),(41,32,'a','c'),
(39,33,'a','b'),(40,33,'a','c'),(39,34,'a','b'),(40,34,'a','c'),(39,35,'a','b'),(40,35,'a','c'),(39,36,'a','e'),(40,36,'a','b'),(38,37,'a','e'),(39,37,'a','c'),(38,38,'a','c'),
# M3 storm
(35,24,'e','c'),(39,24,'e','c'),(34,25,'c','b'),(35,25,'c','b'),(37,25,'c','b'),(38,25,'c','b'),

(27,29,'b','e'),(29,29,'e','c'),(30,29,'e','c'),(31,29,'e','c'),(35,29,'e','b'),
(23,30,'c','b'),(27,30,'c','b'),(28,30,'c','b'),(29,30,'c','b'),(31,30,'e','c'),(34,30,'e','b'),(35,30,'e','b'),
(25,32,'e','b'),(27,33,'c','w'),
(30,34,'c','b'),(34,34,'c','e'),(35,34,'c','b'),(31,35,'c','e'),(34,35,'c','e'),(35,35,'c','b'),(33,37,'e','w'),(37,34,'c','e'),
]
bad=0
for x,y,a,b in M:
    if rows[y][x]!=a: print('MISMATCH',x,y,rows[y][x],a); bad+=1
    rows[y][x]=b
print(len(M),'pixels, mismatch',bad)
open(sys.argv[1],'w').write('\n'.join(''.join(r) for r in rows)+'\n')
im=Image.new('RGB',(64,64),(255,255,255))
for y in range(64):
  for x in range(64):
    if rows[y][x]!='.': im.putpixel((x,y),PAL[rows[y][x]])
im.save(sys.argv[2])
