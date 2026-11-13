# hand.py: handwerk op de onderlaag (basis0.txt) -> raster.txt. Elke regel: P(y, x0, 'letters') overschrijft vanaf (x0,y); '=' laat staan.
import pal,sys
R=[list(r) for r in pal.load('basis0.txt')]
def P(y,x,s):
    for i,ch in enumerate(s):
        if ch!='=': R[y][x+i]=ch
ZONES={}
def zone(f): ZONES[f.__name__]=f; return f

@zone
def kop():
    P(9,23,'d'); P(9,38,'d')
    P(10,23,'do'); P(10,36,'dabo')
    P(11,23,'dao'); P(11,35,'dabo')
    P(12,23,'dabo'); P(12,34,'dadco')
    P(13,23,'dabbo'); P(13,32,'daadcco')
    P(14,23,'oabbcoddoaadccco')
    P(15,23,'dbbdaaabbbbdcco')
    P(16,23,'odaaaaabbbdccco')
    P(17,23,'oaaaaaabbbbdco')
    P(18,23,'daaaaaabbbbcdo')
    P(19,22,'daaaaaaaabbbbco')
    P(20,22,'daaaaaaaadbbbcco')
    P(21,21,'dacaaabacddbbbcco')
    P(22,21,'daoaaaaowwabbbccco')
    P(23,21,'oowdaadaaaabbbccco')
    # klaver (enige rood)
    P(18,25,'tr'); P(19,25,'rr'); P(20,24,'trrs'); P(21,25,'s')   # bovenste lob 2x2, zijlobben op rij 20, steel

@zone
def platen_snuit():
    P(23,39,'ooo')
    P(24,20,'knmoaadbbbbbbcccooonnnnoo')
    P(25,19,'knnmdaadbbobcoooomnnnnmmmo')
    P(26,18,'omnmmdadbbbcooommommmmmmmko')
    P(27,18,'oommbdadbomobommmommmmmkooo')
    P(28,20,'oboadbbomobbommommmmkobo')
    P(29,20,'oboobcomaaobommommmkobbbo')
    P(30,19,'ddbomoom'+'awwwa'+'mmmm'+'oooooooo'+'abo')

@zone
def borst_buik():
    P(31,24,'omawwwwwammmmmmo')
    P(32,25,'kawwwwwwammmmo')
    P(33,25,'owwaaawwammmko')
    P(34,26,'oaoooaaammko')
    P(35,26,'oommmmommmko')
    P(36,27,'ommmmmommo')
    P(37,27,'odaaamommo')

@zone
def kaarthand():
    P(19,3,'dd')
    P(20,2,'dwwo')
    P(21,1,'dwwwo')
    P(22,1,'owwowo')
    P(23,1,'owoooo')
    P(24,2,'oaodwo')        # (6,24) w = nagel van de gestrekte vinger (Jordi)
    P(25,2,'oaaobbo')
    P(26,3,'oodobbo')
    P(28,4,'dabdbbo')
    P(31,6,'obbdbomnooo')
    P(32,7,'ooooommmnndbbo')

@zone
def openhand():
    P(21,53,'dao'); P(22,53,'dbo')
    P(23,52,'dao'); P(23,58,'ddddo')
    P(24,52,'dao'); P(24,56,'daabwo')
    P(25,47,'dd'); P(25,51,'dabodaboo'+'o')
    P(26,46,'dbadbabbbbbo')
    P(27,45,'dowdaabbbbbbo')

@zone
def benen():
    P(39,27,'d'); P(40,26,'dwwwwwabdcbo')
    P(42,24,'daboawwbbdbbbboooo')
    P(43,23,'daabbdaabbdbaabo')
    P(44,22,'daabbboaaabdbaaabo')
    P(45,26,'boooaabobaaabo')
    P(46,19,'knnobbo')
    P(47,19,'knmmoo'); P(47,37,'nnm')
    P(48,19,'kmmmko'); P(48,37,'nmmm')
    P(49,19,'ommkoo'); P(49,37,'mmmk')
    P(50,20,'okobo'); P(50,38,'mkk')
    P(51,21,'dabo')

@zone
def voeten():
    P(55,26,'oo'); P(56,16,'ddddadabbccwo'); P(57,15,'dwabddaboooooo'); P(58,15,'oowoaboo'); P(59,17,'owco'); P(60,18,'oo')
    P(58,39,'daaaabdd'); P(60,38,'dao'); P(60,44,'obwo'); P(61,38,'owo')

@zone
def staart():
    P(36,54,'ddddd')

@zone
def schaduw():
    # staart: licht boven (a), basis (b), sikkel c langs de onderrand die naar de wortel breder wordt
    for y,x,t in ((38,51,'aaaaabc'),(39,50,'aaaaabc'),(40,49,'aaaaabc'),(41,48,'aaaaabc'),(42,47,'aaaaabbc'),(43,45,'aaaaaabbc'),
                  (44,40,'bbbbbbaaaabbcc'),(45,40,'bbbbbbbbbbbcc'),(46,41,'bbbbbbbbbccc'),(47,41,'bbbbbbbcccc'),(48,42,'bbbbbcccc'),
                  (49,42,'bbbbccccc'),(50,42,'bbbcccc'),(51,43,'cccc')): P(y,x,t)
    P(51,41,'c')
    # onderkant van de dij tussen de benen
    P(47,32,'bccc'); P(48,32,'bccc'); P(49,33,'ccc'); P(50,34,'ccc'); P(51,36,'c')
    # handpalm rechtsonder, bovenarm onder de plaat
    P(27,56,'c'); P(28,55,'cc'); P(29,54,'cc'); P(28,42,'c'); P(29,41,'c')
    # zwart materiaal: m basis, n klein licht linksboven, k schaduw rechtsonder
    P(24,39,'nnmm'); P(25,36,'mnnmmmmk'); P(26,36,'mmmmmmkk'); P(27,36,'mmmmkk'); P(28,36,'mmmkk'); P(29,36,'mkkk')
    P(31,36,'kkk'); P(32,34,'mmmk'); P(33,34,'mmkk'); P(34,34,'mkk'); P(35,33,'mmkk'); P(36,34,'mk'); P(37,34,'mk')
    P(27,20,'mk')
    P(33,13,'mmmmk'); P(34,15,'kkk')
    P(31,50,'k'); P(32,46,'mkk'); P(33,47,'k')

@zone
def opschonen():
    # open randen dicht, losse tintpixels weg (controle.py), lijnen in een tint per rand
    P(10,36,'ddco'); P(11,37,'c'); P(13,32,'ddadcco'); P(14,27,'b')
    P(21,23,'d'); P(21,27,'a'); P(21,29,'d')
    P(23,39,'kkk'); P(24,42,'ko')
    P(21,54,'a'); P(22,54,'a'); P(24,56,'ddaawo')
    P(25,31,'b'); P(26,29,'b'); P(26,47,'aadd')
    P(27,21,'m'); P(28,5,'aa')
    P(28,42,'b'); P(29,41,'bbb'); P(30,44,'bd'); P(29,25,'b')
    P(30,23,'o'); P(30,13,'k'); P(31,16,'k')
    P(31,12,'nn'); P(32,14,'nnm'); P(31,19,'b')
    P(31,46,'nnmkk'); P(32,46,'mmk')
    P(33,25,'k')
    P(40,35,'dd')
    P(41,27,'d'); P(42,27,'d'); P(43,28,'o')
    P(42,41,'d'); P(43,42,'d')
    P(45,26,'o')
    P(52,39,'ccc')
    P(56,24,'c'); P(58,19,'bb'); P(59,19,'b'); P(59,45,'b')
    P(16,23,'d')
    P(25,56,'b'); P(57,17,'aa')
    P(27,53,'d')   # plooi in de handpalm (model: 1 cel)

@zone
def selout():
    # buitenlijn aan de lichtkant (transparant links of boven, niet rechts of onder): o -> d naast grijs/wit, o -> k naast zwart materiaal.
    # Uitzonderingen blijven o: kaartrand en -symbool, snorstrengen, vingerlijnen (lijst NIET).
    NIET={(1,22),(1,23),(5,20),(6,22),(24,10),(25,11),(26,12),(27,13),(28,14)}
    T=lambda x,y: not(0<=x<64 and 0<=y<64) or R[y][x]=='.'
    for y in range(64):
        for x in range(64):
            if R[y][x]!='o' or (x,y) in NIET: continue
            if (T(x-1,y) or T(x,y-1)) and not (T(x+1,y) or T(x,y+1)):
                nb=[R[y+dy][x+dx] for dx,dy in ((1,0),(0,1),(-1,0),(0,-1)) if not T(x+dx,y+dy)]
                if any(c in 'abcw' for c in nb): R[y][x]='d'
                elif any(c in 'mnk' for c in nb): R[y][x]='k'

for n in list(ZONES): ZONES[n]()
if len(sys.argv)>3 and sys.argv[3]=='zonder_nagel': P(24,6,'d'); P(25,6,'aa')   # variant voor het vel
open(sys.argv[2] if len(sys.argv)>2 else 'raster.txt','w').write('\n'.join(''.join(r) for r in R)+'\n')
