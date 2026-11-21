# zet.py raster.txt y x0 tekst : zet tekst op rij y vanaf kolom x0 (in-place)
import sys
f,y,x0,t=sys.argv[1],int(sys.argv[2]),int(sys.argv[3]),sys.argv[4]
R=[r.rstrip('\n') for r in open(f)]
r=list(R[y]); r[x0:x0+len(t)]=list(t); R[y]=''.join(r)[:38]
open(f,'w').write('\n'.join(R)+'\n')
