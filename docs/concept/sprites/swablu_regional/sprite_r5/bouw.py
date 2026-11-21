# Swablu r5: Jordi over r4: "de mond van swablu is nog niet herkenbaar genoeg, de mondlijn, verder vind ik hem wel goed".
# Alleen de mondlijn; alles buiten de snavel bevroren (diff 0). Draaien vanuit swablu_regional/.
# Modelplek (natief): mondlijn (93,59)-(94..97,61)-(99..100,60)-(102,59)-(103..104,58) = sprite (21,31)(22,31)(23,31)(24,30)(25,30): stijgende lijn naar rechts.
import sys, numpy as np; from PIL import Image
sys.path.insert(0,'gereedschap'); import gemeen as G
r4=Image.open('sprite_r4/swablu_r4.png'); o=np.asarray(r4).astype(int); start=o.copy()
G.PAL=[tuple(r4.getpalette()[3*i:3*i+3]) for i in range(15)]
LIJN=[(21,31),(22,31),(23,31),(24,30),(25,30)]
for X,Y in LIJN: o[Y,X]=12          # selout donker (46,60,78): donkerste tint zonder zwart
d=np.argwhere(o!=start); assert all(21<=x<=26 and 27<=y<=32 for y,x in d)
G.opslaan(o,'sprite_r5/swablu_r5.png'); G.rgb(o,(255,255,255)).resize((512,512),Image.NEAREST).save('sprite_r5/swablu_r5_8x.png')
print('anders dan r4:',[(int(x),int(y),int(start[y,x]),int(o[y,x])) for y,x in d])
