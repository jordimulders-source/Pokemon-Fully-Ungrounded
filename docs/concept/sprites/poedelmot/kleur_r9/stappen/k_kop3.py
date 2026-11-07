Z=set(tuple(map(int,l.split(','))) for l in open('spriet_zone.txt'))
def P(c,pts):
    for x,y in pts:
        if r[y][x]=='.': raise SystemExit(f'P op transparant {x},{y}')
        r[y][x]=c
def H(c,y,x0,x1):  P(c,[(x,y) for x in range(x0,x1+1)])
# schuine vleugelvoetlijn (kop | vleugel), met de hand op de bron: (37,29) -> (41,47)
DIAG={y:36+round((y-29)*6/17) for y in range(30,48)}
# 1) witte basis voor alles links van de lijn (sprieten, buitenrand blijven)
for y in range(26,48):
    for x in range(5,DIAG.get(y,37)):
        if r[y][x]!='.' and (x,y) not in Z: r[y][x]='A'
for y,x in DIAG.items(): r[y][x]='3'
for y,x in DIAG.items():
    if r[y][x+1] not in '.': r[y][x+1]='6'          # slagschaduw van de kop op de vleugelvoet
# 2) kruin: plukjes tussen de sprietvoeten
P('9',[(23,28),(23,29),(23,30),(26,28),(26,29),(26,30)])
P('9',[(28,31),(29,31),(30,31),(31,31)])            # schaduw van de sprietvoet op de kop
# 3) verre vleugel: wit, zachte schaduw onder de spriet en rechtsonder, getande rand met plukjes
P('9',[(11,28),(11,29),(12,29),(13,29),(14,29),(15,30),(16,30)])
P('9',[(11,34),(11,35),(12,35)])
# 4) ver oog: smal, staand ovaal (zwart x16-19), glans 2 px
EYE_F={32:(17,"22"),33:(17,"11"),34:(16,"1A11"),35:(16,"1A11"),36:(16,"1111"),37:(16,"1111"),38:(16,"2B11"),39:(17,"212")}
for y,(x0,s) in EYE_F.items():
    for i,c in enumerate(s): r[y][x0+i]=c
P('9',[(15,34),(15,35),(15,36),(15,37),(15,38),(16,39)])      # zachte rand links van het verre oog
# 5) nabij oog met tan ring rondom
EYE_N={32:(29,"222"),33:(27,"211112"),34:(26,"2AA11112"),35:(25,"21AA11112"),36:(25,"211111112"),37:(25,"21111BB12"),38:(25,"211BBB12"),39:(25,"2111112"),40:(26,"22222")}
for y,(x0,s) in EYE_N.items():
    for i,c in enumerate(s): r[y][x0+i]=c
RING=[(28,31),(29,31),(30,31),(31,31),(32,31),(27,32),(28,32),(32,32),(33,32),(26,32),(26,33),(25,33),(33,33),(34,33),
      (25,34),(24,34),(34,34),(24,35),(34,35),(24,36),(34,36),(24,37),(34,37),(24,38),(33,38),(34,38),(24,39),(32,39),(33,39),
      (24,40),(25,40),(31,40),(32,40),(25,41),(26,41),(27,41),(28,41),(29,41),(30,41),(31,41)]
P('6',RING)
# 6) snuit en glimlachboog (laagste punt x22-26, y43)
P('7',[(20,40),(21,40),(22,40),(23,40),(21,41),(22,41),(23,41),(24,41),(23,42),(24,42),(25,42)])
P('4',[(19,40),(19,41)])
P('3',[(20,41),(21,42),(22,42),(22,43),(23,43),(24,43),(25,43),(26,43),(26,42),(27,42),(28,42),(29,41),(30,41)])
P('4',[(31,41)]); P('9',[(20,42)])
# 7) schaduwsikkels (koel) en slagschaduw onder de kin
P('9',[(23,44),(24,44),(25,44),(26,44),(27,43),(28,43),(29,43),(30,43),(31,43),(29,42),(30,42),(31,42)])
for y in range(31,36):
    if DIAG[y]>37: P('9',[(37,y)])
for y in range(36,40): P('9',[(38,y)])
for y in range(40,44): P('9',[(38,y)]); P('8',[(39,y)])
for y in range(44,47): P('9',[(39,y)]); P('8',[(40,y)])
P('9',[(35,40),(36,40),(35,41),(36,41)])
P('9',[(34,46),(35,46),(36,46),(37,46),(36,45),(37,45),(38,45)])
# 8) plukjes (haarstreepjes van 3 px) in kraag en langs de linkerrand
for pl in [[(17,44),(17,45),(18,45)],[(21,45),(21,46),(22,46)],[(27,45),(27,46),(28,46)],[(32,44),(32,45),(33,45)],
           [(13,40),(13,41),(14,41)],[(15,44),(15,45),(16,45)]]:
    P('9',pl)
P('9',[(16,40),(16,41),(16,42),(17,42),(17,43)])
