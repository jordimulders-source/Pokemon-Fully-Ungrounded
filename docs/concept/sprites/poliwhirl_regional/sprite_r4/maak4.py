# r4: basis r3_E6; alleen de oogzone. E6-ogen (pixels ongewijzigd) op de modelpositie, gemeten op de zwarte BUITENRAND van het modeloog
# (cellen, afgelezen op het model met spriteraster, ±0,2): links x 13,6-18,0 y 2,6-7,4 (midden 15,8; 5,0) - het oog vormt daar het silhouet;
# rechts x 26,8-31,5 y 1,9-7,5 (midden 29,2; 4,7) - bovenop/rechts tegen de zwarte vlek.
import numpy as np
import maak3 as M3
M3.r2=np.load('r3_E6.npy')
M3.OOGC=[(15.6,4.6),(28.6,4.6)]   # -> linkeroog x 13-18 y 2-7, rechteroog x 26-31 y 2-7 (celmiddens 16,0;5,0 en 29,0;5,0)
def maak():
    M3.INFO.clear(); return M3.maak('E6')
