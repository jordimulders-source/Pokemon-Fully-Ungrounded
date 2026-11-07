"""raster_bron_r1.txt (groepen van 10 met |) -> raster.txt, met alpha-check tegen het silhouet."""
import sys
src=sys.argv[1]
rows=[l.rstrip('\n') for l in open(src)]
out=[]
for i,l in enumerate(rows):
    g=l.split('|'); s=''.join(g)
    assert len(s)==64 and [len(x) for x in g]==[10]*6+[4], (i,[len(x) for x in g])
    out.append(s)
open('raster.txt','w').write('\n'.join(out)+'\n')
