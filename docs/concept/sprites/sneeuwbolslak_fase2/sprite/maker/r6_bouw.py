# r6: KEURING_r5 MOET 1-4 op raster_r5, verder diff 0. Vanuit sneeuwbolslak_fase2/: python3 sprite/maker/r6_bouw.py
R=[list(l.rstrip('\n')) for l in open('sprite/maker/raster_r5.txt')]
O=[r[:] for r in R]
def P(x,y,ch): assert R[y][x]!='.'; R[y][x]=ch
# 1 aansluiting bol/lijf links + gesloten ringeinde
P(22,38,'a'); P(22,39,'c'); P(23,39,'a')   # d/# gaf 2 nieuwe rechte stukken van 4 px (recht 23); a = halfdonker (model L 96/78)
P(24,40,'#'); P(25,41,'r')
# 2 ring: grond r, alleen middenstrook s (27-32,42), geen t
for x in (25,26): P(x,40,'r')
for x in range(26,30): P(x,41,'r')
for x in range(34,38): P(x,41,'r')
for x in range(37,40): P(x,40,'r')
P(39,39,'r')
for x in range(29,32): P(x,43,'r')
# 3 staartnaad doorgaand
P(49,33,'d'); P(49,34,'a'); P(49,35,'d')
# 4 kopschaduw als boog
for x in (12,13,18): P(x,42,'e')
P(11,43,'e')
open('sprite/maker/raster_r6.txt','w').write('\n'.join(''.join(r) for r in R)+'\n')
print('pixels gewijzigd t.o.v. r5:',sum(R[y][x]!=O[y][x] for y in range(64) for x in range(64)))
print('t over:',sum(r.count('t') for r in R),' s:',[(x,y) for y in range(64) for x in range(64) if R[y][x]=='s'])
