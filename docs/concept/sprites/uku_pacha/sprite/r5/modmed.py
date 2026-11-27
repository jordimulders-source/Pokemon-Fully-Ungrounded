# model-helderheid per spritepixel (mediaan van de voetafdruk), voor vergelijking met het raster
from PIL import Image; import numpy as np, math, os
D=os.path.dirname(os.path.abspath(__file__))
N=np.asarray(Image.open(os.path.join(D,'../../model/r2_natief.png')).convert('RGB')).astype(int); L=N.mean(2)
F=64/92
def med(i,j):
    x0=5+i/F; x1=5+(i+1)/F; y0=7+(j-2)/F; y1=7+(j-1)/F
    return float(np.median([L[cy,cx] for cy in range(int(y0),math.ceil(y1)) for cx in range(int(x0),math.ceil(x1)) if 0<=cy<100 and 0<=cx<100]))
