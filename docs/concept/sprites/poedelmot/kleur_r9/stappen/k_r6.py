def P(c,pts):
    for x,y in pts:
        if r[y][x]!='.': r[y][x]=c
def lijn(c,pts):
    for (x0,y0),(x1,y1) in zip(pts,pts[1:]):
        n=max(abs(x1-x0),abs(y1-y0))
        for i in range(n+1):
            x=round(x0+(x1-x0)*i/n); y=round(y0+(y1-y0)*i/n)
            if r[y][x] not in '.123': r[y][x]=c
# 1. vleugelvoet: geen rechte kolom; zachte voetlijn en gebogen aders die naar de rand waaieren
DIAG={y:36+round((y-29)*6/17) for y in range(30,48)}
for y,x in DIAG.items():
    r[y][x]='4' if 33<=y<=43 else '6'                        # voetlijn: één zachte lijntint, taps (6) aan de uiteinden
# 2. mond/kin: zachte tapse boog in lichte lijntint (geen donkere streep)
for x in range(17,31):
    for y in (40,41,42):
        if r[y][x] in '34' and x not in (24,25,26,27,28,29,30,31) or (y in (41,42) and r[y][x]=='3' and x<=29):
            r[y][x]='7'
P('3',[(19,41),(20,41),(21,41),(22,42),(23,42),(24,42),(25,42),(26,41),(27,41)])   # kinboog zoals het model: dunne donkere boog met dip
# kruin: witte plukjes (kuif) tussen de sprietvoeten
P('4',[(22,27),(23,27),(24,27),(25,27)])   # buitenrand in selout (Gen 3); witte kuif eronder
# 3. linkervleugel: tapse binnenlijn tussen de lob achter de kop en het gezicht
P('7',[(12,28),(14,37)]); P('3',[(12,29),(13,30),(13,31),(13,32),(14,33),(14,34),(14,35),(14,36)])
# 4. pluimen: ronde bovenkant (boog), klauwtjes als schuine stompjes aan de pluim
P('3',[(16,49),(17,48),(18,48),(19,48),(20,48),(21,49)])
P('3',[(24,49),(25,48),(26,48),(27,48),(28,48),(29,49)])
P('A',[(16,48)] if r[48][16]!='.' and False else [])
r[26][21]='3'
