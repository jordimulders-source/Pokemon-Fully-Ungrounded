"""Controle r6 (S/M/L): alpha-diff met kleur_r4/silhouet_r4.txt, snavelzone gelijk aan r4, tintclusters < 3 px, open randen, tinten per kleurgroep, helderheidsstappen."""
import sys; sys.path.insert(0,'/home/user/Pokemon-Fully-Ungrounded/docs/concept/sprites/kolibrie_pre/blender/A/kleur_r6')
import subprocess, palet
A='/home/user/Pokemon-Fully-Ungrounded/docs/concept/sprites/kolibrie_pre/blender/A/'
r4=[l.rstrip('\n') for l in open(A+'kleur_r4/raster.txt')][:64]
sil=[l.rstrip('\n') for l in open(A+'kleur_r4/silhouet_r4.txt')][:64]
P=[(x,y) for y in range(64) for x in range(64)]
for m in 'SML':
    r=[l.rstrip('\n') for l in open(A+f'kleur_r6/raster_{m}.txt')][:64]
    nb4=lambda x,y:[(r[y+dy][x+dx] if 0<=y+dy<64 and 0<=x+dx<64 else '.') for dx,dy in ((1,0),(-1,0),(0,1),(0,-1))]
    print(f'== {m}: alpha-diff {sum((sil[y][x]=="#")!=(r[y][x]!=".") for x,y in P)}',
          '| snavelzone (x<=20, y13-22) afwijkend van r4:',[p for p in P if p[0]<=20 and 13<=p[1]<=22 and r[p[1]][p[0]]!=r4[p[1]][p[0]]],
          '| open randen:',[(x,y,r[y][x]) for x,y in P if r[y][x]!='.' and '.' in nb4(x,y) and r[y][x] not in '12CDF9'])
    print(subprocess.run(['python3',A+'kleur_r6/clusters.py',A+f'kleur_r6/raster_{m}.txt'],capture_output=True,text=True).stdout.strip())
L=lambda c: round(0.3*c[0]+0.59*c[1]+0.11*c[2])
GROEP={'kop/lijf lila':'543','buik':'765','vleugel':'8A','kap':'BE','omlijning':'21'}
for n,cs in GROEP.items(): print(n,'tinten',list(cs),'luma',[L(palet.PAL[palet.CH.index(c)]) for c in cs])
print('Taillow ter vergelijking: blauw 107/72/43 (+zwart 16), rood 123/87, wit 255/191')
