# Ronde 5: A = ronde 4 + band hoger (met de hand getypte segmenten); B = A + kuiflijn (de oude kopomtrek van Silicobra).
from PIL import Image
B='/home/user/Pokemon-Fully-Ungrounded/docs/concept/sprites/silicobra_uyuni/'
g=[list(l.rstrip('\n')) for l in open(B+'ronde4/silicobra_uyuni_raster.txt')][:64]
def s(y,x,t):
    for i,c in enumerate(t): g[y][x+i]=c
# A: bovenrand band 1 px hoger (midden, rechts, linksmidden); boog blijft
s(32,38,'rst')
s(33,22,'qqd'); s(33,25,'cccccccc'); s(33,33,'ddrssss'); s(33,40,'t')
s(34,19,'rqaaaqqr'); s(34,27,'ccccd'); s(34,32,'rrrsssss')
s(35,19,'rqqqqaaqrqrrrrrsssstt')
s(36,28,'r')
open(B+'ronde5/silicobra_uyuni_raster.txt','w').write('\n'.join(''.join(r) for r in g)+'\n')
# B: kuiflijn langs de onderrand van de kuif = de oorspronkelijke kopomtrek
o=list(Image.open('/home/user/Pokemon-Fully-Ungrounded/graphics/pokemon/silicobra/anim_front.png').get_flattened_data())
lijn=[(x,16) for x in range(23,33)]+[(20,17),(21,17),(22,17),(33,17),(34,17),(35,18),(36,18),(37,19),(38,20),(39,21),(39,22),(40,23),(40,24)]+[(41,y) for y in range(25,30)]+[(40,30),(40,31)]
for x,y in lijn:
    assert o[y*64+x]!=0
    g[y][x]='h' if (x<=28 and y<=17) else 'K'
open(B+'ronde5/silicobra_uyuni_kuiflijn_raster.txt','w').write('\n'.join(''.join(r) for r in g)+'\n')
print(len(lijn),'lijnpixels')
