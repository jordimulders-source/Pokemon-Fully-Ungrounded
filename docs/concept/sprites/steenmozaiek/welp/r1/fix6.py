# Ronde 1, stap 7: silhouet heup-rug hersteld, toon naar het model (borst/onderarm/voorpoot/heup donkerder), onderarmkrul duidelijker.
from edit import *
g[48][47]='.'; g[48][46]='1'; g[49][47]='1'
# borst: overwegend 3, kleine middentint (model)
for y,s in [(42,"3333"),(43,"3343"),(44,"3343"),(45,"2343"),(46,"2343"),(47,"3333"),(48,"3332")]:
    put(y,21,s)
# onderarm: bovenrand 4, midden 3, onderkant 2; lila krul (C) x17-21 y45-48
put(45,17,"48772"); put(46,17,"83337"); put(47,17,"73236"); put(48,15,"3336633")
put(49,16,"2222222")
put(46,22,"2"); put(47,22,"2")
# voorpoot: facet minder licht
for y in range(50,57):
    for x in range(26,33):
        if g[y][x]=='5': g[y][x]='4'
        elif g[y][x]=='4' and x>=30: g[y][x]='3'
# heup: onderste helft donkerder
for y in range(53,57):
    for x in range(37,47):
        if g[y][x]=='4': g[y][x]='3'
save()
