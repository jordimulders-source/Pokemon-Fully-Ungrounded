# bouw.py: r11 = r10 met alleen tintindexen veranderd (zie RAPPORT.md). Edits als (x,y,waarde) per onderdeel.
import numpy as np; from PIL import Image
R10='../sprite_r10/gnometrotter_rock.png'
im=Image.open(R10); a=np.array(im).copy()
H={'7':7,'8':8,'F':15,'6':6,'1':1,'2':2,'3':3,'4':4,'5':5,'9':9,'A':10,'B':11,'C':12,'D':13,'E':14}
FAM=[{7,8,15},{3,4,5},{10,11,12},{5,13,14}]
VRIJ=set()   # (x,y) waar een lijnkleur bewust wijzigt (alleen neus)
FOUT=[]
def rij(y,x0,s):
    for i,c in enumerate(s):
        if c==' ' or c=='.': continue
        x=x0+i; o=int(a[y,x]); n=H[c]
        if o==n: continue
        if (x,y) not in VRIJ and not any(o in f and n in f for f in FAM): FOUT.append((x,y,o,n)); continue
        a[y,x]=n
E={}
def zet(naam,regels):
    E[naam]=regels
# ---- neus: bolschaduw, hooglicht linksboven, sikkel rechtsonder; omtrek rond ----
VRIJ.update({(25,16)})
zet('neus',[(16,20,'8888'),(17,19,'8FF887'),(18,18,'8FF8887'),(19,18,'8888877'),(20,18,'8888877'),(21,18,'888777'),(22,20,'777'),
            (16,25,'3'),   # dubbele hoekpixel rechtsboven: neuslijn -> mutsschaduw (omtrek rond)
            (21,25,'D'),(22,24,'D'),(23,23,'D')])  # verdubbelde lijn rechtsonder (5-diagonaal in baard) -> baardmidden

# ---- lijf: één groot schaduwplan (licht linksboven; schaduw rechts, onder, onder muts/haar/baard) ----
# alleen roze vulpixels (7/8/F); naden 6 blijven
zet('lijf',[
 (20,27,'78887 7'.replace(' ','7')),          # b: onder de mutsrand: 7 met klein midden
 (21,28,'7 77'.replace(' ','6')),
 (19,40,'77'),(20,38,'777777'),(21,37,'7777'),  # c: onder het haar rechts: schaduw
 (22,36,'7777'),(23,35,'88877'),
 (22,32,'788'),(23,31,'777'),                  # d: rechts naast de baard, onder het haar
 (24,34,'8'),(25,32,'778'),(26,32,'78'),(27,32,'77'),(28,32,'7'),   # f: slagschaduw baard
 (26,33,'7'),(26,34,'8'),
 # g: hoofdvlak, hooglicht linksboven, sikkel rechtsonder
 (25,36,'FF88'),(26,36,'F8888'),(27,35,'8888777'),(28,34,'8888877'),(29,34,'8888777'),
 (30,34,'8877'),(31,34,'877'),(31,36,'777'),(32,35,'77'),
 # e: schouderschijf, bovenvlak licht linksboven, rechts/onder schaduw
 (22,41,'88F87'),(23,41,'8FF8877'),(24,42,'8887777'),(25,41,'8877777'),
 (26,45,'77777'),(27,43,'7777777'),
 # j: rechtsonder op de romp: schaduw, smalle lichte kant linksboven
 (29,42,'887777'),(30,41,'8877777'),(31,40,'8877777'),(32,39,'8877777'),(33,37,'8877777'),(34,37,'777777'),
 # l: onderste plaat naast de baard: midden linksboven, onderkant schaduw
 (30,31,'88'),(31,31,'88'),(32,31,'887'),(33,31,'8777'),(34,30,'777777'),(35,29,'7887777'),(36,28,'7777777'),
])

# ---- armen: rechterarm en -hand liggen aan de schaduwkant: kleiner hooglicht, grotere sikkel ----
zet('armR',[(27,51,'8'),(28,51,'8F8'),(29,51,'788'),(30,51,'7887'),(31,51,'7777'),(32,53,'77')])
zet('handR',[(34,55,'8F88'),(35,54,'8FF887'),(36,53,'8F88877'),(37,53,'8888777'),(38,53,'7887777'),(39,53,'7777777'),(40,56,'777')])
# ---- rugrots: geen baardlicht op de achterste rots ----
zet('rugrots',[(9,46,'5'),(10,45,'5')])
# ---- broek: rechterbeen aan de schaduwkant, lichte banden weg ----
zet('broek',[(41,43,'AAAAA'),(42,40,'AABBAAAA'),(43,40,'ABCBAAA'),(44,39,'AABBAAAAA'),(45,39,'AABAAAAA'),
             (46,26,'AAA'),
             (51,43,'ACBBA'),(52,42,'ABBBAA')])
# ---- riem: rechterdeel onder de buik in schaduw ----
zet('riem',[(38,36,'4444'),(39,34,'33333'),(40,31,'333')])


# ---- bijstellen na de kaart: lijf binnen bereik van de referenties (licht deel iets ruimer), rugrots en rechterzool aan de schaduwkant ----
zet('lijf2',[(32,31,'888'),(33,31,'8877'),(34,30,'788777'),(31,34,'88777'),(30,34,'8887'),(30,41,'8887777'),(31,40,'8887777')])
zet('rugrots2',[(11,45,'44'),(12,45,'4'),(13,45,'4'),(14,45,'4')])
zet('zoolR',[(55,41,'4'),(56,41,'44'),(57,41,'4444')])
# ---- opruimen: vlekjes < 3 px die door de nieuwe verdeling ontstonden ----
zet('vlek',[(23,33,'8'),(22,45,'8'),(33,39,'8'),(35,30,'77'),(36,54,'8')])
for n,rr in E.items():
    for y,x0,s in rr: rij(y,x0,s)
if FOUT: print('GEWEIGERD (geen vulpixel):',FOUT)
out=Image.fromarray(a,'P'); out.putpalette(im.getpalette()); out.info['transparency']=0
out.save('gnometrotter_rock.png',transparency=0)
