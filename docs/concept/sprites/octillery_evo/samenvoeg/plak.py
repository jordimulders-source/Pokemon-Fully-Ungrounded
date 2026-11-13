# Plakt het kanon (kanon_masker.png uit seg.py) uit r5 op r10. Gebruik: python3 plak.py [schaal] [ox] [oy]
import sys; from PIL import Image; import numpy as np
s=float(sys.argv[1]) if len(sys.argv)>1 else 1.24
a=np.asarray(Image.open('referenties/gemini_gekozen_r5.png').convert('RGB'))
M=np.asarray(Image.open('samenvoeg/kanon_masker.png'))>0
M&=a.min(axis=2)<235
ox=round(float(sys.argv[2])) if len(sys.argv)>2 else round(392-360*s); oy=round(float(sys.argv[3])) if len(sys.argv)>3 else round(221-200*s)
piece=Image.fromarray(np.dstack([a,M*255]).astype('uint8'),'RGBA').resize((round(1024*s),round(559*s)),Image.NEAREST)
out=Image.open('gemini/r10_rupsband.png').convert('RGBA'); out.alpha_composite(piece,(ox,oy))
out.convert('RGB').save('samenvoeg/v1.png')
