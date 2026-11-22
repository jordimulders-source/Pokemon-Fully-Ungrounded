# bouw.py RASTER.txt UIT.png: tekstraster -> 64x64 P-png (index 0 transparant)
import sys, numpy as np; from PIL import Image
CH='.#dmlRrOYbBkpWM'
PAL=[(0,0,0),(3,1,1),(27,26,25),(51,50,50),(72,72,71),(108,19,20),(162,41,41),(242,113,57),(252,208,89),
     (76,51,36),(101,69,52),(139,102,75),(198,98,92),(248,246,236),(127,56,50)]
rows=[r.rstrip('\n') for r in open(sys.argv[1])][:64]
o=np.array([[CH.index(c) for c in r.ljust(64,'.')[:64]] for r in rows],'uint8')
im=Image.fromarray(o,'P'); p=[c for t in PAL for c in t]; p+=[0]*(768-len(p)); im.putpalette(p); im.save(sys.argv[2],transparency=0,bits=4)
