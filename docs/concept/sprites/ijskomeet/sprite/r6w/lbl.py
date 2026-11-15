import numpy as np
def label(m,conn=4):
    H,W=m.shape; lab=np.zeros((H,W),int); k=0
    nb=[(1,0),(-1,0),(0,1),(0,-1)]+([(1,1),(1,-1),(-1,1),(-1,-1)] if conn==8 else [])
    for y in range(H):
        for x in range(W):
            if m[y,x] and not lab[y,x]:
                k+=1; st=[(y,x)]; lab[y,x]=k
                while st:
                    a,b=st.pop()
                    for dy,dx in nb:
                        yy,xx=a+dy,b+dx
                        if 0<=yy<H and 0<=xx<W and m[yy,xx] and not lab[yy,xx]: lab[yy,xx]=k; st.append((yy,xx))
    return lab,k
