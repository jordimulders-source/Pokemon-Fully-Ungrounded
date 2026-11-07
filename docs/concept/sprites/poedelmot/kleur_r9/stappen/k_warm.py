# geen lila in het lijf: koele tinten uit r3 -> warme bronkleuren; alleen de pootpluimen houden grijsroze
B=[('E',49.5,50.2,4.6,4.6),('D',44.3,55.2,3.3,4.1),('b',28.0,57.2,3.0,2.3),('A',18.3,51.6,3.3,4.3),('B',26.3,52.1,4.4,4.4),('C',37.8,57.0,3.3,3.9)]
pluim=set()
for n,cx,cy,rx,ry in B:
    for y in range(44,62):
        for x in range(12,57):
            if ((x-cx)/rx)**2+((y-cy)/ry)**2<=1.0: pluim.add((x,y))
for y in range(64):
    for x in range(64):
        c=r[y][x]
        if c=='9': r[y][x]='7'
        elif c=='8' and (x,y) not in pluim: r[y][x]='6'
