import sys,numpy as np; from PIL import Image
sys.path.insert(0,'.'); import r5
def spikkels(S,zone,n8=True):
    seen=np.zeros(S.shape,bool); out=[]
    nb=[(1,0),(-1,0),(0,1),(0,-1)]+([(1,1),(1,-1),(-1,1),(-1,-1)] if n8 else [])
    for y,x in zip(*np.where(zone&np.isin(S,(1,2,3,4,5,10)))):
        if seen[y,x]: continue
        v=S[y,x]; st=[(y,x)]; c=[]; seen[y,x]=1
        while st:
            a,b=st.pop(); c.append((b,a))
            for dy,dx in nb:
                q,w=a+dy,b+dx
                if 0<=q<64 and 0<=w<64 and not seen[q,w] and S[q,w]==v and zone[q,w]: seen[q,w]=1; st.append((q,w))
        if len(c)<3: out.append(('A' if v==10 else str(v),sorted(c)))
    return out
if __name__=='__main__':
    S=np.array(Image.open(sys.argv[1])).astype(int)
    print(spikkels(S,r5.LIJF&(r5.yy>=40)))
