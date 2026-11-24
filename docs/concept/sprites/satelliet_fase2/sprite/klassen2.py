# Paneelrasters als eigen klasse (dunne lijnen, voorrang in kaal.py):
#  groot paneel: lichte lijnen (2-5,11) -> 11; donkere rasterlijnen (15, en 6/7 verder dan 22 modelpx van de rand) -> 15
#  klein paneel: rasterlijnen (8/10/15) -> 15
import numpy as np; from PIL import Image
from scipy import ndimage as nd
k=np.load('klassen.npy'); Z=np.array(Image.open('zones.png')); PAL=np.load('pal.npy')
k2=k.copy()
rand=nd.distance_transform_edt(~np.isin(k,[0,1]))
k2[(Z==2)&np.isin(k,[2,3,4,5,11])]=11
k2[(Z==2)&((k==15)|(np.isin(k,[6,7,8])&(rand>22)))]=15
k2[(Z==1)&np.isin(k,[8,10,15])]=15
np.save('klassen2.npy',k2)
pal=[int(v) for c in PAL for v in c]
im=Image.fromarray(k2,'P'); im.putpalette(pal+[0]*(768-len(pal))); im.convert('RGB').save('klassen2.png')
