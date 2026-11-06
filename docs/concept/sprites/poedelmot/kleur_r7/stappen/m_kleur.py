Z=set(tuple(map(int,l.split(","))) for l in open("spriet_zone.txt"))
# r2 -> r3 tinten: wit A en 9 samen tot A, grijsroze 8 -> koel licht 9, C -> koel diep 8
M={'A':'A','9':'A','8':'9','C':'8'}
for y in range(64):
    for x in range(64):
        c=r[y][x]
        if c in M and (x,y) not in Z: r[y][x]=M[c]
