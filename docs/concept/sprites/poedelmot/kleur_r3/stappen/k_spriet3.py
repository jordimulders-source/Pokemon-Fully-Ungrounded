Z=set(tuple(map(int,l.split(','))) for l in open('spriet_zone.txt'))
NERF=[(3,18),(4,18),(5,18),(6,19),(7,19),(8,19),(9,20),(10,20),(11,20),(12,21),(13,21),(14,21),(15,22),(16,22),(17,23),(17,24),(18,25),(18,26),(19,27),(19,28),
      (51,19),(50,19),(49,19),(48,19),(47,19),(46,19),(45,20),(44,20),(43,20),(42,20),(41,21),(40,21),(39,21),(38,22),(37,22),(36,23),(35,23),(34,24),(33,24),(32,25),(31,26),(30,27),(29,28),(29,29)]
N=set(NERF); nerfy={}
for x,y in NERF: nerfy.setdefault(x,[]).append(y)
def buiten(x,y): return not (0<=x<64 and 0<=y<64) or r[y][x]=='.'
def rand(x,y): return [(dx,dy) for dx,dy in ((1,0),(-1,0),(0,1),(0,-1)) if (x+dx,y+dy) not in Z]
TIP={(1,18),(2,18),(2,19),(2,20),(3,20),(52,18),(52,19),(52,20),(51,20),(51,21)}
for (x,y) in Z:
    rd=rand(x,y)
    if (x,y) in N: c='C'
    elif rd:
        # belichte bovenkant/links tegen de achtergrond: bruin; elders zwartbruin
        lit=any(buiten(x+dx,y+dy) and (dy<0 or dx<0) for dx,dy in rd)
        c='3' if lit else '2'
        if (x,y) in TIP: c='4'
    else:
        top=min(nerfy.get(x,[99]))
        if y<top: c='1'                                # boven de nerf donker (geen kammetjes: dambordeffect)
        else:
            k=(x*7+y*13)%11                            # onregelmatig (vaste volgorde, geen ruis)
            if (x - y) % 3 == 0 and not (k==3 and y-top>3):
                c='6' if y-top<=2 else '5'
            else: c='1'
    r[y][x]=c
