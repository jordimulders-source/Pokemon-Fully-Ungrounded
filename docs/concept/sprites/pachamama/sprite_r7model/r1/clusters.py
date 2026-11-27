# clusters.py IN.npy : telt tintvlakjes < 3 px (4-samenhang), per index
import sys; import numpy as np
def vlakjes(o,maxs=2):
  seen=np.zeros(o.shape,bool); uit=[]
  for y in range(64):
    for x in range(64):
      v=o[y,x]
      if v<2 or seen[y,x]: continue
      st=[(y,x)]; seen[y,x]=1; comp=[]
      while st:
        p=st.pop(); comp.append(p)
        for dy,dx in ((1,0),(-1,0),(0,1),(0,-1)):
          q=(p[0]+dy,p[1]+dx)
          if 0<=q[0]<64 and 0<=q[1]<64 and not seen[q] and o[q]==v: seen[q]=1; st.append(q)
      if len(comp)<=maxs: uit.append((v,comp))
  return uit
if __name__=='__main__':
  o=np.load(sys.argv[1]); u=vlakjes(o); tot={}
  for v,c in u: tot[v]=tot.get(v,0)+1
  print('kleine vlakjes',len(u),dict(sorted(tot.items())))
