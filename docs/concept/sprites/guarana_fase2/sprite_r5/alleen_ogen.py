# r5: alleen de pupillen veranderen. bouw.py levert de hele sprite opnieuw; omdat de ruisstappen van de ogen afhangen, schuiven daarbuiten
# een paar tinten mee (4 px). Daarom: r5 = r4A, met alleen de oogpixels (oogmasker r4 of r5) uit de nieuwe bouw. Pixeldiff buiten de ogen = 0.
import sys, numpy as np; sys.path.insert(0,'sprite_r5'); from gemeen2 import *; from PIL import Image
n=np.array(Image.open('sprite_r5/guarana2_r5_A.png')); r4=np.array(Image.open('sprite_r4/guarana2_r4_A.png'))
oog=np.load('sprite_r5/oog.npy')|np.load('sprite_r4/oog.npy')
o=r4.copy(); o[oog]=n[oog]; opslaan(o,'sprite_r5/guarana2_r5_A.png')
d=o!=r4; print('anders dan r4A:',int(d.sum()),' buiten de ogen:',int((d&~oog).sum()))
