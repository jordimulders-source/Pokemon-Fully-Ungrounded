import numpy as np
def label(fg):
    H,W=fg.shape; lab=np.zeros((H,W),int); n=0
    for y in range(H):
        for x in range(W):
            if fg[y,x] and not lab[y,x]:
                n+=1; st=[(y,x)]; lab[y,x]=n
                while st:
                    cy,cx=st.pop()
                    for dy in (-1,0,1):
                        for dx in (-1,0,1):
                            ny,nx=cy+dy,cx+dx
                            if 0<=ny<H and 0<=nx<W and fg[ny,nx] and not lab[ny,nx]: lab[ny,nx]=n; st.append((ny,nx))
    return lab,n
