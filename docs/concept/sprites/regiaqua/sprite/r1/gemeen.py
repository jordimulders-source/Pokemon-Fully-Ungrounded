# Gedeelde metingen (geen neveneffecten bij import): natief raster, figuurmasker, klassen per natieve pixel.
import numpy as np; from PIL import Image
from scipy import ndimage
import os
D=os.path.dirname(os.path.abspath(__file__))
def natief():
    a=np.array(Image.open(os.path.join(D,'natief.png')).convert('RGB')).astype(int)
    wh=a.min(2)>=215
    lab,n=ndimage.label(wh)
    rand=np.unique(np.r_[lab[0],lab[-1],lab[:,0],lab[:,-1]]); rand=rand[rand>0]
    bg=np.isin(lab,rand)
    fig=~bg
    L=(a*[0.3,0.59,0.11]).sum(2)
    dot=fig&(a[...,1]>170)&(a[...,0]<140)&(a[...,1]-a[...,0]>110)
    blk=fig&(a.max(2)<40)
    return a,fig,L,dot,blk
# toonklassen van het water (modelclusters uit de helderheidshistogram)
GRENS=[60,86,110,140,166,205]   # -> klasse 0..6
def toon(L): return np.digitize(L,GRENS)
