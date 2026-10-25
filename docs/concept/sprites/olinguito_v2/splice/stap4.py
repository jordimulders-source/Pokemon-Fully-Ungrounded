import numpy as np, sys
sys.path.insert(0, sys.argv[1]); S = sys.argv[1]
from common import show
g = np.load(S + '/stap3.npy', allow_pickle=True)
# voeten oudroze (was Linoone's witte klauwtjes)
for y in range(40, 60):
    for x in range(0, 48):
        if g[y, x] == 'C': g[y, x] = 'P'
# Sandslash-klauwen, kleiner: 2 per voorpoot, vast aan elkaar; C licht, g schaduw, K omlijning
def claws(x0, y0):
    pat = ["KCCCK",
           "KCgCK",
           "KCKgK",
           "KgKK.",
           ".K..."]
    for j, r in enumerate(pat):
        for i, c in enumerate(r):
            if c != '.': g[y0 + j, x0 + i] = c
claws(5, 53)    # nabije voorpoot
claws(13, 54)   # verre voorpoot
np.save(S + '/stap4.npy', g); show(g, S + '/stap4.png'); show(g, S + '/stap4_1x.png', 1)
