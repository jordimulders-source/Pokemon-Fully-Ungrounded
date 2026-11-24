import sys,numpy as np; from PIL import Image
p=sys.argv[1]; a=np.load(p) if p.endswith('.npy') else np.array(Image.open(p))
x0,y0,x1,y1=[int(v) for v in sys.argv[2].split(',')]
print('   '+''.join('%3d'%x for x in range(x0,x1)))
for y in range(y0,y1): print('%2d '%y+''.join('  '+('%x'%a[y,x] if a[y,x] else '.') for x in range(x0,x1)))
