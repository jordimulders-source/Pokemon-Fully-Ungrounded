# r6.py: alleen kleurwijzigingen op r5 (raster_r5.txt -> raster.txt); vorm en lijnposities 1-op-1 gelijk.
R=[list(l.rstrip('\n')) for l in open('raster_r5.txt')][:64]
def put(pts,ch,van=None):
    for x,y in pts:
        assert van is None or R[y][x] in van, (x,y,R[y][x]); R[y][x]=ch
# 1. lichtkant van de gevelhuisjes (linker- en bovenranden) van + (B) naar selout e (G); schaduwkant/plankranden blijven +
put([(40,4),(39,5),(39,6),(39,7),(38,8)],'e','+')                                   # linker topgevel, linkerrand
put([(33,8),(31,9),(32,9),(30,10),(30,11),(29,12),(29,13),(28,14),(28,15),(36,9),(37,9)],'e','+')  # middelste gevel + terrasrand erachter
put([(22,18),(23,18),(24,18),(25,18),(20,19),(21,19),(20,20),(19,21),(19,22),(18,23),(18,24),(18,25),(17,26),(16,26)],'e','+')  # linker onderste gevel
put([(34,19),(35,19),(36,19),(37,19),(38,19),(33,20),(32,21),(32,22),(31,23),(31,24)],'e','+')    # rechter onderste gevel
# 3. lange binnenlijnen op lichte vlakken: voet y27 x17-30 en y16 x28-36 -> e
put([(x,27) for x in range(17,31)],'e','+'); put([(x,16) for x in range(28,37)],'e','+')
# 2. linkerhoek van de kap (model tonen.py: y33-34 licht, y35 kapvoorkant 16, y36 schaduwlijn x14+ doorgetrokken tot de hoek)
put([(12,35),(13,35)],'b','d'); put([(12,36),(13,36)],'d','a')
put([(10,40)],'d','a')   # rand gezicht/vleugel (model lijn x10 y38-39, x9 y40+): doorlopend, geen los 2-px stukje
open('raster.txt','w').write('\n'.join(''.join(r) for r in R)+'\n')
