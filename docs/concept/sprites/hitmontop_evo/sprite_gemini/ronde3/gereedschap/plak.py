# plak.py basis.txt blok.txt uit.txt : plakt een met de hand geschreven blok ("rij tekens", start kolom 5; '~' en spatie = laat staan)
import sys
R=[list(l.rstrip('\n').ljust(64,'.')[:64]) for l in open(sys.argv[1])][:64]
for l in open(sys.argv[2]):
  if l.startswith('#') or not l.strip(): continue
  y,s=l.rstrip('\n').split(' ',1); y=int(y)
  for i,ch in enumerate(s):
    if ch in '~ ': continue
    R[y][5+i]=ch
open(sys.argv[3],'w').write('\n'.join(''.join(r) for r in R)+'\n')
