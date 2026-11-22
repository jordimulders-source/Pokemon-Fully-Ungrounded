# kleine tintvlakjes (<3 px, 4-buren) per kleur, behalve zwart/wit/selout
import numpy as np,sys
o=np.load(sys.argv[1] if len(sys.argv)>1 else 'r1.npy'); H,W=o.shape; seen=np.zeros_like(o,bool)
for y in range(H):
    for x in range(W):
        v=o[y,x]
        if v in (0,1,16,17) or seen[y,x]: continue
        st=[(y,x)]; seen[y,x]=True; c=[]
        while st:
            a,b=st.pop(); c.append((b,a))
            for dy,dx in ((1,0),(-1,0),(0,1),(0,-1)):
                yy,xx=a+dy,b+dx
                if 0<=yy<H and 0<=xx<W and not seen[yy,xx] and o[yy,xx]==v: seen[yy,xx]=True; st.append((yy,xx))
        if len(c)<3: print('code',v,c)
