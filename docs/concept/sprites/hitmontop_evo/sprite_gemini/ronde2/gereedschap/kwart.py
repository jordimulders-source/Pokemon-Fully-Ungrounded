# kwart.py raster.txt uit.txt : variant 'arm een kwart korter' = hoofdversie met 1 rij extra armlengte.
# Bovenlijf (alles behalve de onderarm/polsband/hand: kolommen 27-37 vanaf rij 47) gaat 1 rij omhoog;
# de vrijgekomen rij 46 in kolommen 27-37 krijgt een kopie van armrij 47. Diff 0 op alle andere pixels (alleen verschoven).
import sys
R=[list(l.rstrip('\n')) for l in open(sys.argv[1])]
assert all(c=='.' for c in R[0])
N=[['.']*64 for _ in range(64)]
L=lambda x,y: y>=47 and 27<=x<=37
for y in range(64):
  for x in range(64):
    if R[y][x]=='.': continue
    if L(x,y): N[y][x]=R[y][x]
    else: N[y-1][x]=R[y][x]
for x in range(27,38):
  if N[46][x]=='.': N[46][x]=R[47][x]
open(sys.argv[2],'w').write('\n'.join(''.join(r) for r in N)+'\n')
