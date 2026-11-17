# dekking.py x0 y0 x1 y1: per spritepixel de modeldekking (aantal figuur-px van 9 in het natieve 3x3-blok) naast de sprite
import sys, numpy as np; from PIL import Image
B='/home/user/Pokemon-Fully-Ungrounded/docs/concept/sprites/pitahaya_draak_fase2/'
nat=np.array(Image.open(B+'sprite_r9/natief.png').convert('RGB')).astype(int); fg=nat.min(2)<225
sp=np.array(Image.open(sys.argv[5] if len(sys.argv)>5 else B+'sprite_r9/pitahaya2_r9A.png'))
x0,y0,x1,y1=map(int,sys.argv[1:5])
print('    '+''.join('%2d '%(x%100) for x in range(x0,x1)))
for y in range(y0,y1):
    row=[]
    for x in range(x0,x1):
        nx,ny=2+3*x,3*(y-13); c=fg[ny:ny+3,nx:nx+3].sum()
        row.append(('%d'%c if c else '.')+('#' if sp[y,x] else ' ')+' ')
    print('%2d  '%y+''.join(row))
