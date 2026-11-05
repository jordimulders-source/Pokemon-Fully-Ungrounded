"""Controle r10: diff met r9 buiten de zone (x16-21, y24-28) = 0, lijst van elke gewijzigde pixel, linkerrand per rij, open randen, losse pixels/clusters."""
import subprocess
A='/home/user/Pokemon-Fully-Ungrounded/docs/concept/sprites/kolibrie_pre/blender/A/'
r=[l.rstrip('\n') for l in open(A+'kleur_r10/raster.txt')][:64]
o=[l.rstrip('\n') for l in open(A+'kleur_r9/raster.txt')][:64]
P=[(x,y) for y in range(64) for x in range(64)]
zone=lambda x,y: 16<=x<=21 and 24<=y<=28
d=[(x,y) for x,y in P if r[y][x]!=o[y][x]]
print('gewijzigd:',len(d),'px; buiten de zone:',[p for p in d if not zone(*p)])
for x,y in d: print(f'  ({x},{y}) {o[y][x]}->{r[y][x]}')
print('alpha-diff met r9:',sum((r[y][x]!='.')!=(o[y][x]!='.') for x,y in P),'| pixels:',sum(c!='.' for row in r for c in row))
print('linkerrand per rij (y21-41), r9 -> r10:')
for y in range(21,42): print(f'  {y}: {min(x for x in range(15,64) if o[y][x]!=".")} -> {min(x for x in range(15,64) if r[y][x]!=".")}')
nb4=lambda x,y:[(r[y+dy][x+dx] if 0<=y+dy<64 and 0<=x+dx<64 else '.') for dx,dy in ((1,0),(-1,0),(0,1),(0,-1))]
print('open randen:',[(x,y,r[y][x]) for x,y in P if r[y][x]!='.' and '.' in nb4(x,y) and r[y][x] not in '12CD9F'])
print(subprocess.run(['python3',A+'kleur_r10/clusters.py',A+'kleur_r10/raster.txt'],capture_output=True,text=True).stdout.strip())
