# kraag hangt met getande plukken over het achterlijf (geen rechte onderrand)
TAND={29:48,30:49,31:48,32:47,33:48,34:49,35:48,36:47,37:48,38:48,39:47,40:47}
for x,yb in TAND.items():
    for y in range(46,yb+1):
        if r[y][x]!='.': r[y][x]='9' if (y>=yb-1 or x>=38) else 'A'
    for yy in (yb+1,yb+2):
        if r[yy][x] in '567': r[yy][x]='5'        # schaduw onder de pluk op het achterlijf
# kleine reparaties
r[34][10]='9'; r[36][56]='A'; r[42][20]='A'; r[44][15]='A'
r[56][42]='9'; r[58][26]='8'
r[44][40]='9'; r[45][40]='9'
r[36][56]='3'; r[50][32]='5'; r[56][29]='8'; r[57][29]='8'; r[56][42]='A'
r[46][37]='9'
