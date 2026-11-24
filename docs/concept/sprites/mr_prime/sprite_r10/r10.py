# r10 (op de r9-uitvoer; vel10.py draait r7.py, r8.py, r9.py, dan dit): keurderpunten 1-10 op r9. Alleen omkleuren
# met het r9-palet (index 1=16 .. 9=224); geen pixels buiten de omtrek erbij.
R9=C.copy(); LOG.clear()

# ---- 1+2. SNOR lichter (modeltonen): binnen 3/4/5, bovenrand rij 21 een doorlopende rand 2 (lichte kant),
# zwart alleen op de onderste buitencontour en de rechterkant. Krulgaten: links 2 px (26,21-22), rechts (41-42,22).
Z='1-2 snor'
P(Z,20,25,'222')
P(Z,21,24,'23832222222222222221')     # x24-43
P(Z,22,24,'23835544324555443881')
P(Z,23,24,'24344443334454443331')
P(Z,24,24,'23443331111344443331')
P(Z,25,35,'11333221')
zet(Z,20,41,8)

# ---- 3. LINKEROOG naar het schema van het nabije oog (767/636/616/636/767); kopomtrek x28 rij 16-19 -> 5
Z='3 linkeroog'
for y,s_ in zip(range(16,21),('767','636','616','636','767')): P(Z,y,30,s_)
for y in range(16,20): zet(Z,y,28,5)

# ---- 4. LINKERHAAR: tintschema van het rechterhaar (5 boven, 4/3 midden, 2 schaduw, 1 onderrand)
Z='4 linkerhaar'
P(Z,7,17,'25431'); P(Z,8,16,'2554331'); P(Z,9,15,'25544321'); P(Z,10,14,'25443332')
P(Z,11,14,'2433321'); P(Z,12,13,'2332211'); P(Z,13,13,'222'); P(Z,14,13,'1')
# aansluiting: hoedrand als een band (boven 2, midden 4, onderkant 2 zoals de rand rechts), haar eronder een vlak 3
P(Z,10,22,'2222222'); P(Z,11,21,'4444444444'); P(Z,12,21,'222222222')
P(Z,13,20,'23333333333'); P(Z,14,22,'3'); P(Z,14,26,'333')

# ---- 6. JAS LINKS: ovaal 5 rond (26-27,34-38), naar onder breder in 4, 3 alleen als sikkel rechtsonder
Z='6 jas links'
P(Z,31,27,'4443'); P(Z,32,26,'44443'); P(Z,33,26,'45443'); P(Z,34,26,'55443')
for y in (35,36,37): P(Z,y,25,'455443')
P(Z,38,25,'455443'); P(Z,39,24,'4444433'); P(Z,40,25,'444433'); zet(Z,40,31,3)
P(Z,41,25,'444333'); P(Z,42,26,'44333'); P(Z,43,26,'43333'); P(Z,44,27,'333')

# ---- 7. BUIK rechts: grens 4->3 gebogen (bol naar rechtsonder), grens 3->2 als sikkel langs rechtsonder
Z='7 buik'
ARM8={29:46,30:47,31:47,32:48,33:47,34:49,35:50,36:52,37:52,38:52}
M10=np.zeros(C.shape,bool)
for y in range(30,45):
    for x in range(33,53):
        if y in ARM8 and x>=ARM8[y]: continue
        if C[y,x] in (2,3,4,5): M10[y,x]=True
for y in range(30,45):
    for x in range(33,53):
        if not M10[y,x] or C[y,x]==5: continue
        e1=((x+.5-37.5)/7.8)**2+((y+.5-36.0)/7.6)**2
        e2=((x+.5-36.0)/17.0)**2+((y+.5-33.0)/12.5)**2
        zet(Z,y,x,4 if e1<=1 else 3 if e2<=1 else 2)

# ---- 8. losse pixels
Z='8 losse pixels'
zet(Z,42,32,9); zet(Z,57,31,1)

# ---- 9. ONDERARM RECHTS: lichte strook aan de zwarte rand weg (-> 2), licht op de bovenkant (links) van de onderarm
Z='9 onderarm'
zet(Z,32,53,2); P(Z,33,52,'432'); P(Z,34,52,'4432'); P(Z,35,53,'432'); P(Z,36,52,'432'); P(Z,37,53,'32')

# ---- 10. RECHTERBEEN: hooglicht 4 dat naar de knie loopt, sikkel 2 onderlangs; kruislijn links taps (2)
Z='10 rechterbeen'
P(Z,49,44,'33444443333'); P(Z,50,45,'33333444444'); P(Z,51,45,'2222233333332'); P(Z,52,46,'22222222222')
P(Z,50,30,'22')

# ---- nalopen (zelf): losse pixels
Z='nalopen'
zet(Z,24,35,4); zet(Z,11,19,3); zet(Z,39,31,3); zet(Z,41,31,3)
