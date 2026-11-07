# sprieten: vlak (bijna) zwart, nerf als handgetekende curve, baarden fijn schuin omlaag
sil=[[c!='.' for c in row] for row in r]
def coltop(x, y0=0):
    for y in range(y0,64):
        if sil[y][x]: return y
# onderrand (laatste sprietrij) per kolom, met de hand uit de bron
BOT_L={1:18,2:20,3:21,4:23,5:24,6:25,7:25,8:26,9:26,10:27,11:27,12:28,13:28,14:28,15:29,16:29,17:29,18:29,19:29,20:29}
BOT_R={28:29,29:30,30:30,31:30}
BOT_R.update({x:29 for x in range(32,42)}); BOT_R.update({42:28,43:27,44:27,45:26,46:26,47:25,48:24,49:23,50:22,51:21,52:20})
TOP_R={28:27,29:25,30:24}
Z=set()
for x,b in BOT_L.items():
    t=coltop(x)
    if x==20: t=26
    for y in range(t,b+1): Z.add((x,y))
for x,b in BOT_R.items():
    t=TOP_R.get(x, coltop(x,15))
    for y in range(t,b+1): Z.add((x,y))
NERF_L=[(3,18),(4,18),(5,18),(6,19),(7,19),(8,19),(9,20),(10,20),(11,20),(12,21),(13,21),(14,21),(15,22),(16,22),(17,23),(17,24),(18,25),(18,26),(19,27),(19,28)]
NERF_R=[(51,19),(50,19),(49,19),(48,19),(47,19),(46,19),(45,20),(44,20),(43,20),(42,20),(41,21),(40,21),(39,21),(38,22),(37,22),(36,23),(35,23),(34,24),(33,24),(32,25),(31,26),(30,27),(29,28),(29,29)]
N=set(NERF_L)|set(NERF_R)
def rand(x,y): return any((x+dx,y+dy) not in Z for dx,dy in ((1,0),(-1,0),(0,1),(0,-1)))
nerfy={}
for x,y in N: nerfy.setdefault(x,[]).append(y)
for (x,y) in Z:
    c='1'
    if (x,y) in N: c='6'
    elif rand(x,y): c='1'
    elif y < min(nerfy.get(x,[99])):           # kammetje boven de nerf
        c='3' if x%3==0 else '1'
    else:                                       # baarden: fijne schuine streepjes
        if (x - y//2) % 4 == 0:
            low = (x, y+1) in Z and rand(x, y+1)
            c = '3' if low else '4'
    r[y][x]=c
