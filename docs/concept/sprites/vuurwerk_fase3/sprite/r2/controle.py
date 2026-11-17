# Controle: 64x64, aantal kleuren, tintvlakjes < 3 px (8-buren) binnen het lijf, losse omlijningspixels (index 1) midden in een vlak.
import numpy as np; from PIL import Image
im=Image.open('sprite.png'); a=np.asarray(im).astype(int); H,W=a.shape
print('formaat',im.size,'modus',im.mode,'kleuren',len(np.unique(a)))
def clusters(m):
    seen=np.zeros_like(m,bool); r=[]
    for y in range(H):
        for x in range(W):
            if not m[y,x] or seen[y,x]: continue
            st=[(y,x)]; seen[y,x]=1; c=[]
            while st:
                p=st.pop(); c.append(p)
                for dy in (-1,0,1):
                    for dx in (-1,0,1):
                        q=(p[0]+dy,p[1]+dx)
                        if 0<=q[0]<H and 0<=q[1]<W and m[q] and not seen[q]: seen[q]=1; st.append(q)
            r.append(c)
    return r
klein=[]
for k in range(1,16):
    for c in clusters(a==k):
        if len(c)<3:
            y,x=c[0]; nb=a[max(0,y-1):y+2,max(0,x-1):x+2]
            if (nb==0).sum()==0: klein.append((k,[(q[1],q[0]) for q in c]))
print('tintvlakjes <3 px midden in het lijf:',len(klein)); print(klein)
los=[(x,y) for y in range(1,H-1) for x in range(1,W-1) if a[y,x]==1 and (a[y-1:y+2,x-1:x+2]==0).sum()==0 and ((a[y-1:y+2,x-1:x+2]==1).sum()==1)]
print('losse omlijningspixel midden in een vlak:',los)
