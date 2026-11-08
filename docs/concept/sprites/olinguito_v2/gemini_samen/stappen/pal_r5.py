# r5: index 5 (lijf-hooglicht) lichter: (138,96,62) -> (158,111,71), stap ±39 i.p.v. ±27 boven index 4
import sys
from PIL import Image
p=sys.argv[1]; im=Image.open(p); pal=im.getpalette()[:48]; pal[15:18]=[158,111,71]; im.putpalette(pal); im.save(p,transparency=0)
