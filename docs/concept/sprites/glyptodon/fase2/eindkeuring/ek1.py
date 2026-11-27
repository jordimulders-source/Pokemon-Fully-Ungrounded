# Eindkeuring ronde 1 (ek1): basis = sprite/r7_B_lijn (keuze B). Alleen kleur van lijnpixels + 1 rode pixel (silhouet -1 px op Jordi's rode stip).
# Draaien vanuit deze map: python3 ek1.py
import sys; sys.path.insert(0,'../sprite')
import numpy as np
from basis import png,PAL
I0=np.load('../sprite/r7_B_lijn_I.npy'); I=I0.copy()
K,B,L,G10,G11=1,5,7,10,11
W=[]  # (x,y,oud,nieuw,reden)
def zet(pts,oud,nieuw,reden):
    for x,y in pts:
        assert I[y,x]==oud,(x,y,int(I[y,x]),oud); I[y,x]=nieuw; W.append((x,y,oud,nieuw,reden))
# ROOD
zet([(19,34)],B,L,'R1 streep: model (19,34)=middentint (126,109,91) -> 7; (20,34) blijft 5 (model donker)')
zet([(18,38)],K,B,'R2 vizierrand: hoort bij de lid-lijn (model donker), zelfde kleur als de lijn (B=5)')
zet([(7,49)],K,0,'R3 kin: losse zwarte uitstulping weg')
zet([(7,48)],G10,K,'R3 kin: onderlijn sluit, 1 px')
# GROEN
zet([(x,45) for x in range(36,47)],K,B,'G1 bovenrand schildzoom: model = onderbroken donkerbruine naad, geen zwart; nu eigen donkerste tint 5')
zet([(9,50),(9,51),(9,52),(9,53),(8,54),(8,55),(8,56),(8,57),(8,58),(7,59)],K,G10,'G2 voorpoot links = lichtkant -> outline base grijs 10')
zet([(26,y) for y in range(53,62)],K,G10,'G2 middelste poot links (model ~47) -> outline base grijs 10')
zet([(40,56),(40,57),(40,58),(40,59)],K,G10,'G2 achterpoot links (model ~86) -> outline base grijs 10')
zet([(35,49),(36,49),(35,52),(36,52),(38,52)],K,G10,'G2 tussen de poten: zwarte clusters (2 rijen) -> 1 px lijn + diepste grijs')
zet([(11,50),(12,50)],K,G10,'cluster onder de kin/bovenkant voorpoot -> 1 px lijn + diepste grijs')
# OVERIG (belijning lichtkant, gids)
zet([(4,42),(4,43),(4,44),(5,45),(5,46),(5,47)],K,G10,'kop links = lichtkant -> outline base grijs 10')
zet([(3,36),(3,37),(2,38),(1,38)],K,B,'vizierpunt linksboven = lichtkant -> outline base schild 5 (zoals schildrand erboven)')
# controles
I4=np.load('../sprite/r4_I.npy'); oog=(I4==14)|(I4==15)
assert (I[oog]==I0[oog]).all() and I[41,13]==1, 'oog/pupil geraakt'
print('gewijzigd',len(W),'px; silhouet verschil',int(((I>0)!=(I0>0)).sum()))
np.save('ek1_I.npy',I); png(I,'ek1.png'); png(I,'ek1_8x.png',8)
with open('ek1_wijzigingen.txt','w') as f:
    for x,y,o,n,r in W: f.write(f'({x},{y}) {o}->{n}  {r}\n')
np.save('ek1_W.npy',np.array([(x,y) for x,y,*_ in W]))
