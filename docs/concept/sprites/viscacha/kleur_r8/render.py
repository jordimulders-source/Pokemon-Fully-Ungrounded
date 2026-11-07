"""raster.txt -> viscacha.png (geindexeerd, index 0 transparant), normal.pal, viscacha_8x.png."""
import sys
from PIL import Image
D='/home/user/Pokemon-Fully-Ungrounded/docs/concept/sprites/viscacha/kleur_r8/'
sys.path.insert(0,D); from palet import PAL
r=[l.rstrip('\n') for l in open(D+'raster.txt')][:64]
assert len(r)==64 and all(len(x)==64 for x in r)
im=Image.new('P',(64,64)); im.putpalette([v for c in PAL for v in c]+[0]*(768-48))
im.putdata([0 if c=='.' else int(c,16) for row in r for c in row])
im.info['transparency']=0; im.save(D+'viscacha.png',transparency=0)
open(D+'normal.pal','w').write('JASC-PAL\r\n0100\r\n16\r\n'+''.join('%d %d %d\r\n'%c for c in PAL))
rgb=Image.new('RGB',(64,64)); rgb.putdata([(255,255,255) if c=='.' else PAL[int(c,16)] for row in r for c in row])
rgb.resize((512,512),Image.NEAREST).save(D+'viscacha_8x.png')
