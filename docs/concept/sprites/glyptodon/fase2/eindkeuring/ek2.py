# Eindkeuring ronde 2 (ek2) op ek1: beige streep schoon + pootcontouren naar het model (voetflare, afgeronde hoeken, tenen).
import sys; sys.path.insert(0,'../sprite')
import numpy as np
from basis import png
I1=np.load('ek1_I.npy'); I=I1.copy()
SYM={'.':0,'#':1,'b':5,'m':6,'l':7,'e':8,'E':9,'-':10,'g':11,'G':12,'H':13}
def zet(y,x0,s):
    for i,c in enumerate(s):
        if c!='?': I[y,x0+i]=SYM[c]
# 1. beige linkerstreep: (19,34) en (20,34) -> streeptint E van de buren (18,34)/(21,34)
zet(34,19,'EE')
# 2a. voorpoot: rechterrand loopt taps naar de enkel (model 17,5 -> 16,8 -> 16,2 -> 15,5), voet met tenen, onderkant afgerond (model onderrand y61)
zet(57,16,'#.')          # (16,57) '-'->#, (17,57) #->.
zet(60,6,'.#H-gHG-g#')    # x6..15: hoek weg, teenrij (licht op x8 en x11, naad x9/x13)
zet(61,8,'#######')      # x8..14 nieuwe onderrand
# 2b. middelste poot: voet loopt links uit (model), tenen bestaan al
zet(60,25,'-g')          # (25,60) nieuw randpixel, (26,60) -> vulling
zet(61,26,'g')           # (26,61) '-' -> vulling (rand zit nu op x25)
# 2c. achterpoot: voet loopt links en rechts uit, teenrij, afgeronde onderkant (model onderrand y61, tenen x41-43 en x45-46)
zet(56,47,'#.')          # enkel: rechterrand 1 px naar binnen (model dekking x48 hier 53%)
zet(57,47,'#.')
zet(58,41,'g')           # dubbele lijn naast de rand weg
zet(59,39,'-g???????g#') # (39,59) nieuw rand, (40,59) vulling, (48,59) vulling, (49,59) nieuw rand
zet(60,39,'#gGH-gGHg-#') # teenrij x39..49
zet(61,40,'#########')   # nieuwe onderrand x40..48
zet(58,47,'-')           # sikkelschaduw rechts van enkel naar voet
zet(59,48,'-')
I4=np.load('../sprite/r4_I.npy'); oog=(I4==14)|(I4==15)
assert (I[oog]==I1[oog]).all() and I[41,13]==1
D=np.argwhere(I!=I1); print('gewijzigd',len(D),'silhouet',int(((I>0)!=(I1>0)).sum()))
with open('ek2_wijzigingen.txt','w') as f:
    for y,x in D: f.write(f'({x},{y}) {I1[y,x]}->{I[y,x]}\n')
np.save('ek2_W.npy',D[:,::-1]); np.save('ek2_I.npy',I); png(I,'ek2.png'); png(I,'ek2_8x.png',8)
