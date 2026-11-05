"""Controle r8 t.o.v. r7: alpha-diff alleen in de toegestane zones (met lijst), snavel en oog 0 px, open randen, losse pixels, clusters, rand aan de schaduwkant zwart."""
import subprocess
A='/home/user/Pokemon-Fully-Ungrounded/docs/concept/sprites/kolibrie_pre/blender/A/'
r=[l.rstrip('\n') for l in open(A+'kleur_r8/raster.txt')][:64]
o=[l.rstrip('\n') for l in open(A+'kleur_r7/raster.txt')][:64]
P=[(x,y) for y in range(64) for x in range(64)]
ZONES={'buik links':(16,24,26,36),'pootjes':(24,36,43,46),'vleugelschaduw':(32,41,28,37),'rug':(34,39,24,26),'kop linksboven':(18,20,14,15),'vleugelpunt':(38,41,42,43)}
zone=lambda x,y: next((n for n,(a,b,c,d) in ZONES.items() if a<=x<=b and c<=y<=d),None)
ad=[(x,y) for x,y in P if (r[y][x]!='.')!=(o[y][x]!='.')]
print('alpha-diff met r7:',len(ad),'px; buiten zones:',[p for p in ad if not zone(*p)])
for n in ZONES: print(f'  {n}: +{sum(1 for p in ad if zone(*p)==n and r[p[1]][p[0]]!=".")} / -{sum(1 for p in ad if zone(*p)==n and r[p[1]][p[0]]==".")}',[p for p in ad if zone(*p)==n])
d=[(x,y) for x,y in P if r[y][x]!=o[y][x]]
print('kleur/alpha gewijzigd:',len(d),'px; buiten zones:',[p for p in d if not zone(*p)])
SN={15:(12,12),16:(13,14),17:(14,17),18:(15,18),19:(16,18),20:(13,18),21:(15,17)}
print('snavel (pixels uit r4) en oog (x21-25, y17-21) gewijzigd:',[p for p in d if (p[1] in SN and SN[p[1]][0]<=p[0]<=SN[p[1]][1]) or (21<=p[0]<=25 and 17<=p[1]<=21)])
nb4=lambda x,y:[(r[y+dy][x+dx] if 0<=y+dy<64 and 0<=x+dx<64 else '.') for dx,dy in ((1,0),(-1,0),(0,1),(0,-1))]
print('open randen:',[(x,y,r[y][x]) for x,y in P if r[y][x]!='.' and '.' in nb4(x,y) and r[y][x] not in '12CD9F'])
print('rand rechts/onder (x>=26) niet zwart:',[(x,y,r[y][x]) for x,y in P if r[y][x] not in '.1' and x>=26 and (r[y][x+1]=='.' or r[y+1][x]=='.')])
print(subprocess.run(['python3',A+'kleur_r8/clusters.py',A+'kleur_r8/raster.txt'],capture_output=True,text=True).stdout.strip())
print('pixels:',sum(c!='.' for row in r for c in row),'(r7:',sum(c!='.' for row in o for c in row),')')
