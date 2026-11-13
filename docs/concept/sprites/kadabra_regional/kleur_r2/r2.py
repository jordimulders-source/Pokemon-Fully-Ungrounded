# r2.py: reparaties ronde 2 op basis_r1.txt -> raster.txt. E(x,y,oud,nieuw) controleert eerst de oude letter; P(y,x0,str) zet een rijstuk ('=' = laten staan).
import pal,sys
R=[list(r) for r in pal.load('basis_r1.txt')]; fout=[]
def E(x,y,oud,nieuw):
    if R[y][x]!=oud: fout.append((x,y,'verwacht '+oud,'staat '+R[y][x]))
    R[y][x]=nieuw
def P(y,x,s):
    for i,ch in enumerate(s):
        if ch!='=':
            if R[y][x+i]=='.' or ch=='.': fout.append((x+i,y,'silhouet!'))
            R[y][x+i]=ch
# 1. grijs een stap donkerder: basis b, schaduw c, a alleen als strook linksboven
# kop
P(14,32,'bb')
P(15,27,'bbbbbbb')
P(16,26,'bbbbbbb')
P(17,26,'bbbbbbcc')
P(18,27,'bbbbbccc')
P(19,27,'bbbbbccc')
P(20,28,'bbbdccccc')
P(21,27,'bb'); P(21,32,'ccccc')
P(22,26,'bb'); P(22,31,'ccccccc')
P(23,26,'b'); P(23,28,'bbbbcccccc')
P(24,27,'bbbcccccc')
P(25,30,'cc'); P(26,28,'cc'); P(27,26,'c'); P(28,26,'c'); P(29,25,'c')
# kaartarm, kaarthand
P(31,20,'c'); P(32,19,'c'); P(33,18,'c')
P(28,5,'bb'); P(28,9,'c'); P(29,10,'c'); P(30,10,'c'); P(31,10,'c')
# open hand + bovenarm
P(21,54,'b'); P(22,54,'b'); P(23,53,'b'); P(24,53,'b'); P(25,52,'b'); P(24,58,'bb')
P(26,47,'bb'); P(26,51,'b'); P(27,49,'bb')
P(28,54,'c'); P(29,53,'c')
P(28,42,'c'); P(29,41,'ccc')
# buik onder het wit, dijen
P(44,29,'bbbc'); P(45,30,'bbc')
P(42,26,'b'); P(43,25,'bbc'); P(44,24,'bbcc'); P(45,23,'bcc'); P(46,24,'c')
P(39,36,'c'); P(41,36,'c'); P(42,37,'c'); P(43,36,'bc'); P(44,36,'bbc'); P(45,35,'bbbc'); P(46,36,'bb')
# staart: a = strook van 1-2 px onder de bovenrand, b basis, c sikkel onderlangs (breder naar de wortel)
for y,x,t in ((38,51,'aaabbbc'),(39,50,'aabbbcc'),(40,49,'aabbbcc'),(41,48,'aabbbcc'),(42,47,'aabbbbcc'),(43,45,'aabbbbbcc'),
              (44,40,'bbbbbbbbbbbccc'),(45,40,'bbbbbbbbbcccc'),(46,41,'bbbbbbcccccc'),(47,41,'bbbbccccccc'),(48,42,'bbccccccc'),
              (49,42,'bcccccccc'),(50,42,'ccccccc')): P(y,x,t)
# schenen en voeten
P(51,22,'b'); P(55,21,'bb'); P(54,24,'c'); P(55,24,'cc')
P(56,20,'b'); P(56,22,'bbccc'); P(57,17,'bb'); P(57,21,'bc')
P(53,41,'c'); P(54,42,'c'); P(55,42,'c'); P(56,41,'bbc'); P(57,41,'bbc'); P(58,41,'bbbc'); P(59,39,'bb'); P(59,44,'c'); P(60,39,'b')
# 2. zwarte omlijning rond witte delen en punten
for x,y in ((3,19),(4,19),(2,20),(1,21),(55,19),(56,19),(60,23),(61,23),(16,56),(15,57),(23,9),(38,9)): E(x,y,'d','o')
# 3. linkerplaat zwart en rond
for x,y in ((21,24),(21,25),(20,26)): E(x,y,'n','m')
E(23,25,'d','o'); E(23,26,'d','o')
# 4. onder de kin
E(28,27,'m','o'); E(28,28,'m','o'); E(27,29,'m','k')
# 5. klaver: voet 2 px
E(26,21,'a','s')
# eigen aanvulling: zwarte punten aan de lichtkant (duimtop, vingertop, staartpunt, teen), zodat de lichtkant op 10-20 % komt
for x,y in ((45,27),(46,26),(4,28),(60,37),(38,59),(38,60)): E(x,y,'d','o')
# losse tintvlakjes uit controle.py
P(28,25,'c'); P(29,24,'cc'); P(30,26,'k'); P(31,25,'k'); P(30,44,'c')
P(31,20,'b'); P(32,19,'b'); P(33,18,'b'); P(39,36,'b'); P(45,35,'a'); P(43,32,'c'); P(57,22,'b'); P(56,41,'a')
V=sys.argv[1] if len(sys.argv)>1 else ''
if V=='klaver_A':   # 4x4: lage bovenlob, zijlobben 2 rijen hoog, voet 2 px
    P(18,24,'atra'); P(19,24,'trrr'); P(20,24,'rrrs'); P(21,24,'assa')
if V=='klaver_B':   # 5x5: drie lobben met donkere kern, steel
    P(17,24,'aatab'); P(18,24,'atrrb'); P(19,24,'trrrs'); P(20,24,'trsrs'); P(21,24,'aasab')
open('raster.txt' if not V else V+'.txt','w').write('\n'.join(''.join(r) for r in R)+'\n'); print('afwijkingen:',fout)
