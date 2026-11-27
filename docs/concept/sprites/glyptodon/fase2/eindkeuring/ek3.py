# Eindkeuring ronde 3 (ek3) op ek2: poten als Gen 3-zware viervoeter (Jordi: "ja die mag dat fase 2").
# Bolle bovenpoot met licht vlak linksboven, sikkelschaduw rechts die de bolling volgt, insnoering naar de enkel,
# voeten/tenen uit ek2 blijven. Breedte +-1 px, positie en lengte gelijk. Alleen palet 10-13 + zwart.
import sys; sys.path.insert(0,'../sprite')
import numpy as np
from basis import png
I2=np.load('ek2_I.npy'); I=I2.copy()
SYM={'.':0,'#':1,'-':10,'g':11,'G':12,'H':13}
def zet(y,x0,s):
    for i,c in enumerate(s):
        if c!='?': I[y,x0+i]=SYM[c]
# voorpoot x8..18: links bol (x8) op r52-55, enkel x9 op r56-57, voet uit; rechts taps 18-17-16
zet(52,8,'-GHGGGggg-#')
zet(53,8,'-HHHGGgg-#')
zet(54,8,'-HHGGggg-#')
zet(55,8,'-GHGGgg--#')
zet(56,8,'.-GHGgg-#.')
zet(57,8,'.-GGGgg-#')
zet(58,8,'-GGGggg-#')
# middelste poot x25..35: knie bolt rechts uit (x35 r54-56), enkel x34 r57-58, voet x35
zet(52,26,'GHHGGGGg#')
zet(53,26,'-HHHGGgg#')
zet(54,26,'-HHGGGggg#')
zet(55,26,'-GHGGggg-#')
zet(56,26,'-GGGGgg--#')
zet(57,26,'-GGGGgg-#.')
zet(58,26,'-GGGGggg#.')
zet(59,26,'-GGgGGgg-#')
# achterpoot x38..49: dij met licht linksboven, sikkel rechts, enkel links x41 r56-57
zet(50,38,'gggGGGggg-#')
zet(51,38,'gGGHHGgg-#')
zet(52,38,'-gGHGGGg-#')
zet(53,41,'GGGgg-#')
zet(54,38,'.#gGGgggg-#')
zet(55,39,'.-GGggg--#')
zet(56,40,'.-Gggg-#.')
zet(57,40,'.-Gggg-#')
zet(58,40,'-gGggg--#')
I4=np.load('../sprite/r4_I.npy'); oog=(I4==14)|(I4==15)
assert (I[oog]==I2[oog]).all() and I[41,13]==1
D=np.argwhere(I!=I2); print('gewijzigd',len(D),'silhouet',int(((I>0)!=(I2>0)).sum()))
assert D[:,0].min()>=50 and D[:,0].max()<=59 and D[:,1].max()<=48
with open('ek3_wijzigingen.txt','w') as f:
    for y,x in D: f.write(f'({x},{y}) {I2[y,x]}->{I[y,x]}\n')
np.save('ek3_W.npy',D[:,::-1]); np.save('ek3_I.npy',I); png(I,'ek3.png'); png(I,'ek3_8x.png',8)
