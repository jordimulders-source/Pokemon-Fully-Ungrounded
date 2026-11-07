# pas_toe.py basis.txt hand.txt uit.txt [overslaan-nummers] : zet de handlijst op het raster, controleert de oude waarde
import sys
R=[list(l.rstrip('\n').ljust(64,'.')) for l in open(sys.argv[1])][:64]
skip=set(sys.argv[4].split(',')) if len(sys.argv)>4 else set()
for l in open(sys.argv[2]):
  if l.startswith('#') or not l.strip(): continue
  n,xy,ch=l.split(); x,y=map(int,xy.split(',')); o,nw=ch.split('->')
  if n in skip: continue
  assert R[y][x]==o,(l,R[y][x]); R[y][x]=nw
open(sys.argv[3],'w').write('\n'.join(''.join(r) for r in R)+'\n')
