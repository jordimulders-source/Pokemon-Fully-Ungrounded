# zet.py basis.txt bewerk.txt uit.txt : past met de hand geschreven pixelruns toe op een raster (alleen montage).
# Regelformaat: "rNN: kol=tekens kol=tekens ..." ; "rNN: wis" maakt de rij eerst leeg; "rNN: wis a-b" wist kolommen a..b.
import sys
R=[list(l.rstrip('\n').ljust(64,'.')[:64]) for l in open(sys.argv[1])][:64]
while len(R)<64: R.append(list('.'*64))
for l in open(sys.argv[2]):
  l=l.split('#')[0].strip()
  if not l: continue
  k,v=l.split(':',1); y=int(k[1:])
  for t in v.split():
    if t=='wis': R[y]=list('.'*64); continue
    if t.startswith('wis'): continue
    if '-' in t and '=' not in t:
      a,b=map(int,t.split('-')); 
      for x in range(a,b+1): R[y][x]='.'
      continue
    c,s=t.split('='); c=int(c)
    for i,ch in enumerate(s): R[y][c+i]=ch
open(sys.argv[3],'w').write('\n'.join(''.join(r) for r in R)+'\n')
