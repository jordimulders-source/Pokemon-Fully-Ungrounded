# Gedeeld: schaal, palet, overlap natief r7 -> sprite, opslaan. Geen neveneffecten bij import.
import numpy as np
from PIL import Image
NX0,NX1,NY0,NY1=12,149,4,157        # figuur in het natieve r7-raster (138 x 154)
S=63/154                             # spritepx per natieve px -> figuur 56 x 63
OX,OY=4,0                            # plek in het 64-vak
PAL=[(152,208,160),                  # 0 transparant
 (26,16,20),                         # 1 omlijning (r5-lijn)
 (124,76,18),(196,148,53),(229,184,79),(246,214,124),  # 2-5 goud: donker/selout, r5-midden (=r7-schaduw), r5-licht (=r7-hoofdtint), hooglicht
 (206,188,180),(244,240,234),        # 6-7 wit r5: schaduw, licht
 (128,28,42),(166,48,63),(208,99,104),# 8-10 rood r5 (kop, kam, karmijn pennen): donker, midden, licht
 (186,82,38),(222,118,50),           # 11-12 oranje r5: schaduw, midden
 (50,41,52),                        # 13 donkere penpunt r5
 (204,192,148),                      # 14 snavel/klauw schaduw (r7-snavel gemeten: 238,234,222 / 202,191,150)
 (240,160,84)]                       # 15 oranje licht (r2, hooglicht pennen)
def overlap(X,Y):
    """natieve cellen (u,v,gewicht) die spritepixel (X,Y) bedekt"""
    x0=NX0+(X-OX)/S; x1=NX0+(X-OX+1)/S; y0=NY0+(Y-OY)/S; y1=NY0+(Y-OY+1)/S
    out=[]
    for v in range(int(np.floor(y0)),int(np.ceil(y1))):
        hy=min(y1,v+1)-max(y0,v)
        if hy<=0: continue
        for u in range(int(np.floor(x0)),int(np.ceil(x1))):
            hx=min(x1,u+1)-max(x0,u)
            if hx>0: out.append((u,v,hx*hy*S*S))
    return out
def opslaan(o,pad):
    im=Image.new('P',(64,64)); flat=[x for c in PAL for x in c]; im.putpalette(flat+[0]*(768-len(flat)))
    im.putdata([int(v) for v in o.ravel()]); im.save(pad,transparency=0)
def rgb(o,bg=None):
    a=np.array(PAL,'uint8')[o]
    if bg is not None: a[o==0]=bg
    return a
