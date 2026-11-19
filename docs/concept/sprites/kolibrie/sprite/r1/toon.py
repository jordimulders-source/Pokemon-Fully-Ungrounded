import sys,numpy as np; from PIL import Image
a=np.array(Image.open(sys.argv[1])); ys,xs=np.where(a>0)
print('   '+''.join(str(x%10) for x in range(64)))
for y in range(ys.min(),ys.max()+1): print('%2d '%y+''.join('.' if v==0 else '%x'%v for v in a[y]))
print({i:int((a==i).sum()) for i in range(16)})
