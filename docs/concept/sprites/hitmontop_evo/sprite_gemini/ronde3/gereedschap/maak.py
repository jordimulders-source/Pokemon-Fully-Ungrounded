# maak.py raster.txt uit.png : tekstraster -> geindexeerde png (index 0 transparant)
import sys; from PIL import Image
sys.path.insert(0,'/home/user/Pokemon-Fully-Ungrounded/docs/concept/sprites/hitmontop_evo/sprite_gemini/ronde3/gereedschap')
from palet import PAL,CH
R=[l.rstrip('\n') for l in open(sys.argv[1])][:64]
im=Image.new('P',(64,64)); flat=[v for p in PAL for v in p]; im.putpalette(flat)
for y,r in enumerate(R):
  for x,ch in enumerate(r.ljust(64,'.')[:64]): im.putpixel((x,y),CH.index(ch))
im.info['transparency']=0; im.save(sys.argv[2],transparency=0)
