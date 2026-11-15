# python3 maker/plak.py basis.txt deel.txt x0 uit.txt : plakt regels "y tekst" vanaf kolom x0 (punten = basis houden)
import sys
B=[list(l.rstrip('\n')) for l in open(sys.argv[1])]; x0=int(sys.argv[3])
for l in open(sys.argv[2]):
  if not l.strip(): continue
  y,t=l.split(); y=int(y)
  for i,ch in enumerate(t):
    if ch!='.': B[y][x0+i]=ch
open(sys.argv[4],'w').write('\n'.join(''.join(r) for r in B)+'\n')
