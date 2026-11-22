# Klassenkaart van het bevroren model (combi_kop silhouet) met de kleurfamilies uit model_v1 (alleen als kaart, niet als kleurbron).
# . = transparant, # = lijn (zwart in v1), o = oranje, g = geel, p = roze
import numpy as np
from PIL import Image
M='../model/'
c=np.asarray(Image.open(M+'combi_kop.png').convert('RGB')).astype(int)
v=np.asarray(Image.open(M+'model_v1.png').convert('RGB')).astype(int)
ORA=[(120,45,25),(190,80,40),(232,120,52),(250,165,80)]
GEE=[(150,105,35),(215,165,50),(245,210,85),(255,238,150)]
ROZ=[(170,70,95),(225,125,140),(250,180,185)]
def klas(p):
    t=tuple(p)
    if min(t)>225: return '.'
    if t==(24,16,16): return '#'
    if t in ORA: return 'o'
    if t in GEE: return 'g'
    if t in ROZ: return 'p'
    return '?'
K=np.array([[klas(v[y,x]) for x in range(99)] for y in range(99)])
# silhouet uit combi_kop
sil=c.min(2)<=225
assert ((K!='.')==sil).all(), 'silhouet v1 != combi_kop'
K=K[12:90,14:92]
np.save('klassen78.npy',K)
print('\n'.join(''.join(r) for r in K))
