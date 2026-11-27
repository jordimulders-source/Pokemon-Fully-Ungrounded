# Gedeeld palet + helpers (geen neveneffecten bij import)
import numpy as np
PAL=[(0,0,0),            # 0 transparant
 (20,18,20),             # 1 omlijning
 (100,88,74),(152,142,124),(194,188,166),   # 2-4 grijsbruin gezicht (2 ook barsten oker, 4 ook sneeuwschaduw)
 (244,242,224),(240,248,250),               # 5 creme, 6 wit sneeuw
 (124,68,64),(184,98,82),                   # 7-8 rood donker/midden (7 ook donkerste roze)
 (168,106,114),(204,134,128),               # 9 roze schaduw, 10 roze / hooglicht rood
 (160,126,58),(204,170,90),                 # 11-12 oker
 (54,86,80),(70,122,109),(112,170,150)]     # 13-15 turquoise
P=np.array(PAL,float)
def lum(a): return a@np.array([.299,.587,.114])
def nearest(px,idx=range(2,16)):
    idx=list(idx); d=((px[...,None,:]-P[idx])**2).sum(-1); return np.array(idx)[d.argmin(-1)]
