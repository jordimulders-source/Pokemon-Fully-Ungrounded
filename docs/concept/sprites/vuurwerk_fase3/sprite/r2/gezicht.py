# Oog en kaaklijn per pixel naar het model (de reductie brak de 1-natieve-px bruine lijnen en vulde het oogwit).
# Gemeten op overlay.py (model op 36x met spriteraster). Elke pixel = modelkleur op die plek.
import sys, json, numpy as np; from PIL import Image
PAL=json.load(open('palet.json'))
IN,OUT=sys.argv[1],sys.argv[2]
a=np.asarray(Image.open(IN)).copy()
FIX={ (15,20):4,                      # model: crème, bruin alleen in de hoek -> bovenlid loopt (16,19)(15,19)(14,20)(13,21)(12,22)
      (14,21):5,(15,21):5,(13,22):5,(14,22):5,(15,22):5,   # oogwit (model lichtcrème)
      (14,23):2,(15,23):2,(16,22):2,  # onderlid (model bruin), loopt op naar rechts
      (16,23):4,(13,24):4,(14,24):4,  # model crème tussen onderlid en kaaklijn
      (11,25):2,                      # kaaklijn doorlopend (model bruin/rood)
      (11,21):11 }                    # rood streepje links van het oog (model)
n=0
for (x,y),v in FIX.items():
    if a[y,x]!=v: a[y,x]=v; n+=1
im=Image.fromarray(a,'P'); im.putpalette(sum(PAL,[])+[0]*(768-48)); im.save(OUT,transparency=0); print('gezicht: gewijzigd',n)
