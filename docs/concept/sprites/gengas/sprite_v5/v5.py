# v5 = v4 + Jordi (15 nov): "ogen en mond zijn nog niet goed" · "lijkt net alsof ze indeuken" · "en linkeroog is slordig".
# Alleen tinten/lijnen in en direct om ogen en grijns (zone rij 29-46, kol 8-32); grootte/plaats van ogen en grijns blijven.
# Wat het kuileffect gaf (gemeten in v4, zie NOTITIES.md): donkere a/lichte u-ring om de ogen, lichtere pixels (m) ONDER
# de ogen en onder de rechtermondhoek, grijze (H/h) bovenrij tanden + grijze punten. Gengar: dunne donkere lijn om oog
# en mond, lijf eromheen in de gewone lijftint, oog onderaan donkerrood op het lijf, tanden wit met lijntjes.
import os
D=os.path.dirname(os.path.abspath(__file__))+'/'
R=[list(l.rstrip('\n')) for l in open(D+'../sprite_v4/raster.txt')][:64]
log=[]
def zet(y,x,c,reden):
    assert 29<=y<=46 and 8<=x<=32, (y,x)
    if R[y][x]!=c: log.append(f'({y},{x}) {R[y][x]}->{c}  {reden}'); R[y][x]=c
# 0) fout uit v3 herstellen: (44,8) was een maanpixel (G) die de vulstrook overschreef
zet(44,8,'G','maanpixel terug (v3-fout)')
# 1) linkeroog: Gengars linkeroog (rij 28-32 van anim_front, kol 19-23) op de plek van het modeloog (rood kol 14-17,
#    rij 30-35); Gengar-rij 30 twee keer (oog is 1 rij hoger dan Gengars). K = lijn/pupil, E = donkerrood (Gengar 6),
#    R = lichtrood (Gengar 5), a = dunne lijftintlijn links (Gengar d), b = lijf.
oog=['aEKbuu',   # r30  Gengar r28: d 6 e d     (schuine bovenlijn begint)
     'aERKKb',   # r31  r29: d 6 5 f e          (pupil f + bovenlijn)
     'aERKEK',   # r32  r30: c 6 5 f 6 e
     'aERREa',   # r33  (r30 herhaald, pupil eindigt)
     'baRRRa',   # r34  r31: d 5 5 5 d
     'bbaEab',   # r35  r32: d 6 d
     'bbbbbb']   # r36  lijf
for i,s in enumerate(oog):
    for j,c in enumerate(s): zet(30+i,13+j,c,'linkeroog Gengar-vorm')
for y in range(30,36): zet(y,12,'b','lijftint naast het oog (geen kom)')
# 2) rechteroog: lijn rechts één tint (a i.p.v. a/m door elkaar), onderkant donkerrood op het lijf (Gengar '666')
for y in (32,33,34): zet(y,31,'a','rechterlijn oog: a (was lichtere m)')
for x in (26,27,28): zet(36,x,'E','onderrij oog donkerrood zoals Gengar'); zet(37,x,'b','geen lichte rand onder het oog (was m)')
zet(36,24,'b','geen lichte pixel onder de ooghoek (was m)')
zet(34,25,'b','geen donkere kom-pixel naast het oog')
# wig (u) en a die direct tegen de wenkbrauw/het oog liggen -> b; de wig zelf blijft in het midden tussen de ogen
for y in range(29,37):
    for x in range(19,32):
        if R[y][x] in 'ua' and any(R[y+dy][x+dx] in 'KER' for dy in(-1,0,1) for dx in(-1,0,1)) and not (x==31 or (y,x) in ((35,23),(35,30),(36,29),(30,31),(31,31))):
            zet(y,x,'b','geen kom tegen het oog')
# 3) grijns: tanden wit, lijntjes één lichte grijs (H) in de naden; punten wit; dunne lijn eromheen
for x in range(14,31):
    for y in range(39,46):
        c=R[y][x]
        if c in 'Hh':
            naad = x in (19,23,28) or (x==24 and y>=44)
            zet(y,x,'H' if naad else 'W','tanden wit, naden H')
zet(39,13,'a','linkerpunt grijns had geen lijn')
zet(39,31,'W','rechterpunt tand wit (was H)')
zet(45,19,'a','onderlip één tint (was u)')
zet(46,25,'a','onderlip één tint (was lichtere m)'); zet(46,26,'a','idem')
zet(42,30,'a','lijn rechtsonder grijns (was lichtere m)'); zet(43,29,'a','idem'); zet(44,29,'a','grijns had hier geen lijn')
zet(45,28,'b','geen lichte pixel onder de mondhoek (was m)'); zet(45,29,'b','idem')
open(D+'raster.txt','w').write('\n'.join(''.join(r) for r in R)+'\n')
open(D+'raster.txt.log','w').write('\n'.join(log)+'\n')
v4=[l.rstrip('\n') for l in open(D+'../sprite_v4/raster.txt')]
buiten=[(y,x) for y in range(64) for x in range(64) if v4[y][x]!=R[y][x] and not(29<=y<=46 and 8<=x<=32)]
print(len(log),'wijzigingen; buiten de gezichtszone:',len(buiten))
