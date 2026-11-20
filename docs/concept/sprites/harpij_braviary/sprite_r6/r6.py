# r6 = r5 + pixelfixes (Jordi A/B + keurder 1-4 + KAN). Variant 'A' (meer zwarte lijn) en 'B' (minder) van de kuif.
import sys, numpy as np; from pal import *
VAR=sys.argv[1] if len(sys.argv)>1 else 'A'
g=lees('harpij_r5.txt'); o=g.copy(); r4=lees('../sprite_r4/harpij_r4.txt'); P={}
V=[tuple(p) for p in np.load('../sprite_r4/veer_mask.npy')]; O=[tuple(p) for p in np.load('../sprite_r4/oog_mask.npy')]
def zet(punt,lst):
  P.setdefault(punt,set())
  for y,x,c in lst:
    if (y,x) in V or (y,x) in O: raise SystemExit(f'bevroren pixel {y,x} in {punt}')
    if g[y,x]!=c: P[punt].add((y,x)); g[y,x]=c
def rij(y,x,s): return [(y,x+i,c) for i,c in enumerate(s)]
# B. kuif terug naar r4 (rijen 0-11, alles behalve de bevroren veren)
zet('B kuif terug naar r4',[(y,x,r4[y,x]) for y in range(0,12) for x in range(38) if (y,x) not in V and r4[y,x]!=g[y,x]])
# B. dwarse banden uit het model (avg): hoge linkerveer rij 4 (min. in kolom 8), middenveer rij 6 (min. in kolom 13), grote rechterveer schuin r3-4 (staat al in r4), liggende linkerveer kolom 2
zet('B banden',rij(4,6,'baaaK')+[(4,13,'b'),(6,13,'a'),(9,2,'a')])
# B. dither weg: hoge veer onder de band in de lengte (c-b-a), buitenveertje in de lengte
zet('B dither',rij(5,8,'cb')+rij(6,8,'cba')+rij(7,8,'cba')+[(6,6,'c'),(9,3,'b'),(11,4,'b')])
# B. zwarte lijnen tussen de veren (beide varianten) en langs de veervoeten op de kop (alleen A)
zet('B lijnen',[(7,7,'K'),(8,11,'K')])
if VAR=='A':
  zet('B veervoeten (A)',[(9,7,'K'),(9,14,'K'),(9,15,'K'),(9,16,'K'),(10,17,'K'),(11,18,'K'),(12,19,'K')])
# A. kop: wangvlek weg, hooglicht linksboven op de schedel, schaduw rechts/onder
zet('A wang weg',[(y,x,'h') for y in range(15,19) for x in range(14,18) if g[y,x]=='i'])
zet('A hooglicht',rij(10,8,'iiii')+rij(11,7,'iiiii')+rij(12,7,'iiii'))
zet('A schaduw',[(13,20,'g'),(14,21,'g')]+([(12,19,'g')] if VAR=='B' else [])+[(y,19,'g') for y in range(16,20)]+[(19,18,'g')]+rij(20,17,'ggg')+rij(21,16,'ggg')+rij(22,10,'gggggggg')+rij(23,8,'ggggg'))
# keurder 1 snavel
zet('1 snavel',rij(18,3,'sssssss')+[(19,1,'s'),(20,1,'K'),(19,2,'s'),(19,3,'t'),(19,4,'t'),(19,6,'t'),(19,7,'t')])
# keurder 2 staart open randen
zet('2 staart',[(50,27,'K'),(52,28,'K'),(52,29,'n'),(52,30,'n')])
# keurder 3 vleugelrand in trapjes
zet('3 vleugelrand',[(45,36,'.'),(45,35,'K'),(50,36,'a'),(51,36,'a'),(52,36,'a'),(52,35,'a'),(50,37,'K'),(51,37,'K'),(52,37,'K')])
# keurder 4 kraagsikkel (m lichter: 74,82,106)
zet('4 kraag',[(25,8,'m'),(25,9,'m'),(25,10,'m'),(26,7,'m'),(26,8,'m'),(27,6,'m'),(27,7,'m'),(28,6,'m')])
# KAN
zet('KAN',[(47,33,'n'),(47,34,'n'),(48,33,'n'),(48,34,'n'),(54,34,'a')])
uit=f'harpij_r6{VAR.lower()}.txt'; schrijf(uit,g)
for k,v in P.items(): print(f'{k:24s} {len(v)}')
print(uit,'totaal r5->r6:',int((g!=o).sum()),'| bevroren veren',all(g[p]==lees('../sprite_r3/harpij_r3b.txt')[p] for p in V),'oog c',all(g[p]==lees('../sprite_r3/harpij_r3c.txt')[p] for p in O),'| kleuren',len(set(g.ravel())-{'.'}))
