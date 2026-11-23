import sys,numpy as np; from PIL import Image
I=np.array(Image.open(sys.argv[1])); x0,y0,x1,y1=map(int,sys.argv[2].split(','))
C='.KL345678abcdeH'   # 0 . 1 K 2 L 3 4 5 6 7 8 9 a 10 b 11 c 12 d 13 e(oog) 14 H
print('    '+''.join(str(x%10) for x in range(x0,x1)))
for y in range(y0,y1): print('%2d  '%y+''.join(C[v] for v in I[y,x0:x1]))
