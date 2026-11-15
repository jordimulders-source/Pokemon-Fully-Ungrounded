# Ronde 1, stap 4: rugrand-pixel terug, schouderspiraal als '@' (spiraalarm naar het midden).
from edit import *
put(39,39,"1")
rows={40:"...aaaaa...",
      41:"..a88877a..",
      42:".a8222227a.",
      43:"a82477742 6a",
      }
S=["...aaaaa...",
   "..a88877a..",
   ".a8222227a.",
   "a82477742a.",
   "a72744472a.",
   "a72742772a.",
   "a72744442a.",
   "a62477722a.",
   ".a6222226a.",
   "..a66666.9.",
   "...aa....9."]
for j,r in enumerate(S):
    for i,c in enumerate(r):
        if c!='.': g[40+j][25+i]=c
# rechterkant van de creme ring zat op x35; houd die (model x35)
for y in range(43,48): g[y][34]='6'; g[y][35]='a'
save()
