# r4: model (natief 74x48) -> 64x48 door 10 hele kolommen te schrappen, GEEN rijen.
# Keuring r3: niet door het verre kano-oog (natief x19-21) of het neusgat (x11-14, y66-68); minder in de hals.
# Hals: 16 en 18 (11 -> 9 px). Achterkant romp + waterval: 74,75,76,77,79,80,82,83
# (blijven: 73, 78, 81 = buitenlijn romp, 84 = rand waterval).
from PIL import Image; import numpy as np
D='docs/concept/sprites/mate_fase2/sprite/'
a=np.asarray(Image.open(D+'r1/natief.png').convert('RGB')).astype(int)[29:77,11:85]
cols=[16,18,74,75,76,77,79,80,82,83]
b=np.delete(a,[c-11 for c in cols],1)
print('kolommen (natief x)',cols,'rijen: geen',b.shape)
Image.fromarray(b.astype('uint8')).save(D+'r4/geschrapt.png')
