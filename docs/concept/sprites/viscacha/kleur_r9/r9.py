"""r9: rugtop (r28-32, x30-42) boller; basis kleur_r8/raster.txt. Rest bevroren."""
V='/home/user/Pokemon-Fully-Ungrounded/docs/concept/sprites/viscacha/'
R=[list(l.rstrip('\n')) for l in open(V+'kleur_r8/raster.txt')][:64]
def put(y,x0,s):
    for i,c in enumerate(s): R[y][x0+i]=c
# nieuwe boog: runs 2 (r30) - 3 (r29) - 5 (r28, top x34-38) - 2 (r29) - 1,1,1 (45 graden naar de bil)
put(28,34,'22222')          # selout top
put(29,31,'222'); put(29,34,'55555'); put(29,39,'21')
put(30,30,'24555555555')    # x30 selout, x31 neksikkel (4) loopt door, x32-40 licht
put(30,41,'1')
put(31,41,'51')
put(32,42,'51')
open(V+'kleur_r9/raster.txt','w').write('\n'.join(''.join(r) for r in R)+'\n')
