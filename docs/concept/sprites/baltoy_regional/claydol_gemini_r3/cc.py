import numpy as np
def label(M,diag=False):
    H,W=M.shape; lab=np.zeros((H,W),int); n=0
    nb=[(1,0),(-1,0),(0,1),(0,-1)]+([(1,1),(1,-1),(-1,1),(-1,-1)] if diag else [])
    for y in range(H):
        for x in range(W):
            if M[y,x] and not lab[y,x]:
                n+=1; st=[(y,x)]; lab[y,x]=n
                while st:
                    a,b=st.pop()
                    for dy,dx in nb:
                        c,d=a+dy,b+dx
                        if 0<=c<H and 0<=d<W and M[c,d] and not lab[c,d]: lab[c,d]=n; st.append((c,d))
    return lab,n
