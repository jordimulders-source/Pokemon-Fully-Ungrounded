import numpy as np, sys; from PIL import Image
O='/home/user/Pokemon-Fully-Ungrounded/docs/concept/sprites/viscacha/icoon/onderdelen/'
B=Image.open(O+'icon_a7.png'); a=np.array(B); n=a.copy()
# rechtersnorharen: 2 lijntjes van 1 px schuin naar rechtsonder (front: x13-22, y35-43)
L1=[(12,19),(13,20),(14,20),(15,21),(16,21)]
L2=[(12,21),(13,21),(14,22),(15,22),(16,23)]
KLEUR=dict(x.split('=') for x in sys.argv[1:])  # "x,y=v" kleurwijzigingen (frame 1)
for x,y in L1+L2: n[y,x]=14
for k,v in KLEUR.items():
    x,y=map(int,k.split(',')); n[y,x]=int(v,16)
# frame 2: hetzelfde, 1 rij lager boven rij 23; rij >=24 gelijk
for y,x in np.argwhere(n[:32]!=a[:32]):
    if y<=22: n[32+y+1,x]=n[y,x]
    elif y>=24: n[32+y,x]=n[y,x]
    elif x<=10: n[32+24,x]=n[y,x]   # wantje zakt in frame 2 mee (zoals a4)
im=Image.fromarray(n,'P'); im.putpalette(B.getpalette()); im.save(O+'icon_a8.png',transparency=0)
im.resize((256,512),Image.NEAREST).save(O+'icon_a8_8x.png',transparency=0)
# onderdelen (frame 1), alleen vulpixels
f=n[:32]
def reg(cells): return [(x,y) for x,y in cells if f[y,x] in (3,6,7)]
R=lambda x0,x1,y0,y1:[(x,y) for y in range(y0,y1+1) for x in range(x0,x1+1)]
kop=reg([c for c in R(6,15,14,20) if not (c[0]>=14 and c[1]>=19)])
poot_op=reg(R(7,10,21,23))
bef=reg([(11,21),(12,21),(11,22),(12,22),(15,23),(17,23),(15,24),(16,24),(17,24)])
staand=reg([(13,22),(12,23),(13,23),(11,24),(12,24),(13,24),(11,25),(13,25)])
dij=reg([c for c in R(19,24,20,28) if not (c[0]>=23 and c[1]<=22) and not (c[0]==24)]+[(19,22),(19,23)])
verre=reg(R(15,18,25,27))
used=set(kop+poot_op+bef+staand+dij+verre)
romp=reg([c for c in R(14,22,16,24) if c not in used and not (c[0]>=19 and c[1]>=20) and not (c[0]>=21 and c[1]<=19 and c[0]>=22)])
for nm,P in [('kop',kop),('romp',romp),('bef/buik',bef),('dij+voet',dij),('staande voorpoot',staand),('opgeheven poot',poot_op),('verre achterpoot',verre)]:
    t=len(P); c={v:sum(f[y][x]==v for x,y in P) for v in (3,6,7)}
    print(f'{nm:18s} n={t:2d} zand {c[7]/t:4.0%} bruin {c[6]/t:4.0%} wit {c[3]/t:3.0%}  bruin:{[p for p in P if f[p[1]][p[0]]==6]}')
print('romp pixels',romp)
for y in range(13,30): print('%2d '%y+''.join('.' if v==0 else '%X'%v for v in f[y][:28]))
