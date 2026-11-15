# Ronde 1, handwerk stap 2: silhouet links (ver oog), oog 1 px naar rechts, oor rechts, mond, rugzwiep, heup- en haakspiraal.
from edit import *
# ver oog op de linkercontour (model x10-12, y30-32); contour links model x10-11
put(28,11,"1"); put(28,12,"5")
put(29,11,"15")
put(30,10,"1d1"); put(31,10,"1d1"); put(32,10,"123")
put(33,10,"15")
# nabij oog: x20-23 (model-midden x22)
put(29,19,"3"); put(29,20,"1112")
put(30,19,"3"); put(30,20,"1e1d2")
put(31,19,"3"); put(31,20,"1e1d2")
put(32,19,"4"); put(32,20,"2aaa3")
# rechteroor/kop: model rand x31 tot y29, kop x30-31 eronder
put(28,28,"2331"); put(29,26,"43331"); put(30,27,"4331"); put(31,28,"321")
# mondhoek: zwarte lijn van de mondhoek schuin omhoog naar de wang (model)
put(36,22,"3"); put(36,23,"11"); put(36,25,"2"); put(37,21,"11"); put(37,25,"2")
put(35,25,"2")
# rugzwiep 1 px van de rugrand af, eindigt in spiraal rond (38,42)
for (x,y) in [(34,36),(34,37),(35,37),(35,38),(36,38),(36,39),(37,39),(38,40),(39,40),(40,41),(41,42),(41,43),(40,44),(39,44),(38,44),(37,43),(37,42),(38,41),(39,41),(39,42),(38,42),(38,43),(39,43),(40,43),(40,42)]:
    g[y][x]='4'
put(34,33,"8"); put(35,33,"8"); put(36,33,"87"); put(37,33,"5"); put(37,34,"87")
put(38,34,"5"); put(38,35,"877"); put(39,35,"5"); put(39,36,"5877")
put(40,37,"5"); put(40,38,"87"); put(40,39,"7")
put(41,36,"4"); put(41,37,"8"); put(41,38,"4"); put(41,39,"4"); put(41,40,"6")
put(42,36,"7"); put(42,37,"5"); put(42,38,"2"); put(42,39,"4"); put(42,40,"6")
put(43,36,"7"); put(43,37,"4"); put(43,38,"3"); put(43,39,"2"); put(43,40,"6")
put(44,37,"6"); put(44,38,"6"); put(44,39,"6"); put(44,40,"3")
put(39,37,"7"); put(39,38,"7")
# schouderspiraal: haak eronder opnieuw
for y in range(49,55):
    for x in range(29,36):
        if g[y][x] in 'a9': g[y][x]='4'
put(49,34,"9"); put(50,34,"9"); put(51,31,"aa 9"); put(52,30,"a 2 9"); put(53,31,"999")
# heup: spiraal opnieuw (groter, rond (43,54))
for y in range(49,58):
    for x in range(38,48):
        if g[y][x] in '6789a': g[y][x]='4'
put(49,37,"5555555")
put(50,38,"8877776"); 
put(51,38,"87444466")
put(52,38,"7444aaa446")
put(53,38,"744a444a46")
put(54,38,"744a424946")
put(55,38,"6449422446")
put(56,38,"36449994 6")
put(57,40,"666666")
save()
