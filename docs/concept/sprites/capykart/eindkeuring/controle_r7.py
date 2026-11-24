"""Controle r7 t.o.v. r6: alpha-diff, palet, gezicht ongewijzigd, nieuwe kleuren."""
from PIL import Image
import os
D=os.path.dirname(os.path.abspath(__file__))
a=Image.open(os.path.join(D,'..','sprite','r6','capykart.png')); b=Image.open(os.path.join(D,'capykart_r7.png'))
pa,pb=a.load(),b.load()
assert a.getpalette()[:48]==b.getpalette()[:48], 'palet gewijzigd'
alpha=sum((pa[x,y]==0)!=(pb[x,y]==0) for x in range(64) for y in range(64))
diff=[(x,y) for x in range(64) for y in range(64) if pa[x,y]!=pb[x,y]]
# gezicht: oog (29-31,18-20), neusgat (15-16,22), mond (18-19,28), tanden (17-23,30-34), morrillo (21-24,15-16)
face=set()
for x0,x1,y0,y1 in [(28,32,17,21),(15,17,22,23),(18,20,28,29),(17,24,30,34),(19,22,34,35),(21,25,15,17)]:
    for x in range(x0,x1):
        for y in range(y0,y1): face.add((x,y))
fd=[p for p in diff if p in face]
print('alpha-diff:',alpha,'| gewijzigde pixels:',len(diff),'| gezicht gewijzigd:',fd,'| kleuren gebruikt:',sorted(set(b.getdata())))
