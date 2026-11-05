# kleur3h = kleur3g met de staart van kleur3f (Jordi, 5 nov): zone x>=48, y>=40, 3f 2 px omlaag geschoven.
from PIL import Image
D='docs/concept/sprites/salticonda/'
f=Image.open(D+'kleur3f/salticonda.png'); g=Image.open(D+'kleur3g/salticonda.png')
F=list(f.get_flattened_data()); G=list(g.get_flattened_data())
H=[(F[(y-2)*64+x] if y>=2 else 0) if (x>=48 and y>=40) else G[y*64+x] for y in range(64) for x in range(64)]
h=Image.new('P',(64,64)); h.putpalette(g.getpalette()); h.putdata(H)
h.save(D+'kleur3h/salticonda.png',transparency=0)
