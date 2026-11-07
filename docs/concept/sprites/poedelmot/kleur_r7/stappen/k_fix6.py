r[21][52]='4'; r[35][58]='9'; r[36][13]='3'
r[41][18]='4'
from collections import Counter
for x,y in [(56,20),(57,20),(55,21),(56,21),(37,34),(37,35),(58,35)]:
    own=r[y][x]
    c=Counter(r[y+dy][x+dx] for dx,dy in ((1,0),(-1,0),(0,1),(0,-1)) if r[y+dy][x+dx] in '56789A' and r[y+dy][x+dx]!=own)
    r[y][x]=c.most_common(1)[0][0] if c else '4'
r[20][56]=r[20][55] if r[20][55] in '56789A' else 'A'
