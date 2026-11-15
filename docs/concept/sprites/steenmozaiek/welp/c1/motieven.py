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
i...ii..i
i..i..i.i
i..i.c..i
.i..i..i.
.i...ii..
i........
"""
STEMPELS=[
((27,33),SCHOUDER),            # schoudervolute, staart omlaag naar de voorpoot
((39,48),spiegel(DIJ)),        # dijvolute, gespiegeld: staart naar achteren/omlaag
((27,52),"ggggggg\n.......\nggggggg"),   # band om de voorpoot
((53,52),"ggg"),               # ring om de staart
# kerfjes (kleine putjes in de steen, 1 px met lichtrand)
((42,41),"g"),((44,55),"g"),
]
