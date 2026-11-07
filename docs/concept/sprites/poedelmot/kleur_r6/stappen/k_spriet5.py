# sprieten: zwart vlak, lichte nerf, baarden als doorlopende schuine streepjes (ongelijke afstand 2-3),
# licht (5) bij de nerf en tussentint (3) verder weg; belichte bovenrand donkerbruin (2)
Z=set(tuple(map(int,l.split(','))) for l in open('spriet_zone.txt'))
NERF=[(3,18),(4,18),(5,18),(6,19),(7,19),(8,19),(9,20),(10,20),(11,20),(12,21),(13,21),(14,21),(15,22),(16,22),(17,23),(17,24),(18,25),(18,26),(19,27),(19,28),
      (51,19),(50,19),(49,19),(48,19),(47,19),(46,19),(45,20),(44,20),(43,20),(42,20),(41,21),(40,21),(39,21),(38,22),(37,22),(36,23),(35,23),(34,24),(33,24),(32,25),(31,26),(30,27),(29,28),(29,29)]
N=set(NERF); nerfy={}
for x,y in NERF: nerfy.setdefault(x,[]).append(y)
def buiten(x,y): return not (0<=x<64 and 0<=y<64) or r[y][x]=='.'
def rand(x,y): return [(dx,dy) for dx,dy in ((1,0),(-1,0),(0,1),(0,-1)) if (x+dx,y+dy) not in Z]
SPATIE={0,2}                      # streep op fase 0 en 2 van 5: afstand 2-3-2-3
for (x,y) in Z:
    rd=rand(x,y)
    if (x,y) in N: c='C'
    elif rd:
        lit=any(buiten(x+dx,y+dy) and dy<0 for dx,dy in rd)
        c='2' if lit else '1'
    else:
        top=min(nerfy.get(x,[99]))
        rib=((x - y//2) % 3 == 0)                                         # ribben schuin zoals in het model (beide sprieten)
        c='4' if rib else '1'                                             # één tint per rib
    r[y][x]=c
