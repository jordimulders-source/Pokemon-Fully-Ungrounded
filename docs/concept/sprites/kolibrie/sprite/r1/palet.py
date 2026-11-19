# Gedeeld palet (index 0 transparant) = palet van af/kolibrie.png; zie NOTITIES voor wijzigingen
import numpy as np
from PIL import Image
_old=Image.open('../../af/kolibrie.png').getpalette()[:48]
PAL=[tuple(_old[i*3:i*3+3]) for i in range(16)]
# enige wijziging: index 15 (96,80,140; 18 px in de oude sprite, valt samen met 11) wordt donker blauwgroen
# voor de schaduwkant van de schouderglans (staat zo in beide modellen; derde tint van de tealgroep)
PAL[15]=(34,86,104)
def nearest(a):
    P=np.array(PAL[1:],float)
    d=((a[...,None,:]-P)**2*[1.0,1.3,0.8]).sum(-1)
    return (d.argmin(-1)+1).astype('uint8')
