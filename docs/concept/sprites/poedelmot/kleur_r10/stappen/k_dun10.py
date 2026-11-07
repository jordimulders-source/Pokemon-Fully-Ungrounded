# dubbele (2 px) binnenlijnen naar 1 px: '3' met '3' erboven en vlak eronder wordt dat vlak
def binnen(x,y): return all(r[y+dy][x+dx]!='.' for dx,dy in ((1,0),(-1,0),(0,1),(0,-1)))
for y in range(44,58):
    for x in range(14,56):
        if r[y][x]=='3' and r[y-1][x] in '23' and r[y+1][x] in '67A' and binnen(x,y): r[y][x]=r[y+1][x]
