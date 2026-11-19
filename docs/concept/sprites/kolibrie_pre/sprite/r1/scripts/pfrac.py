# P- en K-dekking per doelpixel (hulpbestand voor stappen.py)
import numpy as np
src=open('bouw.py').read().split("zone=np.full")[0]; g={}; exec(src,g)
np.save('pfrac.npy',g['fr']['P']/np.maximum(g['fg'],1e-6)); np.save('kfrac.npy',g['fr']['K'])
