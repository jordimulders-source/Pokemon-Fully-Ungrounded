# r5: alleen de halskolommen 16 en 18 (zoals r4) -> 72x48; de rest gaat met naden (r5.py)
from PIL import Image; import numpy as np
D='docs/concept/sprites/mate_fase2/sprite/'
a=np.asarray(Image.open(D+'r1/natief.png').convert('RGB')).astype(int)[29:77,11:85]
b=np.delete(a,[16-11,18-11],1); Image.fromarray(b.astype('uint8')).save(D+'r5/geschrapt72.png'); print(b.shape)
