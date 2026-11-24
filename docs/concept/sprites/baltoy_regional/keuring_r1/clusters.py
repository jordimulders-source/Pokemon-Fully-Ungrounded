from PIL import Image
import numpy as np, sys
a=np.array(Image.open(sys.argv[1]))
H,W=a.shape; seen=np.zeros_like(a,bool)
zones=[('bovenplaat',15,19),('band',19,26),('gezicht',26,39),('lijf/armen',39,64)]
cnt={}
for y in range(H):
  for x in range(W):
    if seen[y,x] or a[y,x] in (0,1): continue
    c=a[y,x]; st=[(y,x)]; seen[y,x]=1; pts=[]
    while st:
      py,px=st.pop(); pts.append((px,py))
      for dy,dx in ((1,0),(-1,0),(0,1),(0,-1)):
        ny,nx=py+dy,px+dx
        if 0<=ny<H and 0<=nx<W and not seen[ny,nx] and a[ny,nx]==c: seen[ny,nx]=1; st.append((ny,nx))
    if len(pts)<3:
      z=[n for n,y0,y1 in zones if y0<=pts[0][1]<y1][0]
      cnt[(z,c)]=cnt.get((z,c),0)+1
      print(z,'kleur',c,pts)
print(cnt)
