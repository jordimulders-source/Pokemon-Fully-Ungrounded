# r22 poten: vorm opnieuw uit het model (meetpoot.py: achtergrondfractie per spritepixel, drempel 0,6), met de keurder-eisen:
# transparante spleet tussen de voeten (x24 rijen 55-58, x23 rijen 57-58), rechtervoet pas vanaf x>=25, geen steeltje (18,59),
# tenen gescheiden ((28,59) lucht). Schrijft vorm.npy (pootpixels = 14, kleur volgt in kleur22.py) en POOT (masker).
import numpy as np
from delen import delen, NAMEN
V=np.load('vorm.npy'); P=delen(V); PO=NAMEN.index('poot')
RIJEN={51:[(25,28),(32,35)],52:[(24,27),(32,35)],53:[(23,26),(31,34)],54:[(22,25),(30,34)],
       55:[(18,23),(30,34)],56:[(17,23),(25,35)],57:[(16,22),(25,36)],58:[(17,21),(25,36)],
       59:[(25,27),(29,31)],60:[(25,25),(29,31)],61:[(29,31)],62:[(29,30)],63:[(29,29)]}
oud=(P==PO)&(V>0)
for y in range(51,64): V[y,:37][oud[y,:37]]=0
POOT=np.zeros((64,64),bool)
for y,rs in RIJEN.items():
    for a,b in rs:
        for x in range(a,b+1):
            if V[y,x]==0 or oud[y,x]: V[y,x]=14; POOT[y,x]=True
np.save('vorm.npy',V); np.save('poot22.npy',POOT)
print('pootpixels',POOT.sum(),'oud',oud.sum())
