# maak.py r8 (vanaf r7): alleen de tweede tooiveer van rechts in de onderste rij (rij 16-18, kol 43-47) 1 px dikker naar
# de modelvorm (model: rij 16.5-19.5): nieuwe bovenrij met selout 5 en gele punt, licht -> donker eronder; sluit zo aan op
# het gele blad links (x41-42) en de vleugel rechts (x48), zonder gat.
import numpy as np; from PIL import Image
from render import schrijf
H='.123456789abcdef'
a=np.array(Image.open('r7_ref.png')).astype(np.uint8)
for y,x,s in [(16,43,'55581'),(17,43,'22366'),(18,43,'33477')]:
    for i,c in enumerate(s): a[y,x+i]=H.index(c)
np.save('samba_r8.npy',a); schrijf(a,'samba.png')
for y in range(14,21): print('%02d '%y+''.join(H[v] for v in a[y,38:52]))
