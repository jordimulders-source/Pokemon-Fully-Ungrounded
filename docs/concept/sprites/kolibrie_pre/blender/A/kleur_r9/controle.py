"""Controle r9: elke gewijzigde pixel t.o.v. r8 (oud->nieuw) tegen het rapport, open randen, losse pixels/clusters."""
import sys, subprocess
A='/home/user/Pokemon-Fully-Ungrounded/docs/concept/sprites/kolibrie_pre/blender/A/'
sys.path.insert(0,A+'kleur_r9'); from reparaties import R
r=[l.rstrip('\n') for l in open(A+'kleur_r9/raster.txt')][:64]
o=[l.rstrip('\n') for l in open(A+'kleur_r8/raster.txt')][:64]
P=[(x,y) for y in range(64) for x in range(64)]
rap={p:(k,'.' if c=='0' else c) for k,l in R.items() for p,c in l}
d=[(x,y) for x,y in P if r[y][x]!=o[y][x]]
print('gewijzigd:',len(d),'px (rapport 42 + optioneel 2 = 44 genoemd)')
for x,y in d: print(f'  ({x},{y}) {o[y][x]}->{r[y][x]}  {rap.get((x,y),("NIET IN RAPPORT",))[0]}')
print('niet in rapport:',[p for p in d if p not in rap])
print('rapportpixels zonder effect (stond al zo):',[(p,o[p[1]][p[0]]) for p in rap if p not in d])
print('alpha-diff met r8:',sum((r[y][x]!='.')!=(o[y][x]!='.') for x,y in P),'| pixels:',sum(c!='.' for row in r for c in row))
nb4=lambda x,y:[(r[y+dy][x+dx] if 0<=y+dy<64 and 0<=x+dx<64 else '.') for dx,dy in ((1,0),(-1,0),(0,1),(0,-1))]
print('open randen:',[(x,y,r[y][x]) for x,y in P if r[y][x]!='.' and '.' in nb4(x,y) and r[y][x] not in '12CD9F'])
print('losse pixels (vlaktinten):',[(x,y,r[y][x]) for x,y in P if r[y][x] in '345678ABE' and r[y][x] not in nb4(x,y)])
print(subprocess.run(['python3',A+'kleur_r9/clusters.py',A+'kleur_r9/raster.txt'],capture_output=True,text=True).stdout.strip())
