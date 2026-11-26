# Gedeelde maskers: paneelpolygonen (ruim, in modelcoordinaten) en modelklassen.
from common import *
from PIL import ImageDraw
import kaal
POLY={
 'PA':[(68,34),(85,21),(124,32),(124,52),(72,40)],          # achter-links (boven), 4 vakken
 'PA2':[(134,38),(141,40),(141,49),(131,54),(130,46)],       # stukje PA rechts van de mast
 'PB':[(120,0),(130,2),(136,10),(136,53),(120,53)],          # mast boven, 3 vakken
 'PC':[(163,54),(173,54),(230,72),(212,87),(160,71)],        # rechts (achterarm), 4 vakken
 'PD':[(1,92),(19,84),(64,97),(64,109),(50,115),(1,98)],     # links voor, 4 vakken
 'PE':[(86,133),(102,116),(152,131),(152,143),(138,153),(87,139)], # voor rechts onder, 4 vakken
 'PF':[(120,94),(138,94),(138,138),(120,138)],               # mast onder, 3 vakken
}
def polymask(H,W,poly):
    im=Image.new('L',(W,H),0); ImageDraw.Draw(im).polygon(poly,fill=1); return np.array(im).astype(bool)
def model():
    a,bg=load(); H,W,_=a.shape
    pal=np.array(kaal.PAL[1:],float)
    lab=((a[:,:,None,:]-pal[None,None])**2).sum(3).argmin(2)+1; lab[bg]=0
    return a,bg,lab
