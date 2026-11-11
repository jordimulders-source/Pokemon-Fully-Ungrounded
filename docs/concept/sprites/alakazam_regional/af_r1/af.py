# af.py: basis_S1.txt -> raster.txt. Eindafwerking per zone (alleen tinten/binnenlijnen), met diffbewijs per zone.
import numpy as np
B=[list(l.rstrip('\n').ljust(64,'.')[:64]) for l in open('basis_S1.txt')][:64]
R=[r[:] for r in B]
Z={}   # zone -> {(x,y):teken}
def put(zone,y,x0,s):
    for i,ch in enumerate(s):
        if ch!='=': Z.setdefault(zone,{})[(x0+i,y)]=ch
# 0. palet: n -> d (licht van zwart), p -> c (glans op zwart)
for y in range(64):
    for x in range(64):
        if B[y][x]=='n': Z.setdefault('palet n->d',{})[(x,y)]='d'
        if B[y][x]=='p': Z.setdefault('palet p->c',{})[(x,y)]='c'
# 1. KOP: licht van linksboven (hooglicht linksboven op de schedel, c-sikkel rechts, selout d links, o rechts)
K='kop'
for (x,y) in [(18,3),(18,4),(19,5),(20,6),(21,7),(21,8),(22,9),(22,10),(23,11),(23,12),(24,13),(23,14),(23,15)]: put(K,y,x,'d')
for (x,y) in [(35,6),(35,7),(35,8),(36,8),(37,9),(38,10),(39,11),(39,12),(40,13),(40,14)]: put(K,y,x,'o')
put(K,4,31,'bc'); put(K,5,31,'bbc'); put(K,6,32,'bbc'); put(K,7,32,'bcc')
put(K,9,23,'bbaaaaabbbbbbb')        # x23-36
put(K,10,23,'baaaaaabbbbbbc')       # x23-36 (37 c)
put(K,10,37,'c')
put(K,11,24,'baaaabbbbbbbcc')       # x24-37 ... 38
put(K,11,38,'c')
put(K,12,24,'bbaabbbbbbbbcc')       # x24-37, 38
put(K,12,38,'c')
put(K,13,25,'bbb'); put(K,13,37,'ccc')
put(K,14,24,'bbb'); put(K,14,36,'bbcc')
put(K,15,24,'bbb'); put(K,15,37,'bbcc')
put(K,16,23,'bb');  put(K,16,38,'bbc')
put(K,17,22,'cb')
# geometrie: bovenrand linkeroor liep 3-3-1-2-2-2; (23,3) eraf en (23,4) wordt rand -> 3-2-2-2-2-2 (1 px silhouet, gemeld)
put('geometrie oor',3,23,'.'); put('geometrie oor',4,23,'d')
# snuit: rechts/onder in de schaduw
put(K,19,39,'bc'); put(K,20,38,'bbcc'); put(K,21,38,'bccc'); put(K,22,41,'c'); put(K,23,42,'c'); put(K,24,42,'c')
# 2. VERRE ARM (rechts): onder de plaat in slagschaduw, geen hooglicht a
A='verre bovenarm'
put(A,29,35,'cccc'); put(A,30,35,'bbbcc'); put(A,31,35,'bbccc'); put(A,32,35,'bcccc')
put('verre onderarm',34,41,'mm'); put('verre onderarm',35,40,'m')
# 3. VERRE BEEN: geen a, schaduwkant breder
V='verre been'
for y in range(49,53): put(V,y,34,'c')
put(V,53,32,'bbc'); put(V,54,32,'bbc'); put(V,55,31,'bbbc'); put(V,56,30,'bbbbc')
# 4. NABIJ BEEN: selout d aan de lichte (linker)kant
N='nabij been'
for (x,y) in [(18,52),(18,53),(17,54),(17,55),(17,56),(16,57),(15,58),(15,59),(15,60),(15,61)]: put(N,y,x,'d')
# 5. NETHEID: oude vlakjes < 3 px uit de basis met alleen tinten opgelost
put('netheid',27,37,'mmmm')   # verre schouderplaat (4 px strook): één tint, ver = donker
put('netheid',34,28,'a')      # losse a (27,34) sluit aan op de a-sikkel van de borstplaat
put('netheid',34,37,'cc')     # elleboog verre arm: d-vlakje -> c, sluit aan op de bovenarm
# toepassen + bewijs
zone_of={}
for z,d in Z.items():
    for (x,y),ch in d.items():
        if (B[y][x]=='.')!=(ch=='.'): print('SILHOUET (gemeld):',z,x,y,B[y][x],'->',ch)
        R[y][x]=ch; zone_of.setdefault((x,y),[]).append(z)
open('raster.txt','w').write('\n'.join(''.join(r) for r in R)+'\n')
diff=[(x,y) for y in range(64) for x in range(64) if R[y][x]!=B[y][x]]
per={}
for p in diff: per[zone_of[p][-1]]=per.get(zone_of[p][-1],0)+1
print('gewijzigd:',len(diff))
for z in Z:
    pts=[p for p in diff if zone_of[p][-1]==z]
    if pts: print(f'  {z}: {len(pts)} px, x{min(p[0] for p in pts)}-{max(p[0] for p in pts)} y{min(p[1] for p in pts)}-{max(p[1] for p in pts)}')
print('buiten zones:',[p for p in diff if p not in zone_of])
