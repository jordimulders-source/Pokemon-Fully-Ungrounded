# bouw.py RASTER.txt UIT.png: tekstraster -> 64x64 P-png (index 0 transparant)
import sys, numpy as np; from PIL import Image
CH='.#dgHhBcCRrOAY'
PAL=[(0,0,0),(3,1,1),(22,22,22),(40,40,40),(50,40,34),(80,64,52),(124,97,77),(218,184,134),(240,229,186),
     (105,20,22),(138,30,34),(205,75,50),(240,135,62),(250,205,110)]
rows=[r.rstrip('\n') for r in open(sys.argv[1])][:64]
o=np.array([[CH.index(c) for c in r.ljust(64,'.')[:64]] for r in rows],'uint8')
im=Image.fromarray(o,'P'); p=[c for t in PAL for c in t]; p+=[0]*(768-len(p)); im.putpalette(p); im.save(sys.argv[2],transparency=0,bits=4)
