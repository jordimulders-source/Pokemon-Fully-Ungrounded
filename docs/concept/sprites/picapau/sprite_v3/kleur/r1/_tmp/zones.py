from PIL import Image
import numpy as np
a=np.array(Image.open('../../r17/picapau.png'))
Y={2,3,4}
# print yellow region labels: E ear, K crest, H head, N neckline, L body
lab=np.full(a.shape,'.',dtype='<U1')
for y in range(64):
  for x in range(64):
    v=a[y,x]
    if v==0: continue
    if v not in Y: lab[y,x]='o'; continue
    if y<=21 and x>=24 and x<=34: lab[y,x]='E'
    elif y<=28 and x>=32: lab[y,x]='K'
    elif y<=37: lab[y,x]='H'
    elif y==38: lab[y,x]='N'
    else: lab[y,x]='L'
for y in range(12,63): print('%2d '%y+''.join(lab[y,14:49]))
