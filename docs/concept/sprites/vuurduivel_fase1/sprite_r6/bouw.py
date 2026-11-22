# bouw.py RASTER.txt UIT.png: tekstraster -> 64x64 P-png (index 0 transparant)
# r6-palet: lijf lichter (Houndour/Umbreon), lijn (16,16,16); X = vlam-middentint = hoornlicht = tong (samengevoegd),
# g = glans op het lijf
import sys, numpy as np; from PIL import Image
CH='.#dmlRrOYbBkXWHg'
PAL=[(0,0,0),(16,16,16),(41,38,38),(66,62,62),(98,92,92),(108,19,20),(162,41,41),(242,113,57),(252,208,89),
     (76,51,36),(101,69,52),(139,102,75),(226,88,62),(248,246,236),(190,45,46),(139,131,131)]
rows=[r.rstrip('\n') for r in open(sys.argv[1])][:64]
o=np.array([[CH.index(c) for c in r.ljust(64,'.')[:64]] for r in rows],'uint8')
im=Image.fromarray(o,'P'); p=[c for t in PAL for c in t]; p+=[0]*(768-len(p)); im.putpalette(p); im.save(sys.argv[2],transparency=0,bits=4)
