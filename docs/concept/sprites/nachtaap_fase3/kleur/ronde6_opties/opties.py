# Opties ronde 6: aanzet opgeheven been / heup. Rijtabel per optie:
# rij: (L, b4, b3, R, xs)  L=linker omlijning (2), L+1..b4-1 = 5, b4..b3-1 = 4, b3..R-1 = 3, R = 1 (zwart)
# xs = vanaf welke kolom de rij wordt herschreven (links daarvan blijft alles staan).
# Rechts van R (tot x43) wordt transparant als het eerder been/rand was.
from PIL import Image
BASIS='../ronde6/nachtaap_fase3.png'

def maak(tabel, extra=None):
    im=Image.open(BASIS); a=im.load()
    for y,(L,b4,b3,R,xs) in tabel.items():
        for x in range(xs, 44):
            if x==L: c=2
            elif x<L: continue
            elif x<b4: c=5
            elif x<b3: c=4
            elif x<R: c=3
            elif x==R: c=1
            else: c=0
            a[x,y]=c
    if extra:
        for (x,y),c in extra.items(): a[x,y]=c
    return im


def tab(contour, rim=None):
    """contour: {rij:(L,R,xs)}; lichtrand 2 px langs L (in de onderste rijen breder, rim), schaduw 2 px langs R."""
    t={}
    for y,(L,R,xs) in contour.items():
        b4 = (rim or {}).get(y, L+3)
        t[y]=(L,b4,R-2,R,xs)
    return t

# A: omtrek van ronde 6, alleen de taille r24-25 dicht en de hoeken aan de wortel 1 px afgerond, toon zoals C: middentoon van de dij loopt door in de heup
A=tab({22:(32,38,31),23:(31,38,30),24:(31,38,30),25:(31,38,30),26:(31,39,30),27:(30,39,29),
       28:(30,40,29),29:(29,40,28),30:(28,41,28),31:(0,41,28),32:(0,42,28),33:(0,42,28)},
      rim={28:33,29:32,30:32,31:32,32:32,33:32})
# B: dij breed aan de wortel (holle curve links naar de rug, rechts naar de staartwortel), toon idem
B=tab({22:(32,38,31),23:(31,39,30),24:(31,39,30),25:(31,40,30),26:(30,40,29),27:(30,41,29),
       28:(29,41,28),29:(28,42,27),30:(27,42,26),31:(0,42,28),32:(0,43,28),33:(0,43,28)},
      rim={28:32,29:31,30:31,31:32,32:32,33:32})
# C: de hele dij taps (dik bij de heup, dun naar de knie) vanaf r18, dus geen trechter alleen onderaan
C=tab({18:(32,39,31),19:(32,39,31),20:(31,39,30),21:(31,40,30),22:(31,40,30),23:(31,40,30),
       24:(30,41,29),25:(30,41,29),26:(30,41,29),27:(29,42,28),28:(29,42,28),29:(28,42,27),
       30:(27,42,26),31:(0,42,28),32:(0,43,28),33:(0,43,28)},
      rim={29:31,30:31,31:32,32:32,33:32})
if __name__=='__main__':
    for n,t in (('A',A),('B',B),('C',C)):
        maak(t).save('optie_%s.png'%n, transparency=0)
