# r15 (hand): schubjes verspringend (linker weg, rechter een rij lager), taps uitlopende naden, koepels D en E
F={}
def put(y,x0,s):
    for i,c in enumerate(s):
        if c!='=': F[(x0+i,y)]=c
# 1 schubjes
put(31,47,"777"); put(32,47,"777")
put(31,51,"777"); put(32,51,"666"); put(33,51,"444")
# 2 naden taps (licht boven, donker in het dal)
put(52,20,"66"); put(53,20,"6")          # A/B: (21,51) 7, (21,52) 6, (21,53-54) 3
put(49,31,"8")           # plaatlijnen beginnen in de plaattint
put(56,28,"6")                           # B/B2-naad loopt rechts uit
put(54,41,"6")                           # C/D-naad begint licht
put(54,35,"5")                           # C-linkerrand begint in de schaduwtint
put(53,46,"7")                           # D/E-naad begint licht
# 3 koepels
put(51,43,"333"); put(52,42,"3AAA3")     # D: ronde top
put(47,45,"3A")                          # E: ronde linkerbovenhoek
W={}
for (x,y),c in F.items(): W.setdefault(y,[]).append((x,c))
