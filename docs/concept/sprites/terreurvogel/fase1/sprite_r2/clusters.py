# Tintclusters <3 px in een sprite (geen randpixels, geen oog), met type: zak (>=2 zwarte buren per pixel) of vlek
import numpy as np, sys; from PIL import Image
def clusters(S):
    seen=np.zeros(S.shape,bool); out=[]
    for y in range(64):
        for x in range(64):
            if seen[y,x] or S[y,x]<=1: continue
            v=S[y,x]; st=[(y,x)]; seen[y,x]=True; cl=[]
            while st:
                cy,cx=st.pop(); cl.append((cy,cx))
                for dy,dx in ((-1,0),(1,0),(0,-1),(0,1)):
                    ny,nx=cy+dy,cx+dx
                    if 0<=ny<64 and 0<=nx<64 and not seen[ny,nx] and S[ny,nx]==v: seen[ny,nx]=True; st.append((ny,nx))
            out.append((int(v),cl))
    return out
def rand(S,y,x): return any(not(0<=y+dy<64 and 0<=x+dx<64) or S[y+dy,x+dx]==0 for dy,dx in ((-1,0),(1,0),(0,-1),(0,1)))
def klein(S):
    res=[]
    for v,cl in clusters(S):
        if len(cl)>=3 or v in (14,15): continue
        if any(rand(S,y,x) for y,x in cl): t='rand'
        elif all(sum(S[y+dy,x+dx]==1 for dy,dx in ((-1,0),(1,0),(0,-1),(0,1)))>=2 for y,x in cl): t='zak'
        else: t='vlek'
        res.append((t,v,[(x,y) for y,x in cl]))
    return res
if __name__=='__main__':
    S=np.array(Image.open(sys.argv[1]))
    for r in klein(S): print(r)
