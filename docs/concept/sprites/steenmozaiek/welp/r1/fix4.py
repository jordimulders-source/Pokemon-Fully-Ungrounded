# Ronde 1, stap 5: heupspiraal opnieuw (twee geneste C's, groter dan model), dijcontour, facetten, selout lichtkant.
from edit import *
H={48:"32222222233",
   49:"25555555523",
   50:"58877777423",   # x37..47 ; dijcontour x36 apart
   51:"84444aaa446",
   52:"7444a444a46",
   53:"744a422a4 6",
   54:"744a4424446",
   55:"6444aaaa446",
   56:"366666666 3"}
# rijen 48-49 beginnen op x37, de rest op x37 met contour op x36
for y,s in H.items():
    for i,c in enumerate(s):
        if c!=' ': g[y][37+i]=c
# creme: onderste rij in schaduwtint, rechterkant donkerder
for x in range(41,45): g[55][x]='9'
g[53][40]='a'; g[54][40]='9'; g[53][41]='4'; g[52][41]='a'
g[51][42]='a'; g[51][43]='a'; g[51][44]='a'; g[52][45]='a'; g[53][45]='9'
for y in range(50,57): g[y][36]='2'
g[49][36]='3'; g[48][36]='3'
for y in range(51,57): g[y][47]='2' if y>51 else '3'
g[50][47]='2'; g[49][47]='3'
# voorpoot (staand): lichte facet links-boven
for y in range(51,57):
    for x in (27,28):
        if g[y][x]=='4': g[y][x]='5'
# rug rechts van de schouderspiraal iets donkerder naar de rand
for y in range(44,48):
    for x in range(41,45):
        if g[y][x]=='4': g[y][x]='3'
# selout (lichtkant: boven en links) -> diep bruin
for (x,y) in [(14,22),(15,22),(13,23),(16,23),(17,24),(18,24),(27,22),(28,22),(29,22),(26,23),
              (12,24),(12,25),(12,26),(12,27),(11,28),(11,29),
              (32,33),(34,34),(34,35),(35,36),(36,37),(37,38),(38,38),
              (12,42),(13,42),(14,42),(15,42),(16,42),(11,43),(10,44),(9,45),(17,44),(18,44),(19,44),
              (24,57),(23,58),(23,59),(51,50),(52,50),(53,50),(50,51)]:
    if g[y][x]=='1': g[y][x]='2'
for x in range(19,26):
    if g[23][x]=='1': g[23][x]='2'
save()
