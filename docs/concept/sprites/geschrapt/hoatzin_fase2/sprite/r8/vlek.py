# vlekjes per tint (4-verbonden) kleiner dan 6 px, per index geteld
import sys, numpy as np; from PIL import Image
for f in sys.argv[1:]:
    a=np.array(Image.open(f)); seen=np.zeros(a.shape,bool); out={}
    for y in range(64):
      for x in range(64):
        t=a[y,x]
        if t==0 or seen[y,x]: continue
        st=[(y,x)]; n=0; seen[y,x]=1; cs=[]
        while st:
            p,q=st.pop(); n+=1; cs.append((p,q))
            for d,e in ((1,0),(-1,0),(0,1),(0,-1)):
                u,v=p+d,q+e
                if 0<=u<64 and 0<=v<64 and not seen[u,v] and a[u,v]==t: seen[u,v]=1; st.append((u,v))
        if n<6: out.setdefault(int(t),[]).append((n,cs[0]))
    print(f, {k:len(v) for k,v in sorted(out.items())}, 'totaal', sum(len(v) for v in out.values()))
    if '-v' in sys.argv[0:1]: pass
