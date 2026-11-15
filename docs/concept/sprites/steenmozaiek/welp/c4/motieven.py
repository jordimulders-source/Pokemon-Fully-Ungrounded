# Chavin-motieven als stempels ((x0,y0), tekst). Met de hand getekend; zie c1.py voor de tekens.
# Jordi (15 nov): "dubbele spiralen etc hoeft niet, een paar lijnen is genoeg, paar grote voluten ook".
def spiegel(t): return '\n'.join(r[::-1] for r in t.strip('\n').split('\n'))
SCHOUDER="""
...iiiii...
.ii.....ii.
.i.......i.
i.........i
i....ii...i
i...i..i..i
i...ic.i..i
i...i.....i
.i..i....i.
.i..i...i..
i....iii...
i..........
"""
DIJ="""
..iiiii..
.i.....i.
i.......i
i.......i
i...ii..i
i..i.c..i
.i..i..i.
.i...ii..
i........
"""
STEMPELS=[
((27,33),SCHOUDER),            # schoudervolute, staart omlaag naar de voorpoot
((27,51),"g.....g\n.ggggg.\ng.....g\n.ggggg."),   # twee banden om de voorpoot, buigen 1 px mee met de rondte
((53,52),"ggg"),               # ring om de staart
# kerfjes (kleine putjes in de steen, 1 px met lichtrand)
((42,41),"g"),((44,55),"g"),
]

# ---- c4: dij opnieuw (keuring c2 MOET 1): facetten + rustige voluut met max. 1,5 omwenteling ----
# Dijvlak: rand boven licht (5), vlak 4, schaduwsikkel 3 rechts en onder (licht linksboven, geen licht aan de achterkant meer).
DIJVLAK={48:(39,'555555443'),49:(38,'55444444333'),50:(38,'54444444333'),51:(38,'54444444333'),52:(38,'54444444333'),
         53:(38,'44444444333'),54:(38,'44444444333'),55:(37,'333333333333'),56:(37,'333333333333')}
# Dijvoluut als pad (x,y): staart rechtsonder -> rechterkant omhoog -> boven -> linkerkant omlaag -> onderkant -> krul naar binnen.
DIJPAD=[(47,56),(47,55),(47,54),(47,53),(47,52),(46,51),(45,50),(44,49),(43,49),(42,49),(41,49),(40,50),(39,51),(39,52),(39,53),
        (40,54),(41,55),(42,55),(43,55),(44,54),(44,53),(43,52),(42,52)]
for y,(x0,t) in DIJVLAK.items(): STEMPELS.append(((x0,y),t))
STEMPELS.extend(((x,y),'g') for x,y in DIJPAD)
