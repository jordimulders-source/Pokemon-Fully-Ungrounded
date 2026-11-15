# Haunters eigen mondpixels (Gen 3, frame 1) als bron, kleuren naar ons palet.
import numpy as np
from PIL import Image
import os
H=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
R=os.path.abspath(H+'/../../../..')
hu=np.array(Image.open(R+'/graphics/pokemon/haunter/anim_front.png'))[:64].astype(int)
X0,X1,Y0,Y1=15,33,38,45   # mond met boven- en onderlip; rij 46 = kinomtrek, x<=16 = wangomtrek
def kern(tong=10):
    g=[]
    for y in range(Y0,Y1+1):
        r=[]
        for x in range(X0,X1+1):
            v=hu[y,x]
            if v==0xe: r.append(1)
            elif v==0xa: r.append(10)
            elif v==9: r.append(tong)
            elif v==5:
                # Haunters donkerste huidtint = zachte mondomtrek (mondhoeken, onderlip) -> donkerbruin 2;
                # op rij 45 alleen de onderlip onder de tong (x27-28), de rest is kinschaduw
                r.append(2 if (y<45 and x>=17) or (y==45 and x in (27,28)) else None)
            else: r.append(None)      # huid (2/3/4) = hoofdkleur: tanden en lip
        g.append(r)
    return g
if __name__=='__main__':
    print('   '+''.join(str(x%10) for x in range(X0,X1+1)))
    for j,r in enumerate(kern()): print('%2d '%(Y0+j)+''.join('.' if v is None else '%x'%v for v in r))
