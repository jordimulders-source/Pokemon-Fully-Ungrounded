# Sprite-palet fruitvampier (Emolga-lijn fase 3). Lijf/geel/wit = tinten van fase 2 (emolga_evo/af/model.png, index 1-10 gelijk),
# masker in de modeltinten (staalblauw, model 66/76/86 - 109/128/148 - 149/160/169) naar Gen 3-stappen.
from PIL import Image; import numpy as np
PAL=[(152,208,160),   # 0 transparant
     (16,16,24),      # 1 K zwart (fase 2)
     (38,38,52),      # 2 D lijf donker (fase 2; model 31)
     (64,64,82),      # 3 E lijf midden (fase 2; model 58) = ook vizier fase 2
     (98,96,114),     # 4 G lijf licht (fase 2) = ook vizier-licht fase 2
     (184,140,24),    # 5 y geel schaduw (fase 2)
     (224,184,40),    # 6 Y geel (fase 2)
     (248,220,80),    # 7 L geel licht (fase 2)
     (180,194,208),   # 8 B wit schaduw (fase 2)
     (240,246,250),   # 9 W wit (fase 2)
     (140,152,172),   # 10 w wit diepe schaduw (fase 2)
     (64,78,98),      # 11 M masker omlijning (model 66,76,86)
     (106,126,150),   # 12 N masker (model 109,128,148)
     (150,166,186)]   # 13 O masker licht (model 149,160,169)
CH='.KDEGyYLBWwMNO'
def rgb(o,bg=None):
    img=np.zeros(o.shape+(3,),'uint8'); img[:]=bg if bg else PAL[0]
    for k in range(1,len(PAL)): img[o==k]=PAL[k]
    return Image.fromarray(img)
def opslaan(o,path):
    p=Image.fromarray(o.astype('uint8'),'P'); pal=[v for c in PAL for v in c]; p.putpalette(pal+[0]*(48-len(pal)))   # precies 16 paletplaatsen
    p.save(path,transparency=0,bits=4)
# klassen fv.KL2 ('.KDGyYLMNBW') -> palet
VAN2=[0,1,2,3,5,6,7,11,12,8,9]
