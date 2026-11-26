# Telt tintvlakjes < 3 px (4-verbonden, zelfde index) per index, binnen de figuur, zonder zwart en oog.
import sys, numpy as np; from PIL import Image
def kleine(s,minp=3):
    seen=np.zeros(s.shape,bool); uit=[]
    for y in range(64):
        for x in range(64):
            v=s[y,x]
            if v<=1 or seen[y,x]: continue
            st=[(y,x)]; comp=[]; seen[y,x]=True
            while st:
                a,b=st.pop(); comp.append((b,a))
                for dy,dx in ((1,0),(-1,0),(0,1),(0,-1)):
                    yy,xx=a+dy,b+dx
                    if 0<=yy<64 and 0<=xx<64 and not seen[yy,xx] and s[yy,xx]==v: seen[yy,xx]=True; st.append((yy,xx))
            if len(comp)<minp: uit.append((int(v),comp))
    return uit
if __name__=='__main__':
    for f in sys.argv[1:]:
        k=kleine(np.array(Image.open(f)))
        from collections import Counter
        print(f, len(k), dict(Counter(v for v,_ in k)))
