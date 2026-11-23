# bouw_r3.py: r3 = r2 + reparaties 1-8 van de keurder (keuring_r2/KEURING.md), als bovenlaag per pixel. Controle: controle_r3.py.
import sys; sys.path.insert(0,'/home/user/Pokemon-Fully-Ungrounded/docs/concept/sprites/emolga_evo_fase3/sprite_r3/gereedschap')
from fv import *; import palet
CH=palet.CH; I={c:i for i,c in enumerate(CH)}
R2=D+'sprite_r2/'; R3=D+'sprite_r3/'
ALLE={   # zone -> {(x,y): (oud, nieuw)}; 'oud' wordt gecontroleerd
 '1 onderste vleugelvlak (E-bolling links van de vouw, taps; D blijft langs de vouw en onderaan)':
   {**{(x,24):('D','E') for x in (32,33,34)}, **{(x,25):('D','E') for x in (31,32,33,34)}, **{(x,26):('D','E') for x in (31,32,33,34)},
    **{(x,27):('D','E') for x in range(29,35)}, **{(x,28):('D','E') for x in range(28,34)}, **{(x,29):('D','E') for x in range(29,34)},
    **{(x,30):('D','E') for x in (30,31,32)}, (31,31):('D','E'),(32,31):('D','E'), (32,32):('D','E')},
 '2 open rand: (38,41) wordt lijn (model: dekking x38 90 %, x39 20 %)': {(38,41):('Y','K')},
 '3 zwart op de lichtkant': {(21,18):('K','D')},
 '4 kin: links/boven W, B alleen rechts en onder': {(28,31):('B','W'),(29,31):('B','W'),**{(x,32):('B','W') for x in (27,28,29,30)},(26,33):('B','W'),(25,34):('B','W'),(25,35):('B','W')},
 '5 borstvlakje: rechts/onder B': {(31,9):('W','B'),(31,10):('W','B'),(30,11):('W','B'),(30,12):('W','B'),(29,13):('W','B'),(27,14):('W','B')},
 '6 vuisten: inkeping x30 (model 65 %, fijn: gat op x30,5) en x34 (66 %), rechterrand vuist K': {(30,0):('D','.'),(34,0):('K','.'),(33,0):('D','K')},
}
A0_ONLY={'7 voorhoofdgeel 1 px breder (model 24,49: 35 %, volgende na de bestaande 4)': {(24,49):('W','L')}}
A_ONLY={'8 los vlakje in de kap': {(24,50):('E','D')}}
def toepassen(o,zones,log):
    o=o.copy()
    for z,px in zones.items():
        for (x,y),(oud,nieuw) in px.items():
            assert CH[o[y,x]]==oud,(z,x,y,CH[o[y,x]],oud); o[y,x]=I[nieuw]; log.append((z,x,y,oud,nieuw))
    return o
if __name__=='__main__':
    for nm,extra in (('A0',A0_ONLY),('A',A_ONLY),('A_geel',A_ONLY)):
        o=np.asarray(Image.open(R2+nm+'.png')).astype(int); log=[]
        o=toepassen(o,{**ALLE,**extra},log); palet.opslaan(o,R3+nm+'.png')
        print(nm,len(log))
