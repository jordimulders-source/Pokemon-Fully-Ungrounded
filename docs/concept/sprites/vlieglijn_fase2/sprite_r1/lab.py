import numpy as np
def label(m):
    H,W=m.shape; lab=np.zeros((H,W),int); n=0
    for y in range(H):
        for x in range(W):
            if m[y,x] and not lab[y,x]:
                n+=1; st=[(y,x)]; lab[y,x]=n
                while st:
                    p=st.pop()
                    for dy in (-1,0,1):
                        for dx in (-1,0,1):
                            q=(p[0]+dy,p[1]+dx)
                            if 0<=q[0]<H and 0<=q[1]<W and m[q] and not lab[q]: lab[q]=n; st.append(q)
    return lab,n
