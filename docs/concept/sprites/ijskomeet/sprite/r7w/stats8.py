import sys; sys.path.insert(0,'r7w')
from proj import *
lum=A.mean(2)
P20=np.zeros((64,64)); P50=np.zeros((64,64)); P80=np.zeros((64,64))
for j in range(64):
  for i in range(64):
    x0,y0,x1,y1=box(i,j); b=lum[max(0,int(round(y0))):max(0,int(round(y1))),max(0,int(round(x0))):max(0,int(round(x1)))].ravel()
    b=b[b>=90]
    if b.size<10: continue
    P20[j,i],P50[j,i],P80[j,i]=np.percentile(b,[20,50,80])
np.save('r7w/P20.npy',P20); np.save('r7w/P50.npy',P50); np.save('r7w/P80.npy',P80)
