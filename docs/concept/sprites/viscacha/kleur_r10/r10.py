"""r10: alleen de rug (Jordi: "bijna een perfect bolle rug") + uitstekende pixel (49,44). Basis kleur_r9/raster.txt.
Boog: ellips (midden x35,5 r43, halve assen 13 x 15), trappen 2-3-5 omhoog, 5-3-2-1-1 opzij, dan verticaal 2-4."""
V='/home/user/Pokemon-Fully-Ungrounded/docs/concept/sprites/viscacha/'
R=[list(l.rstrip('\n')) for l in open(V+'kleur_r9/raster.txt')][:64]
O=[r[:] for r in R]
def put(y,x0,s):
    for i,c in enumerate(s): R[y][x0+i]=c
# boven: r28-30 expliciet (x29-49)
for y in (28,29,30):
    for x in range(30,50): R[y][x]='.'
put(28,34,'22222')
put(29,31,'222'); put(29,34,'BBBB5'); put(29,39,'211')
put(30,30,'24'); put(30,32,'5BBBBB5555'); put(30,42,'11')
# rechterflank: binnen tot Rr-1, omlijning op Rr, daarbuiten transparant; sikkel 4 vanaf Lk
RR={31:44,32:45,33:46,34:46,35:47,36:47,37:47,38:47,39:48,40:48,41:48,42:48,43:48,44:48}
LK={31:43,32:43,33:44,34:44,35:44,36:44,37:44,38:44,39:44,40:44,41:44,42:44,43:43,44:44}
for y,rr in RR.items():
    for x in range(39,50):
        if x>rr: R[y][x]='.'
        elif x==rr: R[y][x]='1'
        elif x>=LK[y]: R[y][x]='4'
        elif x>=42 or O[y][x] in '12.': R[y][x]='5'
put(31,33,'BBB')
open(V+'kleur_r10/raster.txt','w').write('\n'.join(''.join(r) for r in R)+'\n')
