"""Controle r7: alpha-diff met r6 S, lijst gewijzigde pixels (oud->nieuw) tegen het rapport, open randen, losse pixels, clusters."""
import sys, subprocess
A='/home/user/Pokemon-Fully-Ungrounded/docs/concept/sprites/kolibrie_pre/blender/A/'
sys.path.insert(0,A+'kleur_r7'); from reparaties import R
r=[l.rstrip('\n') for l in open(A+'kleur_r7/raster.txt')][:64]
o=[l.rstrip('\n') for l in open(A+'kleur_r6/raster_S.txt')][:64]
P=[(x,y) for y in range(64) for x in range(64)]
print('alpha-diff met r6 S:',sum((r[y][x]!='.')!=(o[y][x]!='.') for x,y in P))
rap={p:(k,c) for k,l in R.items() for p,c in l}
d=[(x,y) for x,y in P if r[y][x]!=o[y][x]]
print('gewijzigd:',len(d),'px (rapport: 36)')
for x,y in d: print(f'  ({x},{y}) {o[y][x]}->{r[y][x]}  {rap.get((x,y),("NIET IN RAPPORT",))[0]}')
print('rapportpixels die niets veranderden:',[p for p in rap if p not in d])
nb4=lambda x,y:[(r[y+dy][x+dx] if 0<=y+dy<64 and 0<=x+dx<64 else '.') for dx,dy in ((1,0),(-1,0),(0,1),(0,-1))]
print('open randen:',[(x,y,r[y][x]) for x,y in P if r[y][x]!='.' and '.' in nb4(x,y) and r[y][x] not in '12CD9'])
print('losse pixels (geen 4-buur zelfde index, vlaktinten):',[(x,y,r[y][x]) for x,y in P if r[y][x] in '345678ABE' and r[y][x] not in nb4(x,y)])
print(subprocess.run(['python3',A+'kleur_r7/clusters.py',A+'kleur_r7/raster.txt'],capture_output=True,text=True).stdout.strip())
print('F nog gebruikt:',sum(row.count('F') for row in r))
