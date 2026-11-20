# r21: lijnen afgelezen op het model (44x-uitsnede kuif, profielmeting donkerste modelpixels per spritekolom voor de vleugel)
# kuifplukken: polylijnen (x,y) van uiteinde naar basis bij de kop
PLUK={
 'A':[(7,11),(9,15)],                           # buitenste streng links, dun tegen de lucht
 'B':[(12,9),(12,15),(11,17),(11,19)],                  # staande streng in de linker kwab
 'C':[(15,12),(14,15),(13,19)],                 # streng in de middelste kwab
 'D':[(22,10),(16,16)],                         # lange diagonaal (tip (23,10) valt buiten het silhouet)
 'E':[(24,14),(20,16),(18,17)],                 # vlakke streng naar rechts
 'F':[(28,19),(24,17),(21,18)],
 'G':[(19,19),(12,20)],                         # liggende streng boven het oog (model y 19-20)                 # onderste streng, steekt rechts uit (buitenste stuk = buitenlijn)
}
# vleugel: scheidingslijnen tussen de armpennen (donkerste modelpixels L<40 per kolom, prof.py), van voorrand naar achterrand
VEER=[
 [(37,27),(39,27),(43,29),(48,30)],
 [(34,29),(36,29),(37,28),(40,30),(44,32),(48,32)],
 [(36,30),(38,31),(40,33),(43,34),(45,34)],
 [(34,31),(36,32),(38,34),(40,36),(42,36)],
 [(32,32),(34,33),(36,35),(38,37)],
]
# slagpennen: waaier vanaf C (polar.py: per hoek het modellicht langs de straal). (hoek in graden, straal in spritepx), binnen -> buiten
C=(33.0,23.0)
# lichte schachten (maxima); begin pas waar de buurschacht >= 2,5 px verder ligt (anders klonteren ze op 1x)
SCHACHT=[[(-72,10),(-71,17)],[(-58,11),(-56.5,18)],[(-45,12),(-43,21)],[(-33,13),(-32,23)],
         [(-24,17),(-22,22)],[(-3,8),(-3,16)],[(8,8),(8,15)]]          
SCHEID=[[(-62,11),(-54,21.5)],[(-50,12),(-46,20.5)],[(-36.5,12),(-35,21)],[(-28.5,13),(-27,23)],
        [(-17,12),(-14.5,21.5)],[(-7,12),(-5,18)]]                       # donkere scheidingen tussen de pennen (minima)
import math
def xy(p):
    t=math.radians(p[0]); return (int(math.floor(C[0]+p[1]*math.cos(t))),int(math.floor(C[1]+p[1]*math.sin(t))))
def hoek(x,y):
    return math.degrees(math.atan2(y+.5-C[1],x+.5-C[0])), math.hypot(x+.5-C[0],y+.5-C[1])
# dekverenband langs de voorrand (r22): lichte strepen schuin omhoog, afgelezen op het model (22x-uitsnede x22-40, y12-42)
BAND=[[(25,37),(30,25),(32,19)],[(28,37),(33,27)]]
