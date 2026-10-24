import numpy as np, sys
from PIL import Image
sys.path.insert(0,'.')
from teken import build
im=np.array(build()); s=np.array(Image.open('../silhouet/silhouet_v6_groot_1x.png'))[:,:,3]>0
m=im>0
add=m&~s; rem=s&~m
print('px',m.sum(),'sil',s.sum(),'erbij',add.sum(),'eraf',rem.sum())
for y in range(64):
    row=''
    for x in range(64):
        row+= '+' if add[y,x] else ('-' if rem[y,x] else ('#' if m[y,x] else '.'))
    if '+' in row or '-' in row: print('%2d'%y,row)
