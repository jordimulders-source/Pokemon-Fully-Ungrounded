# Stap 1: kleine geest uit het natieve model kwantiseren naar 6 (donker), 5 (midden), 2 (licht), W (glimp). Geen hertekening.
from PIL import Image; import numpy as np
n=np.array(Image.open('model/natief.png').convert('RGB')).astype(int)
X0,X1,Y0,Y1=29,63,6,22
rows=[]
for y in range(Y0,Y1):
    s=''
    for x in range(X0,X1):
        c=n[y,x]
        if c.min()>235: s+='.'; continue
        if c.min()>200: s+='W'; continue
        if not c[1]>c[0]+25: s+='#'; continue
        G=c[1]; s+='6' if G<150 else ('5' if G<214 else '2')
    rows.append(s)
open('sprite_r6/geest_kwant.txt','w').write('\n'.join(rows)+'\n')
for y,s in zip(range(Y0,Y1),rows): print('%2d'%y,s)
print('   '+''.join(str(x%10) for x in range(X0,X1)))
