"""Handmatige herteken-stappen op raster.txt: SET(y, x0, tekens); spatie = laten staan."""
import sys
f=sys.argv[1]
r=[list(l.rstrip('\n')) for l in open(f)][:64]
def SET(y,x0,s):
    for i,c in enumerate(s):
        if c==' ': continue
        if r[y][x0+i]=='.' and c!='.': raise SystemExit(f'SET op transparant {x0+i},{y}')
        if c=='.' and r[y][x0+i]!='.': raise SystemExit(f'SET maakt gat {x0+i},{y}')
        r[y][x0+i]=c
exec(open(sys.argv[2]).read())
open(f,'w').write('\n'.join(''.join(l) for l in r)+'\n')
