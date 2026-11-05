"""Controle: alpha-diff met silhouet_open.txt, open randen, losse pixels, palet/tekens."""
H='/home/user/Pokemon-Fully-Ungrounded/docs/concept/sprites/kolibrie_pre/blender/A/'
sil=[l.rstrip('\n') for l in open(H+'silhouet_open.txt')][:64]
r=[l.rstrip('\n') for l in open('raster.txt')][:64]
CH='.123456789ABCDEF'
assert all(len(x)==64 for x in r) and len(r)==64
diff=[(x,y) for y in range(64) for x in range(64) if (sil[y][x]=='#')!=(r[y][x]!='.')]
print('alpha-diff:',len(diff),diff[:10])
print('pixels:',sum(c!='.' for row in r for c in row),'(silhouet',sum(c=='#' for row in sil for c in row),')')
bad=[c for row in r for c in row if c not in CH]; print('ongeldige tekens:',len(bad))
# open randen: rand-pixel (naast transparant, 4-buren) mag geen licht vlak zijn
ok_rand=set('123AEF9C2')  # buitenlijn, selout, snavel/mond (dunne delen)
ok_rand=set('12AEF9CD3')  # 3 = gekleurde selout aan de lichtkant
open_=[]
for y in range(64):
    for x in range(64):
        c=r[y][x]
        if c=='.': continue
        nb=[r[y+dy][x+dx] if 0<=y+dy<64 and 0<=x+dx<64 else '.' for dx,dy in ((1,0),(-1,0),(0,1),(0,-1))]
        if '.' in nb and c not in ok_rand: open_.append((x,y,c))
print('open randen (licht vlak naast transparant):',open_)
# rand aan de schaduwkant (rechts/onder) moet 1 zijn, behalve dunne delen
sch=[]
for y in range(64):
    for x in range(64):
        c=r[y][x]
        if c=='.' : continue
        right = x+1>63 or r[y][x+1]=='.'; down = y+1>63 or r[y+1][x]=='.'
        if (right or down) and c not in '1' and x>=26: sch.append((x,y,c))
print('schaduwkant-rand niet zwart (x>=26):',sch)
# losse pixels: kleur die geen enkele 4-buur van dezelfde kleur heeft (alleen vlakken 3-7,B,E)
los=[]
for y in range(64):
    for x in range(64):
        c=r[y][x]
        if c not in '34567BE': continue
        nb=[r[y+dy][x+dx] for dx,dy in ((1,0),(-1,0),(0,1),(0,-1)) if 0<=y+dy<64 and 0<=x+dx<64]
        if c not in nb: los.append((x,y,c))
print('losse pixels:',los)
