# meldt clusters < 3 px per kleur (4-buren), behalve oog/glans/tanden
import numpy as np,sys
a=np.load(sys.argv[1] if len(sys.argv)>1 else 'welp_r6.npy'); H,W=a.shape; CH='.KdSMLPQRgWCTGH'
seen=np.zeros((H,W),bool); out=[]
for j in range(H):
    for i in range(W):
        if seen[j,i] or a[j,i]==0: continue
        c=a[j,i]; st=[(j,i)]; cl=[]; seen[j,i]=True
        while st:
            y,x=st.pop(); cl.append((y,x))
            for yy,xx in ((y+1,x),(y-1,x),(y,x+1),(y,x-1)):
                if 0<=yy<H and 0<=xx<W and not seen[yy,xx] and a[yy,xx]==c: seen[yy,xx]=True; st.append((yy,xx))
        if len(cl)<3 and CH[c] in 'SMLHd': out.append((CH[c],[(x,y) for y,x in cl]))
for o in out: print(o)
print(len(out),'clusters <3 (x,y)')
