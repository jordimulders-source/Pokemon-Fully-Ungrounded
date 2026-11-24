"""Capykart r9 -> r10: keurderpunten (DC-keuring r9), alleen tintwissels. Coördinaten = grid (geen offset; gecontroleerd op de vlekjes van punt 1)."""
import os
from PIL import Image
D=os.path.dirname(os.path.abspath(__file__))
im=Image.open(os.path.join(D,'../r9/capykart.png')); W,H=im.size
g=[[im.getpixel((x,y)) for x in range(W)] for y in range(H)]
LOG=[]; MIS=[]
def sw(pts, frm, to, punt):
    for x,y in pts:
        v=g[y][x]
        if v==0: raise SystemExit(f'transparant {x},{y}')
        if v in frm: g[y][x]=to; LOG.append((punt,x,y,v,to))
        elif v!=to: MIS.append((punt,x,y,v))
R=lambda xs,ys:[(x,y) for y in ys for x in xs]
# 1 rood blok
sw([(46,17),(47,17),(45,18),(48,18),(49,18)],[5],12,'1 oranje vlekjes rood -> rood')
sw(R(range(45,53),[18]),[12,5],7,'1 bovenste rij rood blok = slagschaduw onder geel')
# 2 geel blok
sw(R(range(51,55),[11]),[5],13,'2 geel rechtervlak onder overhang')
# 3 blauw blok
sw(R(range(46,50),[26]),[9],10,'3 geen wit direct onder rood')
sw(R(range(50,55),[26]),[10],8,'3 slagschaduw van rood op blauwe zijkant')
# 4 kop sikkel wang
for y,xs in [(22,[35]),(23,[35,36]),(24,[34,35]),(25,[32,33,34]),(26,[30,31,32,33]),(27,[27,28,29,30])]:
    sw([(x,y) for x in xs],[2],3,'4 sikkel wang rechtsonder')
sw(R([37],range(18,23)),[3],4,'4 binnenrand rechts')
# 6 neusvoorvlak
sw(R([3,4,6,7],range(45,52)),[13],6,'6 strepen x3/4, x6/7 weg')
sw(R(range(5,16),[50,51]),[6],13,'6 sikkel boven onderlijn')
# 7 middenpaneel
sw(R(range(36,47),range(47,50)),[4],13,'7 middenpaneel r47-49 4->13')
# 8 losse pixels
sw([(13,40)],[13],6,'8'); sw([(18,44)],[6],13,'8'); sw([(56,35)],[13],6,'8')
sw(R(range(52,57),[43]),[4],13,'8 achterbak r43')
def save(name, extra=()):
    gg=[r[:] for r in g]
    for x,y in extra: gg[y][x]=5
    o=Image.new('P',(W,H)); o.putpalette(im.getpalette()); o.putdata([v for r in gg for v in r])
    o.save(os.path.join(D,name),transparency=0)
    o.convert('RGBA').resize((W*8,H*8),Image.NEAREST).save(os.path.join(D,name.replace('.png','_8x.png')))
save('r10_zonder_hooglicht.png')
HL=[(x,y) for (x,y) in [(25,14),(26,14),(27,14),(24,15),(25,15),(26,15),(24,16),(25,16)] if g[y][x]==2]
save('r10_met_hooglicht.png',HL)
print('wijzigingen',len(LOG),'hooglicht',HL)
for m in MIS: print('AFWIJKEND (niet gewijzigd):',m)
with open(os.path.join(D,'wijzigingen.txt'),'w') as f:
    for p,x,y,a,b in LOG: f.write(f'{p}: ({x},{y}) {a:X}->{b:X}\n')
    for m in MIS: f.write(f'AFWIJKEND niet gewijzigd: {m}\n')
    f.write(f'hooglicht-variant 2->5: {HL}\n')
