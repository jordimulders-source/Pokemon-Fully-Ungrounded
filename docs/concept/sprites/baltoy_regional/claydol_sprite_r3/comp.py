# connected components (4-buren) van niet-transparante pixels; staven moeten eigen componenten zijn
import sys,numpy as np; from PIL import Image
def label(m):
    H,W=m.shape; lab=np.zeros((H,W),int); n=0
    for y0 in range(H):
        for x0 in range(W):
            if m[y0,x0] and not lab[y0,x0]:
                n+=1; st=[(y0,x0)]
                while st:
                    y,x=st.pop()
                    if 0<=y<H and 0<=x<W and m[y,x] and not lab[y,x]:
                        lab[y,x]=n; st+=[(y+1,x),(y-1,x),(y,x+1),(y,x-1)]
    return lab,n
def comps(S):
    lab,n=label(S>0); out=[]
    for i in range(1,n+1):
        ys,xs=np.where(lab==i); out.append((len(ys),xs.min(),xs.max(),ys.min(),ys.max()))
    return sorted(out,reverse=True)
if __name__=='__main__':
    for f in sys.argv[1:]:
        S=np.load(f) if f.endswith('.npy') else np.array(Image.open(f))
        print(f,comps(S))
