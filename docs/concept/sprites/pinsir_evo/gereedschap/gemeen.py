# Gedeelde hulpjes Pinsir-evolutie: spritepalet, opslaan, tonen, labels.
import numpy as np; from PIL import Image
from model import label
# Spritepalet (index: kleur). Tonen in de volgorde van het model; kleur iets opgelicht t.o.v. het (zeer donkere) model zodat
# de lijftinten op 1x van de zwarte lijn loskomen (Jordi: "Je mag met kleur altijd van het model afwijken").
PAL=[(120,200,160),(20,14,12),
     (50,42,38),(82,68,58),(116,98,82),(156,136,114),    # 2-5 lijf: donker, middendonker, midden, licht (khaki pantser)
     (84,38,30),(128,68,50),(164,104,78),                # 6-8 kaak: donker, midden, licht (donker roodbruin)
     (74,42,20),(150,104,64),(200,154,102),              # 9-11 dekschild: vlek, midden, licht (r2: vlek en midden naar de modelmediaan 77,46,22 / 139,100,69)
     (230,214,200),(168,150,138),                        # 12 tand/oog crème (model 217,198,187, iets lichter), 13 tandschaduw
     (0,0,0),(0,0,0)]
CH='.K2345abcvmlTt??'
LIJF={2,3,4,5}; KAAK={6,7,8}; SCHILD={9,10,11}
def rgb(o,bg=None):
    img=np.zeros(o.shape+(3,),'uint8'); img[:]=bg if bg else PAL[0]
    for k in range(1,len(PAL)): img[o==k]=PAL[k]
    return Image.fromarray(img)
def opslaan(o,path,n=14):
    p=Image.fromarray(o.astype('uint8'),'P'); pal=[v for c in PAL[:n] for v in c]; p.putpalette(pal+[0]*(768-len(pal))); p.save(path,transparency=0)
def toon(o,y0=0,y1=64,x0=0,x1=64):
    print('   '+''.join(str(x%10) for x in range(x0,x1)))
    for y in range(y0,y1): print('%2d '%y+''.join(CH[v] for v in o[y,x0:x1]))
