"""Controle r4: alpha-diff met kleur_r3/silhouet_r3.txt, open randen, losse pixels, palet."""
H='/home/user/Pokemon-Fully-Ungrounded/docs/concept/sprites/kolibrie_pre/blender/A/'
sil=[l.rstrip('\n') for l in open(H+'kleur_r3/silhouet_r3.txt')][:64]
r=[l.rstrip('\n') for l in open(H+'kleur_r5/raster.txt')][:64]
r3=[l.rstrip('\n') for l in open(H+'kleur_r3/raster.txt')][:64]
CH='.123456789ABCDEF'
assert len(r)==64 and all(len(x)==64 for x in r)
assert all(c in CH for row in r for c in row)
diff=[(x,y) for y in range(64) for x in range(64) if (sil[y][x]=='#')!=(r[y][x]!='.')]
toeg=lambda x,y: (y==45 and 27<=x<=32 and r[44][x]!='.') or (x,y)==(45,42)
print('alpha-diff totaal:',len(diff),diff)
print('  buiten de toegestane zones:',[d for d in diff if not toeg(*d)])
print('pixels:',sum(c!='.' for row in r for c in row),'(silhouet r3:',sum(c=='#' for row in sil for c in row),')')
# snavel bevroren
SN={15:(12,12),16:(13,14),17:(14,17),18:(15,18),19:(16,18),20:(13,18),21:(15,17)}
sd=[(x,y) for y,(a,b) in SN.items() for x in range(a,b+1) if r[y][x]!={'A':'2'}.get(r3[y][x],r3[y][x])]
print('snavel afwijkend (vorm/kleur, A->2 toegestaan):',sd)
nb4=lambda x,y:[(r[y+dy][x+dx] if 0<=y+dy<64 and 0<=x+dx<64 else '.') for dx,dy in ((1,0),(-1,0),(0,1),(0,-1))]
OK_RAND=set('12')|set('CDFE9')   # omlijning; snavel/mond/poot/kap-selout
open_=[(x,y,r[y][x]) for y in range(64) for x in range(64) if r[y][x]!='.' and '.' in nb4(x,y) and r[y][x] not in OK_RAND]
print('open randen (licht vlak naast transparant):',open_)
sch=[(x,y,r[y][x]) for y in range(64) for x in range(64) if r[y][x] not in '.1' and x>=27 and (r[y][x+1]=='.' or r[y+1][x]=='.')]
print('schaduwkant (rechts/onder, x>=27) niet zwart:',sch)
los=[(x,y,r[y][x]) for y in range(64) for x in range(64) if r[y][x] in '34567BE' and r[y][x] not in nb4(x,y)]
print('losse pixels (geen 4-buur met dezelfde kleur):',los)
print('kleuren gebruikt:',sorted(set(c for row in r for c in row)-{'.'}))
