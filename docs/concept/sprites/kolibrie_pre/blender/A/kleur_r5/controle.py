"""Controle r5: alpha-diff met kleur_r4/silhouet_r4.txt, snavelzone en rest pixel voor pixel gelijk aan r4, oog = r10, open randen, losse pixels."""
A='/home/user/Pokemon-Fully-Ungrounded/docs/concept/sprites/kolibrie_pre/'
r=[l.rstrip('\n') for l in open(A+'blender/A/kleur_r5/raster.txt')][:64]
r4=[l.rstrip('\n') for l in open(A+'blender/A/kleur_r4/raster.txt')][:64]
sil=[l.rstrip('\n') for l in open(A+'blender/A/kleur_r4/silhouet_r4.txt')][:64]
r10=[l.rstrip('\n') for l in open(A+'maker/kleur_r10/raster.txt')][:64]
P=[(x,y) for y in range(64) for x in range(64)]
print('alpha-diff met silhouet_r4:',sum((sil[y][x]=='#')!=(r[y][x]!='.') for x,y in P))
snavel=[(x,y) for x,y in P if x<=20 and 13<=y<=22]
print('snavelzone (x<=20, y13-22) afwijkend van r4:',[p for p in snavel if r[p[1]][p[0]]!=r4[p[1]][p[0]]])
oog=lambda x,y: 21<=x<=25 and 16<=y<=21
vleugel=lambda x,y: 31<=x<=41 and 27<=y<=42
d=[(x,y) for x,y in P if r[y][x]!=r4[y][x]]
print('gewijzigd t.o.v. r4:',len(d),'| buiten oogvak en vleugelvak:',[p for p in d if not oog(*p) and not vleugel(*p)])
print('oog (x21-25, y17-21) gelijk aan r10 (x21-25, y14-18):',all(r[y+3][x]==r10[y][x] for y in range(14,19) for x in range(21,26) if r10[y][x] in '1257' and not (x in (21,25) and y in (14,18))))
nb4=lambda x,y:[(r[y+dy][x+dx] if 0<=y+dy<64 and 0<=x+dx<64 else '.') for dx,dy in ((1,0),(-1,0),(0,1),(0,-1))]
print('open randen:',[(x,y,r[y][x]) for x,y in P if r[y][x]!='.' and '.' in nb4(x,y) and r[y][x] not in '12CDFE9'])
print('losse pixels:',[(x,y,r[y][x]) for x,y in P if r[y][x] in '345678ABE' and r[y][x] not in nb4(x,y)])
print('kleuren:',sorted(set(''.join(r))-{'.'}))
