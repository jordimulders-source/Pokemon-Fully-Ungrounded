# sprieten terug naar de r2-basis: zwart vlak, één doorlopende lichte nerf, fijne schuine baarden van 1 px
Z=set(tuple(map(int,l.split(','))) for l in open('spriet_zone.txt'))
NERF=[(3,18),(4,18),(5,18),(6,19),(7,19),(8,19),(9,20),(10,20),(11,20),(12,21),(13,21),(14,21),(15,22),(16,22),(17,23),(17,24),(18,25),(18,26),(19,27),(19,28),
      (51,19),(50,19),(49,19),(48,19),(47,19),(46,19),(45,20),(44,20),(43,20),(42,20),(41,21),(40,21),(39,21),(38,22),(37,22),(36,23),(35,23),(34,24),(33,24),(32,25),(31,26),(30,27),(29,28),(29,29)]
N=set(NERF); nerfy={}
for x,y in NERF: nerfy.setdefault(x,[]).append(y)
def rand(x,y): return any((x+dx,y+dy) not in Z for dx,dy in ((1,0),(-1,0),(0,1),(0,-1)))
for (x,y) in Z:
    if (x,y) in N: c='C'
    elif rand(x,y): c='1'
    else:
        top=min(nerfy.get(x,[99]))
        if y<top: c='3' if x%3==0 else '1'
        else:
            k=(x*7+y*13)%11
            if (x - y//2) % 4 == 0 and k!=5:
                low=(x,y+1) in Z and rand(x,y+1)
                c='4' if low else '5'
            else: c='1'
    r[y][x]=c
