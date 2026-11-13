# maak_r5.py: r4 + Jordi's punten over r4 (oog, oor, rechte lijnen). Gebruik (vanuit kleur_r5/): python3 maak_r5.py
# Elke edit = (x, y, nieuw teken, zone); reden per pixel in LOG.md. Letters: zie ../kleur_r3/maak_r3.py (NAAM) + T, I.
import numpy as np; from PIL import Image
NAAM={0:'.',1:'K',2:'L',3:'1',4:'2',5:'3',6:'T',7:'s',8:'m',9:'b',10:'h',11:'I'}; CH={v:k for k,v in NAAM.items()}
src=Image.open('../kleur_r4/abra_r4.png'); r4=np.array(src).astype(int)

OOG_A=[(22,30,'b'),(22,29,'K')]            # Jordi: linkerpixel 1 omhoog
OOG_B=[(23,30,'b'),(23,31,'K')]            # modelplek: (22,30) -> (23,31), rechterpixel 1 omlaag
EDITS=[
 # rechteroor: rare lichte pixel weg, lichtstrook en binnenlijn volgen het model
 (34,16,'s','oor'),(31,17,'L','oor'),(33,17,'b','oor'),
 (30,18,'L','oor'),(31,18,'h','oor'),(32,18,'b','oor'),
 (30,19,'h','oor'),(31,19,'b','oor'),(31,22,'s','oor'),
 # kop, rechterrand (kop -> schouderplaat): 3-run L/K-wissel weg, modellijn
 (35,24,'s','kop'),(36,25,'s','kop'),(37,25,'K','kop'),(38,25,'K','kop'),
 (38,27,'K','kop'),(41,27,'3','kop'),(42,27,'K','kop'),
 (36,28,'s','kop'),(37,28,'K','kop'),(38,28,'3','kop'),(35,29,'K','kop'),
 # kin: onderlijn een kleur (model zwart)
 (24,36,'K','kin'),(27,36,'K','kin'),
 # linkerarm: rechterlijn volgt de modelcurve (x26 -> x25 -> x26 -> x27), linkerrand een lijnkleur
 (25,45,'L','arm'),(25,46,'L','arm'),(25,47,'L','arm'),
 (26,45,'m','arm'),(26,46,'s','arm'),(26,47,'s','arm'),
 (22,41,'L','arm'),(22,42,'L','arm'),
 # staart rechts: buitenrand rondt af zoals het model (rij 51 en 57 een pixel naar binnen)
 (54,51,'K','staart'),(55,51,'.','staart'),(55,57,'.','staart'),
 # staart bovenrand (van lijf naar rechts): model zwart, geen L/K-wissel
 (41,45,'K','staart'),(42,45,'K','staart'),(43,45,'K','staart'),
 (45,46,'K','staart'),(46,46,'K','staart'),(47,46,'K','staart'),(49,47,'K','staart'),
]
EXTRA=[]   # kritische ronde (stap 4), aangevuld na het vel

def bouw(oog,naam):
    a=r4.copy(); log=[]
    for x,y,c,*z in [(x,y,c,'oog') for x,y,c in oog]+EDITS+EXTRA:
        v=CH[c]
        if a[y,x]!=v: log.append((z[0],x,y,NAAM[a[y,x]],c)); a[y,x]=v
    out=Image.fromarray(a.astype('uint8'),'P'); out.putpalette(src.getpalette()); out.save(naam,transparency=0)
    return a,log
a,log=bouw(OOG_A,'abra_r5.png'); bouw(OOG_B,'abra_r5_oogB.png')
im=Image.open('abra_r5.png').convert('RGBA'); im.resize((512,512),Image.NEAREST).save('abra_r5_8x.png')
sil=[(x,y,'erbij' if a[y,x] else 'weg') for y,x in zip(*np.where((a>0)!=(r4>0)))]
print('gewijzigd t.o.v. r4:',len(log)); print('silhouet:',sil)
for z in sorted(set(l[0] for l in log)): print(' ',z,len([l for l in log if l[0]==z]))
if '-v' in __import__('sys').argv:
    for l in log: print(l)
