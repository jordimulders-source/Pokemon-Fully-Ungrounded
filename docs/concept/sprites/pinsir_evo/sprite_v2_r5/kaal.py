# Kale reductie van het model per spritepixel in het r4-palet (alleen als meetlaag; geen eindbeeld).
import numpy as np
from PIL import Image
DF=np.load('sprite_v2_r5/DF.npy');ML=np.load('sprite_v2_r5/ML.npy');RG=np.load('sprite_v2_r5/RG.npy')
r4=Image.open('sprite_v2_r4/pinsir_evo_v2_r4_B.png')
def idx(y,x,lijn=0.4):
    d=DF[y,x]; l=ML[y,x]
    if d<0: return 0
    if d>=lijn: return 1
    if RG[y,x]>45:
        return 9 if l<45 else 10 if l<75 else 11 if l<105 else 12
    if l>=225 and 20<=y<=23 and 12<=x<=24: return 13
    if l>=168: return 6 if l<200 else 7 if l<228 else 8
    return 2 if l<60 else 3 if l<90 else 4 if l<115 else 5 if l<141 else 14
K=np.array([[idx(y,x) for x in range(64)] for y in range(64)],np.uint8)
np.save('sprite_v2_r5/kaal.npy',K)
o=Image.fromarray(K,'P'); o.putpalette(r4.getpalette()); o.save('sprite_v2_r5/kaal.png',transparency=0)
