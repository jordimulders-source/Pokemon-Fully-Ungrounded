"""raster.txt -> viscacha.png (geindexeerd), normal.pal, en een 8x-preview naast de bron64."""
import sys
from PIL import Image
D='/home/user/Pokemon-Fully-Ungrounded/docs/concept/sprites/viscacha/kleur_r6/'
sys.path.insert(0,D); from palet import PAL
r=[l.rstrip('\n') for l in open(D+'raster.txt')][:64]
im=Image.new('P',(64,64)); im.putpalette([v for c in PAL for v in c])
im.putdata([0 if c=='.' else int(c,16) for row in r for c in row])
im.info['transparency']=0; im.save(D+'viscacha.png',transparency=0)
open(D+'normal.pal','w').write('JASC-PAL\r\n0100\r\n16\r\n'+''.join('%d %d %d\r\n'%c for c in PAL))
bg=Image.new('RGB',(64,64),(255,255,255))
bg.putdata([(255,255,255) if c=='.' else PAL[int(c,16)] for row in r for c in row])
src=Image.open(D+'gemini64.png').convert('RGB')
W=Image.new('RGB',(512*2+16+128,512),'white'); W.paste(bg.resize((512,512),Image.NEAREST),(0,0)); W.paste(src.resize((512,512),Image.NEAREST),(528,0))
W.paste(bg,(1040,0)); W.paste(bg.resize((128,128),Image.NEAREST),(1040,80))
W.save('/tmp/claude-0/-home-user-Pokemon-Fully-Ungrounded/233aecfd-d2f5-59c9-a0e1-17e5813db81d/scratchpad/prev.png')
