# handreparaties r6 (X, Y, tint): 2 selout, 3 donker, 4 midden, 5 licht, 6 hooglicht. Per bol, plek uit het model.
def rij(Y,X,t):
    for i,ch in enumerate(t):
        if ch!='_': FIX.append((X+i,Y,{'s':2,'0':3,'1':4,'2':5,'3':6}[ch]))
# --- rechtervleugel ---
rij(17,59,'3'); rij(18,56,'3'); rij(18,59,'1')            # A: kern 57-59,17 + 56-58,18 (model: lichte kap op de punt)
rij(19,54,'122210')                                        # A: lichte ring onder de kern, punt rechts donker
rij(20,48,'_____')                                         # (kuifrand blijft)
rij(22,46,'2'); rij(22,52,'110')                           # B links ring; Re onderkant
rij(23,44,'220222110')                                     # Rb kap (44-45), B-onderkant met ring, Re-rand
rij(24,43,'2200000001')                                    # Rb/B onderboog (45-46 en 47-51), Re midden
rij(26,44,'20')                                            # D2 kap, D1 linkerrand
rij(27,40,'2221210000')                                    # C ring onder de kern, D2, D1 onderboog (46-49)
rij(28,40,'1111001100')                                    # C lijf, onderboog C/D2 (44-45), F2 bovenkant
rij(29,39,'2_000122211')                                   # E kap, C onderboog, F2 kap (45-47)
rij(30,38,'22')                                            # E kap
rij(31,50,'s')                                             # oude naadpixel terug (losse 3 tussen static en rand)
# --- lijf ---
rij(46,13,'0'); rij(46,18,'11'); rij(46,36,'1'); rij(46,41,'111')   # LB1-lijf onder de ring, R-onderboog loopt schuin op naar rechts
rij(53,35,'0'); rij(53,40,'0'); rij(55,34,'0'); rij(55,39,'0')     # K3-kap rond (geen blok)
rij(55,25,'01111100')                                       # M1-onderboog (model: zwarte boog Y55), K2-kap begint eronder
rij(56,22,'0011111111')                                     # K2-kap rond
rij(57,22,'00000000')                                       # onderkant donker (MOET 6)
rij(21,52,'1')                                              # los donker pixeltje naast de kuif -> Re-midden
rij(51,19,'0'); rij(51,23,'0')                              # M1-kap onderaan rond
rij(47,20,'01111'); rij(47,30,'2'); rij(46,20,'0'); rij(46,21,'1')  # F-onderboog als boog (25-29,47), LB2/M1 eronder midden, naad LB1|LB2
rij(54,27,'111'); rij(55,25,'01111111'); rij(56,24,'00111100')     # K2-kap als koepel (3/7/4), onderkant Y57 donker
