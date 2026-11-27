# voor_r4.py: voorste ster in het natieve r4-model (99x99) = figuur min de vijf achterpunten.
# Grenzen per rij gemeten op natief_r4.png (zie NOTITIES r5): de achterpunt loopt tot/vanaf de buitenlijn van de voorste ster.
import sys, numpy as np; from PIL import Image
sys.path.insert(0,'gereedschap'); from voor import vul_gaten
NATIEF='sprite_r5/gereedschap/natief_r4.png'
TL={16:45,17:45,18:44,19:44,20:43,21:43,22:42,23:42,24:41,25:41,26:40,27:39,28:39,29:39,30:38,31:38,32:36,33:36,34:32}   # achter: x < grens
TR={15:55,16:56,17:57,18:57,19:58,20:59,21:59,22:60,23:60,24:60,25:61,26:62,27:62,28:64,29:63,30:63,31:64,32:64,33:66,34:70}  # achter: x > grens
LL={53:17,54:18,55:20,56:21,57:22,58:23,59:24,60:24,61:24,62:23,63:23,64:23,65:22,66:22,67:22,68:22}   # achter: x <= grens
RL={54:76,55:75,56:74,57:72,58:71,59:70,60:70,61:70,62:70,63:71,64:71,65:71,66:71,67:71,68:71}   # achter: x > grens
BO={76:(46,49),77:(44,50),78:(43,52),79:(42,54),80:(41,54),81:(42,54),82:(43,53)}               # achter: lo <= x <= hi; vanaf rij 83 alles x38-60
def natief(): return np.asarray(Image.open(NATIEF).convert('RGB')).astype(int)
def figuur(a): return vul_gaten(a.min(2)<215)
def punten(a=None):
    a=natief() if a is None else a; f=figuur(a); P=np.zeros((99,99),object); P[:]=''
    for y in range(99):
        for x in range(99):
            if not f[y,x]: continue
            if y<=15 and x<44: P[y,x]='linksboven'
            elif y in TL and x<TL[y]: P[y,x]='linksboven'
            elif y==35 and 23<=x<27: P[y,x]='linksboven'
            elif y<=14 and x>55: P[y,x]='rechtsboven'
            elif y in TR and x>TR[y]: P[y,x]='rechtsboven'
            elif y in LL and x<=LL[y]: P[y,x]='linksonder'
            elif y in RL and x>RL[y]: P[y,x]='rechtsonder'
            elif y in BO and BO[y][0]<=x<=BO[y][1]: P[y,x]='onder'
            elif y>=83 and 38<=x<=60: P[y,x]='onder'
    return P
def voor_mask(a=None):
    a=natief() if a is None else a
    return figuur(a)&(punten(a)=='')
