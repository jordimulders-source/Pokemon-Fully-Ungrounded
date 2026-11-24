# k10 = k9 (poort) + bergwand terug op de k8-structuur, daarna per steen behandeld zoals de voorvlakken:
# licht linksboven (6), schaduwsikkel rechtsonder (e), putje (e, 3 px). Grenzen horizontaal/verticaal.
import sys, numpy as np
sys.path.insert(0,'../k1')
from gereedschap import *
a8,_=laad('../k8/tempel.png'); a9,pal=laad('../k9/tempel.png'); a=a9.copy()
# 1. diagonale barsten/facetten van k9 weg: bergwand terug naar k8
box=np.zeros_like(a,bool); box[15:57,48:62]=True
a[box]=a8[box]
assert ((a!=a8)&box).sum()==0
C={'h':6,'f':15,'e':14,'.':None}
ONTWERP={  # rij: (x-start, tekens); '.' = k8 laten staan
 # steen boven (x48-57, y22-26): licht linksboven, putje, sikkel onder/rechts; e-streep x50 weg
 22:(48,'hhhffffef'),
 23:(48,'hfeeffffe'),
 24:(48,'ffe.fffee'),
 25:(48,'fffffffeee'),
 26:(53,'eeeee'),
 # midden links (x49-52, y33-39)
 33:(50,'hh.'),
 34:(50,'h'),
 36:(49,'.ee'),
 37:(49,'.e.e'),
 38:(52,'e'),
 39:(50,'eee'),
 # midden rechts (x54-59, y32-39): streep e x56-58 opgenomen in de steen
}
ONTWERP2={
 32:(54,'hhfff'),
 33:(54,'hfffe'),
 34:(54,'ffffe'),
 35:(54,'feefee'),
 36:(54,'fefaee'.replace('a','f')),
 37:(54,'ffffee'),
 38:(54,'feeeee'),
 39:(54,'ee'),
 # onder rechts boven (x55-61, y42-48)
 42:(56,'hhffe'),
 43:(56,'hfffe'),
 44:(56,'feefe'),
 45:(56,'fef'),
 46:(56,'fff'),
 47:(56,'ffff'),
 48:(55,'eeeeeee'),
 # onder (x49-60, y49-56): links van de voeg-schaduw x53 en rechts ervan
 49:(54,'h'),
 50:(54,'hh'),
 51:(50,'hh'),
 52:(50,'h'),
 53:(50,'ee'),
 54:(50,'e'),
 55:(51,'ee'),
 56:(50,'ee'),
}
ONTWERP3={52:(56,'eee'),53:(56,'e')}
ONTWERP4={49:(60,'e'),50:(59,'ee'),51:(59,'e')}
fout=[]
for O in (ONTWERP,ONTWERP2,ONTWERP3,ONTWERP4):
    for y,(x0,s) in O.items():
        for i,ch in enumerate(s):
            x=x0+i
            if C[ch] is None: continue
            if a8[y,x] not in (6,14,15): fout.append((x,y,int(a8[y,x]))); continue
            a[y,x]=C[ch]
print('geen muurpixel, overgeslagen:',fout)
# 2. latei steekt rechts 2 px uit voorbij de rechterstijl (Jordi; model)
LATEI={(25,46):5,          # oude stijllijn wordt lateivlak
       (26,45):7,                    # bovenkant (lichtkant) in de voegtint
       (26,46):6,(26,47):6,(25,47):6, # kopse kant/onderkant in de donkere eigen tint
       (26,49):5,                    # schaduw onder de overstek
       (27,45):1,(27,46):1,(27,47):1,(26,48):1,(27,48):1}  # zwart aan de schaduwkant (rechts en onder)
for (x,y),c in LATEI.items(): a[y,x]=c
bewaar(a,pal,'tempel.png')
