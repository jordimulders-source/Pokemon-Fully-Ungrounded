# fix.py: per-pixel reparaties op de kale reductie (raster_kaal.txt -> raster.txt), per zone gelogd
import sys
R=[list(l.rstrip('\n')) for l in open('../raster_kaal.txt')][:64]
def put(ch,pts):
    for x,y in pts: R[y][x]=ch
def hl(ch,y,xa,xb): put(ch,[(x,y) for x in range(xa,xb+1)])
def vl(ch,x,ya,yb): put(ch,[(x,y) for y in range(ya,yb+1)])
SELOUT=int(sys.argv[1]) if len(sys.argv)>1 else 1
R2=int(sys.argv[2]) if len(sys.argv)>2 else 1
OUT=sys.argv[3] if len(sys.argv)>3 else '../raster.txt'
exec(open('fixes.py').read())
open(OUT,'w').write('\n'.join(''.join(r) for r in R)+'\n')
