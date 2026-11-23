# bouw.py: grid.txt (hex per pixel, '.'=0) + palet -> gnometrotter_rock.png
import numpy as np; from PIL import Image
PAL=Image.open('../sprite_r8/r7b_basis.png').getpalette()[:48]
import json,os
if os.path.exists('palet.json'): PAL=sum(json.load(open('palet.json')),[])
rows=[l.rstrip('\n') for l in open('grid.txt') if l.strip()]
a=np.array([[0 if c=='.' else int(c,16) for c in r] for r in rows],'uint8'); assert a.shape==(64,64),a.shape
p=Image.fromarray(a,'P'); p.putpalette(PAL+[0]*(768-len(PAL))); p.save('gnometrotter_rock.png',transparency=0)
