# Gedeeld palet + helpers (geen neveneffecten bij import). r7-model: gezicht 4 tonen (2 lijn, 3 donker, 4 midden, 13 licht);
# 13 is ook de schaduw van kap/sneeuw. Sneeuwwit en kapcreme delen index 5; turquoise 6/14/15.
import numpy as np
PAL=[(0,0,0),            # 0 transparant
 (20,18,20),             # 1 omlijning
 (80,66,56),(116,104,90),(152,140,122),     # 2 gezichtslijn/donkerst bruin, 3 gezicht donker, 4 gezicht midden
 (244,242,224),(206,216,224),               # 5 creme kap, 6 blauwgrijze sneeuw (r2; donker turquoise samengevoegd met 14)
 (124,68,64),(184,98,82),                   # 7-8 rood donker/midden
 (175,111,117),(240,248,252),               # 9 roze (r2: roze schaduw + roze licht samen), 10 sneeuwwit (r2)
 (160,126,58),(204,170,90),                 # 11-12 oker
 (186,176,154),                             # 13 gezicht licht / schaduw creme en sneeuw
 (70,122,109),(112,170,150)]                # 14-15 turquoise
P=np.array(PAL,float)
TURK=(14,15); GRIJS=(2,3,4,5,6,10,13)
def lum(a): return a@np.array([.299,.587,.114])
def nearest(px,idx=range(2,16)):
    idx=list(idx); d=((px[...,None,:]-P[idx])**2).sum(-1); return np.array(idx)[d.argmin(-1)]
