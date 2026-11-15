# r5: KEURING_r4 MOET 1-9 + MAG (pootje, oog). Alleen kleur/lijn binnen het bevroren silhouet (sil56_r4).
# python3 sprite/maker/r5_bouw.py  -> sprite/maker/raster_r5.txt
R=[list(l.rstrip('\n')) for l in open('sprite/maker/raster_r4.txt')]
def S(y,x0,s):
    for i,ch in enumerate(s):
        if ch==' ': continue
        assert R[y][x0+i]!='.', (x0+i,y); R[y][x0+i]=ch
# --- MOET 2 + 1: bol binnen (kringelende strepen, w alleen glans <=3 px) en rechterkant (sikkel 'a' langs de buitenlijn)
S(24,27,'cbbbcccce')
S(25,24,'eeeccccbbbcc'); S(25,37,'cca')
S(26,24,'ewwe');         S(26,37,'ccba')
S(27,23,'eewee'); S(27,31,'ec'); S(27,36,'cecba')
S(28,25,'ee'); S(28,31,'e');     S(28,36,'eccba')
S(29,22,'eecccbceeecc'); S(29,37,'cbcba')
S(30,23,'cbbbccce');     S(30,37,'beeca')
S(31,38,'bcca')
S(32,38,'bbba')
S(33,23,'bbbccbc');      S(33,38,'caa')
S(34,23,'bceeccbceecc'); S(34,37,'cbaa')
S(35,23,'ceeccbbbceecc'); S(35,37,'cbaa')
S(36,22,'ceecbbcccewec'); S(36,35,'cb'); S(36,38,'baa')
S(37,23,'ceeecbbcewecbcbaa')
S(38,24,'ceeecceeeccecba')
# --- MOET 9: staartpunt
S(22,57,'ec'); S(23,56,'eb'); S(24,55,'ecb'); S(25,54,'eebb'); S(26,54,'ecbb')
# --- MOET 3: bovenste waaier (bovenkant scherven d, naden volgens model en taps, twee tonen per scherf)
S(25,53,'d'); S(26,51,'dcd'); S(30,47,'d')
S(27,51,'ecd'); S(27,54,'ecba')                 # x51-53, x54-57 (58 = d naad)
S(28,51,'edc'); S(28,54,'ccbdc')                # x54-58
S(29,51,'eac'); S(29,54,'ccacb')                # (52,29) d, (53,29) c; x54-58
S(30,48,'accebcca'); S(30,56,'cb')              # x48-55, x56-57
S(31,46,'ecdeccbbbab')                          # x46-56
S(32,46,'eccdcbbbba')                           # x46-55
S(33,46,'eccaccbba')                            # x46-54
S(34,46,'eccbbccba')                            # x46-54
# --- MOET 4: onderste segment (grond b, lichte strepen x42-43 en x48-49, schaduw onderaan).
# Naad: niet de verticale r4-naad x47 maar het modelpad (49,35)a (49,36)(48,37)(47,38)(47,39)(46,40)(45,41)(44,42)d (43,42)a;
# px.py: p15 43-63 op dat pad, dus de dunne modellijn bestaat; schaduw 'a' links ervan zoals het model.
S(35,45,'aaccaabba')                            # x45-53
S(36,43,'ecbaebdccbb')                          # x43-53
S(37,41,'bcecbbbdecbbb')                        # x41-53
S(38,40,'abeecbbdbecbbb')                       # x40-53
S(39,41,'beecbadccbbbb')                        # x41-53
S(40,41,'beebadccbbbb')                         # x41-52
S(41,40,'bbecadcbbbbbb')                        # x40-52
S(42,41,'baadabbbbbba')                         # x41-52
S(43,43,'babbbbbba')                            # x43-51
S(44,43,'bbbbbbba')                             # x43-50
# --- MOET 5: ring
S(39,39,'s')
S(40,24,'ttt'); S(40,37,'sss')
S(41,25,'ttttt'); S(41,34,'ssssr')
S(42,25,'##ssssssrrrr')                         # x25-36
S(43,27,'##sssrr')                              # x27-33: (27-28,43)#, 29-31 s, 32-33 r
S(43,34,'###'); S(42,37,'####')
S(44,29,'#')                                    # (29,44)#, (30-33,44) al #
# --- MOET 7: zijflap
S(44,34,'eeeecccb')                             # x34-41
S(45,29,'ceeeeecccbbb')                         # x29-40
S(46,28,'ceeecccbbbbb')                         # x28-39
S(47,27,'ceecbbbbccb')                          # x27-37
# --- MOET 8: lijfnaad als boog 2-3-4-3-2, uiteinden a
S(50,25,'bad'); S(51,27,'bddd'); S(52,31,'dddd'); S(51,31,'bbbb'); S(51,35,'ddd'); S(51,38,'b')
S(50,38,'dab'); S(49,40,'a')
# --- MAG: pootje (buitenrand #), oog-pixel
S(53,13,'#'); S(54,12,'#'); S(48,12,'b')
O=[l.rstrip('\n') for l in open('sprite/maker/raster_r4.txt')]
for y in range(64):
    for x in range(64):
        if O[y][x]=='#' and R[y][x]!='#': print('let op: # weg op',(x,y),'->',R[y][x])
open('sprite/maker/raster_r5.txt','w').write('\n'.join(''.join(r) for r in R)+'\n')
