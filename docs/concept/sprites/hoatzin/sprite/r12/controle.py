# controle r10: alpha-diff en lijn-diff t.o.v. r9, kleuren, lichte tint op de buitenrand, tintvlekjes < 3 px (4-buren)
import os,numpy as np
from PIL import Image
H=os.path.dirname(os.path.abspath(__file__))
r9=np.array(Image.open(H+'/../r9/hoatzin_r9.png'))
N={2:'donker',3:'midden',4:'licht',10:'hooglicht'}
for k in ['r12']:
    im=Image.open(H+'/hoatzin_r12.png'); o=np.array(im); p=im.getpalette()
    print(f'== {k}: mode {im.mode} {im.size} transp {im.info.get("transparency")} kleuren {len(np.unique(o))} (incl. transparant)')
    print('  alpha-diff',((o>0)!=(r9>0)).sum(),'| zwarte lijn-diff',((o==1)!=(r9==1)).sum(),'| niet-lijf gewijzigd',((o!=r9)&~np.isin(r9,[2,3,4])).sum(),'| lijf gewijzigd',((o!=r9)).sum())
    for t in N: print('  ',N[t],tuple(p[3*t:3*t+3]),(o==t).sum())
    rand=[(y,x) for y in range(64) for x in range(64) if o[y,x] in (3,4,10) and any(not(0<=y+dy<64 and 0<=x+dx<64) or o[y+dy,x+dx]==0 for dy,dx in((1,0),(-1,0),(0,1),(0,-1)))]
    print('  lichte lijftint op de buitenrand:',rand)
    for t in (3,4,10):
        m=o==t; seen=np.zeros_like(m); klein=[]
        for y,x in zip(*np.where(m)):
            if seen[y,x]: continue
            st=[(y,x)]; seen[y,x]=1; c=[]
            while st:
                a,b=st.pop(); c.append((a,b))
                for dy,dx in((1,0),(-1,0),(0,1),(0,-1)):
                    yy,xx=a+dy,b+dx
                    if 0<=yy<64 and 0<=xx<64 and m[yy,xx] and not seen[yy,xx]: seen[yy,xx]=1; st.append((yy,xx))
            if len(c)<3: klein.append([(b,a) for a,b in c])
        print(f'  vlekjes <3 px {N[t]} (x,y):',klein)
