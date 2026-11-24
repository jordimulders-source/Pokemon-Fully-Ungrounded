# r8 (op de r7-uitvoer, r7.py draait eerst in vel8.py): keurderreparaties 1-12 op r7. Niets nieuw getekend: alleen
# bestaande pixels/tinten van de sprite (r7-palet), verschoven, geknipt of omgekleurd; vormen uit model r9 / Mr. Rime /
# Gen 3 Mr. Mime. Coordinaten in de commentaren x,y; P(zone,y,x0,s) zet rij y vanaf x0.
R7=C.copy(); LOG.clear()

# ---- 1. HAND + STOK. Model r9: de stok ligt VOOR de handschoen (lijn loopt ononderbroken over het witte vlak).
# Dus: stok doorlopend (lijnen zwart waar hij over de hand ligt), handschoen = links de palm, rechts de vingers die om
# de stok vallen, beide schoon wit met licht linksboven en een schaduwsikkel rechtsonder; grijze ruis weg.
Z='1 hand + stok'
P(Z,26,15,'44.')            # bovenrand vingers (outline wit = 4)
P(Z,27,15,'8844')
P(Z,28,16,'8891')           # (17,28) 4 -> wit, (19,28) lijn
P(Z,29,17,'891')            # (17,29) 7 -> wit
P(Z,30,17,'77')             # (18,30) 1 -> 7 (vingertop)
P(Z,31,18,'7')
P(Z,29,10,'488'); P(Z,30,10,'488'); P(Z,31,10,'1887'); P(Z,32,11,'1777')   # palm: sikkel rechtsonder

# ---- 2. HAAK: 4 px breed overal (2/4/3/1), hooglicht 4 doorlopend schacht -> boog -> dalend deel, 164-vlek weg.
Z='2 haak'
HAAK={15:(0,'...222.....'),
      16:(0,'..24441....'),
      17:(0,'.2433431...'),
      18:(0,'24331431...'),
      19:(0,'2431.2431..'),
      20:(0,'2431..2431.'),
      21:(0,'2431...2431'),
      22:(0,'2431...2431'),
      23:(0,'.1331...2431'),
      24:(0,'..11.....2431')}
for y,(x0,s) in HAAK.items(): P(Z,y,x0,s)

# ---- 3. LINKERHAAR: gat tussen vleugel en hoedrand dicht, vleugel loopt onder de rand door.
Z='3 linkerhaar'
P(Z,10,23,'2222')           # bovenrand vleugel -> rand (outline base 2, zoals vleugel en rand)
P(Z,11,24,'1333'); P(Z,12,25,'133')   # vleugel loopt onder de rand door; rand-einde = 1 doorlopende lijn (24,11)-(25,12)-(25,13)

# ---- 4. LINKEROOG (ver oog): ring buiten donker (licht kant 4 = 100, schaduwkant rechts/onder 3 = 66), binnen iris 6 +
# pupil 1 (zoals het nabije oog: ring, iris, pupil); losse lichte pixels eromheen -> gezichtswit.
Z='4 linkeroog'
P(Z,16,30,'747'); P(Z,17,30,'463'); P(Z,18,30,'413'); P(Z,19,30,'463'); P(Z,20,30,'737')
for (x,y) in ((33,18),(34,19),(34,20)): zet(Z,y,x,8)
P(Z,21,32,'888')            # (32-34,21): gezicht boven de snor (snorrand ligt hier op rij 22)

# ---- 5. KOP RECHTS ROND (boog Gen 3 Mr. Mime-kop): lijn rij 14 x46, 15-16 x47, 17-21 x48, 22 x47, 23 x46, 24 x44-45.
# 1-px streep 224 weg -> een sikkel 200 rechtsonder.
Z='5 kop rechts'
for y in range(13,25):
    for x in range(42,49):
        if C[y,x]==9: zet(Z,y,x,8)
P(Z,16,47,'1.'); P(Z,17,47,'71'); P(Z,18,47,'71'); P(Z,19,45,'8771'); P(Z,20,45,'8771')
P(Z,21,44,'87771'); P(Z,22,44,'7771.'); P(Z,23,44,'771.'); P(Z,24,44,'11.')
# ---- 6. (45,25) gat -> lijn, (44,26) losse 4 -> lijn
Z='6 kin/kraag rechts'
zet(Z,25,45,1); zet(Z,26,44,1)

# ---- 7. HOED: bol als bol (licht linksboven, sikkel rechtsonder), rand met verloop links->rechts i.p.v. rijen.
Z='7 hoed'
P(Z,4,34,'5554443')
P(Z,5,32,'45554444333')
P(Z,6,31,'3444444333322')
P(Z,7,31,'3344433332222')
P(Z,9,32,'55544444443333')
P(Z,10,29,'4444433333333333322222')
P(Z,11,28,'444333222222222222222')

# ---- 8. SNOR: twee lobben met een gebogen bovenrand, krullen aan de uiteinden (gat = gezichtswit zoals het model),
# volume per lob (hooglicht linksboven, schaduw rechtsonder), geen doorlopende strepen.
Z='8 snor'
P(Z,21,26,'111111')         # bovenrand linkerlob (was gezichtswit tussen krul en lob)
P(Z,22,28,'5544')
P(Z,23,27,'44444')
P(Z,21,25,'4'); P(Z,23,25,'4'); P(Z,20,27,'2')
P(Z,24,26,'44333')
P(Z,21,35,'111111')         # bovenrand rechterlob
P(Z,20,41,'11'); P(Z,21,40,'1891'); P(Z,22,40,'1111')   # rechterkrul: lus met gat
P(Z,22,35,'555444')
P(Z,23,34,'3544444333')
P(Z,24,33,'1344444333')
P(Z,25,37,'33322')
P(Z,23,32,'41')             # midden: scheiding 1 px i.p.v. zwart blok

# ---- 9. wit -> broek: blur 164 onder de buikband -> lijn; linkerschoen
Z='9 buikband/schoen'
P(Z,48,35,'1111')
zet(Z,56,26,1); P(Z,58,28,'76')

# ---- 11. RECHTERBEEN: 1 buitenlijn, 3 lichte strook boven, 2 schaduw onder; interne lijnpixels weg
Z='11 rechterbeen'
P(Z,49,44,'33333333333')
P(Z,50,45,'33333333333')
P(Z,51,44,'1222222222222')
P(Z,52,45,'12222222222')
zet(Z,53,48,2)

# ---- 12. STRIKJE: knoop zwart, lussen met licht linksboven en schaduw rechtsonder (geen rijstrepen)
Z='12 strikje'
zet(Z,29,34,1)
P(Z,27,30,'44'); P(Z,27,41,'4433')
P(Z,28,35,'55443322')
P(Z,29,36,'44322')

# ---- 10. JASJE RECHTS: een bolling (buik) met hooglicht bovenaan links, sikkel 2 rechtsonder die de buik volgt.
Z='10 jasje rechts'
ARM8={29:46,30:47,31:47,32:48,33:47,34:49,35:50,36:52,37:52,38:52}
M=np.zeros(C.shape,bool)
for y in range(30,45):
    for x in range(33,53):
        if y in ARM8 and x>=ARM8[y]: continue
        if C[y,x] in (2,3,4,5): M[y,x]=True
cx,cy,rx,ry=43.0,36.5,12.0,11.0
import math
I=np.full(C.shape,-9.)
Lv=np.array([-0.75,-0.5,0.5]); Lv/=np.linalg.norm(Lv)
for y,x in zip(*np.where(M)):
    nx=(x+.5-cx)/rx; ny=(y+.5-cy)/ry; r2=min(nx*nx+ny*ny,0.98); nz=math.sqrt(1-r2)
    I[y,x]=nx*Lv[0]+ny*Lv[1]+nz*Lv[2]
v=np.sort(I[M]); n=len(v); gr=[]; acc=0
for f in (0.26,0.36,0.28):
    acc+=f; gr.append(v[min(n-1,int(acc*n))])
for y,x in zip(*np.where(M)):
    zet(Z,y,x,(2,3,4,5)[sum(I[y,x]>=g for g in gr)])
for y,x in zip(*np.where(M)):        # hooglicht alleen bovenaan de bolling (x37-41, y31-34), niet als strook langs de V
    if y>=35 and C[y,x]==5: zet(Z,y,x,4)

# ---- nalopen (zelf): losse pixels
Z='nalopen'
zet(Z,45,53,1)              # losse 4 in de rand van de jaspand rechts
P(Z,54,54,'46')             # rechterschoen: lijn 4 doorlopend, losse 4 -> schoentint
