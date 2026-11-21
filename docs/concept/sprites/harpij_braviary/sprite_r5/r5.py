# r5 = r4 + pixelfixes volgens de keuring (punt -> lijst (rij,kolom,letter)); telt per punt; bewijst diff 0 elders
import numpy as np; from pal import *
g=lees('harpij_r4.txt'); o=g.copy(); P={}
def zet(punt,lst):
  P.setdefault(punt,[])
  for y,x,c in lst:
    if g[y,x]!=c: P[punt].append((y,x)); g[y,x]=c
def rij(y,x,s): return [(y,x+i,c) for i,c in enumerate(s)]
# 1 wangvlek rond en kleiner
zet('1 wang',[(14,15,'h'),(14,16,'h'),(14,17,'h'),(15,14,'h'),(15,17,'h'),(17,18,'h'),(18,13,'h'),(18,14,'h'),(18,18,'h'),(19,15,'h'),(19,16,'h')])
# 2 kop rechts: smalle schaduw k20 r14-19
zet('2 kop rechts',[(y,20,'g') for y in range(14,20)])
# 3 kuif: per veer in de lengte c (links) - b - a (rechts), geen dither
k=[]
k+=rij(0,8,'bK')+rij(1,7,'cbK')+rij(2,7,'cbK')+rij(3,7,'cbaK')            # hoge linkerveer
k+=rij(4,6,'bcbaK')+rij(5,5,'cbKcbK')+rij(6,5,'cbKcbaK')+rij(7,5,'cbacbaK')+rij(8,6,'bab') # kleine buitenveer + onderkant hoge veer
k+=rij(0,14,'bK')+rij(1,13,'cbK')+rij(2,12,'cbaK')+rij(3,12,'cbaK')+rij(4,12,'cbK')+rij(5,12,'cbK')+rij(6,12,'cbKK')+rij(7,12,'cbK') # middenveer
k+=rij(1,21,'cbK')+rij(2,19,'cbbaK')+rij(3,18,'cacbaK')+rij(4,17,'cbacaK')+rij(5,16,'ccbbaK')+rij(6,16,'ccbbaK')+rij(7,15,'ccbbaK')+rij(8,15,'cbbbaa')+rij(9,17,'cba') # grote rechterveer
k+=rij(8,1,'cccc')+rij(9,0,'cbbbbb')+rij(10,1,'bbbbb')+rij(11,2,'aaa')   # linkerveer liggend: boven licht, onder donker
k+=[(8,10,'g'),(8,11,'h')]                                                   # overgang kop: gghh
zet('3 kuif',k)
# 4 vleugelkorrel: zwarte binnenpixels -> veerlijn in n (donkerder dan a, geen K); dubbele rand k32 -> a
zet('4 veerlijnen',[(y,x,'m' if False else 'n') for y,x in [(33,27),(34,27),(35,28),(36,28),(39,25),(39,26),(40,23),(40,27),(42,28),(43,29),(39,31),(42,34)]])
zet('4 dubbele rand',[(36,32,'a'),(37,32,'a'),(38,32,'a')])
# 5 volume: c-sikkel op de schouder, a-blok -> b, kraag lichtrand m
zet('5 schoudersikkel',rij(24,19,'cccccc')+rij(25,18,'ccccc')+rij(26,18,'ccc')+rij(27,17,'cc')+rij(28,17,'c'))
zet('5 a-blok',rij(29,21,'bbb')+rij(30,19,'bbbbb')+rij(31,19,'bb'))
zet('5 kraag',rij(24,8,'mmmmmmmmm')+[(25,7,'m'),(26,6,'m')])
# 6 rechte randen
zet('6 kop',[(19,21,'.'),(19,20,'K')])
zet('6 vleugel',[(y,36,'K') for y in range(45,51)]+[(y,35,'a') for y in range(45,51)])
# KAN
zet('kan snavelpunt',[(21,3,'.')])
zet('kan voet',[(54,6,'s')])
zet('kan borst',[(32,17,'i'),(33,17,'i'),(34,17,'i'),(35,17,'i'),(36,18,'i'),(37,18,'i'),(38,18,'i'),(39,19,'i'),(40,20,'i')])
schrijf('harpij_r5.txt',g)
alle=set(p for v in P.values() for p in v)
for k_,v in P.items(): print(f'{k_:18s} {len(v)}')
print('totaal',len(alle),' diff r4->r5 =',int((g!=o).sum()))
r3=lees('../sprite_r3/harpij_r3b.txt'); r3c=lees('../sprite_r3/harpij_r3c.txt')
V=[tuple(p) for p in np.load('../sprite_r4/veer_mask.npy')]; O=[tuple(p) for p in np.load('../sprite_r4/oog_mask.npy')]
print('veren bevroren:',all(g[p]==r3[p] for p in V),' oog c bevroren:',all(g[p]==r3c[p] for p in O))
print('kleuren',len(set(g.ravel())-{'.'}))
