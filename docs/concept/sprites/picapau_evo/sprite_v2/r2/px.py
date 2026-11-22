# Meet per spritecel het model: per cel de natieve klassen (3x3) als letters en de zwartfractie in het 1024-model.
# Gebruik: python3 px.py x0 y0 x1 y1  -> twee kaarten: model-meerderheid | schoon.npy (zelfde letters)
import sys; import numpy as np; from PIL import Image
x0,y0,x1,y1=map(int,sys.argv[1:5]); f=sys.argv[5] if len(sys.argv)>5 else 'schoon.npy'
K=np.load('klassen.npy'); o=np.load(f); OY,OX=1,4
CH='.Z' 'lmd' 'LMD' 'r' 'gGh' 'yY' 'w'
CH={0:'.',1:'#',2:'l',3:'m',4:'d',5:'C',6:'c',7:'k',8:'r',9:'g',10:'G',11:'h',12:'y',13:'Y',14:'w',15:'s'}
a=np.asarray(Image.open('../../gemini/r9_prompt_v6.png').convert('L')).astype(int)
print('     '+''.join('%-4d'%x if x%2==0 else '    ' for x in range(x0,x1)))
for y in range(y0,y1):
    row=''; srow=''
    for x in range(x0,x1):
        b=K[OY+3*y:OY+3*y+3,OX+3*x:OX+3*x+3].ravel()
        c=np.bincount(b,minlength=15); top=np.argsort(-c)[:2]
        hy,hx=int((OY+3*y)*5.12),int((OX+3*x)*5.12); bf=(a[hy:hy+15,hx:hx+15]<70).mean()
        row+=CH[top[0]]+(CH[top[1]] if c[top[1]]>=2 else ' ')+str(min(9,int(bf*10)))+' '
        srow+=CH[o[y,x]]
    print('%2d   %s  %s'%(y,row,srow))
