"""Handmatige pixelcorrecties: fix.py bestand  'x,y=c' ... (globale coördinaten)"""
import sys
f=sys.argv[1]; L=[list(l.rstrip('\n')) for l in open(f)]
for a in sys.argv[2:]:
    xy,c=a.split('='); x,y=map(int,xy.split(','))
    for i,ch in enumerate(c): L[y][x+i]=ch
open(f,'w').write('\n'.join(''.join(r) for r in L)+'\n')
